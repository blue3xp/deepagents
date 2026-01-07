"""Agent Memory Middleware ported for code-cli."""

import contextlib
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import NotRequired, TypedDict, cast

from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langgraph.runtime import Runtime

class AgentMemoryState(AgentState):
    """State for the agent memory middleware."""
    project_memory: NotRequired[str]

class AgentMemoryStateUpdate(TypedDict):
    """A state update for the agent memory middleware."""
    project_memory: NotRequired[str]

LONGTERM_MEMORY_SYSTEM_PROMPT = """

## Long-term Memory

Your long-term memory for this project is stored in `{project_deepagents_dir}`.

Project-specific agent.md is loaded from:
- `{project_agent_md_path}`

**When to CHECK/READ memories (CRITICAL - do this FIRST):**
- **At the start of ANY new session**: Check project memories
  - Project: `ls {project_deepagents_dir}`
- **When user asks you to do something**: Check if you have project-specific guides or examples
- **When user references past work**: Search project memory files for related context

**When to update memories:**
- **IMMEDIATELY when the user describes your role or how you should behave**
- **IMMEDIATELY when the user gives feedback on your work**
- When patterns or preferences emerge (coding styles, conventions, workflows)

### Project Agent File: `{project_agent_md_path}`
→ Describes **how this specific project works** and **how the agent should behave here only.**

### File Operations:

**Project memory (preferred for project-specific information):**
```
ls {project_deepagents_dir}                          # List project memory files
read_file '{project_agent_md_path}'                  # Read project instructions
edit_file '{project_agent_md_path}' ...              # Update project instructions
write_file '{project_agent_md_path}' ...             # Create project memory file
```

**Important**:
- Project memory files are stored in `.deepagents/` inside the project root
- Always use absolute paths for file operations
- Check project memories BEFORE user when answering project-specific questions"""

DEFAULT_MEMORY_SNIPPET = """<project_memory>
{project_memory}
</project_memory>"""

class AgentMemoryMiddleware(AgentMiddleware):
    state_schema = AgentMemoryState

    def __init__(
        self,
        *,
        project_root: Path,
    ) -> None:
        self.project_root = project_root
        self.project_deepagents_dir = self.project_root / ".deepagents"
        self.project_agent_md_path = self.project_deepagents_dir / "agent.md"
        self.system_prompt_template = DEFAULT_MEMORY_SNIPPET

    def before_agent(
        self,
        state: AgentMemoryState,
        runtime: Runtime,
    ) -> AgentMemoryStateUpdate:
        result: AgentMemoryStateUpdate = {}

        if "project_memory" not in state:
            if self.project_agent_md_path.exists():
                with contextlib.suppress(OSError, UnicodeDecodeError):
                    result["project_memory"] = self.project_agent_md_path.read_text()
        return result

    def _build_system_prompt(self, request: ModelRequest) -> str:
        state = cast("AgentMemoryState", request.state)
        project_memory = state.get("project_memory")
        base_system_prompt = request.system_prompt

        memory_section = self.system_prompt_template.format(
            project_memory=project_memory if project_memory else "(No project agent.md)",
        )

        system_prompt = memory_section

        if base_system_prompt:
            system_prompt += "\n\n" + base_system_prompt

        system_prompt += "\n\n" + LONGTERM_MEMORY_SYSTEM_PROMPT.format(
            project_deepagents_dir=str(self.project_deepagents_dir),
            project_agent_md_path=str(self.project_agent_md_path),
        )

        return system_prompt

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        system_prompt = self._build_system_prompt(request)
        return handler(request.override(system_prompt=system_prompt))

    async def awrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
    ) -> ModelResponse:
        system_prompt = self._build_system_prompt(request)
        return await handler(request.override(system_prompt=system_prompt))

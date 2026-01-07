import asyncio
import sys
import os
from pathlib import Path
from typing import Any

# DeepAgents Core Imports
from deepagents.graph import create_deep_agent
from deepagents.backends.composite import CompositeBackend
from deepagents.backends.filesystem import FilesystemBackend
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown

from deepagents_code_cli.config import config

console = Console()

def create_local_agent(model_name: str, system_prompt: str, assistant_id: str):
    """
    Create a deep agent configured for local execution.
    Replaces deepagents_cli.agent.create_cli_agent
    """

    # 1. Initialize Model
    # Using ChatOpenAI directly or init_chat_model
    # deepagents uses init_chat_model internally if model is a string,
    # but we can pass a configured model instance.
    if "gpt" in model_name:
         model = ChatOpenAI(model=model_name, api_key=config.openai_api_key)
    else:
         model = init_chat_model(model_name, model_provider="openai") # Fallback assuming openai compatible

    # 2. Setup Backend (Filesystem)
    # Using FilesystemBackend for local file access
    fs_backend = FilesystemBackend()

    # CompositeBackend is used by deepagents to route paths (e.g. sandboxes),
    # but for purely local, we just wrap the filesystem backend.
    backend = CompositeBackend(default=fs_backend, routes={})

    # 3. Create Agent
    # deepagents.graph.create_deep_agent sets up the graph and middleware
    agent = create_deep_agent(
        model=model,
        tools=[], # deepagents adds default filesystem tools via middleware/graph if backend is provided
        system_prompt=system_prompt,
        backend=backend,
        interrupt_on={}, # auto_approve=True equivalent (no interrupts)
        checkpointer=None, # In-memory only for this CLI
    )

    return agent, backend

async def execute_task(prompt: str, agent: Any, assistant_id: str):
    """
    Execute the agent loop.
    Replaces deepagents_cli.execution.execute_task
    """

    console.print(f"[bold green]Starting Agent Task...[/bold green]")

    stream_input = {"messages": [{"role": "user", "content": prompt}]}
    config = {"configurable": {"thread_id": "1"}} # Simple thread ID

    async for chunk in agent.astream(
        stream_input,
        stream_mode=["messages", "updates"],
        subgraphs=True,
        config=config,
    ):
        if not isinstance(chunk, tuple) or len(chunk) != 3:
            continue

        _namespace, current_stream_mode, data = chunk

        if current_stream_mode == "messages":
            message, _metadata = data

            # Print Assistant text
            if hasattr(message, "content") and message.content:
                if not isinstance(message, ToolMessage) and not isinstance(message, HumanMessage):
                     # Likely AIMessage
                     # Handle content blocks if present (Anthropic/OpenAI) or just content string
                     if isinstance(message.content, str) and message.content.strip():
                         # Check if it's the final chunk of a message to avoid spamming partials
                         # Ideally we buffer, but for simplicity let's just print full messages or chunks
                         # Actually deepagents stream returns chunks.
                         pass
                         # For a cleaner CLI, implementing full streaming pretty print is complex.
                         # We'll rely on the fact that we just want to see it's working.
                         sys.stdout.write(message.content)
                         sys.stdout.flush()

        # Handle tool execution visualization (Updates)
        elif current_stream_mode == "updates":
            # In deepagents, updates often contain the tool calls or state changes
            pass

    console.print("\n[bold green]Task Completed.[/bold green]")


async def run_autonomous_loop():
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        sys.exit(1)

    console.print(f"Codebase Path: {config.codebase_path}")
    console.print(f"Reference Codebase Path: {config.reference_codebase_path}")

    # Skill and Knowledge Loading
    package_skills_dir = Path(__file__).parent / "skills"
    package_knowledge_dir = Path(__file__).parent / "knowledge"

    skill_path = package_skills_dir / "implement_adapter.md"
    if not skill_path.exists():
         console.print(f"[bold red]Error:[/bold red] Skill file not found at {skill_path}")
         sys.exit(1)

    skill_content = skill_path.read_text()

    knowledge_content = ""
    if package_knowledge_dir.exists():
        knowledge_files = sorted(package_knowledge_dir.glob("*.md"))
        for kf in knowledge_files:
            knowledge_content += f"\n\n### {kf.stem}\n{kf.read_text()}"

    # Construct Prompt
    prompt = f"""
You are an autonomous coding agent specialized in implementing Adapter patterns.

Target Codebase: {config.codebase_path}
Reference Codebase: {config.reference_codebase_path}
Skills Directory: {package_skills_dir}

## Knowledge Base
The following internal libraries are available. You MUST use them where appropriate:
{knowledge_content}

You must follow the instructions in the "Implement Adapter" skill below:

---
{skill_content}
---

Execute the task completely. Run tests to verify. Correct any errors.
Do not ask for user input. If you are stuck, try to solve it yourself or report the failure.
"""

    # Create Agent
    assistant_id = "code-cli-agent"
    agent, backend = create_local_agent(config.model_name, "", assistant_id)

    # Execute
    await execute_task(prompt, agent, assistant_id)

def main():
    asyncio.run(run_autonomous_loop())

if __name__ == "__main__":
    main()

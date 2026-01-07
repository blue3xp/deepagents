import asyncio
import sys
import os
import subprocess
from pathlib import Path
from typing import Any

# DeepAgents Core Imports
from deepagents.graph import create_deep_agent
from deepagents.backends.composite import CompositeBackend
from deepagents.backends.filesystem import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown

from deepagents_code_cli.config import config
from deepagents_code_cli.skills.middleware import SkillsMiddleware
from deepagents_code_cli.agent_memory import AgentMemoryMiddleware

console = Console()

def run_shell_command(command: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.getcwd()
        )
        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"
        if result.returncode != 0:
            output += f"\nExit Code: {result.returncode}"
        return output
    except Exception as e:
        return f"Error executing command: {e}"

def create_local_agent(model_name: str, system_prompt: str, assistant_id: str, skills_dir: Path):
    """
    Create a deep agent configured for local execution.
    Replaces deepagents_cli.agent.create_cli_agent
    """

    # 1. Initialize Model
    if "gpt" in model_name:
         model = ChatOpenAI(model=model_name, api_key=config.openai_api_key)
    else:
         model = init_chat_model(model_name, model_provider="openai")

    # 2. Setup Backend (Filesystem)
    fs_backend = FilesystemBackend()
    backend = CompositeBackend(default=fs_backend, routes={})

    # 3. Get Default Tools
    fs_middleware = FilesystemMiddleware(backend=backend)
    tools = fs_middleware.tools

    # Add Shell Tool (for 'shell' or 'execute' capability)
    shell_tool = StructuredTool.from_function(
        func=run_shell_command,
        name="shell",
        description="Execute a shell command. Use this to run scripts, tests, or other commands."
    )
    tools.append(shell_tool)

    # 4. Setup Middleware
    skills_middleware = SkillsMiddleware(
        skills_dir=skills_dir,
        assistant_id=assistant_id
    )

    # Agent Memory Middleware
    memory_middleware = AgentMemoryMiddleware(
        project_root=Path(config.codebase_path).resolve()
    )

    # 5. Create Agent
    agent = create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        backend=backend,
        middleware=[skills_middleware, memory_middleware],
        interrupt_on={},
        checkpointer=None,
    )

    return agent, backend

async def execute_task(prompt: str, agent: Any, assistant_id: str):
    """
    Execute the agent loop.
    Replaces deepagents_cli.execution.execute_task
    """

    console.print(f"[bold green]Starting Agent Task...[/bold green]")

    stream_input = {"messages": [{"role": "user", "content": prompt}]}
    config = {"configurable": {"thread_id": "1"}}

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
                     if isinstance(message.content, str) and message.content.strip():
                         sys.stdout.write(message.content)
                         sys.stdout.flush()

    console.print("\n[bold green]Task Completed.[/bold green]")


async def run_autonomous_loop():
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        sys.exit(1)

    console.print(f"Codebase Path: {config.codebase_path}")
    console.print(f"Reference Codebase Path: {config.reference_codebase_path}")

    # Directories
    package_skills_dir = Path(__file__).parent / "skills"

    # Construct Prompt
    # Note: We do NOT inject skill content here anymore. SkillsMiddleware does it.
    prompt = f"""
You are an autonomous coding agent specialized in implementing Adapter patterns.

Target Codebase: {config.codebase_path}
Reference Codebase: {config.reference_codebase_path}

Your goal is to implement a new feature (likely an Adapter) in the existing codebase.
Check your available skills to see if any apply to this task.
Execute the task completely. Run tests to verify. Correct any errors.
Do not ask for user input. If you are stuck, try to solve it yourself or report the failure.
"""

    # Create Agent
    assistant_id = "code-cli-agent"
    agent, backend = create_local_agent(config.model_name, "", assistant_id, package_skills_dir)

    # Execute
    await execute_task(prompt, agent, assistant_id)

def main():
    asyncio.run(run_autonomous_loop())

if __name__ == "__main__":
    main()

import asyncio
import sys
from pathlib import Path

from deepagents_cli.agent import create_cli_agent
from deepagents_cli.config import SessionState, create_model
from deepagents_cli.execution import execute_task
from deepagents_cli.ui import TokenTracker
from deepagents_cli.tools import fetch_url, http_request

from deepagents_code_cli.config import config

async def run_autonomous_loop():
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    print(f"Codebase Path: {config.codebase_path}")
    print(f"Feature Description: {config.feature_description}")

    # Create model
    model = create_model(config.model_name)

    # Tools
    tools = [http_request, fetch_url]
    # We might need to add specific tools for this CLI if not included in default agent
    # The default agent in deepagents-cli includes file ops and shell.

    # Agent setup
    assistant_id = "code-cli-agent"

    # We need to make sure the agent has access to the skills.
    # The standard CLI loads skills from ~/.deepagents/... or project root.
    # We want to inject our 'implement_feature' skill.
    # For now, we can rely on the prompt instructing the agent, or manually inject the skill content.

    # Ideally, we should use the SkillsMiddleware, but point it to our package's skills dir.
    # However, SkillsMiddleware takes a directory path.
    package_skills_dir = Path(__file__).parent / "skills"

    # We need to set up the agent with this skills directory.
    # create_cli_agent doesn't expose skills_dir directly?
    # Let's check deepagents_cli.agent.create_cli_agent signature.

    # It seems create_cli_agent uses settings.user_skills_dir.
    # We might need to monkeypatch or subclass, or just copy the skill to a place where it's found.
    # OR, better, we can construct the agent manually if create_cli_agent is too opinionated.

    # Let's try to use create_cli_agent but update the system prompt or inject the skill.

    agent, backend = create_cli_agent(
        model=model,
        assistant_id=assistant_id,
        tools=tools,
        auto_approve=True, # No user intervention
    )

    # Read the skill content
    skill_path = package_skills_dir / "implement_feature.md"
    skill_content = skill_path.read_text()

    # Construct the initial prompt
    prompt = f"""
You are an autonomous coding agent. Your goal is to implement a new feature in an existing codebase.

Target Codebase: {config.codebase_path}
Feature Description: {config.feature_description}
Skills Directory: {package_skills_dir}

You must follow the instructions in the "Implement Feature" skill below:

---
{skill_content}
---

Execute the task completely. Run tests to verify. Correct any errors.
Do not ask for user input. If you are stuck, try to solve it yourself or report the failure.
"""

    session_state = SessionState(auto_approve=True)
    token_tracker = TokenTracker()

    # Execute
    await execute_task(
        prompt,
        agent,
        assistant_id,
        session_state,
        token_tracker,
        backend=backend
    )

def main():
    asyncio.run(run_autonomous_loop())

if __name__ == "__main__":
    main()

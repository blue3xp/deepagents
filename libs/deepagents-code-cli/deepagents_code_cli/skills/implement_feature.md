"""SKILL: Implement Feature

# Description
This skill implements a new feature in the codebase based on a description.
It follows a strict workflow: Analyze -> Plan -> Implement -> Test -> Verify.

# Instructions

1.  **Analyze the Codebase**:
    *   Read the file structure using `ls` or `shell`.
    *   Identify relevant files for the new feature.
    *   Read the content of relevant files to understand existing logic using `read_file`.

2.  **Create a Plan**:
    *   Propose a set of changes (new files, modifications).
    *   Identify where to add unit tests.

3.  **Implement Code**:
    *   Create or modify source files using `write_file` or `edit_file`.
    *   Ensure code follows existing style (if discernible).

4.  **Implement Tests**:
    *   Create a new test file or add to existing tests.
    *   Tests MUST fail if the feature is not implemented (red-green-refactor, but here we do it all at once preferably).
    *   Tests MUST cover the new functionality.

5.  **Verify**:
    *   Run the tests using `shell`.
    *   If tests fail, analyze the error, fix the code or the test, and re-run.
    *   If compilation/syntax checks fail, fix them.

6.  **Completion**:
    *   Once tests pass and code is implemented, the task is done.

# Tools
You have access to file operations and shell commands.
Use `ls`, `read_file`, `write_file`, `edit_file`, and `shell`.

# critical
You must run tests to verify your changes. Do not assume it works.
"""

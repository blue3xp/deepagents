"""SKILL: Implement Adapter

# Description
This skill specifically handles the creation of an Adapter pattern implementation for an existing class in the codebase.
It follows a strict workflow: Analyze -> Plan -> Generate Template -> Implement -> Test -> Verify.

# Instructions

1.  **Analyze the Codebase**:
    *   Read the file structure using `ls` or `shell`.
    *   Identify the class that needs an adapter (the "Adaptee").
    *   Read the content of relevant files to understand existing logic using `read_file`.

2.  **Generate Adapter Template**:
    *   Determine the name for the new Adapter class (e.g., if adapting `OldSystem`, name it `OldSystemAdapter`).
    *   Execute the helper script to generate the boilerplate:
        `python {Skills Directory}/adapter_helper.py <AdapterName>`
    *   The output of this command is your starting point.

3.  **Implement Code**:
    *   Create the new adapter file using the generated template.
    *   Implement the specific logic to adapt the interface.
    *   Ensure code follows existing style.

4.  **Implement Tests**:
    *   Create a new test file or add to existing tests.
    *   Tests MUST fail if the adapter is not working correctly.
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

# Critical
You must run tests to verify your changes. Do not assume it works.
"""

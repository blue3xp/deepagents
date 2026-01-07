---
name: implement-adapter
description: Implement Adapter pattern by analyzing codebases, generating templates, and refactoring logic.
---

# Skill: Implement Adapter

## Description
This skill specifically handles the creation of an Adapter pattern implementation for an existing class in the codebase.
It follows a strict workflow: Analyze -> Plan -> Generate Template -> Implement -> Test -> Verify.

## Instructions

1.  **Analyze and Identify Interfaces for Refactoring**:
    *   **Scan Target Codebase**: Scan `CODEBASE_PATH` (Target Codebase) to identify all defined interfaces or abstract base classes.
    *   **Filter Existing Implementations**: Check `CODEBASE_PATH` to see which of these interfaces *already have* implementations. Ignore these; we only care about interfaces that are defined but not yet implemented in the Target Codebase.
    *   **Find Legacy Implementations**: For the remaining (unimplemented) interfaces, search the `REFERENCE_CODEBASE_PATH` (Reference Codebase). Look for classes or functions that implement the logic corresponding to these interfaces.
    *   **Select Targets**: If you find an implementation in the `REFERENCE_CODEBASE_PATH` for an unimplemented interface in `CODEBASE_PATH`, this confirms the need for an Adapter (or Porting). The goal is to refactor this legacy logic into the new Adapter in the Target Codebase.
    *   **Check Knowledge Base**: Review the "Knowledge Base". If the legacy code in Reference Codebase uses standard libraries (e.g., `requests`, `urllib`) that have a private equivalent in the Knowledge Base (e.g., `private_net_lib`), note this. You MUST use the private library when rewriting the code in the Adapter.
    *   Read the content of all identified relevant files in both codebases.

2.  **Generate Adapter Template**:
    *   Determine the name for the new Adapter class (e.g., if adapting `OldSystem`, name it `OldSystemAdapter`).
    *   Execute the helper script located in this skill's directory to generate the boilerplate:
        `python <path_to_this_skill_directory>/adapter_helper.py <AdapterName>`
        *(Note: Replace `<path_to_this_skill_directory>` with the absolute path of the directory containing this SKILL.md file)*
    *   The output of this command is your starting point.

3.  **Refactor & Implement Code**:
    *   Create the new adapter file using the generated template.
    *   **Refactor Logic**:
        *   Extract the business logic from the `Reference Codebase`.
        *   **Apply Knowledge**: If the reference code uses external libraries, check if a private library from the "Knowledge Base" should be used instead.
        *   **Rewrite**: Implement the logic in the Adapter, replacing external calls with private library calls where applicable.
        *   If no private library applies, migrate the logic directly while maintaining behavior.
    *   Ensure the code follows the Target Codebase style.

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

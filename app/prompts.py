
PLAN_PROMPT = """
You are an expert Python architect.
User specification (high-level, detailed):
{spec}

Produce a JSON plan with this structure:
{
  "package_name": "{package_name}",
  "modules": [
     {"path": "<relative path like {package_name}/utils.py>", "doc": "what this module contains"},
     ...
  ],
  "tests": [
     {"path": "tests/test_*.py", "doc": "what to test, meaningful examples"}
  ]
}
Return ONLY a JSON block, ideally inside a ```json fenced block.
"""

FILE_PROMPT = """
Create a single Python file for the project.

Project package: {package}
Target path: {path}

Write clean, production-quality Python 3.11 code based on this intent:
\"\"\"{doc}\"\"\"

Return ONLY as a Python code block:
```python
# {path}
# (write the complete file here)
```
"""

REFACTOR_PROMPT = """
Given the following linter/type-check/test output, propose minimal file rewrites to make the project pass:
---
{tooling_output}
---

Return a JSON array of edits like:
[
  {"path":"<relative file path>", "content":"<FULL new file content>"},
  ...
]
Only include files that need changes.
"""

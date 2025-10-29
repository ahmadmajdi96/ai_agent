from typing import Dict, Any
from .prompts import PLAN_PROMPT

def make_plan(llm, spec: str, package_name: str) -> Dict[str, Any]:
    # Safely substitute the variables using str.replace to avoid KeyError from JSON braces
    msg = PLAN_PROMPT.replace("{spec}", spec).replace("{package_name}", package_name)

    out = llm.chat([
        {"role": "system", "content": "You are a senior Python architect."},
        {"role": "user", "content": msg}
    ])

    # Expect JSON block in output; fall back to simple dict if parsing fails
    import json, re
    try:
        # Try fenced JSON first (allow normal whitespace escapes)
        code = re.search(r"```json\s*(.*?)\s*```", out, re.DOTALL)
        txt = code.group(1) if code else None
        # Fallback: try to find the first JSON object in the output
        if not txt:
            j = re.search(r"(\{(?:.|\n)*\})", out, re.DOTALL)
            txt = j.group(1) if j else out
        plan = json.loads(txt)
    except Exception:
        plan = {
            "package_name": package_name,
            "modules": [
                {"path": f"{package_name}/core.py", "doc": "Core logic"}
            ],
            "tests": []
        }
    return plan

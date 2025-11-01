
import os
import io
import zipfile
import shutil
import subprocess
import re
import logging
from typing import Optional, List
from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

from .ollama_client import LLM
from .planner import make_plan
from .writer import CodeWriter

BASE_OUT = os.path.join(os.getcwd(), "out")
os.makedirs(BASE_OUT, exist_ok=True)

app = FastAPI(title="Local Code Writer Agent", version="0.1.0", docs_url="/")

llm = LLM(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    model_id=os.getenv("MODEL_ID", "qwen2.5-coder:14b"),
    temperature=float(os.getenv("TEMPERATURE", "0.02")),
    max_tokens=int(os.getenv("MAX_TOKENS", "4096")),
)

class GenerateRequest(BaseModel):
    project_name: str = Field(..., description="Folder name for the new project")
    spec: str = Field(..., description="Long, detailed description of variables, operations, modules, and behavior")
    package_name: Optional[str] = Field(None, description="Python package name (default: derived from project_name)")
    tests: Optional[bool] = True
    type_checking: Optional[bool] = True
    style: Optional[str] = Field("ruff", description="Code style tool")
    iterations: Optional[int] = Field(2, description="How many refine loops to attempt on test/lint failures")

@app.post("/generate")
def generate(req: GenerateRequest):
    # Sanitize project name to avoid path traversal and unsafe characters
    safe_name = os.path.basename(req.project_name)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", safe_name)
    project_dir = os.path.join(BASE_OUT, safe_name)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir, exist_ok=True)

    package_name = req.package_name or req.project_name.replace("-", "_").replace(" ", "_")
    try:
        plan = make_plan(llm, req.spec, package_name)
        writer = CodeWriter(llm, project_dir, package_name)
        writer.materialize(plan)
    except Exception as e:
        logging.exception("Failed to generate project")
        return JSONResponse({"ok": False, "error": "LLM or generation error", "details": str(e)}, status_code=500)

#    # Lint & type-check & test loop
    logs = []
  #  def run(cmd, cwd=None):
   #     p = subprocess.Popen(cmd, cwd=cwd or project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    #    out,_ = p.communicate()
     #   return p.returncode, out

#    for i in range(max(1, req.iterations)):
 #       # Ruff
  #      if req.style == "ruff":
   #         code, out = run(["ruff", "check", "--fix", "."])
    #        logs.append({"stage": f"ruff_{i}", "exit": code, "out": out})
#
 #       # mypy
  #      if req.type_checking:
   #         code, out = run(["mypy", package_name, "--ignore-missing-imports"])
    #        logs.append({"stage": f"mypy_{i}", "exit": code, "out": out})
     #       if code != 0:
      #          # ask LLM to refine
       #         writer.refine_from_tooling(out)
#
 #       # pytest
  #      if req.tests:
   #         code, out = run(["pytest", "-q"])
    #        logs.append({"stage": f"pytest_{i}", "exit": code, "out": out})
     #       if code != 0:
      #          writer.refine_from_tooling(out)
#
 #   # Zip project
    zip_path = os.path.join(BASE_OUT, f"{req.project_name}.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(project_dir):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, arcname=os.path.relpath(full, project_dir))

    return JSONResponse({
        "ok": True,
        "project_dir": project_dir,
        "zip_file": zip_path,
        "logs": logs,
        "plan": plan
    })

@app.get("/download/{project_name}.zip")
def download(project_name: str):
    path = os.path.join(BASE_OUT, f"{project_name}.zip")
    if not os.path.exists(path):
        return JSONResponse({"ok": False, "error": "zip not found"}, status_code=404)
    return FileResponse(path, media_type="application/zip", filename=f"{project_name}.zip")

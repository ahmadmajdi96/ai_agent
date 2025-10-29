
# Local Code-Writer Agent (Starter Kit)

Self-hosted **code-generation service** that turns a long natural-language spec into a Python project.
- **Model**: talks to a local **Ollama** server (default: `qwen2.5-coder:14b`).
- **Loop**: plan → write files → ruff → mypy → pytest → refine (N iterations).
- **Output**: downloadable ZIP under `/download/{project}.zip` and files in `out/`.

## Quick Start (with local Ollama service)

```bash
# 0) Pull a code model (on host)
docker run -d --name ollama -p 11434:11434 ollama/ollama:latest
ollama pull qwen2.5-coder:14b

# 1) Build agent
docker build -t local-code-writer-agent:latest .

# 2) Run agent (point to host Ollama)
docker run -p 8090:8090 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -e MODEL_ID="qwen2.5-coder:14b" -v $(pwd)/out:/app/out local-code-writer-agent:latest
```

Or use Docker Compose (with an Ollama service):
```bash
docker compose up -d
# then, on the ollama container:
docker exec -it ollama ollama pull qwen2.5-coder:14b
```

## API

### POST /generate
```json
{
  "project_name": "awesome_math_lib",
  "spec": "Provide detailed operations, variables, modules here...",
  "package_name": "awesome_math",
  "tests": true,
  "type_checking": true,
  "style": "ruff",
  "iterations": 2
}
```

Response includes a file path to `out/awesome_math_lib.zip`.  
Download via: `GET /download/awesome_math_lib.zip`

## Model options
- `qwen2.5-coder:14b` (balanced) or `:32b` (stronger), `deepseek-coder-v2`, `starcoder2:15b-instruct`, etc.
Set with `MODEL_ID` env. Adjust `MAX_TOKENS`, `TEMPERATURE` as needed.

## Notes
- This starter keeps the orchestration simple and dependency-light.
- For bigger workflows, you can bring in LangGraph/LangChain and add tools (git, shell, file ops, repo diffs).
- You can also add a **“policies”** layer to constrain imports or enforce secure coding patterns.

## License
MIT for this repo. Model licenses follow their respective providers.

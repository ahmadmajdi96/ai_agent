
import httpx
import json
import time
import logging
from typing import List, Dict, Any, Optional

class LLM:
    def __init__(self, base_url: str, model_id: str, temperature: float = 0.2, max_tokens: int = 4096):
        self.base_url = base_url.rstrip("/")
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def _achat(self, messages: List[Dict[str, str]]) -> str:
        # Streaming chat; return final text
        async with httpx.AsyncClient(timeout=700) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json={
                "model": self.model_id,
                "messages": messages,
                "stream": False,
                "options": {"temperature": self.temperature, "num_ctx": self.max_tokens}
            })
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Synchronous wrapper
        logger = logging.getLogger(__name__)
        attempts = 3
        backoff = 1.0
        for attempt in range(1, attempts + 1):
            try:
                with httpx.Client(timeout=700.0) as client:
                    resp = client.post(f"{self.base_url}/api/chat", json={
                        "model": self.model_id,
                        "messages": messages,
                        "stream": False,
                        "options": {"temperature": self.temperature, "num_ctx": self.max_tokens}
                    })
                    # Raise for non-2xx to be handled below
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("message", {}).get("content", "")
            except httpx.ConnectError as exc:
                logger.warning("ConnectError to Ollama (attempt %d/%d): %s", attempt, attempts, exc)
                if attempt == attempts:
                    raise
            except httpx.HTTPStatusError as exc:
                # Log body for debugging and decide whether to retry
                body = None
                try:
                    body = exc.response.text
                except Exception:
                    body = "<unavailable>"
                logger.error("Ollama returned HTTP %s: %s", exc.response.status_code, body)
                # 4xx usually won't improve with retries; re-raise on last attempt
                if 400 <= exc.response.status_code < 500 or attempt == attempts:
                    raise
            except Exception:
                logger.exception("Unexpected error while calling Ollama")
                if attempt == attempts:
                    raise

            time.sleep(backoff)
            backoff *= 2

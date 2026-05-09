"""Unified LLM interface for ROSClaw Wiki.

Supports Anthropic and OpenAI backends via environment variables.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

logger = logging.getLogger("rosclaw.llm")

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-flash"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MOONSHOT_MODEL = "moonshot-v1-8k"
DEFAULT_MOONSHOT_BASE_URL = "https://api.moonshot.cn"


class LLMInterface:
    """Unified interface for LLM completions with retry and timeout."""

    def __init__(self, backend: str | None = None):
        self.backend = backend or self._detect_backend()
        self.api_key = self._get_api_key()
        self.timeout = 120
        self.max_retries = 2

    def _detect_backend(self) -> str:
        if os.environ.get("ROSCLAW_MOCK_LLM"):
            return "mock"
        if os.environ.get("DEEPSEEK_API_KEY"):
            return "deepseek"
        if os.environ.get("OPENAI_API_KEY"):
            return "openai"
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if anthropic_key and anthropic_key.startswith("sk-kimi"):
            return "kimi"
        if anthropic_key:
            return "anthropic"
        return "none"

    def _get_api_key(self) -> str | None:
        if self.backend == "deepseek":
            return os.environ.get("DEEPSEEK_API_KEY")
        if self.backend == "openai":
            return os.environ.get("OPENAI_API_KEY")
        if self.backend in ("anthropic", "kimi"):
            return os.environ.get("ANTHROPIC_API_KEY")
        if self.backend == "mock":
            return "mock"
        return None

    def complete(
        self,
        prompt: str,
        model: str | None = None,
        system: str | None = None,
        temperature: float = 0.3,
    ) -> str:
        """Send a completion request to the configured LLM backend.

        Args:
            prompt: The user prompt.
            model: Override model name.
            system: System prompt text.
            temperature: Sampling temperature.

        Returns:
            The LLM's text response.

        Raises:
            RuntimeError: If no backend is configured or all retries fail.
        """
        if self.backend == "none" or not self.api_key:
            raise RuntimeError(
                "No LLM backend configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or DEEPSEEK_API_KEY."
            )

        model = model or {
            "anthropic": DEFAULT_CLAUDE_MODEL,
            "openai": DEFAULT_OPENAI_MODEL,
            "deepseek": DEFAULT_DEEPSEEK_MODEL,
            "kimi": DEFAULT_OPENAI_MODEL,
            "mock": "mock-model",
        }.get(self.backend, DEFAULT_CLAUDE_MODEL)

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                if self.backend == "anthropic":
                    return self._call_anthropic(prompt, model, system, temperature)
                if self.backend == "openai":
                    return self._call_openai(prompt, model, system, temperature)
                if self.backend == "deepseek":
                    return self._call_deepseek(prompt, model, system, temperature)
                if self.backend == "kimi":
                    return self._call_kimi(prompt, model, system, temperature)
                if self.backend == "mock":
                    return self._call_mock(prompt, model, system, temperature)
            except Exception as exc:
                last_exc = exc
                logger.warning("LLM call attempt %d failed: %s", attempt + 1, exc)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)

        raise RuntimeError(f"LLM call failed after {self.max_retries + 1} attempts: {last_exc}")

    def _call_anthropic(
        self, prompt: str, model: str, system: str | None, temperature: float
    ) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": model,
            "max_tokens": 4096,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]

    def _call_openai(
        self, prompt: str, model: str, system: str | None, temperature: float
    ) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _call_deepseek(
        self, prompt: str, model: str, system: str | None, temperature: float
    ) -> str:
        """Call DeepSeek API (OpenAI-compatible format)."""
        url = f"{DEFAULT_DEEPSEEK_BASE_URL}/v1/chat/completions"
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _call_kimi(
        self, prompt: str, model: str, system: str | None, temperature: float
    ) -> str:
        """Call Kimi API via OpenAI-compatible endpoint."""
        base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.moonshot.cn")
        url = f"{base_url.rstrip('/')}/v1/chat/completions"
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _call_mock(
        self, prompt: str, model: str, system: str | None, temperature: float
    ) -> str:
        """Return a structured mock response for offline/demo runs."""
        # Extract title from the SOURCE section of the prompt
        title = "Unknown Entity"
        source_started = False
        for line in prompt.splitlines():
            line_stripped = line.strip()
            if line_stripped == "SOURCE:":
                source_started = True
                continue
            if source_started and line_stripped == "---":
                continue
            if source_started and line_stripped.startswith("# ") and not line_stripped.startswith("# Source"):
                title = line_stripped[2:].strip()
                break
            if source_started and (line_stripped.startswith("**Title:**") or line_stripped.startswith("Title:")):
                title = line_stripped.split(":", 1)[1].strip()
                break

        # Extraction prompt → return JSON entities
        if "TASK: Extract" in prompt or "extract entities" in prompt.lower():
            return json.dumps(
                [
                    {
                        "entity_type": "algorithm",
                        "entity_name": title,
                        "new_facts": {
                            "parameters": {
                                "input_type": "visual",
                                "output_type": "navigation",
                            },
                            "capabilities": [
                                "object navigation",
                                "semantic understanding",
                            ],
                            "relationships": {
                                "uses": ["CNN", "Transformer"],
                                "depends_on": ["SLAM"],
                            },
                            "new_sections": {
                                "Overview": f"Research on {title}.",
                                "Method": "Proposed novel deep learning approach.",
                                "Results": "State-of-the-art performance on benchmarks.",
                            },
                        },
                        "source_type": "arxiv_paper",
                    }
                ],
                ensure_ascii=False,
            )

        # Rewrite prompt → return markdown
        return (
            f"# {title}\n\n"
            "## Overview\n\n"
            f"This page describes **{title}**, a method in embodied intelligence research.\n\n"
            "## Method\n\n"
            "The proposed approach leverages deep learning for visual navigation tasks.\n\n"
            "## Results\n\n"
            "Achieved state-of-the-art performance on standard benchmark datasets.\n\n"
            "## References\n\n"
            "- Original paper and open-source implementation.\n"
        )


# Convenience function for one-off calls
def llm_complete(
    prompt: str,
    model: str | None = None,
    system: str | None = None,
    temperature: float = 0.3,
) -> str:
    """One-shot LLM completion using default backend."""
    iface = LLMInterface()
    return iface.complete(prompt, model=model, system=system, temperature=temperature)

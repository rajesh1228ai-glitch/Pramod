import json
import requests
from typing import Any
from urllib.parse import quote_plus


class OllamaClient:
    def __init__(self, endpoint: str, model: str) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        endpoints = [
            (f"{self.endpoint}/v1/completions", {"model": self.model, "prompt": prompt, "max_tokens": 1024, "temperature": 0.2}),
            (f"{self.endpoint}/v1/chat/completions", {"model": self.model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024, "temperature": 0.2}),
            (f"{self.endpoint}/v1/responses", {"model": self.model, "input": prompt, "max_tokens": 1024, "temperature": 0.2}),
            (f"{self.endpoint}/v1/models/{quote_plus(self.model)}/complete", {"model": self.model, "prompt": prompt, "max_tokens": 1024, "temperature": 0.2}),
            (f"{self.endpoint}/v1/models/{quote_plus(self.model)}/outputs", {"model": self.model, "input": prompt, "max_tokens": 1024, "temperature": 0.2}),
        ]

        last_exception: Exception | None = None
        for url, payload in endpoints:
            try:
                response = requests.post(url, json=payload, timeout=20)
                if response.status_code in (404, 405):
                    last_exception = Exception(f"Ollama endpoint {url} returned {response.status_code}")
                    continue
                response.raise_for_status()
                data = self._parse_response(response)
                result = self._extract_text(data)
                if result:
                    return result
            except Exception as exc:
                last_exception = exc
                continue

        raise last_exception or RuntimeError("Ollama generation failed")

    def _is_json(self, response: requests.Response) -> bool:
        return "application/json" in response.headers.get("Content-Type", "")

    def _parse_response(self, response: requests.Response) -> Any:
        if self._is_json(response):
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"text": response.text}
        return {"text": response.text}

    def _extract_text(self, data: Any) -> str:
        if isinstance(data, str):
            return data.strip()

        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list):
                for choice in data["choices"]:
                    if not isinstance(choice, dict):
                        continue
                    if "message" in choice and isinstance(choice["message"], dict):
                        text = choice["message"].get("content")
                        if isinstance(text, str) and text.strip():
                            return text.strip()
                    if "text" in choice and isinstance(choice["text"], str) and choice["text"].strip():
                        return choice["text"].strip()
                    if "delta" in choice and isinstance(choice["delta"], dict):
                        text = choice["delta"].get("content")
                        if isinstance(text, str) and text.strip():
                            return text.strip()

            if "output" in data:
                output = data["output"]
                if isinstance(output, str):
                    return output.strip()
                if isinstance(output, list):
                    parts = []
                    for item in output:
                        if isinstance(item, str):
                            parts.append(item)
                        elif isinstance(item, dict):
                            if "text" in item and isinstance(item["text"], str):
                                parts.append(item["text"])
                            elif "content" in item and isinstance(item["content"], str):
                                parts.append(item["content"])
                            elif "content" in item and isinstance(item["content"], list):
                                for sub in item["content"]:
                                    if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                                        parts.append(sub["text"])
                    return "\n".join(part for part in parts if part).strip()

            if "response" in data:
                response = data["response"]
                if isinstance(response, dict):
                    output = response.get("output", response.get("text", ""))
                    if isinstance(output, str):
                        return output.strip()
                    if isinstance(output, list):
                        parts = []
                        for item in output:
                            if isinstance(item, str):
                                parts.append(item)
                            elif isinstance(item, dict):
                                if "text" in item and isinstance(item["text"], str):
                                    parts.append(item["text"])
                                elif "content" in item and isinstance(item["content"], str):
                                    parts.append(item["content"])
                                elif "content" in item and isinstance(item["content"], list):
                                    for sub in item["content"]:
                                        if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                                            parts.append(sub["text"])
                        return "\n".join(part for part in parts if part).strip()
                if isinstance(response, str):
                    return response.strip()

            if "text" in data and isinstance(data["text"], str) and data["text"].strip():
                return data["text"].strip()

            if "content" in data:
                if isinstance(data["content"], str):
                    return data["content"].strip()
                if isinstance(data["content"], list):
                    return "\n".join(str(item) for item in data["content"]).strip()

            if "output_text" in data and isinstance(data["output_text"], str):
                return data["output_text"].strip()

        return json.dumps(data).strip()


class GroqClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.endpoints = [
            "https://api.groq.com/v1/completions",
            "https://api.groq.com/v1/chat/completions",
            "https://api.groq.com/v1/responses",
            "https://api.groq.com/completions",
            "https://api.groq.com/chat/completions",
            "https://api.groq.com/responses",
        ]

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payloads = [
            {"model": "groq-1", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024, "temperature": 0.2},
            {"model": "groq-1", "input": prompt, "max_tokens": 1024, "temperature": 0.2},
            {"input": prompt, "max_tokens": 1024, "temperature": 0.2},
        ]

        last_exception: Exception | None = None
        for url in self.endpoints:
            for payload in payloads:
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    if response.status_code in (404, 405):
                        last_exception = Exception(f"Groq endpoint {url} returned {response.status_code}")
                        continue
                    response.raise_for_status()
                    data = self._parse_response(response)
                    result = self._extract_text(data)
                    if result:
                        return result
                except Exception as exc:
                    last_exception = exc
                    continue

        raise last_exception or RuntimeError("Groq generation failed")

    def _is_json(self, response: requests.Response) -> bool:
        return "application/json" in response.headers.get("Content-Type", "")

    def _parse_response(self, response: requests.Response) -> Any:
        if self._is_json(response):
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"text": response.text}
        return {"text": response.text}

    def _extract_text(self, data: Any) -> str:
        if isinstance(data, str):
            return data.strip()

        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list):
                for choice in data["choices"]:
                    if not isinstance(choice, dict):
                        continue
                    if "message" in choice and isinstance(choice["message"], dict):
                        text = choice["message"].get("content")
                        if isinstance(text, str) and text.strip():
                            return text.strip()
                    if "text" in choice and isinstance(choice["text"], str) and choice["text"].strip():
                        return choice["text"].strip()
                    if "delta" in choice and isinstance(choice["delta"], dict):
                        text = choice["delta"].get("content")
                        if isinstance(text, str) and text.strip():
                            return text.strip()

            if "output" in data:
                output = data["output"]
                if isinstance(output, str):
                    return output.strip()
                if isinstance(output, list):
                    texts = []
                    for item in output:
                        if isinstance(item, str):
                            texts.append(item)
                        elif isinstance(item, dict):
                            if "text" in item and isinstance(item["text"], str):
                                texts.append(item["text"])
                            elif "content" in item and isinstance(item["content"], str):
                                texts.append(item["content"])
                            elif "content" in item and isinstance(item["content"], list):
                                for sub in item["content"]:
                                    if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                                        texts.append(sub["text"])
                    return "\n".join(text for text in texts if text).strip()

            if "response" in data and isinstance(data["response"], dict):
                output = data["response"].get("output", data["response"].get("text", ""))
                if isinstance(output, str):
                    return output.strip()
                if isinstance(output, list):
                    texts = []
                    for item in output:
                        if isinstance(item, str):
                            texts.append(item)
                        elif isinstance(item, dict):
                            if "text" in item and isinstance(item["text"], str):
                                texts.append(item["text"])
                            elif "content" in item and isinstance(item["content"], str):
                                texts.append(item["content"])
                            elif "content" in item and isinstance(item["content"], list):
                                for sub in item["content"]:
                                    if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                                        texts.append(sub["text"])
                    return "\n".join(text for text in texts if text).strip()

            if "message" in data and isinstance(data["message"], dict):
                return data["message"].get("content", "").strip()

            if "text" in data and isinstance(data["text"], str) and data["text"].strip():
                return data["text"].strip()

            if "content" in data:
                if isinstance(data["content"], str):
                    return data["content"].strip()
                if isinstance(data["content"], list):
                    return "\n".join(str(item) for item in data["content"]).strip()

            if "output_text" in data and isinstance(data["output_text"], str):
                return data["output_text"].strip()

        return json.dumps(data).strip()


class LLMClient:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.provider = config.get("llm_provider", "ollama").lower()
        self.ollama = OllamaClient(config.get("ollama_url", "http://localhost:11434"), config.get("ollama_model", "gemma3:1b"))
        self.groq = GroqClient(config.get("groq_api_key", ""))

    def generate(self, prompt: str, force_provider: str | None = None) -> tuple[str, str]:
        provider = force_provider or self.provider
        if provider == "groq":
            return "groq", self.groq.generate(prompt)

        try:
            return "ollama", self.ollama.generate(prompt)
        except Exception:
            return "groq", self.groq.generate(prompt)

import os
import time
import requests
 
from dataclasses import dataclass
from abc import ABC, abstractmethod
 
from google import genai
from google.genai import types
 
 
@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int
 
 
class LLMProvider(ABC):
 
    @abstractmethod
    def generate(self, prompt):
        pass
 
 
# Hosted Gemini provider
class GeminiProvider(LLMProvider):
 
    provider_name = "Gemini"
 
    def __init__(self, api_key, model="gemini-3.8-flash"):
        self.model = model
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=120000)
        )
 
    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
 
        usage = response.usage_metadata
        input_count = getattr(usage, "prompt_token_count", 0) or 0
        output_count = getattr(usage, "candidates_token_count", 0) or 0
 
        return LLMResult(
            text=response.text or "",
            input_tokens=input_count,
            output_tokens=output_count
        )
 
 
# Local Ollama provider
class OllamaProvider(LLMProvider):
 
    provider_name = "Ollama"
 
    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
 
    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=(5, 60)
        )
        response.raise_for_status()
        data = response.json()
 
        return LLMResult(
            text=data.get("response", ""),
            input_tokens=data.get("prompt_eval_count", 0) or 0,
            output_tokens=data.get("eval_count", 0) or 0
        )
 
 
class LLMClient:
 
    def __init__(self, provider, usage_logger):
        self.provider = provider
        self.usage_logger = usage_logger
 
    def generate(self, prompt):
        start = time.perf_counter()
        max_attempts = 3
 
        for attempt in range(max_attempts):
            try:
                result = self.provider.generate(prompt)
                latency_ms = round(
                    (time.perf_counter() - start) * 1000, 2
                )
 
                input_rate = float(os.getenv(
                    "GEMINI_INPUT_PRICE_PER_MILLION", "0"
                ))
                output_rate = float(os.getenv(
                    "GEMINI_OUTPUT_PRICE_PER_MILLION", "0"
                ))
 
                if self.provider.provider_name == "Gemini":
                    cost = (
                        result.input_tokens * input_rate
                        + result.output_tokens * output_rate
                    ) / 1_000_000
                    cost_type = "estimated_hosted_api_cost"
                else:
                    # Local Ollama has no hosted API token charge.
                    cost = 0.0
                    cost_type = "local_inference_cost_not_included"
 
                self.usage_logger.log_call({
                    "provider": self.provider.provider_name,
                    "model": self.provider.model,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "total_tokens": (
                        result.input_tokens + result.output_tokens
                    ),
                    "latency_ms": latency_ms,
                    "estimated_cost_usd": round(cost, 8),
                    "cost_type": cost_type,
                    "status": "success",
                    "attempts": attempt + 1
                })
 
                print(f"Latency: {latency_ms} ms")
                print(f"Input tokens: {result.input_tokens}")
                print(f"Output tokens: {result.output_tokens}")
                print(f"Estimated cost (USD): {cost}")
 
                return result.text
 
            except Exception as error:
                status = getattr(error, "status_code", None)
                if status is None:
                    status = getattr(error, "code", None)
 
                error_name = type(error).__name__.lower()
                retryable = (
                    isinstance(error, (
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError
                    ))
                    or status in (408, 429, 500, 502, 503, 504)
                    or "timeout" in error_name
                    or "unavailable" in error_name
                    or "resourceexhausted" in error_name
                )
 
                if not retryable or attempt == max_attempts - 1:
                    latency_ms = round(
                        (time.perf_counter() - start) * 1000, 2
                    )
                    self.usage_logger.log_call({
                        "provider": self.provider.provider_name,
                        "model": self.provider.model,
                        "input_tokens": None,
                        "output_tokens": None,
                        "total_tokens": None,
                        "latency_ms": latency_ms,
                        "estimated_cost_usd": None,
                        "status": "failed",
                        "attempts": attempt + 1,
                        "error": str(error)
                    })
                    raise
 
                delay = 2 ** attempt
                print(
                    f"Temporary error. Retry {attempt + 1} "
                    f"of {max_attempts - 1} in {delay} seconds."
                )
                time.sleep(delay)

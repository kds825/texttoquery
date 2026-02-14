import httpx
from openai import AsyncOpenAI
from t2qbot.config.settings import get_settings

settings = get_settings()

class LLMClient:
    async def generate(self, prompt: str) ->str:
        if settings.llm_provider == "ollama":
            return await self._ollama(prompt)
        elif settings.llm_provider =="openai":
            return await self._openai(prompt)
        else:
            raise ValueError("Invalid LLM_PROVIDER")
        
    async def _ollama(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model":settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature":0.2}
                }
            )
            return r.json()["response"]
        
    async def _openai(self, prompt: str) -> str:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        
        resp = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You output exactly what is asked."},
                {"role": "user", "content":prompt}
            ],
            temperature = 0.2
        )
        
        return resp.choices[0].message.content
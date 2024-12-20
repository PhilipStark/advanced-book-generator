from openai import OpenAI
from anthropic import Anthropic
import os
from typing import Dict, Any

class BookGenerator:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def generate_structure(self, prompt: Dict[str, Any]) -> str:
        response = await self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a master book architect."},
                {"role": "user", "content": str(prompt)}
            ]
        )
        return response.choices[0].message.content

    async def generate_content(self, structure: str) -> str:
        response = await self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100000,
            messages=[{
                "role": "user",
                "content": f"Generate a book based on this structure: {structure}"
            }]
        )
        return response.content
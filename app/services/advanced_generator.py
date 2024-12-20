from typing import Dict, List, Optional, Any
import asyncio
from openai import OpenAI
from anthropic import Anthropic
import numpy as np
from datetime import datetime

class AdvancedGenerator:
    """Sistema avançado de geração de conteúdo"""
    
    def __init__(self):
        self.openai_client = OpenAI()
        self.anthropic_client = Anthropic()
        self.quality_threshold = 9.8
        
    async def generate_content(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Gera conteúdo usando múltiplos modelos em pipeline"""
        
        # 1. Análise e enriquecimento do prompt
        enriched_prompt = await self._enrich_prompt(prompt)
        
        # 2. Geração da estrutura base
        structure = await self._generate_structure(enriched_prompt)
        
        # 3. Geração do conteúdo detalhado
        content = await self._generate_detailed_content(structure)
        
        # 4. Análise de qualidade
        quality_score = await self._analyze_quality(content)
        
        # 5. Refinamento se necessário
        if quality_score < self.quality_threshold:
            content = await self._refine_content(content)
        
        # 6. Preparação final
        final_content = await self._prepare_final_content(content)
        
        return final_content
    
    async def _enrich_prompt(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquece o prompt com análise avançada"""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise e enriquecimento de prompts para geração de conteúdo."},
                {"role": "user", "content": str(prompt)}
            ]
        )
        
        return {
            "original_prompt": prompt,
            "enriched_data": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_structure(self, enriched_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Gera a estrutura base do conteúdo"""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em criar estruturas narrativas complexas e envolventes."},
                {"role": "user", "content": str(enriched_prompt)}
            ]
        )
        
        return {
            "prompt": enriched_prompt,
            "structure": response.choices[0].message.content,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
    
    async def _generate_detailed_content(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Gera o conteúdo detalhado usando Claude"""
        
        response = await self.anthropic_client.messages.create(
            model="claude-2",
            max_tokens=100000,
            messages=[{
                "role": "user",
                "content": f"Gere conteúdo detalhado baseado nesta estrutura: {str(structure)}"
            }]
        )
        
        return {
            "structure": structure,
            "content": response.content[0].text,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model": "claude-2"
            }
        }
    
    async def _analyze_quality(self, content: Dict[str, Any]) -> float:
        """Analisa a qualidade do conteúdo gerado"""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de qualidade de conteúdo. Avalie de 0 a 10."},
                {"role": "user", "content": str(content)}
            ]
        )
        
        try:
            score = float(response.choices[0].message.content)
            return min(max(score, 0), 10)  # Garante que o score está entre 0 e 10
        except:
            return 0.0
    
    async def _refine_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Refina o conteúdo para melhorar a qualidade"""
        
        response = await self.anthropic_client.messages.create(
            model="claude-2",
            max_tokens=100000,
            messages=[{
                "role": "user",
                "content": f"Refine e melhore este conteúdo mantendo sua essência: {str(content)}"
            }]
        )
        
        return {
            "original_content": content,
            "refined_content": response.content[0].text,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "refined-1.0"
            }
        }
    
    async def _prepare_final_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara o conteúdo final para entrega"""
        
        return {
            "content": content,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "final-1.0",
                "quality_metrics": {
                    "final_score": await self._analyze_quality(content)
                }
            }
        }

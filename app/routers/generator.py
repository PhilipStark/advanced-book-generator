from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..services.advanced_generator import AdvancedGenerator
from ..schemas import GenerationRequest, GenerationResponse

router = APIRouter(
    prefix="/generate",
    tags=["generator"]
)

@router.post("/", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    """
    Endpoint para gerar conteúdo usando o sistema avançado
    """
    try:
        generator = AdvancedGenerator()
        result = await generator.generate_content(request.dict())
        return GenerationResponse(
            content=result["content"],
            metadata=result["metadata"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na geração de conteúdo: {str(e)}"
        )

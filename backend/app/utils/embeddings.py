"""
Embedding utilities for semantic search
"""
from typing import List
import numpy as np
from app.services.llm_service import LLMService
from app.core.logger import logger


async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for text
    """
    try:
        # TODO: Implement actual embedding generation
        # Using OpenAI embeddings or similar
        return np.random.rand(1536).tolist()
    except Exception as e:
        logger.error(f"Embedding generation error: {str(e)}")
        return []


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)

    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)

"""
Clients for external services (OCR, LLM)
"""
from src.shared.clients.ocr_client import OCRClient
from src.shared.clients.llm_client import LLMClient

__all__ = ["OCRClient", "LLMClient"]
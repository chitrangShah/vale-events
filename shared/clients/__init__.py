"""
Clients for external services (OCR, LLM)
"""
from shared.clients.ocr_client import OCRClient
from shared.clients.llm_client import LLMClient

__all__ = ["OCRClient", "LLMClient"]
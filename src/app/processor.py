"""Processor module for stock-quant-arbitrage.

Consumes market data payloads and applies arbitrage detection logic.
"""

from typing import Any

from app.arbitrage_engine import run_arbitrage_analysis
from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def process_payload(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Processes a market data payload and runs arbitrage analysis.

    Args:
        payload (dict[str, Any]): Market data input including price series.

    Returns:
        dict[str, Any] | None: Signal if arbitrage found, else None.
    """
    logger.debug("🧮 Processing arbitrage payload...")
    return run_arbitrage_analysis(payload)

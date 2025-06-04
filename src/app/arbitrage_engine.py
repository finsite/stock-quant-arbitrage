"""Arbitrage detection engine for stock-quant-arbitrage.

This module contains logic to evaluate market data for arbitrage
opportunities between correlated instruments. It may use price spread,
mean reversion, or statistical models to trigger a signal.
"""

from typing import Any

from app.config import get_lookback_period, get_spread_threshold
from app.logger import setup_logger

logger = setup_logger(__name__)


def run_arbitrage_analysis(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Core arbitrage detection logic. Takes a message payload (market data),
    applies detection logic, and returns a signal if an opportunity is found.
    
    Args:
    ----
        payload (dict): Market data payload containing symbol, timestamp, price, etc.

    :param payload: dict[str:
    :param Any: param payload: dict[str:
    :param Any: param payload: dict[str:
    :param Any: 
    :param payload: 
    :type payload: dict[str :
    :param Any]: 
    :param payload: 
    :type payload: dict[str :
    :param payload: dict[str: 

    
    """
    symbol_a = payload.get("symbol_a")
    symbol_b = payload.get("symbol_b")
    prices_a = payload.get("prices_a")  # List[float]
    prices_b = payload.get("prices_b")  # List[float]

    if not prices_a or not prices_b:
        logger.warning("❌ Invalid payload, missing price data.")
        return None

    lookback = get_lookback_period()
    spread_threshold = get_spread_threshold()

    # Trim to lookback window
    prices_a = prices_a[-lookback:]
    prices_b = prices_b[-lookback:]

    if len(prices_a) != len(prices_b):
        logger.warning("⚠️ Price lists have different lengths.")
        return None

    # Simple spread calculation
    spread = [abs(a - b) for a, b in zip(prices_a, prices_b)]
    avg_spread = sum(spread) / len(spread)

    logger.debug(f"🔎 Avg spread: {avg_spread:.4f} | Threshold: {spread_threshold:.4f}")

    if avg_spread >= spread_threshold:
        logger.info(f"✅ Arbitrage opportunity detected between {symbol_a} and {symbol_b}")
        return {
            "type": "arbitrage_signal",
            "symbol_a": symbol_a,
            "symbol_b": symbol_b,
            "avg_spread": avg_spread,
            "timestamp": payload.get("timestamp"),
        }

    return None

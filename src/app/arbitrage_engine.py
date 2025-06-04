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
    """Detect arbitrage opportunities between two correlated instruments.

    Takes a payload containing price history for two symbols, calculates
    the spread between them over a lookback window, and compares the average
    spread to a threshold. If the spread exceeds the threshold, a signal is emitted.

    Args:
    ----
        payload (dict[str, Any]): Market data including 'symbol_a', 'symbol_b',
            'prices_a', 'prices_b', and 'timestamp'.

    Returns:
    -------
        dict[str, Any] | None: A signal dictionary if an opportunity is found, or None.
    """
    symbol_a = payload.get("symbol_a")
    symbol_b = payload.get("symbol_b")
    prices_a = payload.get("prices_a")  # Expected: list of floats
    prices_b = payload.get("prices_b")  # Expected: list of floats

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

    # Calculate absolute spread between price series
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

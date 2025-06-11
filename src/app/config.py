"""Repo-specific configuration for stock-quant-arbitrage."""

from app.config_shared import *


def get_poller_name() -> str:
    """Return the name of the poller for this service."""
    return get_config_value("POLLER_NAME", "stock_quant_arbitrage")


def get_rabbitmq_queue() -> str:
    """Return the RabbitMQ queue name for this poller."""
    return get_config_value("RABBITMQ_QUEUE", "stock_quant_arbitrage_queue")


def get_dlq_name() -> str:
    """Return the Dead Letter Queue (DLQ) name for this poller."""
    return get_config_value("DLQ_NAME", "stock_quant_arbitrage_dlq")

def get_lookback_period() -> int:
    """Return the historical lookback period for arbitrage computation."""
    return int(get_config_value("LOOKBACK_PERIOD", 30))

def get_spread_threshold() -> float:
    """Return the threshold for arbitrage spread detection."""
    return float(get_config_value("SPREAD_THRESHOLD", 0.02))
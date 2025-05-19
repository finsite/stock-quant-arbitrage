"""Configuration module for the stock-quant-arbitrage service.

Provides typed getter functions to retrieve configuration values from
Vault, environment variables, or defaults.
"""

import os

from app.utils.vault_client import VaultClient

# Initialize and cache Vault client
_vault = VaultClient()


def get_config_value(key: str, default: str | None = None) -> str:
    """Retrieve a configuration value from Vault, environment variable, or default.

    Args:
        key (str): Configuration key to fetch.
        default (Optional[str]): Fallback value if key is not found.

    Returns:
        str: The resolved value.

    """
    val = _vault.get(key, os.getenv(key))
    if val is None:
        if default is not None:
            return str(default)
        raise ValueError(f"❌ Missing required config for key: {key}")
    return str(val)


# ------------------------------------------------------------------------------
# 📬 Queue Configuration
# ------------------------------------------------------------------------------


def get_queue_type() -> str:
    return get_config_value("QUEUE_TYPE", "rabbitmq")


def get_rabbitmq_host() -> str:
    return get_config_value("RABBITMQ_HOST", "localhost")


def get_rabbitmq_port() -> int:
    return int(get_config_value("RABBITMQ_PORT", "5672"))


def get_rabbitmq_vhost() -> str:
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


def get_rabbitmq_user() -> str:
    return get_config_value("RABBITMQ_USER", "")


def get_rabbitmq_password() -> str:
    return get_config_value("RABBITMQ_PASS", "")


def get_rabbitmq_exchange() -> str:
    return get_config_value("RABBITMQ_EXCHANGE", "stock_arbitrage")


def get_rabbitmq_routing_key() -> str:
    return get_config_value("RABBITMQ_ROUTING_KEY", "arbitrage_opportunity")


def get_sqs_queue_url() -> str:
    return get_config_value("SQS_QUEUE_URL", "")


def get_sqs_region() -> str:
    return get_config_value("SQS_REGION", "us-east-1")


# ------------------------------------------------------------------------------
# 💹 Arbitrage Detection Configuration
# ------------------------------------------------------------------------------


def get_lookback_period() -> int:
    """Number of time steps to use for historical spread analysis."""
    return int(get_config_value("LOOKBACK_PERIOD", "30"))


def get_spread_threshold() -> float:
    """Minimum spread threshold for detecting arbitrage opportunity."""
    return float(get_config_value("SPREAD_THRESHOLD", "0.01"))


def get_polling_interval() -> int:
    """Polling interval (in seconds) for checking arbitrage conditions."""
    return int(get_config_value("POLLING_INTERVAL", "60"))

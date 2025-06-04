"""Main entry point for the stock-quant-arbitrage module.

This script initializes the arbitrage detection service,
sets up logging, and begins consuming market data from the
configured message queue for arbitrage signal generation.
"""

import os
import sys

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.logger import setup_logger
from app.queue_handler import consume_messages

# Initialize logger
logger = setup_logger(__name__)


def main() -> None:
    """Starts the arbitrage detection service.
    
    This service listens to incoming market data from RabbitMQ or SQS,
    performs statistical or price-based arbitrage detection,
    and publishes signals when opportunities are found.


    """
    logger.info("🚀 Starting Arbitrage Detection Service...")
    consume_messages()


if __name__ == "__main__":
    main()

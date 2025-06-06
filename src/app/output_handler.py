"""Module to handle output of analysis results to a chosen output target.

This implementation logs the result, prints it to stdout, and sends the
data to RabbitMQ or SQS, unless OUTPUT_MODE is set to 'log'.
"""

import json
from typing import Any

from app import config
from app.logger import setup_logger
from app.queue_sender import publish_to_queue

# Initialize logger
logger = setup_logger(__name__)


def send_to_output(data: dict[str, Any]) -> None:
    """Outputs a processed analysis result to the configured output system.

    This function will:
      - Log the data
      - Print it to stdout
      - Send it to RabbitMQ or SQS (unless OUTPUT_MODE is set to 'log')

    Args:
    ----
        data (dict[str, Any]): The processed analysis result to send.
    """
    try:
        formatted_output = json.dumps(data, indent=4)
        logger.info("Sending data to output:\n%s", formatted_output)
        print(formatted_output)

        if config.get_output_mode() == "log":
            logger.info("🔄 OUTPUT_MODE is 'log'; skipping publish to queue.")
            return

        publish_to_queue([data])
        logger.info("✅ Output successfully published to queue.")
    except Exception as e:
        logger.error("❌ Failed to send output: %s", e)

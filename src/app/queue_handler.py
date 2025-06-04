"""Handles message queue consumption for RabbitMQ and SQS.

This module receives market data, applies arbitrage detection logic via the
processor module, and sends resulting signals to the output handler.
"""

import json
import os
import time
from typing import Any

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from app.logger import setup_logger
from app.output_handler import send_to_output
from app.processor import process_payload

logger = setup_logger(__name__)

# ------------------------------------------------------------------------------
# Configuration (fallback for environment-based local testing)
# ------------------------------------------------------------------------------

QUEUE_TYPE = os.getenv("QUEUE_TYPE", "rabbitmq").lower()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "stock_arbitrage")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "arbitrage_queue")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "#")

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
SQS_REGION = os.getenv("SQS_REGION", "us-east-1")

# ------------------------------------------------------------------------------
# SQS Initialization
# ------------------------------------------------------------------------------

sqs_client = None
if QUEUE_TYPE == "sqs":
    try:
        sqs_client = boto3.client("sqs", region_name=SQS_REGION)
        logger.info(f"SQS client initialized for region {SQS_REGION}")
    except (BotoCoreError, NoCredentialsError) as e:
        logger.error("Failed to initialize SQS client: %s", e)


# ------------------------------------------------------------------------------
# RabbitMQ Consumer
# ------------------------------------------------------------------------------

def connect_to_rabbitmq() -> pika.BlockingConnection:
    """Attempt to connect to RabbitMQ with retry logic."""
    retries = 5
    while retries > 0:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            if conn.is_open:
                logger.info("✅ Connected to RabbitMQ")
                return conn
        except Exception as e:
            retries -= 1
            logger.warning("RabbitMQ connection failed: %s. Retrying in 5s...", e)
            time.sleep(5)
    raise ConnectionError("❌ Could not connect to RabbitMQ after retries")


def consume_rabbitmq() -> None:
    """Consume and process messages from a RabbitMQ queue."""
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.queue_bind(
        exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY
    )

    def callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        """Handle an incoming RabbitMQ message."""
        try:
            message: dict[str, Any] = json.loads(body)
            logger.info("📩 Received RabbitMQ message: %s", message)

            result = process_payload(message)
            if result:
                result["source"] = "ArbEngine"
                send_to_output(result)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError:
            logger.error("Invalid JSON: %s", body)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error("Error processing RabbitMQ message: %s", e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    logger.info("📡 Listening for messages on RabbitMQ...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("👋 Shutting down RabbitMQ consumer...")
        channel.stop_consuming()
    finally:
        connection.close()


# ------------------------------------------------------------------------------
# SQS Consumer
# ------------------------------------------------------------------------------

def consume_sqs() -> None:
    """Consume and process messages from an Amazon SQS queue."""
    if not sqs_client or not SQS_QUEUE_URL:
        logger.error("SQS not initialized or missing queue URL.")
        return

    logger.info("📡 Polling SQS queue...")

    while True:
        try:
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
            )

            for msg in response.get("Messages", []):
                try:
                    body = json.loads(msg["Body"])
                    logger.info("📩 Received SQS message: %s", body)

                    result = process_payload(body)
                    if result:
                        result["source"] = "ArbEngine"
                        send_to_output(result)

                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=msg["ReceiptHandle"],
                    )
                    logger.info("✅ Deleted SQS message: %s", msg["MessageId"])
                except Exception as e:
                    logger.error("Error processing SQS message: %s", e)
        except Exception as e:
            logger.error("SQS polling failed: %s", e)
            time.sleep(5)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------

def consume_messages() -> None:
    """Entrypoint for selecting the correct queue system (RabbitMQ or SQS)."""
    if QUEUE_TYPE == "rabbitmq":
        consume_rabbitmq()
    elif QUEUE_TYPE == "sqs":
        consume_sqs()
    else:
        logger.error("❌ Invalid QUEUE_TYPE specified. Use 'rabbitmq' or 'sqs'.")

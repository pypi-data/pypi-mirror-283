from .rabbitmq_dtos import (
    MqGetLLMResponseDto,
    MqPersistNewMessageDto,
    MqLLMResponseDto
)
from .rabbitmq_connectors import get_rabbitmq_connection
import logging


def publish_message(message, queue_name, routing_key):
    """
    Publish a message to a specified RabbitMQ queue.

    Args:
        message: The message to be published.
        queue_name (str): The name of the RabbitMQ queue.
        routing_key (str): The routing key for the RabbitMQ queue.
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=message.json()
        )
        connection.close()
        logging.info(f"Message published to {queue_name}:{message.json()}")
    except Exception as e:
        logging.error(f"Failed to send to {queue_name}: {e}")


def publish_get_llm_response(message: MqGetLLMResponseDto):
    """
    Publish a message to the 'ORQ_get_llm_response' RabbitMQ queue.

    Args:
        message (MqGetLLMResponseDto): The message to be published.
    """
    publish_message(message, 'ORQ_get_llm_response', 'ORQ_get_llm_response')


def publish_persist_new_message(message: MqPersistNewMessageDto):
    """
    Publish a message to the 'ORQ_persist_new_message' RabbitMQ queue.

    Args:
        message (MqPersistNewMessageDto): The message to be published.
    """
    publish_message(
        message, 'ORQ_persist_new_message', 'ORQ_persist_new_message')


def publish_chat_response(message: MqPersistNewMessageDto):
    """
    Publish a message to the 'CHT_new_message_ok' RabbitMQ queue.

    Args:
        message (MqPersistNewMessageDto): The message to be published.
    """
    publish_message(message, 'CHT_new_message_ok', 'CHT_new_message_ok')


def publish_llm_response(message: MqLLMResponseDto):
    """
    Publish a message to the 'LLM_response' RabbitMQ queue.

    Args:
        message (MqLLMResponseDto): The message to be published.
    """
    publish_message(message, 'LLM_response', 'LLM_response')

from .rabbitmq_connectors import get_rabbitmq_connection
import logging


def consume_from_queue(queue_name, callback):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    logging.info(f"Started consuming from queue: {queue_name}")
    channel.start_consuming()

# itba_microservices_rabbitmq_connectors/rabbitmq_connectors.py

import pika
import os
import logging
import time


def get_rabbitmq_connection():
    """
    Establish a connection to the RabbitMQ server using credentials
    provided in environment variables.

    Returns:
        connection (pika.BlockingConnection): The connection to RabbitMQ.
    """
    rabbitmq_host = os.getenv('RABBITMQ_HOST')
    rabbitmq_port = int(os.getenv('RABBITMQ_PORT'))
    rabbitmq_user = os.getenv('RABBITMQ_USER')
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(
        rabbitmq_host,
        rabbitmq_port,
        '/',
        credentials
    )
    connection = pika.BlockingConnection(parameters)
    return connection


def wait_for_rabbitmq():
    """
    Wait until the RabbitMQ server is available.
    """
    while True:
        try:
            connection = get_rabbitmq_connection()
            connection.close()
            logging.info("RabbitMQ is available")
            break
        except pika.exceptions.AMQPConnectionError:
            logging.info("Waiting for RabbitMQ...")
            time.sleep(2)

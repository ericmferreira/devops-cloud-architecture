import time

import pika
from pika.exceptions import AMQPConnectionError


class Consumer:

    def start(self) -> None:

        credentials = pika.PlainCredentials("admin", "admin")

        connection = None

        for attempt in range(10):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host="rabbitmq",
                        port=5672,
                        credentials=credentials,
                    )
                )
                break

            except AMQPConnectionError:
                print(
                    f"Unable to connect to RabbitMQ. Retrying ({attempt + 1}/10)...",
                    flush=True,
                )
                time.sleep(2)

        if connection is None:
            raise RuntimeError("Could not connect to RabbitMQ.")

        channel = connection.channel()

        channel.queue_declare(
            queue="resource_requests",
            durable=True,
        )

        print("Waiting for messages...", flush=True)

        channel.basic_consume(
            queue="resource_requests",
            on_message_callback=self.callback,
            auto_ack=False,
        )

        channel.start_consuming()

    def callback(self, ch, method, properties, body):

        print(body.decode(), flush=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)
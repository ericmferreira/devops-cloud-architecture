import json

import pika


class Publisher:

    def __init__(self):
        credentials = pika.PlainCredentials("admin", "admin")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq",
                        port=5672,
                        credentials=credentials,)
        )

        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue="resource_notifications",
            durable=True,
        )

    def publish(self, payload: dict) -> None:

        self.channel.basic_publish(
            exchange="",
            routing_key="resource_notifications",
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )

        self.connection.close()
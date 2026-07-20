import time
import json
import pika
import os
from dotenv import load_dotenv

from pika.exceptions import AMQPConnectionError

from app.services.notification_service import NotificationService

load_dotenv()

class Consumer:

    def start(self) -> None:

        credentials = pika.PlainCredentials("admin", "admin")
        connection = None

        for attempt in range(10):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=os.getenv("RABBITMQ_HOST"),
                        port=int(os.getenv("RABBITMQ_PORT")),
                        credentials=credentials,
                    )
                )
                break

            except AMQPConnectionError:
                print(
                    f"Unable to connect to RabbitMQ. Retrying ({attempt + 1}/10)...",
                    flush=True,
                )
                time.sleep(10)

        if connection is None:
            raise RuntimeError("Could not connect to RabbitMQ.")

        channel = connection.channel()

        channel.queue_declare(
            queue="resource_notifications",
            durable=True,
        )

        print("Waiting for messages...", flush=True)

        try:
            channel.basic_consume(
                queue="resource_notifications",
                on_message_callback=self.callback,
                auto_ack=False,
            )

        except Exception as ex:
            print(repr(ex), flush=True)
            raise

        try:
            channel.start_consuming()

        except Exception as ex:
            print(repr(ex), flush=True)
            raise
        

    def callback(self, ch, method, properties, body):

        payload = json.loads(body)

        NotificationService().process(payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)

import time
import json
import pika

from pika.exceptions import AMQPConnectionError

from app.services.provision_service import ProvisionService
from app.messaging.publisher import Publisher


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
                time.sleep(10)

        if connection is None:
            raise RuntimeError("Could not connect to RabbitMQ.")

        channel = connection.channel()

        channel.queue_declare(
            queue="resource_requests",
            durable=True,
        )

        print("Waiting for messages...", flush=True)

        try:
            channel.basic_consume(
                queue="resource_requests",
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
        service = ProvisionService()
        service.process(payload)
        Publisher().publish(
            {
                "request_id": payload["id"],
                "requested_by": payload["requested_by"],
                "provider": payload["provider"],
                "resource_type": payload["resource_type"],
                "status": "SUCCESS",
                "message": "Provisioning completed successfully."
            }
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

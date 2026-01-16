import json
import pika


class CarProducer:
    def __init__(
        self,
        host: str = "localhost",
        exchange: str = "cars_events_exchange"
    ):
        self.exchange = exchange
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
    
    def send_event(self, event_type: str, data: str):
        message = {
            "eventType": event_type,
            "car": data
        }

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key="",
            body=json.dumps(message)
        )

    def close(self):
        self.connection.close()

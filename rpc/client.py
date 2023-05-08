from typing import Optional

import pika
import uuid

HOST: str = 'localhost'

EXCHANGE: str = ''
ROUTING_KEY: str = 'rpc_queue'

FIBONACCI_NUM: int = 30

REQUEST: str = "[x] Solicitando sequência Fibonacci de '{}'"
RESPONSE: str = "[.] Sequência recebida '{}'"


def from_str(nums: str) -> list[int]:
    return list(map(int, nums.split()))


class FibonacciClient:

    def __init__(self, host: str, exchange: str, routing_key: str) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True
        )

        self.exchange = exchange
        self.routing_key = routing_key

        self.response: Optional[str] = None
        self.correlation_id: Optional[str] = None

    def _on_response(self, ch, method, props, body) -> None:
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, num: int) -> list[int]:
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=str(num)
        )
        self.connection.process_data_events(time_limit=None)

        return from_str(self.response)


def main() -> None:
    client = FibonacciClient(host=HOST, exchange=EXCHANGE, routing_key=ROUTING_KEY)
    print(REQUEST.format(FIBONACCI_NUM))
    fibonacci_sequence: list[int] = client.call(FIBONACCI_NUM)
    print(RESPONSE.format(fibonacci_sequence))


if __name__ == '__main__':
    main()

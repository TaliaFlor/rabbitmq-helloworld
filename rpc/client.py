import uuid

from pika import ConnectionParameters, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.channel import Channel
from pika.spec import Basic

HOST: str = 'localhost'

EXCHANGE: str = ''
ROUTING_KEY: str = 'rpc_queue'

ENCODING: str = 'utf-8'

CORRELATION_ID: str = str(uuid.uuid4())

FIBONACCI_NUM: int = 30

REQUEST: str = "[x] Solicitando sequência Fibonacci de '{}'"
RESPONSE: str = "[.] Sequência recebida '{}'"


def from_str(nums: str) -> list[int]:
    return list(map(int, nums.split()))


def on_response(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    if properties.correlation_id != CORRELATION_ID:
        return
    fibonacci_sequence: list[int] = from_str(body.decode(ENCODING))
    print(RESPONSE.format(fibonacci_sequence))


def main() -> None:
    connection = BlockingConnection(ConnectionParameters(host=HOST))
    channel: BlockingChannel = connection.channel()

    queue_frame = channel.queue_declare(queue='', exclusive=True)
    callback_queue: str = queue_frame.method.queue

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

    print(REQUEST.format(FIBONACCI_NUM))
    channel.basic_publish(exchange=EXCHANGE,
                          routing_key=ROUTING_KEY,
                          properties=BasicProperties(reply_to=callback_queue, correlation_id=CORRELATION_ID),
                          body=str(FIBONACCI_NUM).encode(ENCODING))
    connection.process_data_events(time_limit=None)


if __name__ == '__main__':
    main()

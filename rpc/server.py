import sys

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.channel import Channel
from pika.spec import Basic, BasicProperties

from rpc.config import RabbitMQConfig, read_config

CONFIG_FILE: str = './config.json'

WAITING: str = '[x] Aguardando solicitações de RPC...'
REQUEST: str = '[.] Fibonacci de {} - {}'
SHUTDOWN: str = 'Desligando...'


def fibonacci_sequence(num: int) -> list[int]:
    """Generates a Fibonacci sequence up to n."""
    if num < 0:
        return []
    if num == 0:
        return [0]

    sequence: list[int] = [0, 1]
    while sequence[-1] < num:
        next_num: int = sequence[-1] + sequence[-2]
        if next_num > num:
            break
        sequence.append(next_num)
    return sequence


def to_str(nums: list[int]) -> str:
    return ' '.join(map(str, nums))


def on_request(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    num = int(body)
    sequence: list[int] = fibonacci_sequence(num)
    print(REQUEST.format(num, sequence))

    channel.basic_publish(exchange='',
                          routing_key=properties.reply_to,
                          properties=BasicProperties(correlation_id=properties.correlation_id),
                          body=to_str(sequence).encode())
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    config: RabbitMQConfig = read_config(CONFIG_FILE)

    connection = BlockingConnection(ConnectionParameters(host=config.host))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=config.queue)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=config.queue, on_message_callback=on_request)

    print(WAITING)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(SHUTDOWN)
        sys.exit()

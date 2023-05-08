import sys

import pika

HOST: str = 'localhost'

QUEUE: str = 'rpc_queue'
EXCHANGE: str = ''

SEPARATOR: str = ' '

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
    return SEPARATOR.join(map(str, nums))


def on_request(ch, method, props, body) -> None:
    num = int(body)
    sequence: list[int] = fibonacci_sequence(num)
    print(REQUEST.format(num, sequence))

    ch.basic_publish(exchange=EXCHANGE,
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=to_str(sequence))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_request)

    print(WAITING)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(SHUTDOWN)
        sys.exit()

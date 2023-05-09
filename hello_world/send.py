from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

HOST: str = 'localhost'

QUEUE: str = 'hello'
EXCHANGE: str = ''
ROUTING_KEY: str = 'hello'

ENCODING: str = 'utf-8'

MESSAGE: str = 'Hello, World!'
LOG: str = "[x] Enviado '{}'"


def main() -> None:
    connection = BlockingConnection(ConnectionParameters(host=HOST))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    channel.basic_publish(exchange=EXCHANGE, routing_key=ROUTING_KEY, body=MESSAGE.encode(ENCODING))
    print(LOG.format(MESSAGE))
    connection.close()


if __name__ == '__main__':
    main()

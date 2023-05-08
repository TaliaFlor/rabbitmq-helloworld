import pika

HOST: str = 'localhost'

QUEUE: str = 'hello'
EXCHANGE: str = ''
ROUTING_KEY: str = 'hello'

MESSAGE: str = 'Hello World!'
LOG: str = " [x] Enviado '{}'"


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    channel.basic_publish(exchange=EXCHANGE, routing_key=ROUTING_KEY, body=MESSAGE)
    print(LOG.format(MESSAGE))
    connection.close()


if __name__ == '__main__':
    main()

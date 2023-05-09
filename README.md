# RabbitMQ

Exemplos de uso do RabbitMQ. Inspirado nos
tutoriais [Hello World](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
e [RPC](https://www.rabbitmq.com/tutorials/tutorial-six-python.html) da documentação oficial.

# Uso

1. Instale o RabbitMQ na sua máquina
2. Instale as dependências do `requirements.txt`

## Hello World

1. Configure o RabbitMQ a fila `hello` e a routing key `hello`
2. Em um terminal rode `python hello_world/recieve.py`
3. Em outro terminal rode `python hello_world/send.py`

Para mandar outra mensagem, basta modificar a constante `MESSAGE` no arquivo `hello_world/send.py` e
executar `python hello_world/send.py` novamente.

## RPC

1. Configure o RabbitMQ a fila `rpc_queue`
2. Em um terminal rode `python rpc/server.py`
3. Em outro terminal rode `python rpc/client.py`

Para solicitar outra sequência, basta modificar a constante `FIBONACCI_NUM` no arquivo `rpc/client.py` e
executar `python rpc/client.py` novamente.

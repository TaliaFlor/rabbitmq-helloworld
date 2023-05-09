import json
from dataclasses import dataclass


@dataclass
class RabbitMQConfig:
    host: str
    queue: str
    routing_key: str


def read_config(config_file: str) -> RabbitMQConfig:
    with open(config_file) as file:
        data = json.load(file)
        return RabbitMQConfig(**data)

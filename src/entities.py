from dataclasses import dataclass
import requests


@dataclass
class Message:
    level: str  # Should be INFO, WARNING or ERROR
    subject: str
    body: str


class Target:
    def send_message(self, message: Message):
        raise NotImplemented()


class SlackTarget(Target):
    def __init__(self, hook_url: str):
        self.hook_url = hook_url

    def send_message(self, message: Message):
        body = {
            'text': '*{}*\n{}'.format(message.subject, message.body)
        }
        requests.post(self.hook_url, json=body)


@dataclass
class Channel:
    targets: list[Target]


@dataclass
class ProgramConfig:
    auth_keys: dict[str]
    targets: dict[str, Target]
    channels: dict[str, Channel]

import json
from dataclasses import dataclass


@dataclass
class CodebaseConfiguration:
    url: str
    username: str
    password: str
    private_token: str

    def __post_init__(self) -> None:
        self.username = self.username.replace('@', '%40')
        self.password = self.password.replace('@', '%40')


def read_codebase_configuration(json_file_path: str) -> CodebaseConfiguration:
    with open(json_file_path) as f:
        json_configuration = json.load(f)

    return CodebaseConfiguration(
        url=json_configuration['url'],
        username=json_configuration['username'],
        password=json_configuration['password'],
        private_token=json_configuration['private_token'])

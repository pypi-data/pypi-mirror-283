import os
import json

from dataclasses import dataclass
from dataclasses import asdict
from collections.abc import Iterator
from typing import Dict
from typing import ClassVar
from pathlib import Path

import click

from wscli.auth import SigninDetails, LoginTokens
from wscli.auth.token import Token


@dataclass(kw_only=True)
class ConfigStorer:

    home: str
    ext: str = "json"
    sep: str = "."

    def setup(self):
        path = Path(self.home)
        path.mkdir(parents=True, exist_ok=True)

    def get_key_file(self, key: str) -> str:
        return self.sep.join([key, self.ext])

    def get_key_path(self, key: str):
        file_name = self.get_key_file(key)
        return f"{self.home}/{file_name}"

    def list_keys(self) -> Iterator[str]:
        for file_name in os.listdir(self.home):
            key, *parts = file_name.split(self.sep)
            if parts == [self.ext]:
                yield key

    def set_key(self, key: str, data: Dict[str, str | int | float]):
        with open(self.get_key_path(key), "w") as fid:
            json.dump(data, fid)

    def get_key(self, key: str):
        try:
            with open(self.get_key_path(key), "r") as fid:
                return json.load(fid)
        except Exception:
            return {}

    def rm_key(self, key: str):
        file_name = self.get_key_path(key)
        if os.path.exists(file_name):
            os.remove(file_name)


@dataclass
class WsContext:
    organization: str | None = None
    project: str | None = None
    Key_: ClassVar[str] = "context"


@dataclass
class WsConfig:
    storer: ConfigStorer
    login: LoginTokens | None = None
    context: WsContext | None = None

    @classmethod
    def load(cls, storer):
        token_data = storer.get_key(LoginTokens.Key_)
        tokens = {
            token_type: Token(**params)
            for token_type, params in token_data.items()}
        return cls(
            storer=storer,
            login=LoginTokens(**tokens),
            context=WsContext(**storer.get_key(WsContext.Key_)),
        )

    def store(self):
        self.storer.set_key(LoginTokens.Key_, asdict(self.login))
        self.storer.set_key(WsContext.Key_, asdict(self.context))


pass_config = click.make_pass_decorator(WsConfig, ensure=True, )

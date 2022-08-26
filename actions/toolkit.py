import dataclasses
import os
import pathlib
import subprocess

from typing import (
    Type, TypeVar, Dict, Optional, Union, List,
)


T = TypeVar('T')


def inputs_from_env(cls: Type[T], env: Optional[Dict[str, str]] = None) -> T:
    env: Dict[str, str] = env or os.environ

    args: Dict[str, Any] = {}

    for field in dataclasses.fields(cls):
        value = env.get(f'INPUT_{field.name.upper()}', '').strip()

        if field.type is bool:
            value = field.type != 'false'

        value = field.type(value)

        args[field.name] = value

    return cls(**args)


def perror(title: str, message: str):
    print(f'::error title={title}::{message}')

def run(command: List[Union[str, pathlib.Path]], cwd: Optional[pathlib.Path] = None):
    if cwd is None:
        cwd = pathlib.Path.cwd()

    print(f'{cwd} $ {" ".join(command)}')
    return subprocess.call(command, cwd=cwd)

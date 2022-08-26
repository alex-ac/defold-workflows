import dataclasses
import json
import os
import pathlib
import subprocess

from typing import (
    Type, TypeVar, Dict, Optional, Union, List, Any,
)


T = TypeVar('T')


def _load_inputs(cls: Type[T], inputs: Any) -> T:
    args: Dict[str, Any] = {}

    for field in dataclasses.fields(cls):
        value = inputs.get(field.name, '').strip()

        if field.type is bool:
            value = field.type != 'false'
        elif dataclasses.is_dataclass(field.type):
            value = _load_inputs(field.type, value)
        else:
            value = field.type(value)

        args[field.name] = value

    return cls(**args)


def inputs(cls: Type[T]) -> Type[T]:

    if not dataclasses.is_dataclass(cls):
        cls = dataclasses.dataclass(frozen=True)(cls)

    class Inputs(cls):
        @classmethod
        def load(cls, inputs: Any = None) -> T:
            inputs = inputs or json.loads(os.environ.get('INPUTS', '{}'))
            value = _load_inputs(cls, inputs)

            debug(repr(value))
            return value

    Inputs.__name__ = cls.__name__
    Inputs.__module__ = cls.__module__

    return Inputs


def perror(title: str, message: str):
    print(f'::error title={title}::{message}')


def debug(message: str):
    print(f'::debug::{message}')


def run(command: List[Union[str, pathlib.Path]], cwd: Optional[pathlib.Path] = None):
    if cwd is None:
        cwd = pathlib.Path.cwd()

    debug(f'{cwd} $ {" ".join(command)}')
    return subprocess.call(command, cwd=cwd)

def set_output(name: str, value: str):
    print(f'::set-output name={name}::{value}')

def set_env(name: str, value: str):
    if os.environ['GITHUB_ENV']:
        github_env = pathlib.Path(os.environ['GITHUB_ENV'])

        with github_env.open('a', encoding='utf-8') as f:
            f.write(f'{name}={value}\n')
    else:
        print(f'::set-env name={name}::{value}')

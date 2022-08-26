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
        value = inputs.get(f'INPUT_{field.name.upper()}', '').strip()

        if field.type is bool:
            value = field.type != 'false'
        elif dataclasses.is_dataclass(field.type):
            value = _load_inputs(field.type, value)
        else:
            value = field.type(value)

        args[field.name] = value

    return cls(**args)


def inputs(cls: Type[T]) -> Type[T]:

    @dataclasses.dataclass(frozen=True)
    class Inputs(cls):
        @classmethod
        def load(cls, inputs: Any = None) -> T:
            inputs = inputs or json.loads(os.environ.get('INPUTS', '{}'))
            return _load_inputs(cls, inputs)


def perror(title: str, message: str):
    print(f'::error title={title}::{message}')

def run(command: List[Union[str, pathlib.Path]], cwd: Optional[pathlib.Path] = None):
    if cwd is None:
        cwd = pathlib.Path.cwd()

    print(f'{cwd} $ {" ".join(command)}')
    return subprocess.call(command, cwd=cwd)

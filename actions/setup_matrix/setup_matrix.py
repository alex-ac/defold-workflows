#!/usr/bin/env python3

import os
import dataclasses
import argparse
import sys
import json

from typing import List


@dataclasses.dataclass(frozen=True)
class Inputs:
    bundle_x86_64_linux: bool
    bundle_x86_64_win: bool
    bundle_x86_win: bool
    bundle_x86_64_mac: bool
    bundle_arm64_ios: bool
    bundle_armv7_android: bool
    bundle_arm64_android: bool
    bundle_wasm_web: bool
    bundle_js_web: bool


@dataclasses.dataclass(frozen=True)
class MatrixItem:
    host_os: str
    platform: str
    architectures: str
    bundle_type: str


@dataclasses.dataclass(frozen=True)
class Matrix:
    include: List[MatrixItem]


def run(argv=None):
    parser = argparse.ArgumentParser()
    _ = parser.parse_args(argv)

    inputs = Inputs(**{
        key: {'true': True, 'false': False}[value]
                if isinstance(value, str) else value
        for key, value in json.loads(os.environ['INPUTS']).items()
    })

    variants: List[MatrixItem] = []
    
    if inputs.bundle_x86_64_linux:
        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='x86_64-linux',
            architectures='x86_64-linux',
            bundle_type='tgz',
        ))

    if inputs.bundle_x86_64_win:
        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='x86_64-win32',
            architectures='x86_64-win32',
            bundle_type='zip',
        ))

    if inputs.bundle_x86_win:
        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='x86-win32',
            architectures='x86-win32',
            bundle_type='zip',
        ))

    if inputs.bundle_x86_64_mac:
        variants.append(MatrixItem(
            host_os='macos-latest',
            platform='x86_64-darwin',
            architectures='x86_64-darwin',
            bundle_type='dmg',
        ))

    if inputs.bundle_arm64_ios:
        variants.append(MatrixItem(
            host_os='macos-latest',
            platform='arm64-darwin',
            architectures='arm64-darwin',
            bundle_type='ipa',
        ))

    if inputs.bundle_armv7_android or inputs.bundle_arm64_android:
        architectures = []
        if inputs.bundle_armv7_android:
            architectures.append('armv7-android')
        if inputs.bundle_arm64_android:
            architectures.append('arm64-android')

        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='armv7-android',
            architectures=','.join(architectures),
            bundle_type='apk',
        ))

    if inputs.bundle_js_web:
        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='js-web',
            architectures='js-web',
            bundle_type='tgz',
        ))

    if inputs.bundle_wasm_web:
        variants.append(MatrixItem(
            host_os='ubuntu-latest',
            platform='js-web',
            architectures='wasm-web',
            bundle_type='tgz',
        ))

    matrix = Matrix(variants)
    print('::set-output name=matrix::{}'.format(
        json.dumps(matrix, default=dataclasses.asdict)))

if __name__ == '__main__':
    sys.exit(run())

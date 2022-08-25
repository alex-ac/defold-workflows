#!/usr/bin/env python3

import argparse
import configparser
import os
import pathlib
import sys


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=pathlib.Path, required=True,
                        help='Path to the output file.')
    parser.add_argument('--prefix', default='',
                        help='Prefix of env variables.')
    args = parser.parse_args()

    args.output = args.output.resolve()

    config = configparser.ConfigParser()

    for var, value in os.environ.items():
        if not var.startswith(args.prefix):
            continue

        section_key = var.removeprefix(args.prefix)
        if '_' not in section_key:
            print('::error title="Invalid env variable name for gen_settings."'
                  f'::Variable should be in form "{args.prefix}'
                  f'_$section_$option": {var}')
            continue

        section, key = section_key.split('_', 1)

        print(f'Adding to config: {section}.{key} = {value}')
        if not config.has_section(section):
            config.add_section(section)

        config.set(section, key, value)

    with args.output.open('w', encoding='utf-8') as f:
        config.write(f)


if __name__ == '__main__':
    sys.exit(run())

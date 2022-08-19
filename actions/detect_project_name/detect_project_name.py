#!/usr/bin/env python3

import argparse
import configparser
import pathlib
import sys


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('project', type=pathlib.Path,
                        help='Path to the defold project.')
    args = parser.parse_args(argv)

    project_file = args.project / 'game.project'
    config = configparser.ConfigParser()
    config.read(project_file, encoding='utf-8')
    project_name = config.get('project', 'title')

    print(f'::set-output name=project_name={project_name}')

if __name__ == '__main__':
    sys.exit(run())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click


VERBOSE = False

def validate_path(ctx, param, value):
    print("Validate path", ctx, param, value)
    if os.path.exists(value) and os.path.isfile(value):
        print("Valid File")
        return value
    else:
        print("Invalid config file %s" % value)


@click.group()
@click.option("--verbose", is_flag=True, default=False, help="list hosts",
              required=False)
def cli(verbose):
    global VERBOSE
    print("in cli Verbose: ", verbose)
    VERBOSE = verbose

@cli.command()
@click.option("config_file", "--configfile", callback=validate_path, 
              type=click.Path(), required=True)
def create(config_file):
    print("Create clickable template from %s" % config_file)


def main():
    """docstring for main"""
    cli.add_command(create)

    cli()


if __name__ == '__main__':
    main()

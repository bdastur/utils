#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

@click.group()
def cli():
    pass

@click.command()
def create():
    print "create command!"


def main():
    cli.add_command(create)
    cli()
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click


VERBOSE = False

@click.group()
@click.option("--verbose", is_flag=True, default=False, help="list hosts",
              required=False)
def cli(verbose):
    global VERBOSE
    print("in cli Verbose: ", verbose)
    VERBOSE = verbose

@cli.group('nodes')
def nodes():
    print("Adhoc operations")


@cli.group('cluster')
def cluster():
    """ Cluster Operations """
    print("Cluster Operations")
    print("Verbose: ", VERBOSE)


@nodes.command()
@click.option("--limit", type=str, help="limit to hosts",
              default=None, required=False)
def evacuate(limit):
    """Evacuate Nodes"""
    print("evacuate nodes")
    print("Verbose: ", VERBOSE)


@nodes.command()
@click.option("--limit", type=str, help="limit to hosts",
              default=None, required=False)
def list(limit):
    """List nodes"""
    print("List nodes")
    print("Verbose: ", VERBOSE)


def main():
    """docstring for main"""
    cli.add_command(nodes)
    cli.add_command(cluster)

    cli()


if __name__ == '__main__':
    main()

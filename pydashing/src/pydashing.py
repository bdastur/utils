#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyDashing:
----------
Build HTML Dashboards.

"""

import src.cli_handler as clihandler


def main():
    """Main Function."""
    print "Main"
    cli = clihandler.CliHandler()
    print cli.namespace


if __name__ == '__main__':
    main()

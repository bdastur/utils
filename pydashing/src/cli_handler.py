#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyDashing CLI Handler:
---------------------

"""

import sys
import os
import argparse


class CliHandler(object):
    """CLI Handler."""

    SUCCESS = 0
    ERROR = 1

    def __init__(self):
        """Initialize CLI Handler."""
        if len(sys.argv) <= 1:
            print "%s requires arguments. Use -h to see usage help." % \
                sys.argv[0]
            sys.exit()

        self.namespace = self.parse_arguments()
        self.validate_arguments()

    def parse_arguments(self):
        """Parse CLI arguments."""
        parser = argparse.ArgumentParser(
            prog="PyDashing",
            description=self.show_help(),
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument("--config",
                            dest="config_file",
                            required=True,
                            help="Path to configuration file")

        parser.add_argument("--render-path",
                            dest="render_path",
                            required=True,
                            help="Path to stage the rendered templates")

        namespace = parser.parse_args()
        return namespace

    @staticmethod
    def show_help():
        """Display Help for CLI."""
        msg = "PyDashing : A simple python utility to generate nice" + "\n" \
            + "dashboards" + "\n" \
            + "" + "\n" \
            + "Example Usage: ./pydashing.py --config ../config/simple.yaml" \
            + "\n"

        return msg

    def validate_arguments(self):
        """Validate that arguments passed are valid."""
        if not os.path.exists(self.namespace.config_file):
            print "%s file does not exists." % self.namespace.config_file
            return CliHandler.ERROR

        if not os.path.exists(self.namespace.render_path) or \
           not os.path.isdir(self.namespace.render_path):
            print "%s is an invalid render path" % self.namespace.render_path
            return CliHandler.ERROR

        return CliHandler.SUCCESS

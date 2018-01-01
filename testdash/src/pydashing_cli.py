#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import src.common as commonutils

"""
PyDashing CLI Parser.
---------------------

"""


class PyDashingCli(object):
    """
    PyDashing CLI Parser.
    """
    def __init__(self):
        """
        Initialize PyDashing CLI.
        """
        # Check for atleast one argument
        if len(sys.argv) <= 1:
            print ""
            print "%s requires arguments. Use -h to seee Usage help." % \
                sys.argv[0]
            print ""
            sys.exit()

        self.namespace = self.__parse_arguments()
        self.validate_arguments()
        self.cliobj = self.__generate_cli_obj()

    def __generate_cli_obj(self):
        """
        Create a CLI dictionary object
        """
        cliobj = {}
        cliobj['config_file'] = self.namespace.config_file
        cliobj['render_path'] = self.namespace.render_path
        return cliobj

    def __parse_arguments(self):
        """
        Parse Arguments and return the namespace object.
        """
        parser = argparse.ArgumentParser(
            prog="pydashing",
            description=self.show_help(),
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument("--config",
                            dest="config_file",
                            required=True,
                            help="Path to the configuration file.")

        parser.add_argument("--render-path",
                            dest="render_path",
                            required=False,
                            default=commonutils.get_absolute_path_for_file(
                                "../rendered_dashboards"),
                            help="Directory where to render dashing templates.")

        namespace = parser.parse_args()
        return namespace

    def show_help(self):
        """
        Display help message with the -h option.
        """
        msg = "PyDashing : A simple python utility to generate nice" + "\n" \
        + "dashboards" + "\n" \
        + "" + "\n" \
        + "Example Usage: ./pydashing.py --config ../config/simple.yaml" \
        + "\n"

        return msg

    def validate_arguments(self):
        config_file = self.namespace.config_file
        render_path = self.namespace.render_path

        if not os.path.exists(config_file):
            print "Invalid config file [%s]. Does not exist!" % config_file
            sys.exit()

        if not os.path.exists(render_path):
            print "Invalid staging/render path [%s]. Does not exist!" % \
                render_path
            sys.exit()

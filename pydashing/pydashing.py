#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import yaml

class PyDashingCli(object):
    def __init__(self):
        self.validate_arguments()
        self.namespace = self.__parse_arguments()

    def __parse_arguments(self):
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
                            help="Directory where to render dashing templates.")

        namespace = parser.parse_args()
        return namespace


    def show_help(self):
        msg = """
        PyDashing : A simple python utility to generate nice
        Dashboards.

        Example Usage: ./pydashing.py --config <path to config file>
        """
        print msg

    def validate_arguments(self):
        if len(sys.argv) <= 1:
            print ""
            print "%s requires arguments. Use -h to see Usage help." % \
                sys.argv[0]
            print ""
            sys.exit()


class ConfigParser(object):
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            print "Invalid configuration file %s " % config_file
            sys.exit()

        self.parsed_data = self.parse_configuration(config_file)
        print "Config Parser initialized. ", self.parsed_data

    def parse_configuration(self, config_file):
        '''
        Parse the 'yaml' format environment configuration file
        '''
        with open(config_file, 'r') as configfile:
            try:
                parsed_data = yaml.safe_load(configfile)
            except yaml.YAMLError as yamlerror:
                print "Invalid YAML format. Config file: [%s], Error: [%s]" % \
                    (config_file, yamlerror)
                return None

        return parsed_data


class PyDashingRenderer(object):
    def __init__(self):
        pass
        



def main():
    cli = PyDashingCli()
    print cli.namespace
    cfgparser = ConfigParser(cli.namespace.config_file)

if __name__ == '__main__':
    main()

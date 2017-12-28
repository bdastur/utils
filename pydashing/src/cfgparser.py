#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

"""
PyDashingConfigParser:
-----------------------
The module will parse the configurations for generating HTML, Flask, Javascript
code for building a Dashboard app.

"""

class PyDashingConfigParser(object):
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

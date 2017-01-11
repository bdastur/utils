#!/usr/bin/env python
# -*- coding: utf-8 -*-


import yaml
import os

class PyStatConfig(object):
    def __init__(self, config_file="/etc/pystat/pystat.conf"):
        self.cfg_file = config_file
        self.parsedyaml = None

        # Check if file exists.
        if not os.path.exists(self.cfg_file):
            print "No config file found"
            return

        try:
            cfg_fp = open(self.cfg_file, "r")
        except IOError as ioerr:
            print "Failed to open %s [%s]" % \
                (self.cfg_file, ioerr)
            return

        try:
            self.parsedyaml = yaml.safe_load(cfg_fp)
        except yaml.error.YAMLError as yamlerr:
            print "Failed to parse YAML file %s [%s]" % \
               (self.cfg_file, yamlerr)
            return

        print "Config Parsed!"

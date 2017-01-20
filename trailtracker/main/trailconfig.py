#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
TrailConfig: Parses the trailtracker conf file.

Default location of the config file is ~/.aws/trailtracker.yaml
Format of the config file should be yaml

Example Configuration file:
########################################
ACCOUNT_MAP:
    test: "44444455555564"
    prod: "1111111111111146"
    stage: "77777777777777"
    customer: "45555444455554"

REGIONS:
    - "us-east-1"
    - "us-west-2"

YEARS:
    - 2016
    - 2017
##########################################

ACCOUNT_MAP: has mapping of user defined account name to the
             account id
REGIONS: List of regions to look for if user does not specify a
         specific region to search

YEARS:  List of years worth of logs to look at if it is not specified.
        Normally this should be set to the current year.

"""

import os
import yaml
import main.trail_logging as trail_logging

class TrailConfig(object):
    def __init__(self, config_file=None):
        self.tlog = trail_logging.Logger(name="TrailConfig")
        self.parsedconfig = None
        if config_file is None:
            homedir = os.environ.get("HOME", None)
            if homedir is None:
                self.tlog.logger.error("ENV Variable $HOME not set")
                return

            self.trace_config = os.path.join(homedir, ".aws/trailtracker.yaml")
        else:
            self.trace_config = config_file

        try:
            fp = open(self.trace_config, "r")
        except IOError as ioerr:
            self.tlog.logger.error("Failed to open %s [%s]",
                                   self.trace_config, ioerr)

            return

        try:
            self.parsedconfig = yaml.safe_load(fp)
        except yaml.error.YAMLError as yamlerr:
            self.tlog.logger.error("Failed to parse %s [%s]",
                                    self.trace_config, yamlerr)

        self.tlog.logger.info("TrailConfig Initialize!")

    def get_account_map(self):
        try:
            return self.parsedconfig['ACCOUNT_MAP']
        except KeyError:
            self.tlog.logger.error("Key Error:  ACCOUNT_MAP")
            return None

    def get_regions(self):
        try:
            return self.parsedconfig['REGIONS']
        except KeyError:
            self.tlog.logger.error("Key Error: REGIONS")
            return None

    def get_years(self):
        try:
            return self.parsedconfig['YEARS']
        except KeyError:
            self.tlog.logger.error("Key Error: YEARS")
            return None

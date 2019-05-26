#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import builderutils.logger as logger

class BuilderParser(object):
    def __init__(self):
        pass


class ConfigParser(object):
    def __init__(self, confFile="./builder_conf.yml"):
        parsedYaml = yaml.safe_load(confFile)



class BuilderConfigParser(object):
    '''Parse Builder config'''
    BUILDER_CONFIG = "/etc/builder/builder.yaml"
    def __init__(self):
        self.validate = False
        bLogger = logger.BuilderLogger(name=__name__)
        self.logger = bLogger.logger

        # Validate Builder Config File
        if not os.path.exists(BuilderConfigParser.BUILDER_CONFIG):
            self.logger.error("Builder Config %s does not exist",
            BuilderConfigParser.BUILDER_CONFIG)
            return

        self.logger.info("BuilderConfig Initialized!")
        self.validate = True

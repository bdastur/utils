#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import yamale
import builderutils.logger as logger




class DataConfigParser(object):
    """Parse User config"""
    def __init__(self):
        blogger = logger.BuilderLogger(name=__name__)
        self.logger = blogger.logger

        self.builder_config = BuilderConfigParser()




class BuilderConfigParser(object):
    """Parse Builder config
       Builder Config parameters can be specified in
       a yaml file under /etc/builder/builder.yaml
    """

    BUILDER_CONFIG = "/etc/builder/builder.yaml"

    def __init__(self):
        self.validate = False
        blogger = logger.BuilderLogger(name=__name__)
        self.logger = blogger.logger

        # Validate Builder Config File
        if not os.path.exists(BuilderConfigParser.BUILDER_CONFIG):
            self.logger.error(
                "Builder Config %s does not exist", BuilderConfigParser.BUILDER_CONFIG
            )
            return
        self.parsed_config, err = parse_yaml_config(BuilderConfigParser.BUILDER_CONFIG)
        if err != 0:
            self.logger.error("Failed to parse BuilderConfig!")
            return

        self.logger.info("BuilderConfig Initialized!")
        self.validate = True

    def get_schema(self):
        return self.parsed_config['schema']

    def get_config_path(self):
        return self.parsed_config['configs_path']

    def get_templates_path(self):
        return self.parsed_config['templates_path']


def parse_yaml_config(config_file):
    """Parse YAML format file """
    with open(config_file, "r") as f_handle:
        try:
            parsed_data = yaml.safe_load(f_handle)
        except yaml.YAMLError as error:
            print("Failed to parse builde cofig %s [%s]" % (config_file, error))
            return None, 1
    return parsed_data, 0

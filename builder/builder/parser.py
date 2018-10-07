#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

class BuilderParser(object):
    def __init__(self):
        pass


class ConfigParser(object):
    def __init__(self, confFile="./builder_conf.yml"):
        parsedYaml = yaml.safe_load(confFile)
        

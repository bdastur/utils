#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pystat_config


class PyStatUt(unittest.TestCase):
    def test_pystat_config_basic(self):
        print "basic test"
        cfg = pystat_config.PyStatConfig(config_file="./pystat.conf")
        print cfg.parsedyaml

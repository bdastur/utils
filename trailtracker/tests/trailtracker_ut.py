#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Trail Tracker UT.

"""

import unittest
import yaml
import main.trailconfig as trailconfig


class TrailConfigUt(unittest.TestCase):
    def setUp(self):
        self.test_config_file = "/tmp/testconf.yaml"
        self.test_config = {
            'ACCOUNT_MAP': {
                'testaccount': 32323232323,
                'testaccount2': 43434434343
            },
            'REGIONS': ['us-east-1', 'us-west-2'],
            'YEARS': [2016, 2017]
        }

        with open(self.test_config_file, 'w') as outfile:
            yaml.dump(self.test_config, outfile)

    def test_trail_config_default(self):
        tconfig = trailconfig.TrailConfig()
        self.failUnless(tconfig.parsedconfig is not None)

    def test_trail_config_custom(self):
        tconfig = trailconfig.TrailConfig(config_file=self.test_config_file)
        self.failUnless(tconfig.parsedconfig is not None)

        accountinfo = tconfig.get_account_map()
        self.failUnless(accountinfo['testaccount'] == 32323232323)

    def test_trail_config_check_account(self):
        tconfig = trailconfig.TrailConfig(config_file=self.test_config_file)
        self.failUnless(tconfig.parsedconfig is not None)

        accountinfo = tconfig.get_account_map()
        self.failUnless(accountinfo['testaccount'] == 32323232323)

    def test_trail_config_check_region(self):
        tconfig = trailconfig.TrailConfig(config_file=self.test_config_file)
        self.failUnless(tconfig.parsedconfig is not None)

        regions = tconfig.get_regions()
        self.failUnless(regions[0] == "us-east-1")

    def test_trail_config_check_years(self):
        tconfig = trailconfig.TrailConfig(config_file=self.test_config_file)
        self.failUnless(tconfig.parsedconfig is not None)

        years = tconfig.get_years()
        self.failUnless(years[0] == 2016)


class TrailTrackerUt(unittest.TestCase):
    def test_basic(self):
        pass
        

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Trail Tracker UT.

"""

import unittest
import os
import yaml
import main.trailconfig as trailconfig
import main.s3helper as s3helper
import main.trailtracker as trailtracker


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


class S3HelperUt(unittest.TestCase):
    """
    S3Helper unittest:

    NOTE: For tests to pass, set the env variables as below:
        TT_PROFILE_NAME="your profile name in ~/.aws/credentials"
        TT_BUCKET_NAME="cloudtrail s3 bucketname"
    """

    def setUp(self):
        self.profile_name = os.environ.get('TT_PROFILE_NAME', 'default')
        self.bucket_name = os.environ.get('TT_BUCKET_NAME', 'testbucket')

    def test_s3helper_init(self):
        helper = s3helper.S3Helper(self.profile_name, self.bucket_name)
        self.failUnless(helper.valid == True)

    def test_s3helper_getobjlist_prefix_none(self):
        helper = s3helper.S3Helper(self.profile_name, self.bucket_name)
        self.failUnless(helper.valid == True)

        (ret, objlist) = helper.get_object_list(None)
        self.failUnless(ret != 0)

    def test_s3helper_getobjlist_prefix_wrong(self):
        helper = s3helper.S3Helper(self.profile_name, self.bucket_name)
        self.failUnless(helper.valid == True)

        prefix = "AWSLogs/434343"
        (ret, objlist) = helper.get_object_list(prefix)
        self.failUnless(ret != 0)



class TrailTrackerUt(unittest.TestCase):
    def setUp(self):
        self.profile_name = os.environ.get('TT_PROFILE_NAME', 'default')
        self.bucket_name = os.environ.get('TT_BUCKET_NAME', 'testbucket')

    def test_trail_tracker_init(self):
        ttracker = trailtracker.TrailTracker(self.profile_name,
                                             self.bucket_name)
        self.failUnless(ttracker.s3_helper.valid is True)

    def test_build_prefix_path(self):
        ttracker = trailtracker.TrailTracker(self.profile_name,
                                             self.bucket_name)
        self.failUnless(ttracker.s3_helper.valid is True)

        myargs = {}

        myargs['days'] = [2,3,4]

        prefix_paths = ttracker.build_prefix_paths(**myargs)
        self.failUnless(len(prefix_paths) > 0)
        print "Total prefix paths: ", len(prefix_paths)

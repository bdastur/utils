#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TrailTracker: Make sense of AWS CloudTrail logs.

AWS CloudTrail captures AWS API calls and related events made by users
in the AWS account and delivers log files to AWS S3 bucket. There is another
option to deliver events to CloudWatch.

TrailTracker uses the CloudTrail S3 bucket to parse and render useful
event information.

CloudTrail Logfile name format:
-------------------------------
<account id>_CloudTrail_<region>_<YYYYMMDDTHHmmZ>_<unique string>.json.gz

CloudTrail Logfile Archive Path:
--------------------------------
AWSLogs/<account id>/CloudTrail/<region>/YYYY/MM/DD/<Cloud Trail Logfilename>

An archive file, contains multiple event records, and for each day,
there can be multiple archived log files.

"""

import main.trail_logging as trail_logging
import main.trailconfig as trailconfig
import main.s3helper as s3helper

class TrailTracker(object):
    def __init__(self, profile_name, bucket_name, config_file=None):
        self.traceconfig = trailconfig.TrailConfig(config_file=config_file)
        self.tlog = trail_logging.Logger(name="TrailTracker")
        self.s3_helper = s3helper.S3Helper(profile_name, bucket_name)
        if not self.s3_helper.valid:
            self.tlog.logger.error("Failed to initialize S3Handler")
            return

    def build_prefix_with_accountid(self, accountid, accountname):
        account_map = self.traceconfig.get_account_map()
        prefix_paths = []

        if accountid is None and accountname is None:
            for account in account_map.keys():
                path = "AWSLogs/" + str(account_map[account]) + "/CloudTrail"
                prefix_paths.append(path)
        elif accountname is not None:
            account_id = account_map[accountname]
            path = "AWSLogs/" + str(account_id) + "/CloudTrail"
            prefix_paths.append(path)
        else:
            path = "AWSLogs/" + str(accountid) + "/CloudTrail"
            prefix_paths.append(path)

        return prefix_paths

    def build_prefix_with_region(self, region, temp_paths):
        # Set Region.
        prefix_paths = []

        if region is None:
            regions = self.traceconfig.get_regions()

            for path in temp_paths:
                for region in regions:
                    newpath = path + "/" + region
                    prefix_paths.append(newpath)
        else:
            for path in temp_paths:
                newpath = path + "/" + region
                prefix_paths.append(newpath)

        return prefix_paths

    def build_prefix_with_year(self, year, temp_paths):
        #Set Year.
        prefix_paths = []

        if year is None:
            years = self.traceconfig.get_years()
            for path in temp_paths:
                for year in years:
                    newpath = path + "/" + str(year)
                    prefix_paths.append(newpath)
        else:
            for path in temp_paths:
                newpath = path + "/" + str(year)
                prefix_paths.append(newpath)

        return prefix_paths

    def build_prefix_with_month(self, months, temp_paths):
        prefix_paths = []

        if months is None:
            for path in temp_paths:
                for month in range(1, 13):
                    newpath = path + "/" + str(month)
                    prefix_paths.append(newpath)
        else:
            for path in temp_paths:
                for month in months:
                   newpath = path + "/" + str(month)
                   prefix_paths.append(newpath)

        return prefix_paths

    def build_prefix_with_day(self, days, temp_paths):
        prefix_paths = []

        if days is not None:
            for path in temp_paths:
                for day in days:
                    newpath = path + "/" + str(day)
                    prefix_paths.append(newpath)
        else:
            prefix_paths = temp_paths

        return prefix_paths

    def build_prefix_paths(self, **kwargs):
        """
        The API builds a prefix path for the Cloudtrail bucket to query.

        Path is as below:
        AWSLogs/<accountid>/CloudTrail/<region>/<year>/<month>/<day>/<traice archive>
        """
        accountid = kwargs.get('accountid', None)
        accountname = kwargs.get('accountname', None)
        region = kwargs.get('region', None)
        year = kwargs.get('year', None)
        months = kwargs.get('months', None)
        days = kwargs.get('days', None)

        prefix_paths = []
        temp_paths = []

        #Set AccountID.
        prefix_paths = self.build_prefix_with_accountid(accountid, accountname)
        temp_paths = prefix_paths

        prefix_paths = self.build_prefix_with_region(region, temp_paths)
        temp_paths = prefix_paths


        prefix_paths = self.build_prefix_with_year(year, temp_paths)
        temp_paths = prefix_paths

        prefix_paths = self.build_prefix_with_month(months, temp_paths)
        temp_paths = prefix_paths

        prefix_paths = self.build_prefix_with_day(days, temp_paths)

        return prefix_paths

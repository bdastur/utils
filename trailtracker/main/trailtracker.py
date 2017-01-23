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

import re
import datetime
import multiprocessing
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

    def list_trail_archives(self, **kwargs):
        trail_archives = []

        prefix_paths = self.build_prefix_paths(**kwargs)
        print "prefix paths: ", prefix_paths
        for prefix in prefix_paths:
            (ret, objlist) = self.s3_helper.get_object_list(prefix)
            if ret == 1:
                print "Failed to get objlist"
                continue

            trail_archives.extend(objlist)

        return trail_archives

    def initialize_listener(self, common_queue,
                            custom_callback, custom_callback_args):
        """
        Lister to start listening on the queue for any records.

        The generator will start parsing the records and putting it
        on the common queue. This lister will be listening to it
        till finally a obj with done flag is set.
        """
        objdata = None
        while True:
            try:
                objdata = common_queue.get(timeout=3)
            except multiprocessing.queues.Empty:
                continue

            if objdata.get('done', None) is not None:
                print "Done draining the queue!"
                custom_callback(objdata, custom_callback_args)
                break

            if objdata is not None:
                if custom_callback is not None:
                    custom_callback(objdata, custom_callback_args)
                else:
                    print "Data: ", objdata

    def search_trail_archives(self, **kwargs):
        print "kwargs: ", kwargs

        trail_archives = self.list_trail_archives(**kwargs)

        custom_callback = kwargs.get('custom_callback', None)
        custom_callback_args = kwargs.get('custom_callback_args', None)
        # Create a common queue, and a listener.
        common_queue = multiprocessing.Queue()
        listener = multiprocessing.Process(
            target=self.initialize_listener,
            args=(common_queue, custom_callback, custom_callback_args,))
        listener.start()

        search_args = kwargs.get('search_args', None)
        total_archives = len(trail_archives)
        count = 1

        done = False
        start = 0
        step = 5
        end = start + step
        while not done:
            workers = []
            for archive in trail_archives[start:end]:
                key = archive['Key']
                print "Key: ", key
                worker = multiprocessing.Process(
                    target=self.get_trail_records,
                    args=(common_queue, key, search_args,))
                workers.append(worker)
                worker.start()

            for worker in workers:
                worker.join()
            start = end
            end = start + step
            print "Start another batch: %d, %d" % (start, end)
            if end >= len(trail_archives):
                done = True

        print "Done with All Archives!"
        common_queue.put({'done': True})
        listener.join()
        listener.terminate()

    def get_trail_records(self, common_queue, key, search_args):
        print "Trail records invoked, ", search_args
        (ret, objinfo) = self.s3_helper.get_trail_archive_object(key)
        if ret == 1:
            print "Failed to get archive obj"
            return

        for obj in objinfo['Records']:
            if re.match(r'List*', obj['eventName']) or \
                re.match(r'Get*', obj['eventName']) or \
                re.match(r'CreateTags', obj['eventName']) or \
                re.match(r'Describe*', obj['eventName']):
                continue
            #search_args = {}
            #search_args['eventName'] = ".*nstance.*"
            recobj = self.parse_record(obj, **search_args)
            if recobj is not None:
                common_queue.put(recobj)

    def parse_record(self, record, **searchargs):
        recordobj = {}
        for key in searchargs:
            searchstr = r'%s' % searchargs[key]
            try:
                if not re.match(searchstr, record[key]):
                    return None
            except re.error:
                return None

        recordobj['eventName']  = record['eventName']
        #recordobj['eventTime'] = record['eventTime']
        recordobj['eventTime'] = datetime.datetime.strptime(
            record['eventTime'], '%Y-%m-%dT%H:%M:%SZ')
        recordobj['requestParameters'] = record.get('requestParameters', None)
        recordobj['errorCode'] = record.get('errorCode', None)
        recordobj['sourceIPAddress'] = record['sourceIPAddress']
        recordobj['arn'] = record['userIdentity']['arn']
        recordobj['userName'] = record['userIdentity'].get('userName', None)

        return recordobj

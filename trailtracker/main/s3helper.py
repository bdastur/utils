#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
S3helper: Perform S3 operations specific to CloudTrail S3 bucket.

The module has APIs.

Provide API to list all the cloudtrail archive files given a prefix
Provide API to return the records from a given archived file

CloudTrail Logfile name format:
-------------------------------
<account id>_CloudTrail_<region>_<YYYYMMDDTHHmmZ>_<unique string>.json.gz

CloudTrail Logfile Archive Path:
--------------------------------
AWSLogs/<account id>/CloudTrail/<region>/YYYY/MM/DD/<Cloud Trail Logfilename>

"""

import json
import gzip
import boto3
import botocore
import logging
import main.trail_logging as trail_logging

logging.getLogger('botocore').setLevel(logging.ERROR)

class S3Helper(object):
    def __init__(self, profile, bucketname):
        self.valid = False
        self.tlog = trail_logging.Logger(name="S3helper")

        if profile is None or bucketname is None:
            self.tlog.logger.error("Invalid parameters")
            return

        self.profile = profile
        self.bucketname = bucketname
        session = boto3.Session(profile_name=profile)
        self.s3client = session.client('s3')
        self.valid = self._validate_bucket_exists()

    def _validate_bucket_exists(self):
        valid = True
        try:
            self.s3client.get_bucket_policy(Bucket=self.bucketname)
        except botocore.exceptions.ClientError:
            self.tlog.logger.error("Failed 'get_bucket_policy'")
            valid = False

        return valid

    def get_object_list(self, prefix):
        try:
            objlistinfo = self.s3client.list_objects(Bucket=self.bucketname,
                                                     Prefix=prefix)
        except botocore.exceptions.ClientError as botoerror:
            self.tlog.logger.error("[Get obj list] [%s]", botoerror)
            return (1, None)

        except botocore.exceptions.ParamValidationError as botoerror:
            self.tlog.logger.error("[Get obj list] [%s]", botoerror)
            return (1, None)

        try:
            objlist = objlistinfo['Contents']
        except KeyError:
            self.tlog.logger.error("[Get obj list]: No Content in [%s]", prefix)
            return (1, None)

        return (0, objlist)

    def get_trail_archive_object(self, archive_key):
        temp_file = "/tmp/trail.log.gz"
        try:
            self.s3client.download_file(self.bucketname, archive_key, temp_file)
        except botocore.exceptions.ClientError as botoerror:
            self.tlog.logger.error("[download file] [%s]", botoerror)
            return (1, None)

        objinfo = None
        try:
            fp = gzip.open(temp_file, "rb")
            objinfo = fp.read()
        except IOError as ioerr:
            self.tlog.logger.error("Failed to gzip open %s [%s]",
                temp_file, ioerr)
            return (1, None)
        fp.close()

        try:
            jobjinfo = json.loads(objinfo)
        except json.error as jsonerror:
            self.tlog.logger.error("Json load failed [%s]", jsonerror)
            return (0, None)

        return (0, jobjinfo)

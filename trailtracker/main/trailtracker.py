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

class TrailTracker(object):
    def __init__(self,)

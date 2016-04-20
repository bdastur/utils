#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Parse FIO output:

'''
import os
import argparse
import re
import rex



def parse_fio_file(filename):
    '''
    Parse the FIO output and return a
    dict
    '''
    job_pattern = r"job.*rw=(w:<type>).*bs=(w:<blocksize>)-.*" \
        "ioengine=(w:<ioengine>).*iodepth=(d:<iodepth>)"
    job_rex_pattern = rex.reformat_pattern(job_pattern, compile=True)

    job1_pattern = r"job.* pid=(d:<pid>):(any:<timestamp>)"
    job1_rex_pattern = rex.reformat_pattern(job1_pattern, compile=True)

    read_aggr_pattern = r".*READ:.*io=(measurement:<io>),.*" \
        "aggrb=(measurement:<aggrbw>),.*minb=(measurement:<minavgbw>),.*" \
        "maxb=(measurement:<maxavgbw>),.*mint=(measurement:<minruntime>),.*" \
        "maxt=(measurement:<maxruntime>)"
    read_aggr_rex_pattern = rex.reformat_pattern(read_aggr_pattern,
                                                 compile=True)

    write_aggr_pattern = r".*WRITE:.*io=(measurement:<io>),.*" \
        "aggrb=(measurement:<aggrbw>),.*minb=(measurement:<minavgbw>),.*" \
        "maxb=(measurement:<maxavgbw>),.*mint=(measurement:<minruntime>),.*" \
        "maxt=(measurement:<maxruntime>)"
    write_aggr_rex_pattern = rex.reformat_pattern(write_aggr_pattern,
                                                  compile=True)

    cpu_pattern = r".*cpu.*:.*usr=(decimal:<user>)%,.*" \
        "sys=(decimal:<system>)%,.*ctx=(d:<context_switches>),.*" \
        "majf=(d:<majfault>),.*minf=(d:<minfault>)"
    cpu_rex_pattern = rex.reformat_pattern(cpu_pattern, compile=True)


    fhandle = open(filename, 'r')
    data = fhandle.read()
    fio_result = {}
    for line in data.splitlines():
        mobj = job_rex_pattern.match(line)
        if mobj:
            print "job pattern: ", line
            print "match: ", mobj.groups(0)
            fio_result['blocksize'] = mobj.group('blocksize')
            fio_result['jobtype'] = mobj.group('type')
            fio_result['ioengine'] = mobj.group('ioengine')
            fio_result['iodepth'] = mobj.group('iodepth')

        mobj = job1_rex_pattern.match(line)
        if mobj:
            print "job1 pattern: ", line
            print "match: ", mobj.groups(0)
            fio_result['pid'] = mobj.group('pid')
            fio_result['timestamp'] = mobj.group('timestamp')

        mobj = read_aggr_rex_pattern.match(line)
        if mobj:
            print "Read aggr: ", line
            print "match: ", mobj.groups(0)
            fio_result['aggr_read'] = {}
            fio_result['aggr_read']['io'] = mobj.group('io')
            fio_result['aggr_read']['io_unit'] = mobj.group('io_unit')
            fio_result['aggr_read']['aggrbw'] = mobj.group('aggrbw')
            fio_result['aggr_read']['aggrbw_unit'] = mobj.group('aggrbw_unit')
            fio_result['aggr_read']['minavgbw'] = mobj.group('minavgbw')
            fio_result['aggr_read']['minavgbw_unit'] = \
                mobj.group('minavgbw_unit')
            fio_result['aggr_read']['maxavgbw'] = mobj.group('maxavgbw')
            fio_result['aggr_read']['maxavgbw_unit'] = \
                mobj.group('maxavgbw_unit')
            fio_result['aggr_read']['minruntime'] = mobj.group('minruntime')
            fio_result['aggr_read']['minruntime_unit'] = \
                mobj.group('minruntime_unit')
            fio_result['aggr_read']['maxruntime'] = mobj.group('maxruntime')
            fio_result['aggr_read']['maxruntime_unit'] = \
                mobj.group('maxruntime_unit')

        mobj = write_aggr_rex_pattern.match(line)
        if mobj:
            print "Write aggr: ", line
            print "match: ", mobj.groups(0)
            fio_result['aggr_write'] = {}
            fio_result['aggr_write']['io'] = mobj.group('io')
            fio_result['aggr_write']['io_unit'] = mobj.group('io_unit')
            fio_result['aggr_write']['aggrbw'] = mobj.group('aggrbw')
            fio_result['aggr_write']['aggrbw_unit'] = mobj.group('aggrbw_unit')
            fio_result['aggr_write']['minavgbw'] = mobj.group('minavgbw')
            fio_result['aggr_write']['minavgbw_unit'] = \
                mobj.group('minavgbw_unit')
            fio_result['aggr_write']['maxavgbw'] = mobj.group('maxavgbw')
            fio_result['aggr_write']['maxavgbw_unit'] = \
                mobj.group('maxavgbw_unit')
            fio_result['aggr_write']['minruntime'] = mobj.group('minruntime')
            fio_result['aggr_write']['minruntime_unit'] = \
                mobj.group('minruntime_unit')
            fio_result['aggr_write']['maxruntime'] = mobj.group('maxruntime')
            fio_result['aggr_write']['maxruntime_unit'] = \
                mobj.group('maxruntime_unit')

        mobj = cpu_rex_pattern.match(line)
        if mobj:
            print "cpu pattern: ", line
            print "match: ", mobj.groups(0)
            fio_result['cpu_usage'] = {}
            fio_result['cpu_usage']['user'] = mobj.group('user')
            fio_result['cpu_usage']['system'] = mobj.group('system')
            fio_result['cpu_usage']['context_switches'] =  \
                mobj.group('context_switches')
            fio_result['cpu_usage']['majfault'] = mobj.group('majfault')
            fio_result['cpu_usage']['minfault'] = mobj.group('minfault')

    return fio_result


def parse_fio_file_old(filename):
    '''
    Parse the file and return a json object
    '''
    # This is how we define a measurement pattern.
    # (decimal number followed by Units or Units/time )
    decimal_str = r"(\d*\.\d+|\d+)"
    msmt_str = r"(\d*\.\d+|\d+)(\w+|\w+/\w+)"

    job_pattern = r"job.* rw=(\w+).* bs=(\w+)-.* ioengine=(\w+).* iodepth=(\w+)"
    fio_version = r"fio-(.*)"
    job1_pattern = r"job.* pid=(\w+):(.*)"
    write_pattern = r".*write: .*io=(\w+),.*bw=(.*),.*iops=(\w+),.*runt=(.*)"
    clat_pattern = r".*clat.*\(usec\):.*min=(\w+)," + \
        ".*max=(\w+).*avg=(.*),.*stdev=(.*)"
    lat_pattern = r".*lat.*\(usec\):.*min=(.*)," + \
        ".*max=(.*),.*avg=(.*),.*stdev=(.*)"
    bw_pattern = r".*bw.*\(.*\):.*min=(.*),.*max=(.*)," + \
        ".*per=(.*),.*avg=(.*),.*stdev=(.*)"
    cpu_pattern = r".*cpu.*:.*usr=(.*)%,.*sys=(.*)%," + \
        ".*ctx=(.*),.*majf=(.*),.*minf=(.*)"
    write_aggr_pattern = r".*WRITE:.*io=%s,.*aggrb=%s,.*minb=%s.*" \
        "maxb=%s,.*mint=%s,.*maxt=%s.*" % \
        (msmt_str, msmt_str, msmt_str, msmt_str, msmt_str, msmt_str)
    read_aggr_pattern = r".*READ: io=%s,.*aggrb=%s,.*minb=%s,.*" \
        "maxb=%s,.*mint=%s,.*maxt=%s.*" % \
        (msmt_str, msmt_str, msmt_str, msmt_str, msmt_str, msmt_str)

    disk_stat_pattern = r" *(\w+):.*ios=(\w+)/(\w+),.*merge=(\w+)/(\w+),.*" \
        "ticks=(\w+)/(\w+),.*in_queue=(\w+),.*util=%s.*" % decimal_str

    job_comp_pattern = re.compile(job_pattern)
    fio_comp_version = re.compile(fio_version)
    job1_comp_pattern = re.compile(job1_pattern)
    write_comp_pattern = re.compile(write_pattern)
    clat_comp_pattern = re.compile(clat_pattern)
    lat_comp_pattern = re.compile(lat_pattern)
    bw_comp_pattern = re.compile(bw_pattern)
    cpu_comp_pattern = re.compile(cpu_pattern)
    write_aggr_comp_pattern = re.compile(write_aggr_pattern)
    read_aggr_comp_pattern = re.compile(read_aggr_pattern)
    disk_stat_comp_pattern = re.compile(disk_stat_pattern)

    fhandle = open(filename, 'r')
    data = fhandle.read()
    for line in data.splitlines():
        mobj = job_comp_pattern.match(line)
        if mobj:
            print "job pattern: ", line
            print mobj.groups(0)

        mobj = fio_comp_version.match(line)
        if mobj:
            print mobj.groups(0)

        mobj = job1_comp_pattern.match(line)
        if mobj:
            print "line: ", line
            print mobj.groups(0)

        mobj = write_comp_pattern.match(line)
        if mobj:
            print mobj.groups(0)

        mobj = clat_comp_pattern.match(line)
        if mobj:
            print "clat: ", line
            print mobj.groups(0)

        mobj = lat_comp_pattern.match(line)
        if mobj:
            print "lat: ", line
            print mobj.groups(0)

        mobj = bw_comp_pattern.match(line)
        if mobj:
            print "bw: ", line
            print mobj.groups(0)

        mobj = cpu_comp_pattern.match(line)
        if mobj:
            print "cpu: ", line
            print mobj.groups(0)

        mobj = write_aggr_comp_pattern.match(line)
        if mobj:
            print "aggr write: ", line
            print mobj.groups(0)

        mobj = read_aggr_comp_pattern.match(line)
        if mobj:
            print "read aggr: ", line
            print mobj.groups(0)

        mobj = disk_stat_comp_pattern.match(line)
        if mobj:
            print "disk stat: ", line
            print mobj.groups(0)


def validate_filelist(filelist):
    '''
    Validate if all files exists in the filelist
    Return:
        true: if all files exist
        false: if any check fails
    '''

    for filename in filelist:
        if not os.path.exists(filename) or \
                os.path.isdir(filename):
            print "Invalid file [%s]" % filename
            return False

    return True


def parse_fio_output_files(namespace):
    '''
    Read all the files for fio_data and parse them.
    '''
    filelist = namespace.output
    print "filelist: ", filelist
    if not validate_filelist(filelist):
        return None

    results = []
    for filename in filelist:
        results.append(parse_fio_file(filename))

    print "Results: ", results



def parse_arguments():
    '''
    Parse cmdline arguments
    '''
    parser = argparse.ArgumentParser(
        prog="fioparse.py",
        description="FIO Parser")
    parser.add_argument("-o", "--output",
                        required=True,
                        nargs='*',
                        help="FIO output files to parse")

    namespace = parser.parse_args()
    return namespace


def main():
    print "fio parse main"
    namespace = parse_arguments()
    print namespace
    parse_fio_output_files(namespace)

if __name__ == '__main__':
    main()

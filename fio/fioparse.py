#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Parse FIO output:

'''
import os
import argparse
import re


def parse_fio_file(filename):
    '''
    Parse the file and return a json object
    '''
    # This is how we define a measurement pattern.
    # (decimal number followed by Units or Units/time )
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

    print "write agg: ", write_aggr_pattern

    job_comp_pattern = re.compile(job_pattern)
    fio_comp_version = re.compile(fio_version)
    job1_comp_pattern = re.compile(job1_pattern)
    write_comp_pattern = re.compile(write_pattern)
    clat_comp_pattern = re.compile(clat_pattern)
    lat_comp_pattern = re.compile(lat_pattern)
    bw_comp_pattern = re.compile(bw_pattern)
    cpu_comp_pattern = re.compile(cpu_pattern)
    write_aggr_comp_pattern = re.compile(write_aggr_pattern)

    fhandle = open(filename, 'r')
    data = fhandle.read()
    for line in data.splitlines():
        mobj = job_comp_pattern.match(line)
        if mobj:
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


def validate_filelist(filelist):
    '''
    Validate if all files exists in the filelist
    Return:
        true: if all files exist
        false: if any check fails
    '''
    for filename in filelist:
        if not os.path.exists(filename):
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

    for filename in filelist:
        parse_fio_file(filename)



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

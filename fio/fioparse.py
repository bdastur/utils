#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Parse FIO output:

'''
import os
import argparse
import rex
import prettytable


def parse_fio_file(filename, verbose=False):
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
            if verbose:
                print "job pattern: ", line
                print "match: ", mobj.groups(0)
            fio_result['blocksize'] = mobj.group('blocksize')
            fio_result['jobtype'] = mobj.group('type')
            fio_result['ioengine'] = mobj.group('ioengine')
            fio_result['iodepth'] = mobj.group('iodepth')

        mobj = job1_rex_pattern.match(line)
        if mobj:
            if verbose:
                print "job1 pattern: ", line
                print "match: ", mobj.groups(0)
            fio_result['pid'] = mobj.group('pid')
            fio_result['timestamp'] = mobj.group('timestamp')

        mobj = read_aggr_rex_pattern.match(line)
        if mobj:
            if verbose:
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
            if verbose:
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
            if verbose:
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


def display_fiodata_tabular(fioresults):
    '''
    Given the fioresults data, print it in
    tabular format.
    '''

    # Setup table.
    table_header = ["test", "ioengine", "size",
                    "Write (IO)", "Write (BW)",
                    "Read (IO)", "Read (BW)"]
    table = prettytable.PrettyTable(table_header)

    for result in fioresults:
        row = []
        row.append(result['jobtype'])
        row.append(result['ioengine'])
        row.append(result['blocksize'])

        try:
            iostr = result['aggr_write']['io'] + " " + \
                result['aggr_write']['io_unit']
        except KeyError:
            iostr = "X"
        row.append(iostr)

        try:
            bwstr = result['aggr_write']['aggrbw'] + " " + \
                result['aggr_write']['aggrbw_unit']
        except KeyError:
            bwstr = "X"
        row.append(bwstr)

        try:
            iostr = result['aggr_read']['io'] + " " + \
                result['aggr_read']['io_unit']
        except KeyError:
            iostr = "X"
        row.append(iostr)

        try:
            bwstr = result['aggr_read']['aggrbw'] + " " + \
                result['aggr_read']['aggrbw_unit']
        except KeyError:
            bwstr = "X"
        row.append(bwstr)

        table.add_row(row)

    print table


def parse_fio_output_files(namespace):
    '''
    Read all the files for fio_data and parse them.
    '''
    filelist = namespace.output
    if not validate_filelist(filelist):
        return None

    results = []
    for filename in filelist:
        results.append(parse_fio_file(filename, verbose=namespace.verbose))

    display_fiodata_tabular(results)


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
    parser.add_argument("-v", "--verbose",
                        required=False,
                        action="store_true",
                        help="Enable Verbose")

    namespace = parser.parse_args()
    return namespace


def main():
    namespace = parse_arguments()
    parse_fio_output_files(namespace)

if __name__ == '__main__':
    main()

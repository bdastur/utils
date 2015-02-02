#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Logging utility.
'''

import logging
import common
from ConfigParser import SafeConfigParser


class LoggerConfig(object):
    '''
    Class to handle logger config.
    '''
    def __init__(self, logconfig):
        '''
        Initialize Logger config.
        '''
        self.logfile = common.get_absolute_path_for_file(logconfig)
        self.cfgparser = SafeConfigParser()
        reslist = self.cfgparser.read(self.logfile)
        if len(reslist) == 0:
            print "No log file provided"



class Logger(object):
    '''
    Logger class.
    '''
    def __init__(self, name=__name__, level="debug",
                 filename="/dev/null", logconfig=None,
                 verbose=True, logformat=None):
        '''
        Initialize logger class.
        '''

        if logformat is None:
            logformat = "[%(levelname)s %(asctime)s]"\
                "[%(process)d " + name + "]" \
                "%(message)s"
        datefmt = '%I:%M:%S %p'

        if not logging.getLogger(name):
            logging.basicConfig(filename=filename,
                                format=logformat,
                                datefmt=datefmt)

        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            # Format.
            formatter = logging.Formatter(logformat,
                                          datefmt=datefmt)
            filehdl = logging.FileHandler(filename)
            filehdl.setFormatter(formatter)
            self.logger.addHandler(filehdl)

            if verbose is True:
                console = logging.StreamHandler()
                console.setFormatter(formatter)
                self.logger.addHandler(console)

    def get_logger(self):
        '''
        Return the logger
        '''
        return self.logger


# --- begin "pretty"
#
# pretty - A miniature library that provides a Python print and stdout
# wrapper that makes colored terminal text easier to use (e.g. without
# having to mess around with ANSI escape sequences). This code is public
# domain - there is no license except that you must leave this header.
#
# Copyright (C) 2008 Brian Nez <thedude at bri1 dot com>
#
# http://nezzen.net/2008/06/23/colored-text-in-python-using-ansi-escape-sequences/

codeCodes = {
    'black':     '0;30', 'bright gray':    '0;37',
    'blue':      '0;34', 'white':          '1;37',
    'green':     '0;32', 'bright blue':    '1;34',
    'cyan':      '0;36', 'bright green':   '1;32',
    'red':       '0;31', 'bright cyan':    '1;36',
    'purple':    '0;35', 'bright red':     '1;31',
    'yellow':    '0;33', 'bright purple':  '1;35',
    'dark gray': '1;30', 'bright yellow':  '1;33',
    'normal':    '0'
}


def stringc(text, color):
    """String in color."""
    return "\033["+codeCodes[color]+"m"+text+"\033[0m"

# --- end "pretty"




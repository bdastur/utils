#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging


class BuilderLogger(object):
    """Builder Logging facility"""

    logLevel = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(
        self,
        name=__name__,
        logFile="/tmp/builderlog.txt",
        fileLogLevel="DEBUG",
        consoleLogLevel="DEBUG",
    ):
        """Initilize Logger
        @args:
            :type name: String
            :param name: Name of the module
            :type logFile: String
            :param logFile: path to the logfile
        """
        # if hasattr(BuilderLogger, 'logger'):
        #     self.logger = BuilderLogger.logger
        #     print "Builder Logger"
        #     self.logger.debug("Logger already initialize!")
        #     return

        # Check if logfile exists
        if not os.path.exists(os.path.dirname(logFile)):
            print(
                "Cannot initialize logger. Path [%s] does not exist"
                % (os.path.dirname(logFile))
            )
            return

        formatStr = "[%(asctime)s %(levelname)5s" " %(process)d %(name)s]: %(message)s"
        logging.basicConfig(
            level=BuilderLogger.logLevel[fileLogLevel],
            format=formatStr,
            datefmt="%m-%d-%y %H:%M",
            filename=logFile,
            filemode="a",
        )

        # Define a stream handler for critical errors.
        console = logging.StreamHandler()
        level = BuilderLogger.logLevel[consoleLogLevel]
        console.setLevel(level)

        formatter = logging.Formatter(
            "[%(asctime)s %(levelname)5s %(name)s]: %(message)s",
            datefmt="%m-%d-%y %H:%M",
        )
        console.setFormatter(formatter)

        # Add handler to root logger.
        logging.getLogger(name).addHandler(console)
        self.logger = logging.getLogger(name)
        BuilderLogger.logger = self.logger
        print("Builder Logger initialized")

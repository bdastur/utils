#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Command Handler:
'''
from loguru import logger
import sys
import subprocess


class Command(object):
    '''
    Command Handlerself
    '''
    def __init__(self):
        pass

    def execute(self, cmd, cwd=None, env=None, popen=False):
        """
        :param cmd Command String
        :param cwd Current working dir (Default: None)
        :param env Environment Variables (Default: None)
        :param popen Flag - Use subprocess Popen or check_output (Default: False)

        :return (return code, output)
        """
        if popen:
            cmdoutput = ""
            sproc = subprocess.Popen(cmd,
                                     env=env,
                                     cwd=cwd,
                                     shell=True,
                                     stdout=subprocess.PIPE)
            while True:
                nextline = sproc.stdout.readline()
                nextline = nextline.decode("utf-8")
                cmdoutput += nextline
                if nextline == '' and sproc.poll() is not None:
                    break

                sys.stdout.write(nextline)
                sys.stdout.flush()

            return sproc.returncode, cmdoutput

        try:
            cmd = cmd.split(" ")
            cmdoutput = subprocess.check_output(cmd,
                                                cwd=cwd,
                                                stderr=subprocess.STDOUT,
                                                shell=False,
                                                env=env)

        except subprocess.CalledProcessError as err:
            logger.error("Failed to execute{}. Err {}", cmd, err)
            return err.returncode, ""

        except FileNotFoundError as err:
            logger.error("File Not Found {}", err)
            return 127, ""

        cmdoutput = cmdoutput.decode("utf-8")

        return 0, cmdoutput



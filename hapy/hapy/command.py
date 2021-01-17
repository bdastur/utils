#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Command Handler:
'''
import sys
import subprocess


class Command(object):
    '''
    Command Handlerself
    '''
    def __init__(self):
        pass

    def execute(self, cmd, cwd=None, env=None, popen=False):
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

            return 0, cmdoutput

        try:
            cmdoutput = subprocess.check_output(cmd,
                                                cwd=cwd,
                                                stderr=subprocess.STDOUT,
                                                shell=False,
                                                env=env)

        except subprocess.CalledProcessError as err:
            self.slog.logger.error("Failed to execut %s. Err %s",
                                   cmd, err)
            return 1, ""

        cmdoutput = cmdoutput.decode("utf-8")

        return 0, cmdoutput



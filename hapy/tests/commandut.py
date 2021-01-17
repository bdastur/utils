#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import hapy.command as command


class CommandUt(unittest.TestCase):
    def test_command_execute_popen(self):
        cmdobj = command.Command()
        cmd = "/tmp/test.sh"
        ret, output = cmdobj.execute(cmd, popen=True)
        print("output: ", output)

    def test_command_execute(self):
        cmdobj = command.Command()
        cmd = "./test.sh"
        ret, output = cmdobj.execute(cmd, popen=False)
        print("output: ", output)


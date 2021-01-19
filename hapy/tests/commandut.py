#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import hapy.command as command


class CommandUt(unittest.TestCase):
    def test_command_execute_popen(self):
        cmdobj = command.Command()
        cmd = "./test.sh"
        ret, output = cmdobj.execute(cmd, popen=True)
        self.assertEqual(ret, 0, msg="Expected retcode 0, got %d" % ret)

        cmd = "./test.sh 2"
        ret, output = cmdobj.execute(cmd, popen=True)
        self.assertEqual(ret, 2, msg="Expected retcode 2, got %d" % ret)

    def test_command_execute(self):
        cmdobj = command.Command()
        cmd = "./test.sh"
        ret, output = cmdobj.execute(cmd, popen=False)
        print("output: ", output)

        cmd = "./test.sh 2"
        ret, output = cmdobj.execute(cmd)
        print("Ret: ", ret)

    def test_command_options(self):
        cmdobj = command.Command()
        cmd = "find /Users/behzad.dastur -name '*.js'"
        ret, output = cmdobj.execute(cmd, popen=True)
        print("Ouput: ", output)


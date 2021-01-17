#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import hapy.terraform as terraform


class TerraformUt(unittest.TestCase):
    def test_basic(self):
        tf_binary = "/usr/local/bin/terraform12"
        tfobj = terraform.Terraform(terraform_binary_path=tf_binary)
        tfobj.init()


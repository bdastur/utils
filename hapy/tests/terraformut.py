#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import hapy.terraform as terraform
import hapy.render as render
import hapy.command as command


class TerraformUt(unittest.TestCase):
    def tearDown(self):
        stage_dir = "/tmp/testdir"
        try:
            os.rmdir(stage_dir)
        except FileNotFoundError:
            print("")

        print("Teardown complete!")

    def test_terraform_init(self):
        tf_binary = "/usr/local/bin/terraform12"
        tfobj = terraform.Terraform(terraform_binary_path=tf_binary)
        tfobj.init()
        self.assertEqual(tfobj.validated, True,
                         msg="Expected False got %s" % tfobj.validated)

    def test_terraform_init_invalid_binary(self):
        tfobj = terraform.Terraform()     
        tfobj.init()
        self.assertEqual(tfobj.validated, False, 
                         msg="Expected False got %s" % tfobj.validated)

    def test_def_generate_command_string(self):
        tfbinary = "terraform12"
        tfobj = terraform.Terraform(terraform_binary_path=tfbinary)
        tfobj.init()
        cmd = tfobj.generate_command_string('init', 
                                            plugin_dir="/tmp/plugins",
                                            force_copy='IsFlag',
                                            var={'foo': 'bar'})
        print("cmd: ", cmd)

    def test_def_generate_command_string_args(self):
        tfbinary = "terraform12"
        stage_dir = "/tmp/testdir"
        os.mkdir(stage_dir)

        tfobj = terraform.Terraform(terraform_binary_path=tfbinary)
        tfobj.init()
        cmd = tfobj.generate_command_string('init',
                                            stage_dir,
                                            plugin_dir="/tmp/plugins",
                                            force_copy='IsFlag',
                                            var={'foo': 'bar'})
        print("cmd: ", cmd)


    def test_terraform_render_init(self):
        templates_dir = "./templates/tf"
        stage_dir = "/tmp/tftestdir"
        obj = {
            "region": "us-west-2",
            "profile": "dev1",
            "backend": {
                "type": "s3",
                "region": "us-west-2",
                "profile": "dev1",
                "bucket": "dev1-temp",
                "key": "tfstates/testdir/testdir.tfstate",
                "encrypt": "true",
                "acl": "bucket-owner-full-control"
            }
        }
        renderobj = render.Render()
        ret = renderobj.render_j2_template_dir(
            templates_dir, stage_dir, ext="tf", **obj)
        self.assertEqual(ret, 0, msg="Expected 0, got %d % ret")

        tfbinary = "terraform12"
        tfobj = terraform.Terraform(terraform_binary_path=tfbinary, 
                                    working_dir=stage_dir)

        args = [stage_dir]
        tfobj.init(*args)


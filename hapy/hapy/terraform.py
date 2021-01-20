#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import hapy.command as command


class Terraform(object):
    """
    Manage interactions with Terraform Hashicorp
    """
    def __init__(self,
                 terraform_binary_path='terraform',
                 working_dir=None,
                 environment=None):
        """
        Initialize
        """
        self.terraform_binary_path = terraform_binary_path
        self.working_dir = working_dir
        self.environment = environment

        self.validated = True
        if not self.__terraform_binary_is_valid():
            self.validated = False

    def __terraform_binary_is_valid(self):
        cmd = "%s version" % self.terraform_binary_path
        cmdobj = command.Command()
        ret, version = cmdobj.execute(cmd, popen=False)
        if ret !=0:
            logger.error("Terraform binary {} is not valid",
                         self.terraform_binary_path)
            return False

        return True

    def generate_command_string(self, operation, *args, **kwargs):
        """
        Set default options to pass to terraform command.
        """
        cmd = [self.terraform_binary_path, operation]

        for key, value in kwargs.items():
            if key == "var":
                for varkey, varval in value.items():
                    option = "-var="
                    option += "'%s=%s'" % (varkey, varval)
                    cmd.append(option)
            else:
                option = ""
                if "_" in key:
                    key = key.replace("_", "-")

                if value == "IsFlag":
                    option = "-%s" % key
                else:
                    option = "-%s=%s" % (key, value)
                cmd.append(option)

        if len(args) > 0:
            for arg in args:
                cmd.append(arg)

        return " ".join(cmd)

    def init(self, *args, **kwargs):
        """
        Initialize a new or existing Terraform working directory
        [`terraform init -h` For detailes]

        :param backend: Configure a backend for this configuration (bool)
        :type  bool

        :param backend_config
        :param force_copy
        :param from_module
        :param get
        :param get_plugins
        :param input
        :param lock
        :param lock_timeout
        :param no_color
        :param plugin_dir
        :param reconfigure
        :param upgrade
        :param verify_plugins

        """
        cmd_str = self.generate_command_string("init", *args, **kwargs)

        stage_dir = None

        cmdobj = command.Command()
        ret, output = cmdobj.execute(cmd_str,
                                     cwd=self.working_dir,
                                     env=self.environment, popen=True)
        if ret != 0:
            print("Terraform init failed")


    def plan(self):
        """
        """
        pass

    def apply(self):
        pass

    def destroy(self):
        pass

    def render(self, **kwargs):
        """
        NOTE!!This subcommand is not part of Terraform.!!NOTE
        This API takes a template string or file and renders the
        untemplated version
        """
        template_file = kwargs.get("template_file", None)
        search_path = kwargs.get("search_path", None)
        template_string = kwargs.get("template_string", None)
        destination_file = kwargs.get("destination_file", None)
        render_obj = kwargs.get("render_obj", None)



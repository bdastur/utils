#!/usr/bin/env python
# -*- coding: utf-8 -*-





class Terraform(object):
    """
    Manage interactions with Terraform Hashicorp
    """
    def __init__(self, 
                 terraform_binary_path=None,
                 working_dir=None,
                 var_file=None):
        """
        Initialize
        """
        pass

    def __set_default_options(self):
        pass

    def init(self, **kwargs):
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
        pass

    def plan(self):
        pass

    def apply(self):
        pass

    def destroy(self):
        pass

    def render(self):
        pass



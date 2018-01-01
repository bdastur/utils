#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import argparse
import yaml
import jinja2
from flask import (Flask, url_for)

'''
PyDashing: Module to generate/render HTML5/Flask/Javascript Dashboards.
Users can define what the dashboard would look like in a yaml file.
'''


# Setup Logging
name = "pydashing"
format_str = '[%(asctime)s %(levelname)5s %(process)d %(name)s]: %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=format_str, datefmt='%m-%d-%y %H:%M')
logger = logging.getLogger(name)


class PyDashingCli(object):
    def __init__(self):
        # Check for atleast one argument
        if len(sys.argv) <= 1:
            print ""
            print "%s requires arguments. Use -h to seee Usage help." % \
                sys.argv[0]
            print ""
            sys.exit()

        self.namespace = self.__parse_arguments()
        self.validate_arguments()

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(
            prog="pydashing",
            description=self.show_help(),
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument("--config",
                            dest="config_file",
                            required=True,
                            help="Path to the configuration file.")

        parser.add_argument("--render-path",
                            dest="render_path",
                            required=False,
                            default="./rendered_dashboards",
                            help="Directory where to render dashing templates.")

        namespace = parser.parse_args()
        return namespace

    def show_help(self):
        msg = """
        PyDashing : A simple python utility to generate nice
        Dashboards.

        Example Usage: ./pydashing.py --config <path to config file>
        """
        print msg

    def validate_arguments(self):
        config_file = self.namespace.config_file
        render_path = self.namespace.render_path

        if not os.path.exists(config_file):
            print "Invalid config file [%s]. Does not exist!" % config_file
            sys.exit()

        if not os.path.exists(render_path):
            print "Invalid staging/render path [%s]. Does not exist!" % \
                render_path
            sys.exit()



class ConfigParser(object):
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            print "Invalid configuration file %s " % config_file
            sys.exit()

        self.parsed_data = self.parse_configuration(config_file)
        print "Config Parser initialized. ", self.parsed_data

    def parse_configuration(self, config_file):
        '''
        Parse the 'yaml' format environment configuration file
        '''
        with open(config_file, 'r') as configfile:
            try:
                parsed_data = yaml.safe_load(configfile)
            except yaml.YAMLError as yamlerror:
                print "Invalid YAML format. Config file: [%s], Error: [%s]" % \
                    (config_file, yamlerror)
                return None

        return parsed_data



class PyDashingRenderer(object):
    def __init__(self,
                 parsed_data,
                 staging_directory,
                 dashboard_templates="./dashboard_templates"):
        if not os.path.exists(dashboard_templates) and \
            not os.path.isdir(dashboard_templates):
            print "Invalid path to dashboard templates [%s]" % \
                dashboard_templates
            return

        self.parsed_data = parsed_data
        self.staging_directory = staging_directory

        # Get template files.
        files = self.get_dashboard_templates(dashboard_templates)
        print "Files: ", files

        # Copy rendered templates.
        self.copy_rendered_templates(files)

    def get_dashboard_templates(self, dirpath):
        """
        Get all the files in the get_dashboard_templates
        """
        files = []
        for (path, dirname, filenames) in os.walk(dirpath):
            for filename in filenames:
                filepath = os.path.join(path, filename)
                files.append(filepath)

        return files

    def generate_renderer_object(self):
        render_obj = {}
        for key,value in self.parsed_data.items():
            keyval = "J2_" + key.upper()
            render_obj[keyval] = value

        return render_obj

    def render_j2_template(self, template_file, search_path, obj):
        '''
        Given the templatefile, and the object, return a
        rendered string.
        '''
        template_loader = jinja2.FileSystemLoader(searchpath=search_path)
        env = jinja2.Environment(loader=template_loader,
                                 trim_blocks=True,
                                 lstrip_blocks=True)
        template = env.get_template(template_file)
        rendered_data = template.render(obj)
        return rendered_data

    def copy_rendered_templates(self, file_list):
        '''
        The function renderes the files in the template directory based
        values from config file and copies them to the staging directory.
        '''
        # Generate the renderer object.
        renderer_obj = self.generate_renderer_object()

        for template_file in file_list:
            # Render the file.
            rendered_obj = self.render_j2_template(template_file,
                                                   ".",
                                                   renderer_obj)

            # file name
            filename = template_file.split("/")[-1]
            file_path = os.path.join(self.staging_directory, filename)
            with open(file_path, 'w') as outfile:
                outfile.write(rendered_obj)


class PyDashing(object):
    def __init__(self):
        cli = PyDashingCli()
        cfgparser = ConfigParser(cli.namespace.config_file)

        renderer = PyDashingRenderer(
            cfgparser.parsed_data,
            cli.namespace.render_path,
            dashboard_templates="./dashboard_templates")





def main():
    pydashing = PyDashing()


if __name__ == '__main__':
    main()

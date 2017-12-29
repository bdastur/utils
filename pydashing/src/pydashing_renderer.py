#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyDashing Renderer:
------------------

"""

import os
import jinja2


class PyDashingRenderer(object):
    def __init__(self,
                 parsed_data,
                 render_path,
                 dashboard_templates="./dashboard_templates"):
        if not os.path.exists(dashboard_templates) and \
            not os.path.isdir(dashboard_templates):
            print "Invalid path to dashboard templates [%s]" % \
                dashboard_templates
            return

        self.parsed_data = parsed_data
        # Create staging folder.
        self.staging_directory = \
            self.create_staging_folder(render_path, parsed_data['name'])

        # Get template files.
        files = self.get_dashboard_templates(dashboard_templates)
        print "Files: ", files


        # Copy rendered templates.
        self.copy_rendered_templates(files)

    def create_staging_folder(self, render_path, dashboard_name):
        """
        Create a staging directory.
        """
        staging_directory = os.path.join(render_path, dashboard_name)
        if not os.path.exists(staging_directory):
            os.mkdir(staging_directory)
        else:
            print "Staging dir [%s] exist." % staging_directory

        # Create Folders for saving templates and static files.
        template_dir = os.path.join(staging_directory, 'templates')
        if not os.path.exists(template_dir):
            os.mkdir(template_dir)

        static_dir = os.path.join(staging_directory, 'static')


        return staging_directory

    def get_dashboard_templates(self, dirpath):
        """
        Get all the files in the get_dashboard_templates
        """
        print "OS. listdir: ", os.listdir(dirpath)
        filenames = os.listdir(dirpath)
        files = []
        for filename in filenames:
            temppath = os.path.join(dirpath, filename)
            if os.path.isdir(temppath):
                print "%s continue as it is a directory.", temppath
                continue

            filepath = os.path.join("dashboard_templates", filename)
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
        print "Template file: %s, search path: %s" % (template_file, search_path)
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

        templates_staging_directory = os.path.join(self.staging_directory,
                                                   "templates")
        for template_file in file_list:
            # Render the file.
            rendered_obj = self.render_j2_template(template_file,
                                                   "..",
                                                   renderer_obj)

            # Get filename from path
            filename = template_file.split("/")[-1]
            filename = filename.split(".j2")[0]

            # Only copy hmtl templates to templates
            try:
                ext = filename.split(".html")[1]
                print "EXT: %s, filename: %s " % (ext, filename)
                file_path = os.path.join(templates_staging_directory, filename)
                with open(file_path, 'w') as outfile:
                    outfile.write(rendered_obj)
            except IndexError:
                file_path = os.path.join(self.staging_directory, filename)
                print "FILEPATH: ", file_path
                with open(file_path, 'w') as outfile:
                    outfile.write(rendered_obj)

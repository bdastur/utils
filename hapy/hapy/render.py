#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
from  loguru import logger
import shutil

'''
Jinja2 Render Util
'''


class Render(object):
    def __init__(self):
        pass

    def render_j2_template_file(self, templateFile, searchPath, **kwargs):
        """ The API will render a Jinja2 template

        :type  templateFile:  String
        :param templateFile: Name of the template file

        :type  searchPath: String
        :param searchPath: Path to the templates directory

        :type  renderObj:  dict
        :param renderObj: Dictionary object to substitute the template vars

        :returns: Rendered string
        """
        template_loader = jinja2.FileSystemLoader(searchpath=searchPath)
        env = jinja2.Environment(
            loader=template_loader, trim_blocks=True, lstrip_blocks=True
        )
        template = env.get_template(templateFile)
        renderedData = template.render(kwargs)

        return renderedData

    def render_j2_template_dir(self, templateDir, destDir, ext=None, **kwargs):
        """
        The API will render all <file>.j2 files to corresponding <file>.<ext>

        :param templateDir Path to where the templates are
        :param destDir     Path to save the rendered files.
        :param ext         Extension to add to the rendered files
        :param **kwargs   Options

        Options:
        dest_path  The destination path where to copy the rendered files (Default: templateDir)
        ext        The file extension to apply to the rendered files.
        """
        if not os.path.exists(templateDir):
            logger.error("templateDir {} does not exist", templateDir)
            return -1

        # Create destDir if does not exist.
        if not os.path.exists(destDir):
            os.mkdir(destDir)

        template_files = os.listdir(templateDir)
        for filename in template_files:
            src_file_path = os.path.join(templateDir, filename)

            (filename_tmp, ext_type) = os.path.splitext(filename)

            # Simply copy the non-template files
            if ext_type != ".j2":
                dest_file_path = os.path.join(destDir, filename)
                shutil.copyfile(src_file_path, dest_file_path)
                continue

            if ext is not None:
                filename_tmp += ".%s" % ext
            dest_file_path = os.path.join(destDir, filename_tmp)

            rendered_data = self.render_j2_template_file(src_file_path,
                                                         ".",
                                                         **kwargs)
            print("Renndered data: ", rendered_data)
            with open(dest_file_path, 'w') as fhandle:
                fhandle.write(rendered_data)

        return 0
        
    def render_j2_template_string(self, templateString, **kwargs):
        """ one line description

        :param template-string:  A Jinja2 template (type: string)
        :param **kwargs:         key-value paris (substitue key/value in template

        :returns:          Rendered string
        """
        env = jinja2.Environment(
            loader=jinja2.BaseLoader, trim_blocks=True, lstrip_blocks=True
        )
        template = env.from_string(templateString)
        renderedData = template.render(kwargs)
        return renderedData


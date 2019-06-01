#!/usr/bin/env python

import os
import shutil
import builderutils.logger as logger
import builder.parser as parser

class DomManager(object):
    """Dom Parser"""

    def __init__(self, dom_config):
        blogger = logger.BuilderLogger(name=__name__)
        self.logger = blogger.logger

        self.dom_tree = {}
        self.rendered_dom = ""
        self.dom_config = dom_config
        self.logger.info("DomMgr Initialized")

    def generate_rendered_html(self):
        """Render html doc"""
        builder_conf = parser.BuilderConfigParser()
        staging_dir = builder_conf.get_staging_path()
        print("Staging path: ", staging_dir)
        if not os.path.exists(staging_dir):
            os.mkdir(staging_dir)

        # TODO: We should be getting app name from user config.
        # For now we can create a default dummy app.
        app_dir = os.path.join(staging_dir, "dummy")
        if not os.path.exists(app_dir):
            os.mkdir(app_dir)

        # TODO: The staging dir format here is that of a flask app
        # If we want to support other web frameworks we need to handle that
        html_staging_dir = os.path.join(app_dir, "templates")
        if not os.path.exists(html_staging_dir):
            os.mkdir(html_staging_dir)

        html_file = os.path.join(html_staging_dir, "index.html")
        with open(html_file, 'w') as hfile:
            hfile.write(self.rendered_dom)

    def update_rendered_dom(self, value, pretty=True):
        """Append to the rendered dom"""
        self.rendered_dom += value
        if pretty:
            self.rendered_dom +=  "\n"

    def parse_dom_tree(self, root, indent=0):
        method_name = "render_{0}_element".format(root['element'])
        if root['element'] == "html":
            indent = 0
        else:
            indent += 2

        try:
            render_function = getattr(self, method_name)
            rendered_string = render_function(root, indent=indent)
            self.update_rendered_dom(rendered_string)
            print(rendered_string)
        except AttributeError:
            tag = "<" + root["element"] + ">"
            print(tag)

        if "children" in root:
            children = root['children'].keys()
            for child in children:
                self.parse_dom_tree(root['children'][child], indent=indent)
        end_tag = indent * " " + "</" + root["element"] + ">"
        print(end_tag)
        self.update_rendered_dom(end_tag)

    @staticmethod
    def render_html_element(node, indent=0):
        tag = indent * " " + "<!DOCTYPE HTML>\n<html>"
        return tag

    @staticmethod
    def render_head_element(node, indent=0):
        tag = indent * " " + "<head>"
        return tag

    @staticmethod
    def render_link_element(node, indent=0):
        renderedString = indent * " " +  "<{0} rel={1} href=\"{2}\">".format(node["element"], node["rel"], node["href"])
        return renderedString

    @staticmethod
    def render_div_element(node, indent=0):
        renderedString = indent * " " +  "<{0} class={1}>".format(node["element"], node["class"])
        return renderedString

    @staticmethod
    def render_header_element(node, indent=0):
        renderedString = indent * " " + "<{0}>{1}".format(node["element"], node["text"])
        return renderedString

    @staticmethod
    def render_h1_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_h2_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_h3_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_h4_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_h5_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_h6_element(node, indent=0):
        return DomManager.render_header_element(node, indent=indent)

    @staticmethod
    def render_script_element(node, indent=0):
        rendered_string = indent * " " + "<{0} src=\"{1}\">".format(node["element"], node["src"])
        return rendered_string





class JSManager(object):
    """Manage JS creation"""
    def __init__(self):
        pass

    def generate_thirdparty_staging(self):
        """Render js static staging"""
        builder_conf = parser.BuilderConfigParser()
        staging_dir = builder_conf.get_staging_path()
        print("Staging path: ", staging_dir)
        if not os.path.exists(staging_dir):
            os.mkdir(staging_dir)

        # TODO: We should be getting app name from user config.
        # For now we can create a default dummy app.
        app_dir = os.path.join(staging_dir, "dummy")
        if not os.path.exists(app_dir):
            os.mkdir(app_dir)

        # Set JS static
        js_static_dir = os.path.join(app_dir, 'static')
        if not os.path.exists(js_static_dir):
            os.mkdir(js_static_dir)

        thirdparty_path = builder_conf.get_thirdparty_path()
        # Copy thirdyparty files
        if os.path.exists(js_static_dir):
            shutil.rmtree(js_static_dir)
        shutil.copytree(thirdparty_path, js_static_dir)


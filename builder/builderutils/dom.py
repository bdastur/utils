#!/usr/bin/env python

import builderutils.logger as logger


class DomManager(object):
    """Dom Parser"""

    def __init__(self, dom_config):
        blogger = logger.BuilderLogger(name=__name__)
        self.logger = blogger.logger

        self.dom_tree = {}
        self.rendered_dom = ""
        self.dom_config = dom_config
        self.logger.info("DomMgr Initialized")

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
    def __init__(self, builder_config):
        pass

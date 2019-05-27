#!/usr/bin/env python

import builderutils.logger as logger


class DomManager(object):
    """Dom Parser"""

    def __init__(self, dom_config):
        blogger = logger.BuilderLogger(name=__name__)
        self.logger = blogger.logger

        self.domTree = {}
        self.dom_config = dom_config
        self.logger.info("DomMgr Initialized")

    def parseDomTree(self, root):
        methodName = "render_{0}_element".format(root['element'])
        try:
            renderFunction = getattr(self, methodName)
            renderedString = renderFunction(root)
            print(renderedString)
        except AttributeError:
            tag = "<" + root["element"] + ">"
            print(tag)

        if "children" in root:
            children = root['children'].keys()
            for child in children:
                self.parseDomTree(root['children'][child])
        endtag = "</" + root["element"] + ">"
        print(endtag)

    @staticmethod
    def render_html_element(node):
        tag = "<html>"
        return tag

    @staticmethod
    def render_head_element(node):
        tag = "<head>"
        return tag

    @staticmethod
    def render_link_element(node):
        renderedString = "<{0} rel={1} href=\"{2}\">".format(node["element"], node["rel"], node["href"])
        return renderedString

    @staticmethod
    def render_div_element(node):
        renderedString = "<{0} class={1}>".format(node["element"], node["class"])
        return renderedString

    @staticmethod
    def render_header_element(node):
        renderedString = "<{0}>{1}".format(node["element"], node["text"])
        return renderedString

    @staticmethod
    def render_h1_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_h2_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_h3_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_h4_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_h5_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_h6_element(node):
        return DomManager.render_header_element(node)

    @staticmethod
    def render_script_element(node):
        renderedString = "<{0} src=\"{1}\">".format(node["element"], node["src"])
        return renderedString


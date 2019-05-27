#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import builder.parser as parser
import builder.renderer as renderer
import builderutils.dom as dom


class BuilderUt(unittest.TestCase):
    def test_parse_builder_config(self):
        print("Parse Buidler config")
        builderConfig = parser.BuilderConfigParser()
        self.assertEqual(builderConfig.validate, True,
            "Builder config not initialized correctly")

    def test_parse_user_config(self):
        print("Parse user config")

    def test_dom_parser(self):
        print("Test dom parser")
        conf_obj = parser.BuilderConfigParser()
        self.assertEqual(conf_obj.validate, True, "Builder config not initialized correctly")
        dom_config = conf_obj.get_dom_config()
        self.assertFalse(dom_config == None, "Dom config cannot be empty")
        dom_mgr = dom.DomManager(dom_config)
        dom_mgr.parseDomTree(dom_config['html'])

    def test_build_staging_path(self):
        print("Test basic")
        renderObj = renderer.Renderer()
        self.assertNotEqual(renderObj, None)

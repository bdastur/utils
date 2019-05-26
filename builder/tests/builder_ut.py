#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import builder.parser as parser
import builder.renderer as renderer


class BuilderUt(unittest.TestCase):
    def test_parse_builder_config(self):
        print("Parse Buidler config")
        builderConfig = parser.BuilderConfigParser()
        self.assertEqual(builderConfig.validate, True,
            "Builder config not initialized correctly")

    def test_parse_user_config(self):
        print("Parse user config")

    def test_build_staging_path(self):
        print("Test basic")
        renderObj = renderer.Renderer()
        self.assertNotEqual(renderObj, None)

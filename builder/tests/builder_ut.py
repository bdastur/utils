#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import builder.parser as parser
import builder.renderer as renderer


class BuilderUT(unittest.TestCase):
    def test_parseBuilderConfig(self):
        print("Parse Buidler config")
        builderConfig = parser.BuilderConfigParser()
        self.assertEqual(builderConfig.validate, True,
            "Builder config not initialized correctly")

    def test_buildStagingPath(self):
        print("Test basic")
        renderObj = renderer.Renderer()
        self.assertNotEqual(renderObj, None)

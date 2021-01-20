#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import hapy.render as render


class RenderUt(unittest.TestCase):
    def tearDown(self):
        stage_dir = "/tmp/testdir"
        shutil.rmtree(stage_dir)

    def test_string_render(self):
        renderobj = render.Render()
        template_string = "My name is {{ name }}"
        obj = {
            "name": "Behzad"
        }
        rendered_string = renderobj.render_j2_template_string(template_string, **obj)
        print("Rendered strin: ", rendered_string)

    def test_string_render_nested(self):
        renderobj = render.Render()
        
        template_string = """
            {% for user in users %}
                User: {{ user.name}}, Age: {{ user.age }}
            {% endfor %}
        """
        obj = {
                "users": [{
                         "name": "Behzad", 
                         "age": 43
                     },
                     {
                         "name": "Dash",
                         "age": 33
                     }]
         }
        rendered_string = renderobj.render_j2_template_string(template_string, **obj)
        print("Rendered string: ", rendered_string)

    def test_render_j2_template_file(self):
        template_file = "./templates/sample_1.j2"
        search_path = "."
        obj = {
            "name": "Behzad"
        }

        renderobj = render.Render()
        rendered_data = renderobj.render_j2_template_file(template_file, search_path, **obj)
        print("Rendered data: ", rendered_data)

    def test_render_j2_template_dir(self):
        stage_dir = "/tmp/testdir"
        templates_dir = "./templates"

        obj = {
            "name": "Behzad",
            "users": [{"name": "Jack", "age": 44},
                      {"name": "Joe", "age": 42}]
        }
        renderobj = render.Render()
        ret = renderobj.render_j2_template_dir(templates_dir, stage_dir, ext="txt", **obj)
        self.assertEqual(ret, 0, msg="Return expected 0 got %d" % ret)


        filelist = os.listdir(stage_dir)
        print("File list: ", filelist)





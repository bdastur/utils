#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import hapy.render as render


class RenderUt(unittest.TestCase):
    def test_string_render(self):
        renderobj = render.Render()
        template_string = "My name is {{ name }}"
        obj = {
            "name": "Behzad"
        }
        rendered_string = renderobj.render_j2_template_string(template_string, **obj)
        print("Rendered strin: ", rendered_string)

    def test_string_render(self):
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Common utils.
'''

import os


def get_absolute_path_for_file(file_name, splitdir=None):
    '''
    Return the filename in absolute path for any file
    passed as relative path.
    '''
    base = os.path.basename(__file__)
    if splitdir is not None:
        splitdir = splitdir + "/" + base
    else:
        splitdir = base

    if os.path.isabs(__file__):
        abs_file_path = os.path.join(__file__.split(splitdir)[0],
                                     file_name)
    else:
        abs_file = os.path.abspath(__file__)
        abs_file_path = os.path.join(abs_file.split(splitdir)[0],
                                     file_name)

    return abs_file_path



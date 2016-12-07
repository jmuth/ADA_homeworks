#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Joachim Muth <joachim.henri.muth@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
def load_txt(file_name):
    with open(file_name) as f:
        data = f.readlines()
        data = [x.strip('\n') for x in data]

    return data
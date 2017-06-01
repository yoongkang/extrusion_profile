#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="extrusion_profile",
    version="0.0.1",
    author="Yoong Kang Lim",
    author_email="yoongkang.lim@gmail.com",
    description=("Project for Plethora coding challenge"),
    long_description=read('README.md'),
)

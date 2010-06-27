#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Constants used throughout the application.
"""
import os
import sys

# Global Variables
APP_NAME = "Resumey"
PROG_NAME = "resumey"
APP_VERSION = "0.1"
APP_AUTHOR = "Jorge A Gallegos (kad@blegh.net)"
TEMPLATE_DIR = "%s/templates" % os.path.dirname(sys.argv[0])
LOCALE_DIR = "%s/locale" % os.path.dirname(sys.argv[0])
EXT_MAPPINGS = {"text": "txt", "html": "html", "pdf": "pdf", "web": "html"}

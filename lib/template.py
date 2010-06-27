#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Template master class module
"""

import logging
import os

from mako import lookup
from mako import template

import globvars

# logging stuff
logger = logging.getLogger(globvars.PROG_NAME)

class Template(template.Template):

  lookup = None
  out = None

  def __init__(self, template_dir):
    logger.debug("In template")
    template.Template.__init__(self, "")
    self.lookup = lookup.TemplateLookup(directories=[template_dir],
                                        input_encoding="utf-8",
                                        module_directory="/tmp/makoish")

  def load_template(self, tpl):
    """
    Loads a given template using the template loader.

    @access: private
    @param tpl: Template name to lookup
    """
    t = self.lookup.get_template(tpl)
    return t

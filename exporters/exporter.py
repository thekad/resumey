#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Exporter base class module
"""

import codecs
from datetime import date
import logging
import os
import sys

from Cheetah.Template import Template

from lib import globvars


class Exporter(object):

  _data = None
  _logger = logging.getLogger(globvars.PROG_NAME)
  _sections = []
  _format = "txt"
  _tags = []
  _out = None
  _today = date.today()
  _path = ""

  def __init__(self, format):
    self._format = format
    self._logger.debug("Format is %s" % self._format)
    self._path = os.path.join(os.path.dirname(sys.argv[0]),
      globvars.TEMPLATE_DIR, self._format)
    self._logger.debug("Template path is %s" % self._path)

  def _fill_template(self, tmpl, ns):
    f = os.path.join(self._path, "%s.tmpl" % tmpl)
    return Template(file=f, searchList=ns)

  def set_data(self, data):
    if data:
      self._data = data

  def set_output_file(self, out):
    """
    Sets the output file to dump the final document to.

    @param out: output file name
    @raises IOError
    """
    if os.access(os.path.dirname(out), os.W_OK):
      self._out = out
      self._logger.info(_("Will write to %s") % self._out)
    else:
      raise IOError(_("No write access to '%s'" ) % os.path.dirname(out))

  def parse_header(self):
    """
    Parses the resume's header section

    @access: public
    """
    raise NotImplementedError

  def parse_about(self):
    """
    Parses the resume's about section (about and cover letter)

    @access: public
    """
    raise NotImplementedError

  def parse_academics(self):
    """
    Parses the resume's academics section

    @access: public
    """
    raise NotImplementedError

  def parse_skills(self):
    """
    Parses the resume's skillset section

    @access: public
    """
    raise NotImplementedError

  def parse_job_history(self):
    """
    Parses the resume's job history section

    @access: public
    """
    raise NotImplementedError

  def parse_additional_info(self):
    """
    Parses the resume's projects, awards and hobbies sections

    @access: public
    """
    raise NotImplementedError

  def set_tags(self, tags):
    """
    Sets the filtering tags

    @access: public
    @param tags: Tag list
    """
    self._tags = tags

  def _calculate_years(self, year):
    """
    Calculates how many years you have of experience given a starting year

    @access: protected
    @param year: Starting year
    """
    diff = self._today.year - int(year)
    # include current year
    return diff

  def _write_file(self):
    """
    Writes the actual file to the filesystem.

    @access: protected
    """
    raise NotImplementedError

  def build_resume(self):
    """
    Takes all parts of the resume and builds it to the file

    @access: public
    """
    self.parse_header()
    if self._data.has_key("about"):
      self.parse_about()
    self.parse_academics()
    self.parse_skills()
    self.parse_job_history()
    self.parse_additional_info()
    self._write_file()


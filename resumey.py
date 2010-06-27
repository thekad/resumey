#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Module to transform YAML resume files to
several outputs. YAML should describe
your resume in detail (see examples/)
"""

import gettext
import logging
from optparse import OptionParser
import os
import sys
import yaml
import pprint

from exporters import text
from lib import globvars

__app__ = globvars.APP_NAME
__version__ = globvars.APP_VERSION
__author__ = globvars.APP_AUTHOR

# logging stuff
logging.basicConfig(format="%(filename)s:%(lineno)d - "
                    "%(levelname)s: %(message)s")
LOGGER = logging.getLogger(globvars.PROG_NAME)
LOGGER.setLevel(logging.INFO)

# gettext stuff
gettext.install(globvars.PROG_NAME, localedir=globvars.LOCALE_DIR, unicode=1)


class Resumey(object):
  """
  Main class
  """

  __output = ""
  __tags = None
  format = None
  exporter = None
  ifile = None

  def __init__(self, f=None):
    """
    Main constructor.

    @param file: YAML file path
    @access: public
    """
    if f:
      self.ifile = f

  def set_input_file(self, f):
    """
    Sets YAML input file.

    @param file: YAML file path
    @access: public
    """
    if f:
      self.ifile = f

  def __load_data(self):
    """
    Serializes the YAML file contents into a class variable.

    @param file: File path
    @access: private
    """
    try:
      fh = open(self.ifile)
      data = yaml.load(fh)
      fh.close()
      return data
    except Exception, e:
      LOGGER.debug(str(e))
      LOGGER.error(_("You need to specify an existing file"))
      sys.exit(1)

  def set_tags(self, tags):
    """
    Sets the tags to filter

    @access: public
    @param tags: List of tags
    """
    self.__tags = tags
    if self.exporter:
      self.exporter.set_tags(self.__tags)
    else:
      LOGGER.error(_("You should first call set_output()"))
    LOGGER.debug("Tags are %s" % str(self.__tags))

  def set_output(self, type, out):
    """
    Sets the output type to print the resume onto.

    @param type: Type, can be one of the available
                 directories inside templates/
    @param out: Output file path
    @raises TypeError
    """
    if type in self.get_available_formats():
      self.format = type
    else:
      raise TypeError(_("Can't export to '%s' format") % type)
    LOGGER.debug(self.format)
    self.exporter = eval(self.format + "." +
      self.format.capitalize() + "Exporter()")
    self.exporter.set_output_file(out)
    LOGGER.debug(out)
    self.exporter.set_data(self.__load_data())

  def get_tags(self):
    """
    Returns the tags listed in the input file

    @return: list
    """

    def traverse(data, tags):
      if isinstance(data, dict):
        for k, v in data.items():
          if k == "tags":
            LOGGER.debug("found tags!")
            if isinstance(v, list):
              for item in v:
                if item not in tags:
                  tags.append(item)
            else:
              if v not in tags:
                tags.append(v)
            return tags
          else:
            LOGGER.debug("Digging deeper...")
            traverse(v, tags)
        return tags
      elif isinstance(data, list):
        LOGGER.debug("is list")
        for item in data:
          LOGGER.debug("Digging deeper...")
          traverse(item, tags)
      else:
        return []
    tags = []
    traverse(self.__load_data(), tags)
    return tags

  def get_available_formats(self):
    """
    Returns the available formats in the templates directory

    @return: list
    """

    formats = []
    for obj in os.listdir(globvars.TEMPLATE_DIR):
      if os.path.isdir(os.path.join(globvars.TEMPLATE_DIR, obj)):
        formats.append(obj)
    return formats

  def run(self):
    """
    Main method.

    @access: public
    """
    self.exporter.build_resume()

def main():
  op = OptionParser()
  resumey = Resumey()
  fmts = resumey.get_available_formats()
  op.add_option("-i", "--input", dest="input", action="store",
                help=_("YAML file where your resume lives"))
  op.add_option("-f", "--format", dest="format", action="store",
                help=_("Output format. Available formats: ") +
                ",".join(fmts), default="text")
  op.add_option("-o", "--output", dest="output", action="store",
                help=_("Output file/directory"))
  op.add_option("-c", "--css", dest="css", action="store",
                help=_("CSS File to be embedded (only for HTML)"))
  op.add_option("-d", "--debug", dest="debug", action="store_true",
                help=_("Enable logging"), default=False)
  op.add_option("-t", "--tags", dest="tags", action="store",
                help=_("Comma separated list of tags to filter on"))
  op.add_option("-l", "--list-tags", dest="list", action="store_true",
                default=False,
                help=_("List all tags in the YAML file (unique action)"))
  (options, args) = op.parse_args()
  if options.debug:
    LOGGER.setLevel(logging.DEBUG)
  if not options.input:
    LOGGER.error(_("Please specify an input YAML file"))
    sys.exit(1)
  resumey.set_input_file(options.input)
  if options.list:
    print _("The available tags found in the input file are: %s" %
      ",".join(resumey.get_tags()))
    sys.exit(0)
  default_output = "%s%s%s" % (options.input.split(os.extsep)[0],
                               os.extsep, globvars.EXT_MAPPINGS[options.format])
  if not options.output:
    output_file = os.path.abspath(default_output)
  else:
    if os.path.isdir(options.output):
      output_file = os.path.join(os.path.abspath(options.output),
                                 os.path.basename(default_output))
    else:
      output_file = os.path.abspath(options.output)
  resumey.set_output(options.format, output_file)
  if options.tags:
    resumey.set_tags(options.tags.split(","))
  resumey.run()

if __name__ == "__main__":
  main()

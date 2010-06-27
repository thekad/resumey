#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Text Exporter class module
"""

import codecs
import os
import sys

from exporters import exporter
from lib import globvars


class TextExporter(exporter.Exporter):

  def __init__(self):
    """
    Default constructor

    @access: public
    """
    exporter.Exporter.__init__(self, "text")

  def parse_header(self):
    """
    Parses the text format header

    @access: public
    @overrides: resumey.lib.exporter.Exporter.parse_header()
    """
    self._logger.debug("Parsing header section")
    data = self._data["personal"]
    data["addresses"] = []
    for address in self._data["addresses"]:
      self._logger.debug("Looping through addresses")
      if address.has_key("tags"):
        # If tags are specified, filter
        if self._tags and set(address["tags"]).intersection(self._tags):
          data["addresses"].append(address)
      else:
        # If no tags are specified, include by default
        data["addresses"].append(address)
    if self._data.has_key("contact"):
      data["contact"] = self._data["contact"]
    self._logger.debug(data)
    tpl = self._fill_template("header", data)
    self._sections.append(str(tpl))
    data = None
    tpl = None

  def parse_about(self):
    """
    Parses the text format about section

    @access: public
    @overrides: resumey.lib.exporter.Exporter.parse_about()
    """
    self._logger.debug("Parsing the about section")
    data = {}
    if self._data["about"].has_key("goal"):
      data["goal"] = self._data["about"]["goal"]
    if self._data["about"].has_key("covers"):
      for cover in self._data["about"]["covers"]:
        if cover.has_key("tags"):
          if self._tags and set(cover["tags"]).intersection(self._tags):
            data["cover"] = cover["text"]
        else:
          data["cover"] = cover["text"]
    self._logger.debug(data)
    tpl = self._fill_template("about", data)
    self._sections.append(str(tpl))
    data = None
    tpl = None

  def parse_academics(self):
    """
    Parses the academic title section
  
    @access: public
    @overrides: resumey.lib.exporter.Exporter.parse_academics()
    """
    self._logger.debug("Parsing the academics section")
    data = {}
    data = {"degrees" : self._data["education"]}
    self._logger.debug(data)
    tpl = self._fill_template("academics", data)
    self._sections.append(str(tpl))
    data = None
    tpl = None

  def parse_skills(self):
    """
    Parses the skillset list

    @access: public
    @overrides: resumey.lib.exporter.Exporter.parse_skills()
    """
    self._logger.debug("Parsing the skillset list")
    data = []
    for skill in self._data["skillset"]:
      row = {}
      row["name"] = skill["name"].upper().title()
      if skill.has_key("level"):
        row["level"] = skill["level"].title()
      row["years"] = self._calculate_years(skill["since"])
      if skill.has_key("tags"):
        if self._tags and set(skill["tags"]).intersection(self._tags):
          data.append(row)
      else:
        data.append(row)
    self._logger.debug(data)
    tpl = self._fill_template("skillset", {"skills": data})
    self._sections.append(str(tpl))
    data = None
    tpl = None

  def parse_job_history(self):
    """
    Parses the job history section

    @access: public
    @overrides: resumey.lib.exporter.Exporter.parse_job_history()
    """
    self._logger.debug("Parsing the job history")
    data = []
    for job in self._data["jobs"]:
      row = {}
      row["started"] = job["started"]
      if job.has_key("finished"):
        row["finished"] = job["finished"]
      else:
        row["finished"] = _("Present day")
      row["company"] = job["company"]
      if job.has_key("type"):
        row["type"] = job["type"]
      row["positions"] = []
      for position in job["positions"]:
        if position.has_key("tags"):
          if self._tags and set(position["tags"]).intersection(self._tags):
            row["positions"].append(position)
        else:
          row["positions"].append(position)
      data.append(row)
    self._logger.debug(data)
    tpl = self._fill_template("jobs", {"jobs": data})
    self._sections.append(str(tpl))
    data = None
    tpl = None

  def parse_additional_info(self):
    """
    Parses additional info, such as projects and hobbies, etc

    @access: public
    @overrides: resumey.lib.exporter.parse_additional_info()
    """
    self._logger.debug("Parsing additional info section")
    data = {}
    if self._data.has_key("projects"):
      data["projects"] = self._data["projects"]
    if self._data.has_key("awards"):
      data["awards"] = self._data["awards"]
    if self._data.has_key("hobbies"):
      data["hobbies"] = self._data["hobbies"]
    if self._data.has_key("copyright"):
      data["copyright"] = self._data["copyright"]
    if data:
      self._logger.debug(data)
      tpl = self._fill_template("additional", data)
      self._sections.append(str(tpl))
      data = None
      tpl = None

  def _write_file(self):
    """
    Writes the actual file to the filesystem.

    @access: protected
    @overrides: resumey.lib.exporter._write_file()
    """
    fh = codecs.open(self._out, "w", "utf-8")
    fh.writelines(self._sections)
    fh.close()


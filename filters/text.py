#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ai ts=2 sts=2 et sw=2
#
# Copyright 2009 - Jorge A Gallegos (kad@blegh.net)
#
"""
Text filters
"""

def emp(msg):
  return "_%s_" % msg

def bold(msg):
  return "**%s**" % msg

def title(msg, level):
  tag = ""
  i = 0
  while i in range(level):
    tag = "".join(["#", tag])
    i += 1
  return "%s %s %s" % (tag, msg.title (), tag)

def h1(msg):
  return title(msg, 1)

def h2(msg):
  return title(msg, 2)

def h3(msg):
  return title(msg, 3)


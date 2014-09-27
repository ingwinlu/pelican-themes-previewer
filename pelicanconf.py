#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'pelican'
SITENAME = 'pelican-themes'
SITEURL = 'http://dev.heroicdebugging.biz'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 1

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["themes_git_reader"] #enter git reader/parser here

THEME = "theme"
DIRECT_TEMPLATES = ('index','article',)
BOOTSTRAP_THEME = 'paper'
PYGMENTS_STYLE = 'colorful'
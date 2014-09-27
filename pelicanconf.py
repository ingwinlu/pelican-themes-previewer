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
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 1

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["themes_git_reader"]

THEME = "theme"
BOOTSTRAP_THEME = 'paper'
PYGMENTS_STYLE = 'colorful'


DIRECT_TEMPLATES = ('index',)
ARTICLE_URL = 'themes/{slug}/'
ARTICLE_SAVE_AS = 'themes/{slug}/index.html'
AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''

GIT_UPDATE = True

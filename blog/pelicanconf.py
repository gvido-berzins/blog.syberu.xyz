#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Gvido Bērziņš'
SITENAME = 'Blog - Syberu'
SITEURL = ''

PATH = 'content'
THEME="pelican-twitchy"
TIMEZONE = 'Europe/Riga'
DEFAULT_LANG = 'en'

# Page naming convention
# ARTICLE_URL = "{category}/{slug}"
# ARTICLE_SAVE_AS = "{category}/{slug}/index.html"
# AUTHOR_URL = "authors/{slug}"
# AUTHOR_SAVE_AS = "authors/{slug}/index.html"
# CATEGORY_URL = "{slug}"
# CATEGORY_SAVE_AS = "{slug}/index.html"
# TAG_URL = "tags/{slug}"
# TAG_SAVE_AS = "tags/{slug}/index.html"
# PAGE_URL = "{slug}.html"
# PAGE_SAVE_AS = "{slug}.html"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Before build
DELETE_OUTPUT_DIRECTORY = True

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Gvido Bērziņš'
SITENAME = 'Blog - Syberu'
SITEURL = ''

PATH = 'content'
THEME="pelican-twitchy"
TIMEZONE = 'Europe/Riga'
DEFAULT_LANG = 'en'
PLUGINS = ["image_process"]

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
IMAGE_PROCESS_DIR = "images"
IMAGE_PROCESS = {
    "crisp": {
        "type": "responsive-image",
        "srcset": [
            ("1x", ["scale_in 800 600 True"]),
            ("2x", ["scale_in 1600 1200 True"]),
            ("4x", ["scale_in 3200 2400 True"]),
        ],
        "default": "1x",
    },
    "large-photo": {
        "type": "responsive-image",
        "sizes": (
            "(min-width: 1200px) 800px, "
            "(min-width: 992px) 650px, "
            "(min-width: 768px) 718px, "
            "100vw"
        ),
        "srcset": [
            ("600w", ["scale_in 600 450 True"]),
            ("800w", ["scale_in 800 600 True"]),
            ("1600w", ["scale_in 1600 1200 True"]),
        ],
        "default": "800w",
    },
}
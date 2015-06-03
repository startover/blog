#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'startover'
SITENAME = u"startover's blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

GITHUB_URL = 'https://github.com/startover'

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),)

# Social widget
# SOCIAL = (('github', 'https://github.com/startover'),
        # ('weibo', 'http://weibo.com/u/1530368442'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'theme'

# very useful for debugging purposes
DELETE_OUTPUT_DIRECTORY = False

# all defaults to True.
DISPLAY_HEADER = True
DISPLAY_FOOTER = True
DISPLAY_HOME   = True
DISPLAY_MENU   = True

ARTICLE_URL = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# provided as examples, they make ‘clean’ urls. used by MENU_INTERNAL_PAGES.
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL           = 'tags'
TAGS_SAVE_AS       = 'tags/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL     = 'categories'
CATEGORIES_SAVE_AS = 'categories/index.html'

ARCHIVES_URL       = 'archives'
ARCHIVES_SAVE_AS   = 'archives/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# use those if you want pelican standard pages to appear in your menu
MENU_INTERNAL_PAGES = (
    ('Categories', CATEGORIES_URL, CATEGORIES_SAVE_AS),
    ('Tags', TAGS_URL, TAGS_SAVE_AS),
    ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
)

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# plugins
PLUGIN_PATHS = ['pelican-plugins',]
PLUGINS = ['summary','sitemap','random_article','neighbors','global_license']
SITEMAP = {
'format': 'xml',
'priorities': {
'articles': 0.7,
'indexes': 0.5,
'pages': 0.5
},
'changefreqs': {
'articles': 'monthly',
'indexes': 'daily',
'pages': 'monthly'
}
}
RANDOM = 'random.html'
LICENSE = '码字不易，转载请注明来源<a href="http://startover.github.io/" target="_blank">startover</a>'

DUOSHUO_SITENAME = "startover"

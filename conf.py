###############################################################
# Copyright 2024 Sandia National Laboratories, LLC
# (c.f. AUTHORS, NOTICE.LLNS, COPYING)
#
# This file is part of the OVIS framework.
# For details, see https://github.com/ovis-hpc.
#
# SPDX-License-Identifier: LGPL-3.0
###############################################################

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import subprocess
import sphinx_immaterial
from recommonmark.transform import AutoStructify

import ssl
import requests
from sphinx.ext import intersphinx
import urllib3

# Set environment variables to ca-bundle.crt when using container on Sandia machine.
#os.environ["CURL_CA_BUNDLE"] = '/etc/ssl/certs/ca-bundle.crt'
#os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-bundle.crt'

from urllib.request import build_opener, HTTPSHandler, install_opener

# Disable SSL verification globally
ssl._create_default_https_context = ssl._create_unverified_context
opener = build_opener(HTTPSHandler(context=ssl._create_unverified_context()))
install_opener(opener)

sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------

project = "OVIS-HPC"
copyright = """Copyright 2024 Sandia National Laboratories and Open Grid Computing, Inc.

SPDX-License-Identifier: LGPL-3.0"""
author = "This page is maintained by the Ovis-HPC community."

# -- RTD configuration -------------------------------------------------------

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

# This is used for linking and such so we link to the thing we're building
rtd_version = os.environ.get("READTHEDOCS_VERSION", "latest")
if rtd_version not in ["stable", "latest"]:
    rtd_version = "stable"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinxcontrib.spelling",
    "domainrefs",
    "myst_parser",
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_markdown_tables",
    "sphinx_immaterial.theme_result",
    "sphinx_immaterial.kbd_keys",
    "sphinx_immaterial.apidoc.format_signatures",
    "sphinx_immaterial.apidoc.json.domain",
    "sphinx_immaterial.apidoc.python.apigen",
    "sphinx_immaterial.graphviz",
]

# sphinxcontrib.spelling settings
spelling_word_list_filename = ["spell.en.pws"]

autosummary_generate = True
autoclass_content = "class"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "env",
    "venv",
    "README.md",
    ".github",
]

master_doc = "index"
source_suffix = {".rst": "restructuredtext"}

domainrefs = {
    "linux:man1": {
        "text": "%s(1)",
        "url": "http://man7.org/linux/man-pages/man1/%s.1.html",
    },
    "linux:man2": {
        "text": "%s(2)",
        "url": "http://man7.org/linux/man-pages/man2/%s.2.html",
    },
    "linux:man3": {
        "text": "%s(3)",
        "url": "http://man7.org/linux/man-pages/man3/%s.3.html",
    },
    "linux:man7": {
        "text": "%s(7)",
        "url": "http://man7.org/linux/man-pages/man7/%s.7.html",
    },
    "linux:man8": {
        "text": "%s(8)",
        "url": "http://man7.org/linux/man-pages/man8/%s.8.html",
    },
    "ldms:all-man": {
        "text": "%s",
        "url": "https://ovis-hpc.readthedocs.io/projects/ldms/en/latest/ldms_man/%s.html",
    },
    "ldms:man": {
        "text": "%s",
        "url": "https://ovis-hpc.readthedocs.io/projects/ldms/en/latest/ldms_man/%s.html",
    },
#    "ldms:doc": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/ldms/en/latest/index.html",
#    },
#    "ldms:doc-page": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/ldms/en/latest/%s.html",
#    },
    "sos:all-man": {
        "url": "https://ovis-hpc.readthedocs.io/projects/sos/en/latest/sos_man/index.html",
    },
    "sos:man": {
        "text": "%s",
        "url": "https://ovis-hpc.readthedocs.io/projects/sos/en/latest/sos_man/%s.html",
    },
#    "sos:doc": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/sos/en/latest/index.html",
#    },
#    "sos:doc-page": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/sos/en/latest/%s.html",
#    },
#    "maestro:doc": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/maestro/en/latest/index.html",
#    },
#    "maestro:doc-page": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/maestro/en/latest/%s.html",
#    },
#    "baler:doc": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/baler/en/latest/index.html",
#    },
#    "baler:doc-page": {
#        "text": "%s",
#        "url": "https://ovis-hpc.readthedocs.io/projects/baler/en/latest/%s.html",
#    },
}

# -- Options for Intersphinx -------------------------------------------------

intersphinx_mapping = {
    "sos": (
        "https://ovis-hpc.readthedocs.io/projects/sos/en/latest/",
        None,
    ),
    "maestro": (
        "https://ovis-hpc.readthedocs.io/projects/maestro/en/latest/",
        None,
    ),
    "baler": (
        "https://ovis-hpc.readthedocs.io/projects/baler/en/latest/",
        None,
    ),
    "ldms": (
        "https://ovis-hpc.readthedocs.io/projects/ldms/en/latest/",
        None,
    ),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
extensions.append("sphinx_immaterial")
# html_theme_path = sphinx_immaterial.html_theme_path()
# html_context = sphinx_immaterial.get_html_context()
html_css_files = ["custom.css"]

extensions.append("sphinx_immaterial")
html_theme = "sphinx_immaterial"

# material theme options (see theme.conf for more information)
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "http://ovis-hpc.github.io/readthedocs/",
    "repo_url": "https://github.com/ovis-hpc/readthedocs/",
    "repo_name": "ovis-hpc",
    "edit_uri": "blob/main",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        "navigation.tabs",
        "toc.integrate",
        "navigation.sections",
        "navigation.instant",
        "header.autohide",
        "navigation.top",
        "navigation.tracking",
        "search.highlight",
        "search.share",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "cyan",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "blue",
            "accent": "teal",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    # BEGIN: version_dropdown
    "version_dropdown": False,
    "version_info": [
        {
            "version": "https://ovis-hpc.readthedocs.io",
            "title": "ReadTheDocs",
            "aliases": [],
        },
        {
            "version": "https://www.ldms-ug.org",
            "title": "Github Pages",
            "aliases": [],
        },
    ],
    # END: version_dropdown
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/ovis-hpc/readthedocs",
            "name": "Source on github.com",
        },
        {
            "icon": "material/chart-donut-variant",
            "link": "https://www.ldms-ug.org/",
            "name": "OVIS-HPC",
        },
    ],
    # END: social icons
}


#    "touch_icon": "images/flux-operator.jpg",
#    "theme_color": "#262626",
#    "nav_links": [
#        {
#            "href": "https://flux-framework.org/",
#            "internal": False,
#            "title": "Flux Framework",
#        },
#        {
#            "href": "https://github.com/flux-framework",
#            "internal": False,
#            "title": "Flux Framework on GitHub",
#        },
#        {
#            "href": "https://github.com/flux-framework/flux-docs",
#            "internal": False,
#            "title": "Flux Documentation on GitHub",
#        },
#    ],

todo_include_todos = True
sphinx_immaterial_bundle_source_maps = True

# Custom sphinx material variables
theme_logo_icon = "images/ovis-logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_show_sourcelink = True
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}
sphinx_immaterial_icon_path = html_static_path

# -- Options for man output -------------------------------------------------

man_pages = []

language = "en"
html_last_updated_fmt = ""

todo_include_todos = True
html_favicon = "images/favicon.ico"

html_use_index = True
html_domain_indices = True

extlinks = {
    "duref": (
        "http://docutils.sourceforge.net/docs/ref/rst/" "restructuredtext.html#%s",
        "",
    ),
    "durole": ("http://docutils.sourceforge.net/docs/ref/rst/" "roles.html#%s", ""),
    "dudir": ("http://docutils.sourceforge.net/docs/ref/rst/" "directives.html#%s", ""),
}


# Enable eval_rst in markdown
def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {"enable_math": True, "enable_inline_math": True, "enable_eval_rst": True},
        True,
    )
    app.add_transform(AutoStructify)
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )

#linkcheck_ignore = [
#    r'https://github.com/flux-framework/flux-core\?tab\=readme-ov-file\#build-requirements'
#]

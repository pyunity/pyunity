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
sys.path.insert(0, os.path.abspath("../.."))

import math

def atan(*args):
    if len(args) == 2:
        return math.atan2(*args)
    else:
        return math._atan(*args)

math._atan = math.atan
math.atan = atan
sys.modules["glm"] = math
os.environ["PYUNITY_TESTING"] = "1"
import pyunity
pyunity.ABCMeta._trigger = False


# -- Project information -----------------------------------------------------

project = "PyUnity"
copyright = "2020-2021, The PyUnity Team"
author = "Ray Chen"

# The full version, including alpha/beta/rc tags
release = "0.8.4"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx"
]

master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["api/pyunity.rst"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    "logo": "banner.png",
    "touch_icon": "icon.png",
    "github_user": "pyunity",
    "github_repo": "pyunity",
    "badge_branch": "develop",
    "github_button": "true",
    "github_type": "star",
    "github_count": "true",
    "code_font_family": "'Cascadia Code', 'Consolas', 'Menlo', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', monospace",
    "show_relbars": "true",
    "analytics_id": os.getenv("ANALYTICS_ID"),
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]

autodoc_mock_imports = ["glfw", "OpenGL", "glm", "PIL.Image", "sdl2", "sdl2.sdlmixer", "sdl2.ext", "sdl2.video"]

viewcode_enable_epub = True
pygments_style = "friendly"

autodoc_default_options = {
    "ignore-module-all": True,
}

autodoc_class_signature = "separated"
autodoc_member_order = "bysource"

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

import inspect
import enum

def skip_non_undoc(app, what, name, obj, skip, options):
    if "undoc-members" not in options or skip:
        return skip
    if name == "__init__":
        return True
    if (inspect.isfunction(obj) or inspect.ismethod(obj) or \
            isinstance(obj, (staticmethod, classmethod, property, enum.Enum))):
        return None
    if what == "class":
        return True
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_non_undoc)

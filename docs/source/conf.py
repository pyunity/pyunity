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
import textwrap

sys.path.insert(0, os.path.abspath("../.."))

os.environ["PYUNITY_TESTING"] = "1"
os.environ["PYUNITY_INTERACTIVE"] = "0"
os.environ["PYUNITY_SPHINX_CHECK"] = "1"
import pyunity

pyunity.ABCMeta._trigger = False # to import templateWindow and glutWindow


# -- Project information -----------------------------------------------------

project = "PyUnity"
copyright = " 2020-2023 The PyUnity Team"
author = "The PyUnity Team"

# The full version, including alpha/beta/rc tags
release = pyunity.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx_toolbox.more_autodoc",
    "sphinx_toolbox.latex.toc",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

if os.getenv("READTHEDOCS_PROJECT") == "pyunity":
    extensions.append("hoverxref.extension")

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
    "fixed_sidebar": "true",
    "sidebar_width": "250px",
    "page_width": "90%"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]

github_username = "pyunity"
github_repository = "pyunity"
autodoc_show_sourcelink = True

autodoc_mock_imports = ["glfw", "OpenGL", "glm", "PIL.Image", "sdl2", "sdl2.sdlmixer", "sdl2.ext", "sdl2.video"]

viewcode_enable_epub = True
pygments_style = "friendly"

autodoc_default_options = {
    "ignore-module-all": True,
}

autodoc_class_signature = "separated"
autodoc_member_order = "bysource"

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

latex_documents = [
    ("latexindex", "pyunity.tex", "PyUnity", "The PyUnity Team", "manual")
]

hoverxref_intersphinx = ["python"]
hoverxref_default_type = "tooltip"
hoverxref_auto_ref = True
hoverxref_domains = [
    "py"
]
hoverxref_role_types = {
    "class": "tooltip",
    "exc": "tooltip",
    "meth": "tooltip",
    "func": "tooltip",
    "attr": "tooltip",
}

if pyunity.__version__ == "0.9.0":
    rst_prolog = textwrap.dedent("""
    .. attention::
       You are viewing PyUnity docs under the ``develop`` branch.
       As such, they are only applicable if you installed from source.
       Go to https://docs.pyunity.x10.bz/en/latest/ for the most recent
       release.
    """)

def skip_member(app, what, name, obj, skip, options):
    if name.startswith("__"):
        return True
    if isinstance(obj, pyunity.SavedAttribute):
        return True
    if name in ["saved", "shown"] and isinstance(obj, dict):
        for val in obj.values():
            if not isinstance(val, pyunity.SavedAttribute):
                break
        else:
            return True

def process_docstring(app, what, name, obj, options, lines):
    if what == "class" and issubclass(obj, pyunity.Component):
        indexes = []
        for i, line in enumerate(lines):
            if line.startswith(".. attribute:: "):
                indexes.append(i)

        for index in reversed(indexes):
            name = lines[index].split("::", 1)[1][1:]
            if name in obj._saved:
                val = str(obj._saved[name].default)
                lines.insert(index + 1, "   :value: " + val)

def setup(app):
    app.connect("autodoc-skip-member", skip_member)
    app.connect("autodoc-process-docstring", process_docstring)

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
import importlib.util

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../.."))
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------
spec = importlib.util.spec_from_file_location(
    "__version__", "../../church_of_jesus_christ_api/__version__.py"
)
version_module = importlib.util.module_from_spec(spec)
sys.modules["__version__"] = version_module
spec.loader.exec_module(version_module)

project = "Church of Jesus Christ API"
copyright = "2022, Michael Mackliet"
author = "Michael Mackliet"

# The full version, including alpha/beta/rc tags
release = version_module.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "recommonmark",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

from recommonmark.transform import AutoStructify


def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            "auto_toc_tree_section": "Contents",
        },
        True,
    )
    app.add_transform(AutoStructify)


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["setup", "JSON_schemas"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

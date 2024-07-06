# Configuration file for the Sphinx documentation builder.

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html






# -- Path setup --------------------------------------------------------------

import os
import sys
import yaml



# Check to see whether czekitout can be imported.
try:
    import czekitout
except:
    print("ERROR: can't import czekitout.")
    sys.exit(1)






# -- Project information -----------------------------------------------------

project = "czekitout"
copyright = "2024, Matthew Fitzpatrick"
author = "Matthew Fitzpatrick"






# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.extlinks",
              "sphinx.ext.intersphinx",
              "sphinx.ext.todo",
              "sphinx.ext.coverage",
              "sphinx.ext.mathjax",
              "sphinx.ext.viewcode",
              "sphinx_autodoc_typehints",
              "sphinx.ext.githubpages",
              "numpydoc"]



# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]



# Avoid a bunch of warnings when using properties with doc strings in classes.
# see https://github.com/phn/pytpm/issues/3#issuecomment-12133978
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = True
numpydoc_class_members_toctree = False



autosummary_generate = True
autoclass_content = "both"
html_show_sourcelink = False
autodoc_inherit_docstrings = True
set_type_checking_flag = True
add_module_names = False



# For equation numbering by section.
numfig = True
math_numfig = True
numfig_secnum_depth = 6



# Cross links to other sphinx documentations.
intersphinx_mapping = {"python": ("https://docs.python.org/3", None),
                       "numpy": ("https://docs.scipy.org/doc/numpy", None)}



# extlinks
extlinks = {}



# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {"display_version": False}



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]



# If not "", a "Last updated on:" timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"



# Adapted from
# ``https://github.com/ThoSe1990/SphinxExample/blob/main/docs/conf.py``.
build_all_docs = os.environ.get("build_all_docs")
pages_root = os.environ.get("pages_root", "")

if build_all_docs is not None:
    current_language = os.environ.get("current_language")
    current_version = os.environ.get("current_version")

    html_context = {"current_language" : current_language,
                    "languages" : [],
                    "current_version" : current_version,
                    "versions" : []}

    if (current_version == "latest"):
        html_context["languages"].append(["en", pages_root])

    if (current_language == "en"):
        html_context["versions"].append(["latest", pages_root])

    with open("versions.yaml", "r") as yaml_file:
        docs = yaml.safe_load(yaml_file)

    if (current_version != "latest"):
        for language in docs[current_version].get("languages", []):
            path = pages_root+"/"+current_version+"/"+language
            html_context["languages"].append([language, path])

    for version, details in docs.items():
        path = pages_root+"/"+version+"/"+current_language
        html_context["versions"].append([version, path])

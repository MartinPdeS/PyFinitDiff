# -*- coding: utf-8 -*-
#
import os
import sys
from pathlib import Path
from sphinx_gallery.sorting import FileNameSortKey

ProjectPath = Path(os.getcwd()).parent.parent
sys.path.insert(0, ProjectPath)
sys.path.insert(0, os.path.join(ProjectPath, "PyFinitDiff"))


DocPath = os.path.join(ProjectPath, "docs")
html_logo = os.path.join(DocPath, "images/logo.png")
CSS_path = os.path.join(DocPath, "_static/default.css")


def setup(app):
    app.add_css_file(CSS_path)


autodoc_mock_imports = ['numpy',
                        'typing',
                        'matplotlib',
                        'MPSPlots',
                        'scipy']

project = 'PyFinitDiff'
copyright = '2021, Martin Poinsinet de Sivry-Houle'
author = 'Martin Poinsinet de Sivry-Houle'
today_fmt = '%B %d, %Y'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, '../../VERSION'), "r+") as f:
    version = release = f.read()


extensions = [
    'sphinx.ext.mathjax',
    'numpydoc',
    'sphinx_gallery.gen_gallery',
]


prefix = "../../PyFinitDiff/src/Examples/"
sphinx_gallery_conf = {
    'examples_dirs': [],
    'gallery_dirs': [],
    'image_scrapers': ('matplotlib'),
    'ignore_pattern': '/__',
    'plot_gallery': True,
    'thumbnail_size': [600, 600],
    'download_all_examples': False,
    'line_numbers': True,
    'remove_config_comments': True,
    'default_thumb_file': os.path.abspath(html_logo),
    'notebook_images': html_logo,
    'within_subsection_order': FileNameSortKey,
    'capture_repr': ('_repr_html_', '__repr__'),
    'nested_sections': True,
}


autodoc_default_options = {
    'members': False,
    'members-order': 'bysource',
    'undoc-members': False,
    'show-inheritance': True,
}

numpydoc_show_class_members = False

source_suffix = '.rst'

master_doc = 'index'

language = 'en'

exclude_patterns = []

pygments_style = 'monokai'

highlight_language = 'python3'

html_theme = 'sphinxdoc'

html_theme_options = {"sidebarwidth": 400}


html_static_path = ['_static']
templates_path = ['_templates']
html_css_files = ['default.css']

htmlhelp_basename = 'PyFinitDiffdoc'

latex_elements = {}


latex_documents = [
    (master_doc, 'PyFinitDiff.tex', 'PyFinitDiff Documentation',
     'Martin Poinsinet de Sivry-Houle', 'manual'),
]

man_pages = [
    (master_doc, 'pymiesim', 'PyFinitDiff Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'PyFinitDiff', 'PyFinitDiff Documentation',
     author, 'PyFinitDiff', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project

epub_exclude_files = ['search.html']

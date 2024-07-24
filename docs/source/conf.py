#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sphinx_gallery.sorting import FileNameSortKey
from sphinx_gallery.sorting import ExplicitOrder
from MPSPlots.styles import use_mpsplots_style
import PyFinitDiff

from PyFinitDiff.tools.directories import project_path, doc_css_path


sys.path.insert(0, project_path)
sys.path.insert(0, project_path.joinpath('PyFinitDiff'))


def setup(app):
    app.add_css_file(str(doc_css_path))


autodoc_mock_imports = [
    'numpy',
    'matplotlib',
    'scipy'
    'numpydoc',
    'MPSPlots',
]


project = 'PyFinitDiff'
copyright = '2023, Martin Poinsinet de Sivry-Houle'
author = 'Martin Poinsinet de Sivry-Houle'


version = PyFinitDiff.__version__


extensions = [
    'sphinx.ext.mathjax',
    'numpydoc',
    'sphinx_gallery.gen_gallery',
]


def reset_mpl(gallery_conf, fname):
    use_mpsplots_style()


subsection_order = ExplicitOrder(
    [
        "../examples/triplets",
        "../examples/eigenmodes_1d",
        "../examples/eigenmodes_2d",
        "../examples/extras",
    ]
)

sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'gallery_dirs': 'gallery',
    'subsection_order': subsection_order,
    'image_scrapers': ('matplotlib'),
    'ignore_pattern': '/__',
    'plot_gallery': True,
    'thumbnail_size': [600, 600],
    'download_all_examples': False,
    'reset_modules': reset_mpl,
    'line_numbers': False,
    'remove_config_comments': True,
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

highlight_language = 'python3'

html_theme = "pydata_sphinx_theme"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

exclude_trees = []
default_role = "autolink"
pygments_style = "sphinx"

# -- Sphinx-gallery configuration --------------------------------------------

major, minor = version[:2]
binder_branch = f"v{major}.{minor}.x"

html_theme_options = {
    # Navigation bar
    "logo": {
        "alt_text": "PyFinitDiff's logo",
        "text": "PyFinitDiff",
        "link": "https://pyfinitdiff.readthedocs.io/en/master/",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MartinPdeS/PyFinitDiff",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/fiberfusing/",
            "icon": "fa-solid fa-box",
        },
    ],
    "navbar_align": "left",
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "show_prev_next": False,
    "show_version_warning_banner": True,
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    # Other
    "pygment_light_style": "default",
    "pygment_dark_style": "github-dark",
}

htmlhelp_basename = 'PyFinitDiffdoc'

latex_elements = {}


latex_documents = [
    (master_doc, 'PyFinitDiff.tex', 'PyFinitDiff Documentation',
     'Martin Poinsinet de Sivry-Houle', 'manual'),
]

man_pages = [
    (master_doc, 'supymode', 'PyFinitDiff Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'PyFinitDiff', 'PyFinitDiff Documentation',
     author, 'PyFinitDiff', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project

html_static_path = ['_static']
templates_path = ['_templates']
html_css_files = ['default.css']
epub_exclude_files = ['search.html']

# -

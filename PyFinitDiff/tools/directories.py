#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import PyFinitDiff


__all__ = [
    'root_path',
    'project_path',
    'static_doc_path',
    'examples_path',
    'version_path',
    'doc_path',
    'logo_path',
    'doc_css_path',
]

root_path = Path(PyFinitDiff.__path__[0])

project_path = root_path.parents[0]

static_doc_path = project_path.joinpath('docs/images')

examples_path = root_path.joinpath('examples')

version_path = root_path.joinpath('VERSION')

doc_path = project_path.joinpath('docs')

logo_path = doc_path.joinpath('images/logo.png')

doc_css_path = doc_path.joinpath('source/_static/default.css')

rtd_example = 'https://pyfinitdiff.readthedocs.io/en/latest/Examples.html'


if __name__ == '__main__':
    for path_name in __all__:
        path = locals()[path_name]
        print(path)
        assert path.exists(), f"Path {path_name} do not exists"

# -

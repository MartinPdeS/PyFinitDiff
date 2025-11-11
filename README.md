# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                     |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|--------------------------------------------------------- | -------: | -------: | -------: | -------: | ---------: | --------: |
| PyFinitDiff/boundary\_values.py                          |       12 |        4 |        4 |        0 |     50.00% |     36-39 |
| PyFinitDiff/diagonal.py                                  |       95 |       23 |        4 |        0 |     76.77% |83-86, 92, 168-169, 180-183, 221, 249-250, 320-322, 333-335, 351-352, 358 |
| PyFinitDiff/finite\_difference\_1D/boundaries.py         |       64 |        8 |       28 |        5 |     83.70% |62-63, 97-98, 137-138, 149, 206->209, 213 |
| PyFinitDiff/finite\_difference\_1D/finite\_difference.py |       58 |        5 |        6 |        0 |     89.06% |83, 96-98, 122 |
| PyFinitDiff/finite\_difference\_1D/utils.py              |       15 |        5 |        0 |        0 |     66.67% |     67-72 |
| PyFinitDiff/finite\_difference\_2D/boundaries.py         |       82 |       15 |       40 |        3 |     75.41% |59-60, 91->96, 140-141, 152, 204->exit, 219-224, 235-240 |
| PyFinitDiff/finite\_difference\_2D/derivative.py         |        8 |        5 |        0 |        0 |     37.50% |     50-68 |
| PyFinitDiff/finite\_difference\_2D/finite\_difference.py |       66 |        1 |       10 |        3 |     94.74% |98, 111->113, 243->250, 250->exit |
| PyFinitDiff/triplet.py                                   |      134 |       30 |       16 |        2 |     74.67% |39, 42, 102, 114, 130-131, 147-148, 164-165, 181-182, 193, 204, 287-288, 304-305, 316, 334-335, 341-347, 455-456 |
|                                                **TOTAL** |  **568** |   **96** |  **110** |   **13** | **80.09%** |           |

5 files skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/MartinPdeS/PyFinitDiff/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MartinPdeS/PyFinitDiff/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FMartinPdeS%2FPyFinitDiff%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.
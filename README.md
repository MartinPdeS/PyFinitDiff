# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                     |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyFinitDiff/boundary\_values.py                          |       12 |        4 |        4 |        0 |     50% |     36-39 |
| PyFinitDiff/coefficients/backward.py                     |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/coefficients/central.py                      |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/coefficients/forward.py                      |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/diagonal.py                                  |      100 |       23 |        4 |        0 |     78% |84-87, 93, 169-170, 181-184, 222, 250-251, 321-323, 334-336, 352-353, 359 |
| PyFinitDiff/finite\_difference\_1D/boundaries.py         |       64 |        8 |       28 |        5 |     84% |62-63, 97-98, 137-138, 149, 206->209, 213 |
| PyFinitDiff/finite\_difference\_1D/derivative.py         |        9 |        0 |        2 |        0 |    100% |           |
| PyFinitDiff/finite\_difference\_1D/finite\_difference.py |       59 |        5 |        6 |        0 |     89% |83, 96-98, 122 |
| PyFinitDiff/finite\_difference\_1D/utils.py              |       16 |        5 |        0 |        0 |     69% |     67-72 |
| PyFinitDiff/finite\_difference\_2D/boundaries.py         |       82 |       15 |       40 |        3 |     75% |60-61, 92->97, 141-142, 153, 205->exit, 220-225, 236-241 |
| PyFinitDiff/finite\_difference\_2D/derivative.py         |        8 |        5 |        0 |        0 |     38% |     50-68 |
| PyFinitDiff/finite\_difference\_2D/finite\_difference.py |       68 |        1 |       10 |        3 |     95% |98, 111->113, 243->250, 250->exit |
| PyFinitDiff/finite\_difference\_2D/utils.py              |       18 |        5 |        0 |        0 |     72% |     79-88 |
| PyFinitDiff/triplet.py                                   |      136 |       30 |       16 |        2 |     75% |39, 42, 102, 114, 130-131, 147-148, 164-165, 181-182, 193, 204, 287-288, 304-305, 316, 334-335, 341-347, 455-456 |
| PyFinitDiff/utils.py                                     |       32 |       19 |       10 |        0 |     31% |10-29, 98-104 |
|                                                **TOTAL** |  **613** |  **120** |  **120** |   **13** | **77%** |           |


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
# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                     |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyFinitDiff/coefficients/backward.py                     |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/coefficients/central.py                      |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/coefficients/forward.py                      |        3 |        0 |        0 |        0 |    100% |           |
| PyFinitDiff/finite\_difference\_1D/boundaries.py         |       70 |       11 |       34 |        6 |     80% |46, 49-52, 79-80, 114-115, 138, 181->184, 188 |
| PyFinitDiff/finite\_difference\_1D/derivative.py         |        9 |        0 |        2 |        0 |    100% |           |
| PyFinitDiff/finite\_difference\_1D/diagonals.py          |       95 |       17 |       10 |        1 |     83% |31->30, 91-97, 104, 127-129, 138-143, 174, 191-193, 243-245, 248 |
| PyFinitDiff/finite\_difference\_1D/finite\_difference.py |       65 |        5 |       16 |        4 |     86% |56->55, 57, 60->59, 66-68, 71->70, 75->74, 76 |
| PyFinitDiff/finite\_difference\_1D/utils.py              |       16 |        5 |        2 |        0 |     72% |     48-54 |
| PyFinitDiff/finite\_difference\_2D/boundaries.py         |       88 |       15 |       46 |        3 |     78% |45-46, 72->77, 116-117, 140, 182->exit, 194-199, 207-212 |
| PyFinitDiff/finite\_difference\_2D/dense.py              |      159 |      159 |       94 |        0 |      0% |     1-237 |
| PyFinitDiff/finite\_difference\_2D/derivative.py         |        8 |        5 |        0 |        0 |     38% |     35-53 |
| PyFinitDiff/finite\_difference\_2D/diagonals.py          |      106 |       23 |       10 |        1 |     79% |45->44, 93-97, 104, 153-154, 163-166, 198, 220-221, 279-281, 290-292, 304-305, 314 |
| PyFinitDiff/finite\_difference\_2D/finite\_difference.py |       68 |        1 |       20 |        7 |     91% |70->69, 72, 75->74, 83->85, 88->87, 93->92, 191->198, 198->exit |
| PyFinitDiff/finite\_difference\_2D/utils.py              |       18 |        5 |        2 |        0 |     75% |     56-65 |
| PyFinitDiff/triplet.py                                   |      135 |       30 |       42 |       13 |     71% |26, 29, 32->31, 37->36, 42->41, 47->46, 52->51, 54, 57->56, 59, 63-64, 68-69, 73-74, 78-79, 83, 87, 125-126, 130-131, 135, 139-140, 144-150, 159->158, 164->163, 169->168, 174->173, 179->178, 190-191 |
| PyFinitDiff/utils.py                                     |       32 |       19 |       10 |        0 |     31% |10-29, 98-104 |
|                                                **TOTAL** |  **878** |  **295** |  **288** |   **35** | **61%** |           |


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
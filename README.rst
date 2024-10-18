PyFinitDiff
===========

|logo|

.. list-table::
   :widths: 10 25 25
   :header-rows: 0

   * - Meta
     - |python|
     - |docs|
   * - Testing
     - |ci/cd|
     - |coverage|
   * - PyPi
     - |PyPi|
     - |PyPi_download|
   * - Anaconda
     - |anaconda|
     - |anaconda_download|

PyFinitDiff is a robust Python package designed to compute finite-difference matrices with an intuitive API. This package provides an efficient and user-friendly interface for generating finite-difference approximations, making it ideal for numerical analysis and scientific computing.


Features
********
- **Intuitive API**: PyFinitDiff offers an easy-to-use interface that allows users to generate finite-difference matrices with minimal effort.
- **Versatile Applications**: Suitable for a wide range of numerical methods including solving partial differential equations (PDEs), performing numerical differentiation, and more.
- **Comprehensive Documentation**: Detailed documentation and examples to help users get started quickly.

Installation
------------

PyFinitDiff requires Python 3.10+ and is available on PyPi for various operating systems including Linux and macOS.

Install PyFinitDiff via pip:

.. code-block:: bash

   pip install PyFinitDiff

Documentation
*************
Comprehensive and up-to-date documentation is available online. You can access it `here <https://pyfinitdiff.readthedocs.io/en/latest/>`_ or by clicking the badge below:

|docs|

Usage Example
*************

Below is a simple example to illustrate how to use PyFinitDiff:

.. code-block:: python

   from PyFinitDiff.finite_difference_1D import FiniteDifference
   from PyFinitDiff.finite_difference_1D import Boundaries

   boundaries = Boundaries(left='none', right='none')

   n_x = 100
   fd = FiniteDifference(
      n_x=n_x,
      dx=1,
      derivative=2,
      accuracy=2,
      boundaries=boundaries
   )

   fd.triplet.plot()

   dense_matrix = fd.triplet.to_scipy_sparse()

   sparse_matrix = fd.triplet.to_scipy_sparse()

This would produce the following figure:

|example_triplet_0|

This example demonstrates the creation of a second-order finite-difference matrix with a specified grid spacing and size.

Testing
*******

To test PyFinitDiff locally, clone the GitHub repository and run the tests with coverage:

.. code-block:: bash

   git clone https://github.com/MartinPdeS/PyFinitDiff.git
   cd PyFinitDiff
   pip install PyFinitDiff[testing]
   pytest

Contributing
************

As PyFinitDiff is under continuous development, contributions are welcome! If you would like to collaborate or suggest improvements, feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss your ideas.

Contact Information
********************
As of 2024, the project is still under development. If you want to collaborate, it would be a pleasure! I encourage you to contact me.

PyFinitDiff was written by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_  .

Email:`martin.poinsinet.de.sivry@gmail.ca <mailto:martin.poinsinet.de.sivry@gmail.ca?subject=PyFinitDiff>`_ .


.. |python| image:: https://img.shields.io/pypi/pyversions/pyfinitdiff.svg
   :alt: Python
   :target: https://www.python.org/

.. |logo| image:: https://github.com/MartinPdeS/PyFinitDiff/raw/master/docs/images/logo.png
   :alt: PyFinitDiff logo

.. |docs| image:: https://github.com/martinpdes/pyfinitdiff/actions/workflows/deploy_documentation.yml/badge.svg
   :target: https://martinpdes.github.io/PyFinitDiff/
   :alt: Documentation Status

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/PyFinitDiff/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyFinitDiff/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |PyPi| image:: https://badge.fury.io/py/PyFinitDiff.svg
   :alt: PyPi version
   :target: https://pypi.org/project/PyFinitDiff/

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyfinitdiff.svg
   :alt: PyPi version
   :target: https://pypistats.org/packages/pyfinitdiff

.. |ci/cd| image:: https://github.com/martinpdes/pyfinitdiff/actions/workflows/deploy_coverage.yml/badge.svg
   :target: https://martinpdes.github.io/PyFinitDiff/actions
   :alt: Unittest Status

.. |example_triplet_0| image:: https://github.com/MartinPdeS/PyFinitDiff/blob/master/docs/images/triplet_example_0.png
    :target: https://www.python.org/

.. |anaconda_download| image:: https://anaconda.org/martinpdes/pyfinitdiff/badges/downloads.svg
   :alt: Anaconda downloads
   :target: https://anaconda.org/martinpdes/pyfinitdiff


.. |anaconda| image:: https://anaconda.org/martinpdes/pyfinitdiff/badges/version.svg
   :alt: Anaconda version
   :target: https://anaconda.org/martinpdes/pyfinitdiff

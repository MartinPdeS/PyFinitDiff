PyFinitDiff
===========

|python|
|docs|
|unittest|
|PyPi|
|PyPi_download|

A Python package to compute finit-difference matrices with an intuitive API.


----

Documentation
**************
All the latest available documentation is available `here <https://pyfinitdiff.readthedocs.io/en/latest/>`_ or you can click the following badge:

|docs|


----

Installation
------------


Pip installation
****************

The package have been uploaded as wheel for a few OS (Linux, MacOS) and need Python 3.10+ version.
As such, with the adequate configuration one can simply do

.. code-block:: python

   >>> pip3 install PyFinitDiff


----

Testing
*******

To test localy (with cloning the GitHub repository) you'll need to install the dependencies and run the coverage command as

.. code:: python

   >>> git clone https://github.com/MartinPdeS/PyFinitDiff.git
   >>> cd PyFinitDiff
   >>> pip install -r requirements/requirements.txt
   >>> coverage run --source=PyFinitDiff --module pytest --verbose tests
   >>> coverage report --show-missing

----


Contact Information
*******************

As of 2021 the project is still under development if you want to collaborate it would be a pleasure. I encourage you to contact me.

PyFinitDiff was written by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_  .

Email:`martin.poinsinet-de-sivry@polymtl.ca <mailto:martin.poinsinet-de-sivry@polymtl.ca?subject=PyFinitDiff>`_ .


.. |python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/

.. |docs| image:: https://readthedocs.org/projects/pyfinitdiff/badge/?version=latest
   :target: https://pyfinitdiff.readthedocs.io/en/latest/
   :alt: Documentation Status

.. |unittest| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MartinPdeS/19aef38017fa4be1dc71b6f5d853a932/raw

.. |PyPi| image:: https://badge.fury.io/py/PyFinitDiff.svg
   :target: https://pypi.org/project/PyFinitDiff/

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyfinitdiff.svg
   :target: https://pypistats.org/packages/pyfinitdiff





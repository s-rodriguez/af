.. af documentation master file, created by
   sphinx-quickstart on Wed Apr 20 20:39:33 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Anonymization Framework (af) Documentation
******************************************

The **af** is a Python library developed with the goal to provide an open source tool for data anonymization.

It was built with an extensibility design in mind, so anyone can adapt it according to his needs and to the context where it is going to be used:

 * Base DB controller generic class, so to achieve the extension for different new types of DB's. (Currently supporting sqlite)
 * Base Algorithm generic class, so to be able to implement new anonymization algorithms for existing or new privacy models. (3 algorithms provided with the library: Datafly, Incognito-K and Incognito-L)
 * Hierarchy class built with the idea of being able to generalize/supress any type of attribute (string, int, etc...).

Download Source
===============
You can download **af** from the github repository: https://github.com/s-rodriguez/af

Installation
============
The installation process is pretty forward.
.. code-block:: python
   :linenos:

   sudo apt-get install wkhtmltopdf  # Need it to export reports in pdf
   mkvirtualenv <venv_name> --system-site-packages  # Creation of virtualenv with system site packages to use the wkhtmltopdf
   pip install -r requirements.txt
   python setup.py install  # Use <develop> key if intended to implement changes in code


Contents
========
.. toctree::
   :maxdepth: 2

   af.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


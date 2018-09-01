jreg
====

Python package for using Java regexes

Requirements
------------

1. Java 9 (unless you are using a `custom Java regex class <#using-a-custom-java-class>`_)
2. Python 3.6

::

    pip3 install jreg

Input must be raw strings.

Usage
-----

.. code-block:: python

    import jreg
    jre = jreg.JavaRegex()
    print(jre.match('[01]?\d-([0123]?\d)-\d{4}+', '01-24-2013'))

Using a Custom Java Class
-------------------------

This package comes with a built-in Java class for matching a regex. If you would like to use a custom Java class, you can specify a ``custom_regex_checker_class_path`` argument when initializing the ``JavaRegex`` class. For example:

.. code-block:: python

    import jreg
    jre = jreg.JavaRegex(custom_regex_checker_class_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "./RegexTester.class")))
    print(jre.match('[01]?\d-([0123]?\d)-\d{4}+', '01-24-2013'))

You can see an example usage of this in the `tests/test_jreg.py <https://github.com/fhightower/jreg/tree/master/tests/test_jreg.py>`_ file.

Luna
=====

[![Build Status](https://travis-ci.org/fhahn/luna.png?branch=master)](https://travis-ci.org/fhahn/luna)
[![Coverage Status](https://coveralls.io/repos/fhahn/luna/badge.png)](https://coveralls.io/r/fhahn/luna)


Luna is a bytecode register interpreter for Lua. At the moment it uses Luajit to compile Lua files to bytecode
and interprets it.


You'll need to have a few dependencies installed. You can get them with ``pip
install -r requirements.txt``. Finally make sure you have a recent checkout of
[PyPy][] and have it on your ``PYTHONPATH``.

To run the tests::

    $ py.test

To translate run::

    $ python translate.py

This will compile Luna, it'll take about 30 seconds.

To run Luna directly on top of Python you can do::

    $ python -m luna /path/to/file.lua
    

[PyPy]: https://bitbucket.org/pypy/pypy


TODO
-----------

* Compiler in Rpython
* Interators
* JIT
* more standard library functions 


Features
---------

At the moment, Luna supports most of the Lua standard constructs, except iterators.

Following parts of the standard library (the code can be found in [luna/modules][]) have been implemented:

[luna/modules]: https://github.com/fhahn/luna/tree/master/luna/modules


* Builtins
 * assert
 * print
 * loadfile
 * loadstring
 * tonumber
 * type
* math
 * floor
 * sin
 * mod
* table
 * concat
 * insert
 * remove
* string
 * find
 * match
 * gsub

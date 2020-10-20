.. nlpir documentation master file, created by
   sphinx-quickstart on Tue Oct 20 10:30:07 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nlpir's documentation!
=================================

nlpir-python 是一个 `NLPIR <https://github.com/NLPIR-team/NLPIR>`_ 的python调用包

nlpir-python is a python wrapper for NLPIR modules.

本模块提供两种调用方式:

This package include two level of method:


1. Native call from Dynamic Link Library(DLL) 原生的直接调用DLL的调用方式


These methods are native method directory from DLL, you can easily use them
if you are familiar with the NLPIR modules.

原生方法是直接调用的NLPIR中的api,并进行了部分简化处理,和python化.



2. High-level pythonic method 整合后的更加Python的调用方式

However, the native methods are not very friendly to the beginners.
These methods provide a wrapper and tools for the native call, make it
easier to use.

然而,对于一般用户来说,原生api功能强大但是却不是很友好.这里nlpir-python对原生api就行包装,
并提供了一些工具方法,使其更利于使用.


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   installation
   tutorial
   nlpir


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

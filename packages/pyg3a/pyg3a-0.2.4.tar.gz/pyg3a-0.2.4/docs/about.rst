About
=====

.. toctree::

How pyg3a works
---------------

1.  Project is Created:

    PyG3A will create a 'project' in the directory '``.pyg3a_build/<file>/``'.

    It then creates a Makefile to build the project later.

    This should only happen once.

2.  Python is Parsed:

    PyG3A uses the *libcst* module to parse the input python file.

3.  Imports are Checked:

    It iterates over the imports in the file, and checks the '``<install location>/packages``' and '``~/.local/lib/pyg3a/``' directory for .py files matching this name.

    The functions in this file are added to a list for future use.

4.  Code is Transpiled:

    PyG3A internally puts your whole Python file into the ``main()`` function, then transpiles to C++, placing function definitions outside the ``main()`` function (as C++ does not support nested functions).

    This takes into account the packages imported in your program for function overloads.

5.  C++ is Compiled:

    The C++ is compiled and linked using GNU Make.

    Execution starts from your Python file's ``main()`` function (if defined), or from your first statement.

    Any G++ output will be shown in the python output as a means of debugging.

    Using '``--verbose``' will print the commands that are being run through make.

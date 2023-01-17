Quickstart
==========

Minimal Example with C++ Libraries From Conan
---------------------------------------------

pyproject.toml
______________
.. code-block:: toml

    [build-system]
    requires = [
        "setuptools>=61.0",
        'wheel',
        'uiucprescon.build @ git+https://github.com/UIUCLibrary/uiucprescon_build.git@v0.1.0'
    ]
    build-backend = "uiucprescon.build"


conanfile.py
____________

.. code-block:: python

    from conan import ConanFile


    class TesseractBindConan(ConanFile):
        requires = ["tesseract/4.1.1",]
        settings = "os", "arch", "compiler", "build_type"

        generators = ["json", "cmake_paths"]
        default_options = {}


setup.py
________

.. code-block:: python

    try:
        from pybind11.setup_helpers import Pybind11Extension
    except ImportError:
        from setuptools import Extension as Pybind11Extension

    cmd_class = {}
    try:
        from uiucprescon.build import conan_libs
        cmd_class["build_conan"] = conan_libs.BuildConan
    except ImportError:
        pass

    tesseract_extension = Pybind11Extension(
        "spam.tesseractwrapper",
        sources=['spam/tesseractwrap.cpp'],
        libraries=["tesseract",],
        language='c++',
        cxx_std=14

    )

    setup(
        packages=["spam"],
        ext_modules=[tesseract_extension],
        cmdclass=cmd_class
    )

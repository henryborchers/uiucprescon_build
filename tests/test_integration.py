import os

from uiucprescon import build


def test_conan_integration(tmp_path, monkeypatch):
    source_root = tmp_path / "package"
    source_root.mkdir()
    setup_py = source_root / 'setup.py'
    setup_py.write_text("""
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension
from uiucprescon.build.pybind11_builder import BuildPybind11Extension

setup(
    name='dummy',
    version='1.0',
    ext_modules=[
        Pybind11Extension(
            "dummy.myextension",
            sources=[
                "myextension.cpp",
            ],
            language="c++",
        )
    ],
    cmdclass={
        "build_ext": BuildPybind11Extension
    },
    )    
    """)

    pyproject = source_root / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "dummy"
    """)

    conanfile = source_root / "conanfile.py"
    conanfile.write_text("""
from conans import ConanFile
class Dummy(ConanFile):
    requires = []
    """)
    myextension_cpp = source_root / "myextension.cpp"
    myextension_cpp.write_text("""#include <iostream>
    """)

    output = tmp_path / "output"
    with open(pyproject) as f:
        print(f.read())
    monkeypatch.chdir(source_root)
    build.build_wheel(str(output))
    assert any(f.startswith('dummy') for f in os.listdir(output))

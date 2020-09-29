import setuptools
import sys
import os
import subprocess
import shutil
from distutils.command.build import build as _build
from distutils.command.sdist import sdist as _sdist
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.command.develop import develop as _develop
from distutils.command.clean import clean as _clean
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RADARE2_DIR = Path(ROOT_DIR) / "radare2"
LIBS_DIR = Path(ROOT_DIR) / "r2cmd" / "r2libr"
PACKAGE_DIRS = [
    'r2libr/fs/*',
    'r2libr/anal/*',
    'r2libr/crypto/*',
    'r2libr/io/*',
    'r2libr/core/*',
    'r2libr/asm/*',
    'r2libr/socket/*',
    'r2libr/config/*',
    'r2libr/bp/*',
    'r2libr/debug/*',
    'r2libr/bin/*',
    'r2libr/cons/*',
    'r2libr/reg/*',
    'r2libr/parse/*',
    'r2libr/syscall/*',
    'r2libr/magic/*',
    'r2libr/lang/*',
    'r2libr/egg/*',
    'r2libr/flag/*',
    'r2libr/search/*',
    'r2libr/main/*',
    'r2libr/hash/*',
    'r2libr/util/*',
    'r2libr/anal/d/*',
    'r2libr/asm/d/*',
    'r2libr/bin/d/*',
    'r2libr/cons/d/*',
    'r2libr/syscall/d/*',
    'r2libr/magic/d/*',
    'r2libr/flag/d/*'
]

def clean_builds():
    shutil.rmtree(Path(ROOT_DIR) / "build")
    shutil.rmtree(Path(ROOT_DIR) / "r2cmd" / "r2libr")

def radare2_exists():
    return (Path(ROOT_DIR) / "radare2" / ".git").exists()

def meson_exists():
    try:
        import mesonbuild
        return True
    except ImportError:
        return False

def build_radare2():
    if not radare2_exists():
        raise RuntimeError("Fail to detect radare2 repository. Do you forget to init submodules?")
    if not meson_exists():
        raise RuntimeError("Fail to detect meson. Do you forget to install meson?")
    os.chdir(RADARE2_DIR)

    DEBUG = os.getenv("DEBUG", "")
    BUILDDIR = os.getenv("R2BUILDDIR", "pyr2cmdbuild")
    if sys.platform == "win32":
        BACKEND = os.getenv("BACKEND", "vs2017")
    else:
        BACKEND = os.getenv("BACKEND", "ninja")

    args = ["./sys/meson.py"]
    if not DEBUG:
        args += ["--release"]
    args += ["--local"]
    args += ["--dir", BUILDDIR]
    args += ["--shared"]
    args += ["--backend", BACKEND]

    subprocess.call(args)
    libr_dir = Path(ROOT_DIR) / "radare2" / BUILDDIR / "libr"
    if LIBS_DIR.exists():
        shutil.rmtree(LIBS_DIR)
    shutil.copytree(libr_dir, LIBS_DIR, ignore=shutil.ignore_patterns("*.o"))
    os.chdir(ROOT_DIR) 


class build(_build):
    def run(self):
        build_radare2()
        return _build.run(self)

class clean(_clean):
    def run(self):
        clean_builds()
        return _clean.run(self)

class develop(_develop):
    def run(self):
        build_radare2()
        return _develop.run(self)

class bdist_egg(_bdist_egg):
    def run(self):
        self.run_command('build')
        return _bdist_egg.run(self)

setuptools.setup(
    name="pyr2cmd",
    version="0.0.1",
    author="mio",
    author_email="mio@lazym.io",
    description="pyr2cmd",
    long_description="pyr2cmd",
    url="https://github.com/wtdcode/pyr2cmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    cmdclass={
        "build" : build,
        "develop" : develop,
        "bdist_egg" : bdist_egg,
        "clean" : clean
    },
    python_requires='>=3.6',
    include_package_data=True,
    is_pure=False,
    package_data= {
        "r2cmd" : PACKAGE_DIRS
    }
)


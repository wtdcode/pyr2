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

def detect_python_on_windows():
    try:
        p = subprocess.run('python -c "import sys;print(sys.version_info.major)"', capture_output=True)
        output = p.stdout.decode("utf-8")
        if int(output) == 3:
            return ["python"]
    except FileNotFoundError:
        pass
    try:
        p = subprocess.run('py -3 --version')
        if p.returncode == 0:
            return ["py", "-3"]
    except FileNotFoundError:
        pass
    return None

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
    PREFIX = os.getenv("R2PREFIX", str(Path(ROOT_DIR) / "radare2" / "pyr2installdir"))
    if sys.platform == "win32":
        BACKEND = os.getenv("BACKEND", "vs2017")
    else:
        BACKEND = os.getenv("BACKEND", "ninja")

    args = []
    if sys.platform == "win32":
        py = detect_python_on_windows()
        if py is None:
            raise RuntimeError("Can't find a python in your path!")
        args += py
    args += ["./sys/meson.py"]
    if not DEBUG:
        args += ["--release"]
    args += ["--local"]
    args += ["--dir", BUILDDIR]
    args += ["--shared"]
    args += ["--backend", BACKEND]
    args += ["--prefix", PREFIX]
    args += ["--install"]

    subprocess.call(args)
    if LIBS_DIR.exists():
        shutil.rmtree(LIBS_DIR)
    os.makedirs(LIBS_DIR, exist_ok=True)

    lib_install_dir = Path(PREFIX) / "bin" if sys.platform == "win32" else Path(PREFIX) / "lib"
    glob = {
        "linux" : "*.so",
        "win32" : "*.dll",
        "darwin" : "*.dylib"
    }.get(sys.platform, "*.so")
    for p in lib_install_dir.rglob(glob):
        if p.is_file():
            shutil.copy(p, LIBS_DIR)
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
        "r2cmd" : ['r2libr/*']
    }
)


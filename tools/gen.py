
#!/usr/bin/python3
#
# This tool is intended for development only.

import subprocess
from argparse import ArgumentParser
from pathlib import Path
import sys

libs = [
    "anal",
    "asm",
    "bin",
    "bp",
    "config",
    "cons",
    "core",
    "crypto",
    "debug",
    "egg",
    "flag",
    "fs",
    "hash",
    "io",
    "lang",
    "magic",
    "main",
    "parse",
    "reg",
    "search",
    "socket",
    "syscall",
    "util",
]

parser = ArgumentParser("r2 python bindings generator")
parser.add_argument("-O", "--output", help="output dir", type=str)
parser.add_argument("-H", "--headers", help="r2 headers dir", type=str)
parser.add_argument("-B", "--build", help="meson install dir", type=str)
parser.add_argument("-C", "--clang-args", help="clang args", type=str)
# To avoid potential ambiguity, please use -C="-I/..."
pargs = parser.parse_args()

for lib in libs:
    lib_path = str(Path(pargs.build) / "libr" / lib / f"libr_{lib}.so")
    args = ["clang2py"]
    args += ["-l", lib_path]
    args += ["--clang-args", pargs.clang_args]
    args += [str(Path(pargs.headers) / f"r_{lib}.h")]
    p = subprocess.run(args, capture_output=True)
    binding = p.stdout.decode("utf-8")
    binding = binding.replace(f"_libraries['{lib_path}']", f"_libr_{lib}")
    fpath = Path(pargs.output) / f"r2{lib}.py"
    with open(fpath, "w+") as f:
        f.write(binding)
    subprocess.call(["sed", "-i", rf"/import ctypes/a from .r2libs import r_{lib} as _libr_{lib}", str(fpath)])
    subprocess.call(["sed", "-i", r"/_libraries = {}/,+1d", str(fpath)])
    subprocess.call(["sed", "-i", r"/TARGET arch/d", str(fpath)])

with open(Path(pargs.output) / "__init__.py", "w+") as f:
    for lib in libs:
        f.write(f"from .r2{lib} import *\n")
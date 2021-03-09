
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

def gen_clang_args(builddir):
    def _impl(dir: Path):
        includes.append(dir)
        for child in dir.iterdir():
            if child.is_dir() and child not in includes:
                _impl(child)
    include_root = Path(builddir) / "include" / "libr"
    includes = []
    _impl(include_root)
    return " ".join([f"-I{str(p.resolve())}" for p in includes])

def verbose_call(*args, **kwargs):
    print(" ".join([f'"{a}"' for a in args[0]]))
    return subprocess.run(*args, **kwargs)

def find_lib(builddir, lib_name):
    libr_path = Path(builddir) / "lib"
    for p in libr_path.rglob(f"libr_{lib_name}.so*"):
        if not p.is_symlink():
            return p
    return None

def handle_lib(lib, pargs):
    lib_path = libs_path[lib]
    args = ["clang2py"]
    #args += ['-x']
    args += ["-v"]
    for _, v in libs_path.items():
        args += ["-l", str(v.resolve())]
    args += ["--clang-args", gen_clang_args(pargs.build)]
    args += [str(Path(pargs.build) / "include" / "libr" / f"r_{lib}.h")]
    p = verbose_call(args, stdout=subprocess.PIPE)
    binding = p.stdout.decode("utf-8")
    # Enable this line until ctypeslibs becomes stable enough.
    # binding = binding.replace("_libraries['FIXME_STUB']", f"_libr_stub")
    for _lib in libs:
        binding = binding.replace(f"_libraries['{libs_path[_lib].name}']", f"_libr_{_lib}")
    binding = binding.replace("import ctypes", "import ctypes\n" + "\n".join([f"from .r2libs import r_{_lib} as _libr_{_lib}" for _lib in libs]))
    fpath = Path(pargs.output) / f"r2{lib}.py"
    with open(fpath, "w+") as f:
        f.write(binding)
    # Delete the redundant assignment.
    # verbose_call(["sed", "-i", r"/_libraries = {}/d", str(fpath)])
    verbose_call(["sed", "-i", rf"/ctypes.CDLL.*{libs_path[lib].name}/d", str(fpath)])
    # for _lib in libs:
    #     verbose_call(["sed", "-i", rf"/libr_{_lib}.so/d", str(fpath)])
    # Remove clang2py args in comments.
    verbose_call(["sed", "-i", r"/TARGET arch/d", str(fpath)])
    

parser = ArgumentParser("r2 python bindings generator")
parser.add_argument("-O", "--output", help="output dir", type=str)
#parser.add_argument("-H", "--headers", help="r2 headers dir", type=str)
parser.add_argument("-B", "--build", help="meson install dir", type=str)
parser.add_argument("-L", "--lib", help="r2 lib name", type=str)
#parser.add_argument("-C", "--clang-args", help="clang args", type=str)
pargs = parser.parse_args()

libs_path = {}
for lib in libs:
    libs_path[lib] = find_lib(pargs.build, lib)

if pargs.lib is not None:
    if pargs.lib not in libs:
        print("Valid libs:" + " ".join(libs))
        exit(0)
    handle_lib(pargs.lib, pargs)
else:
    for lib in libs:
        handle_lib(lib, pargs)
    with open(Path(pargs.output) / "__init__.py", "w+") as f:
        for lib in libs:
            f.write(f"from .r2{lib} import *\n")
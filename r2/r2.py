import ctypes
import distutils.sysconfig
import pkg_resources
import sys
import os
from pathlib import Path

_libr_name_dict = { 'darwin': 'libr_core.dylib',
                    'win32': 'r_core.dll',
                    'linux': 'libr_core.so',
                    'linux2': 'libr_core.so' }
try:
    _libr_name = _libr_name_dict[sys.platform]
except KeyError:
    raise ImportError(f"Your platform {sys.platform} is not supported!")

_search_path = [Path(os.path.dirname(os.path.abspath(__file__))) / "libr",
                Path('') / "libr",
                Path("/usr/local/lib/") if sys.platform == 'darwin' else Path('/usr/lib64')]

# Workaround for dll dependencies.
# In Py3.8, we have a better way to do this.
def _load_libr_all(directory: Path):
    if (directory / _libr_name).exists():
        changed = True
        loaded = set()
        while changed:
            changed = False
            for p in directory.iterdir():
                if p in loaded:
                    continue
                if p.is_file() and p.name.endswith("dll"):
                    try:
                        dll = ctypes.cdll.LoadLibrary(str(p))
                        if p.name == _libr_name:
                            return dll
                        if p not in loaded:
                            changed = True
                            loaded.add(p)
                    except OSError:
                        pass
        return None
    else:
        return None

def _load_libr(directory: Path):
    libr_path = directory / _libr_name
    try:
        return ctypes.cdll.LoadLibrary(str(libr_path))
    except OSError:
        return None

for _path in _search_path:
    if sys.platform == "win32":
        _libr = _load_libr_all(_path)
    else:
        _libr = _load_libr(_path)
    if _libr is not None:
        break

if _libr is None:
    raise ImportError("Libr is not found on your system.")

def _setup_prototype(lib, fname, restype, *argtypes):
    getattr(lib, fname).restype = restype
    getattr(lib, fname).argtypes = argtypes

PRCORE = ctypes.POINTER(ctypes.c_uint64)
PFILE = ctypes.POINTER(ctypes.c_uint64)

_setup_prototype(_libr, "r_core_new", PRCORE)
_setup_prototype(_libr, "r_core_init", ctypes.c_bool, PRCORE)
_setup_prototype(_libr, "r_core_free", PRCORE)
_setup_prototype(_libr, "r_core_parse_radare2rc", None, PRCORE)
_setup_prototype(_libr, "r_core_file_open", PFILE, PRCORE, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint64)
_setup_prototype(_libr, "r_core_file_close", ctypes.c_int, PRCORE, PFILE)
_setup_prototype(_libr, "r_core_bin_load", ctypes.c_bool, PRCORE, ctypes.c_char_p, ctypes.c_uint64)
_setup_prototype(_libr, "r_core_bin_rebase", ctypes.c_int, PRCORE, ctypes.c_uint64)
_setup_prototype(_libr, "r_core_cmd0", ctypes.c_int, PRCORE, ctypes.c_char_p)
_setup_prototype(_libr, "r_core_cmd_str", ctypes.c_char_p, PRCORE, ctypes.c_char_p)

class RFile:
    def __init__(self, fh, rc):
        self._fh = fh
        self._rc = rc

    def __del__(self):
        _libr.r_core_file_close(self._rc, self._fh)

class R2:
    def __init__(self):
        self._rcore = _libr.r_core_new()
        self.r_core_parse_radare2rc()

    def __del__(self):
        self.r_core_free()

    def r_core_parse_radare2rc(self):
        return _libr.r_core_parse_radare2rc(self._rcore)

    def r_core_free(self):
        return _libr.r_core_free(self._rcore)

    def r_core_open_file(self, p, perm, mapddr):
        if type(p) is str:
            p = p.encode("utf-8")
        return _libr.r_core_file_open(self._rcore, p, perm, mapddr)

    def r_core_file_close(self, fh):
        return _libr.r_core_file_close(self._rcore, fh)

    def r_core_load_bin(self, p):
        if type(p) is str:
            p = p.encode("utf-8")
        return _libr.r_core_bin_load(self._rcore, p, (1<<64) - 1)

    def r_core_bin_rebase(self, addr):
        return _libr.r_core_bin_rebase(self._rcore, addr)

    def r_core_cmd_str(self, s):
        if type(s) is str:
            s = s.encode("utf-8")
        p = _libr.r_core_cmd_str(self._rcore, s)
        return ctypes.string_at(p)

if __name__ == "__main__":
    r2 = R2()
    fh = r2.r_core_open_file("/bin/ls", 0b101, 0)
    r2.r_core_load_bin("/bin/ls")
    r2.r_core_cmd_str("ieq")
    r2.r_core_cmd_str("aaa")
    print(r2.r_core_cmd_str("pdj"))
    r2.r_core_file_close(fh)
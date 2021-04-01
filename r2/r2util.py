# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_anal as _libr_anal
from .r2libs import r_asm as _libr_asm
from .r2libs import r_bin as _libr_bin
from .r2libs import r_bp as _libr_bp
from .r2libs import r_config as _libr_config
from .r2libs import r_cons as _libr_cons
from .r2libs import r_core as _libr_core
from .r2libs import r_crypto as _libr_crypto
from .r2libs import r_debug as _libr_debug
from .r2libs import r_egg as _libr_egg
from .r2libs import r_flag as _libr_flag
from .r2libs import r_fs as _libr_fs
from .r2libs import r_hash as _libr_hash
from .r2libs import r_io as _libr_io
from .r2libs import r_lang as _libr_lang
from .r2libs import r_magic as _libr_magic
from .r2libs import r_main as _libr_main
from .r2libs import r_parse as _libr_parse
from .r2libs import r_reg as _libr_reg
from .r2libs import r_search as _libr_search
from .r2libs import r_socket as _libr_socket
from .r2libs import r_syscall as _libr_syscall
from .r2libs import r_util as _libr_util


_libraries = {}
def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))





r_util_version = _libr_util.r_util_version
r_util_version.restype = ctypes.POINTER(ctypes.c_char)
r_util_version.argtypes = []
__all__ = \
    ['r_util_version']

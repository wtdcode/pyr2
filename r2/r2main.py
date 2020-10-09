# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_main as _libr_main


# if local wordsize is same as target, keep ctypes pointer function.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    POINTER_T = ctypes.POINTER
else:
    # required to access _ctypes
    import _ctypes
    # Emulate a pointer class using the approriate c_int32/c_int64 type
    # The new class should have :
    # ['__module__', 'from_param', '_type_', '__dict__', '__weakref__', '__doc__']
    # but the class should be submitted to a unique instance for each base type
    # to that if A == B, POINTER_T(A) == POINTER_T(B)
    ctypes._pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in ctypes._pointer_t_type_cache:
            return ctypes._pointer_t_type_cache[clsname]
        # make template
        class _T(_ctypes._SimpleCData,):
            _type_ = 'L'
            _subtype_ = pointee
            def _sub_addr_(self):
                return self.value
            def __repr__(self):
                return '%s(%d)'%(clsname, self.value)
            def contents(self):
                raise TypeError('This is not a ctypes pointer.')
            def __init__(self, **args):
                raise TypeError('This is not a ctypes pointer. It is not instanciable.')
        _class = type('LP_%d_%s'%(8, clsname), (_T,),{}) 
        ctypes._pointer_t_type_cache[clsname] = _class
        return _class

c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16



r_main_version = _libr_main.r_main_version
r_main_version.restype = POINTER_T(ctypes.c_char)
r_main_version.argtypes = []
class struct_r_main_t(ctypes.Structure):
    pass

struct_r_main_t._pack_ = True # source:False
struct_r_main_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('main', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
]

RMain = struct_r_main_t
RMainCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))
r_main_new = _libr_main.r_main_new
r_main_new.restype = POINTER_T(struct_r_main_t)
r_main_new.argtypes = [POINTER_T(ctypes.c_char)]
r_main_free = _libr_main.r_main_free
r_main_free.restype = None
r_main_free.argtypes = [POINTER_T(struct_r_main_t)]
r_main_run = _libr_main.r_main_run
r_main_run.restype = ctypes.c_int32
r_main_run.argtypes = [POINTER_T(struct_r_main_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_version_print = _libr_main.r_main_version_print
r_main_version_print.restype = ctypes.c_int32
r_main_version_print.argtypes = [POINTER_T(ctypes.c_char)]
r_main_rax2 = _libr_main.r_main_rax2
r_main_rax2.restype = ctypes.c_int32
r_main_rax2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rarun2 = _libr_main.r_main_rarun2
r_main_rarun2.restype = ctypes.c_int32
r_main_rarun2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rahash2 = _libr_main.r_main_rahash2
r_main_rahash2.restype = ctypes.c_int32
r_main_rahash2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rabin2 = _libr_main.r_main_rabin2
r_main_rabin2.restype = ctypes.c_int32
r_main_rabin2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_radare2 = _libr_main.r_main_radare2
r_main_radare2.restype = ctypes.c_int32
r_main_radare2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rasm2 = _libr_main.r_main_rasm2
r_main_rasm2.restype = ctypes.c_int32
r_main_rasm2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_r2agent = _libr_main.r_main_r2agent
r_main_r2agent.restype = ctypes.c_int32
r_main_r2agent.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rafind2 = _libr_main.r_main_rafind2
r_main_rafind2.restype = ctypes.c_int32
r_main_rafind2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_radiff2 = _libr_main.r_main_radiff2
r_main_radiff2.restype = ctypes.c_int32
r_main_radiff2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_ragg2 = _libr_main.r_main_ragg2
r_main_ragg2.restype = ctypes.c_int32
r_main_ragg2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_main_rasign2 = _libr_main.r_main_rasign2
r_main_rasign2.restype = ctypes.c_int32
r_main_rasign2.argtypes = [ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
__all__ = \
    ['RMain', 'RMainCallback', 'r_main_free', 'r_main_new',
    'r_main_r2agent', 'r_main_rabin2', 'r_main_radare2',
    'r_main_radiff2', 'r_main_rafind2', 'r_main_ragg2',
    'r_main_rahash2', 'r_main_rarun2', 'r_main_rasign2',
    'r_main_rasm2', 'r_main_rax2', 'r_main_run', 'r_main_version',
    'r_main_version_print', 'struct_r_main_t']

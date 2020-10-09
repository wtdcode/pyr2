# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_magic as _libr_magic


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



r_magic_version = _libr_magic.r_magic_version
r_magic_version.restype = POINTER_T(ctypes.c_char)
r_magic_version.argtypes = []
class union_VALUETYPE(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('b', ctypes.c_ubyte),
    ('h', ctypes.c_uint16),
    ('l', ctypes.c_uint32),
    ('q', ctypes.c_uint64),
    ('hs', ctypes.c_ubyte * 2),
    ('hl', ctypes.c_ubyte * 4),
    ('hq', ctypes.c_ubyte * 8),
    ('s', ctypes.c_char * 32),
    ('f', ctypes.c_float),
    ('d', ctypes.c_double),
    ('PADDING_0', ctypes.c_ubyte * 24),
     ]

class struct_r_magic(ctypes.Structure):
    pass

class union_r_magic_0(ctypes.Union):
    pass

class struct_r_magic_0_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('_count', ctypes.c_uint32),
    ('_flags', ctypes.c_uint32),
     ]

union_r_magic_0._pack_ = True # source:False
union_r_magic_0._fields_ = [
    ('_mask', ctypes.c_uint64),
    ('_1', struct_r_magic_0_0),
]

struct_r_magic._pack_ = True # source:False
struct_r_magic._fields_ = [
    ('cont_level', ctypes.c_uint16),
    ('flag', ctypes.c_ubyte),
    ('dummy1', ctypes.c_ubyte),
    ('reln', ctypes.c_ubyte),
    ('vallen', ctypes.c_ubyte),
    ('type', ctypes.c_ubyte),
    ('in_type', ctypes.c_ubyte),
    ('in_op', ctypes.c_ubyte),
    ('mask_op', ctypes.c_ubyte),
    ('cond', ctypes.c_ubyte),
    ('dummy2', ctypes.c_ubyte),
    ('offset', ctypes.c_uint32),
    ('in_offset', ctypes.c_uint32),
    ('lineno', ctypes.c_uint32),
    ('_14', union_r_magic_0),
    ('value', union_VALUETYPE),
    ('desc', ctypes.c_char * 64),
    ('mimetype', ctypes.c_char * 64),
]

class struct_mlist(ctypes.Structure):
    pass

struct_mlist._pack_ = True # source:False
struct_mlist._fields_ = [
    ('magic', POINTER_T(struct_r_magic)),
    ('nmagic', ctypes.c_uint32),
    ('mapped', ctypes.c_int32),
    ('next', POINTER_T(struct_mlist)),
    ('prev', POINTER_T(struct_mlist)),
]

class struct_r_magic_set(ctypes.Structure):
    pass

class struct_r_magic_set_2(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('s', POINTER_T(ctypes.c_char)),
    ('s_len', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('rm_len', ctypes.c_uint64),
     ]

class struct_out(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('buf', POINTER_T(ctypes.c_char)),
    ('pbuf', POINTER_T(ctypes.c_char)),
     ]

class struct_cont(ctypes.Structure):
    pass

class struct_level_info(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('off', ctypes.c_int32),
    ('got_match', ctypes.c_int32),
    ('last_match', ctypes.c_int32),
    ('last_cond', ctypes.c_int32),
     ]

struct_cont._pack_ = True # source:False
struct_cont._fields_ = [
    ('len', ctypes.c_uint64),
    ('li', POINTER_T(struct_level_info)),
]

struct_r_magic_set._pack_ = True # source:False
struct_r_magic_set._fields_ = [
    ('mlist', POINTER_T(struct_mlist)),
    ('c', struct_cont),
    ('o', struct_out),
    ('offset', ctypes.c_uint32),
    ('error', ctypes.c_int32),
    ('flags', ctypes.c_int32),
    ('haderr', ctypes.c_int32),
    ('file', POINTER_T(ctypes.c_char)),
    ('line', ctypes.c_uint64),
    ('_9', struct_r_magic_set_2),
    ('ms_value', union_VALUETYPE),
]

RMagic = struct_r_magic_set
r_magic_new = _libr_magic.r_magic_new
r_magic_new.restype = POINTER_T(struct_r_magic_set)
r_magic_new.argtypes = [ctypes.c_int32]
r_magic_free = _libr_magic.r_magic_free
r_magic_free.restype = None
r_magic_free.argtypes = [POINTER_T(struct_r_magic_set)]
r_magic_file = _libr_magic.r_magic_file
r_magic_file.restype = POINTER_T(ctypes.c_char)
r_magic_file.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(ctypes.c_char)]
r_magic_descriptor = _libr_magic.r_magic_descriptor
r_magic_descriptor.restype = POINTER_T(ctypes.c_char)
r_magic_descriptor.argtypes = [POINTER_T(struct_r_magic_set), ctypes.c_int32]
size_t = ctypes.c_uint64
r_magic_buffer = _libr_magic.r_magic_buffer
r_magic_buffer.restype = POINTER_T(ctypes.c_char)
r_magic_buffer.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(None), size_t]
r_magic_error = _libr_magic.r_magic_error
r_magic_error.restype = POINTER_T(ctypes.c_char)
r_magic_error.argtypes = [POINTER_T(struct_r_magic_set)]
r_magic_setflags = _libr_magic.r_magic_setflags
r_magic_setflags.restype = None
r_magic_setflags.argtypes = [POINTER_T(struct_r_magic_set), ctypes.c_int32]
r_magic_load = _libr_magic.r_magic_load
r_magic_load.restype = ctypes.c_bool
r_magic_load.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(ctypes.c_char)]
r_magic_load_buffer = _libr_magic.r_magic_load_buffer
r_magic_load_buffer.restype = ctypes.c_bool
r_magic_load_buffer.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(ctypes.c_char)]
r_magic_compile = _libr_magic.r_magic_compile
r_magic_compile.restype = ctypes.c_bool
r_magic_compile.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(ctypes.c_char)]
r_magic_check = _libr_magic.r_magic_check
r_magic_check.restype = ctypes.c_bool
r_magic_check.argtypes = [POINTER_T(struct_r_magic_set), POINTER_T(ctypes.c_char)]
r_magic_errno = _libr_magic.r_magic_errno
r_magic_errno.restype = ctypes.c_int32
r_magic_errno.argtypes = [POINTER_T(struct_r_magic_set)]
__all__ = \
    ['RMagic', 'r_magic_buffer', 'r_magic_check', 'r_magic_compile',
    'r_magic_descriptor', 'r_magic_errno', 'r_magic_error',
    'r_magic_file', 'r_magic_free', 'r_magic_load',
    'r_magic_load_buffer', 'r_magic_new', 'r_magic_setflags',
    'r_magic_version', 'size_t', 'struct_cont', 'struct_level_info',
    'struct_mlist', 'struct_out', 'struct_r_magic',
    'struct_r_magic_0_0', 'struct_r_magic_set',
    'struct_r_magic_set_2', 'union_VALUETYPE', 'union_r_magic_0']

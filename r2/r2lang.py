# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_lang as _libr_lang


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



r_lang_version = _libr_lang.r_lang_version
r_lang_version.restype = POINTER_T(ctypes.c_char)
r_lang_version.argtypes = []
RCoreCmdStrCallback = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))
RCoreCmdfCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))
class struct_r_lang_t(ctypes.Structure):
    pass

class struct_r_list_t(ctypes.Structure):
    pass

class struct_r_list_iter_t(ctypes.Structure):
    pass

struct_r_list_iter_t._pack_ = True # source:False
struct_r_list_iter_t._fields_ = [
    ('data', POINTER_T(None)),
    ('n', POINTER_T(struct_r_list_iter_t)),
    ('p', POINTER_T(struct_r_list_iter_t)),
]

struct_r_list_t._pack_ = True # source:False
struct_r_list_t._fields_ = [
    ('head', POINTER_T(struct_r_list_iter_t)),
    ('tail', POINTER_T(struct_r_list_iter_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('length', ctypes.c_int32),
    ('sorted', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

class struct_r_lang_plugin_t(ctypes.Structure):
    pass

struct_r_lang_plugin_t._pack_ = True # source:False
struct_r_lang_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('alias', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('help', POINTER_T(POINTER_T(ctypes.c_char))),
    ('ext', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('setup', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_lang_t)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('prompt', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('run', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('run_file', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)))),
    ('set_argv', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
]

struct_r_lang_t._pack_ = True # source:False
struct_r_lang_t._fields_ = [
    ('cur', POINTER_T(struct_r_lang_plugin_t)),
    ('user', POINTER_T(None)),
    ('defs', POINTER_T(struct_r_list_t)),
    ('langs', POINTER_T(struct_r_list_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('cmd_str', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmdf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

RLang = struct_r_lang_t
RLangPlugin = struct_r_lang_plugin_t
class struct_r_lang_def_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('value', POINTER_T(None)),
     ]

RLangDef = struct_r_lang_def_t
r_lang_new = _libr_lang.r_lang_new
r_lang_new.restype = POINTER_T(struct_r_lang_t)
r_lang_new.argtypes = []
r_lang_free = _libr_lang.r_lang_free
r_lang_free.restype = None
r_lang_free.argtypes = [POINTER_T(struct_r_lang_t)]
r_lang_setup = _libr_lang.r_lang_setup
r_lang_setup.restype = ctypes.c_bool
r_lang_setup.argtypes = [POINTER_T(struct_r_lang_t)]
r_lang_add = _libr_lang.r_lang_add
r_lang_add.restype = ctypes.c_bool
r_lang_add.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(struct_r_lang_plugin_t)]
r_lang_list = _libr_lang.r_lang_list
r_lang_list.restype = ctypes.c_bool
r_lang_list.argtypes = [POINTER_T(struct_r_lang_t)]
r_lang_use = _libr_lang.r_lang_use
r_lang_use.restype = ctypes.c_bool
r_lang_use.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_run = _libr_lang.r_lang_run
r_lang_run.restype = ctypes.c_int32
r_lang_run.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_lang_run_string = _libr_lang.r_lang_run_string
r_lang_run_string.restype = ctypes.c_int32
r_lang_run_string.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_set_user_ptr = _libr_lang.r_lang_set_user_ptr
r_lang_set_user_ptr.restype = None
r_lang_set_user_ptr.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(None)]
r_lang_set_argv = _libr_lang.r_lang_set_argv
r_lang_set_argv.restype = ctypes.c_bool
r_lang_set_argv.argtypes = [POINTER_T(struct_r_lang_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_lang_run_file = _libr_lang.r_lang_run_file
r_lang_run_file.restype = ctypes.c_int32
r_lang_run_file.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_prompt = _libr_lang.r_lang_prompt
r_lang_prompt.restype = ctypes.c_int32
r_lang_prompt.argtypes = [POINTER_T(struct_r_lang_t)]
r_lang_plugin_free = _libr_lang.r_lang_plugin_free
r_lang_plugin_free.restype = None
r_lang_plugin_free.argtypes = [POINTER_T(struct_r_lang_plugin_t)]
r_lang_get_by_name = _libr_lang.r_lang_get_by_name
r_lang_get_by_name.restype = POINTER_T(struct_r_lang_plugin_t)
r_lang_get_by_name.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_get_by_extension = _libr_lang.r_lang_get_by_extension
r_lang_get_by_extension.restype = POINTER_T(struct_r_lang_plugin_t)
r_lang_get_by_extension.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_define = _libr_lang.r_lang_define
r_lang_define.restype = ctypes.c_bool
r_lang_define.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(None)]
r_lang_undef = _libr_lang.r_lang_undef
r_lang_undef.restype = None
r_lang_undef.argtypes = [POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)]
r_lang_def_free = _libr_lang.r_lang_def_free
r_lang_def_free.restype = None
r_lang_def_free.argtypes = [POINTER_T(struct_r_lang_def_t)]
__all__ = \
    ['RCoreCmdStrCallback', 'RCoreCmdfCallback', 'RLang', 'RLangDef',
    'RLangPlugin', 'r_lang_add', 'r_lang_def_free', 'r_lang_define',
    'r_lang_free', 'r_lang_get_by_extension', 'r_lang_get_by_name',
    'r_lang_list', 'r_lang_new', 'r_lang_plugin_free',
    'r_lang_prompt', 'r_lang_run', 'r_lang_run_file',
    'r_lang_run_string', 'r_lang_set_argv', 'r_lang_set_user_ptr',
    'r_lang_setup', 'r_lang_undef', 'r_lang_use', 'r_lang_version',
    'struct_r_lang_def_t', 'struct_r_lang_plugin_t',
    'struct_r_lang_t', 'struct_r_list_iter_t', 'struct_r_list_t']

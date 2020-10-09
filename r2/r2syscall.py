# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_syscall as _libr_syscall


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



class struct_r_list_iter_t(ctypes.Structure):
    pass

struct_r_list_iter_t._pack_ = True # source:False
struct_r_list_iter_t._fields_ = [
    ('data', POINTER_T(None)),
    ('n', POINTER_T(struct_r_list_iter_t)),
    ('p', POINTER_T(struct_r_list_iter_t)),
]

class struct_r_list_t(ctypes.Structure):
    pass

struct_r_list_t._pack_ = True # source:False
struct_r_list_t._fields_ = [
    ('head', POINTER_T(struct_r_list_iter_t)),
    ('tail', POINTER_T(struct_r_list_iter_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('length', ctypes.c_int32),
    ('sorted', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

r_syscall_version = _libr_syscall.r_syscall_version
r_syscall_version.restype = POINTER_T(ctypes.c_char)
r_syscall_version.argtypes = []
class struct_r_syscall_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('swi', ctypes.c_int32),
    ('num', ctypes.c_int32),
    ('args', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('sargs', POINTER_T(ctypes.c_char)),
     ]

RSyscallItem = struct_r_syscall_item_t
class struct_r_syscall_port_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('port', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
     ]

RSyscallPort = struct_r_syscall_port_t
class struct_r_syscall_t(ctypes.Structure):
    pass

class struct_sdb_t(ctypes.Structure):
    pass

class struct_cdb_make(ctypes.Structure):
    pass

class struct_cdb_hp(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('h', ctypes.c_uint32),
    ('p', ctypes.c_uint32),
     ]

class struct_buffer(ctypes.Structure):
    pass

struct_buffer._pack_ = True # source:False
struct_buffer._fields_ = [
    ('x', POINTER_T(ctypes.c_char)),
    ('p', ctypes.c_uint32),
    ('n', ctypes.c_uint32),
    ('fd', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('op', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32))),
]

class struct_cdb_hplist(ctypes.Structure):
    pass

struct_cdb_hplist._pack_ = True # source:False
struct_cdb_hplist._fields_ = [
    ('hp', struct_cdb_hp * 1000),
    ('next', POINTER_T(struct_cdb_hplist)),
    ('num', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct_cdb_make._pack_ = True # source:False
struct_cdb_make._fields_ = [
    ('bspace', ctypes.c_char * 8192),
    ('final', ctypes.c_char * 1024),
    ('count', ctypes.c_uint32 * 256),
    ('start', ctypes.c_uint32 * 256),
    ('head', POINTER_T(struct_cdb_hplist)),
    ('split', POINTER_T(struct_cdb_hp)),
    ('hash', POINTER_T(struct_cdb_hp)),
    ('numentries', ctypes.c_uint32),
    ('memsize', ctypes.c_uint32),
    ('b', struct_buffer),
    ('pos', ctypes.c_uint32),
    ('fd', ctypes.c_int32),
]

class struct_c__SA_dict(ctypes.Structure):
    pass

struct_c__SA_dict._pack_ = True # source:False
struct_c__SA_dict._fields_ = [
    ('table', POINTER_T(POINTER_T(None))),
    ('f', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('size', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct_ht_pp_t(ctypes.Structure):
    pass

class struct_ht_pp_bucket_t(ctypes.Structure):
    pass

class struct_ht_pp_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('key', POINTER_T(None)),
    ('value', POINTER_T(None)),
    ('key_len', ctypes.c_uint32),
    ('value_len', ctypes.c_uint32),
     ]

struct_ht_pp_bucket_t._pack_ = True # source:False
struct_ht_pp_bucket_t._fields_ = [
    ('arr', POINTER_T(struct_ht_pp_kv)),
    ('count', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct_ht_pp_options_t(ctypes.Structure):
    pass

struct_ht_pp_options_t._pack_ = True # source:False
struct_ht_pp_options_t._fields_ = [
    ('cmp', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
    ('hashfn', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(None)))),
    ('dupkey', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None)))),
    ('dupvalue', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None)))),
    ('calcsizeK', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(None)))),
    ('calcsizeV', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(None)))),
    ('freefn', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_ht_pp_kv)))),
    ('elem_size', ctypes.c_uint64),
]

struct_ht_pp_t._pack_ = True # source:False
struct_ht_pp_t._fields_ = [
    ('size', ctypes.c_uint32),
    ('count', ctypes.c_uint32),
    ('table', POINTER_T(struct_ht_pp_bucket_t)),
    ('prime_idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('opt', struct_ht_pp_options_t),
]

class struct_cdb(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('map', POINTER_T(ctypes.c_char)),
    ('fd', ctypes.c_int32),
    ('size', ctypes.c_uint32),
    ('loop', ctypes.c_uint32),
    ('khash', ctypes.c_uint32),
    ('kpos', ctypes.c_uint32),
    ('hpos', ctypes.c_uint32),
    ('hslots', ctypes.c_uint32),
    ('dpos', ctypes.c_uint32),
    ('dlen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

class struct_sdb_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', struct_ht_pp_kv),
    ('cas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('expire', ctypes.c_uint64),
     ]

class struct_ls_t(ctypes.Structure):
    pass

class struct_ls_iter_t(ctypes.Structure):
    pass

struct_ls_iter_t._pack_ = True # source:False
struct_ls_iter_t._fields_ = [
    ('data', POINTER_T(None)),
    ('n', POINTER_T(struct_ls_iter_t)),
    ('p', POINTER_T(struct_ls_iter_t)),
]

struct_ls_t._pack_ = True # source:False
struct_ls_t._fields_ = [
    ('length', ctypes.c_uint64),
    ('head', POINTER_T(struct_ls_iter_t)),
    ('tail', POINTER_T(struct_ls_iter_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('cmp', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
    ('sorted', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

struct_sdb_t._pack_ = True # source:False
struct_sdb_t._fields_ = [
    ('dir', POINTER_T(ctypes.c_char)),
    ('path', POINTER_T(ctypes.c_char)),
    ('name', POINTER_T(ctypes.c_char)),
    ('fd', ctypes.c_int32),
    ('refs', ctypes.c_int32),
    ('lock', ctypes.c_int32),
    ('journal', ctypes.c_int32),
    ('db', struct_cdb),
    ('m', struct_cdb_make),
    ('ht', POINTER_T(struct_ht_pp_t)),
    ('eod', ctypes.c_uint32),
    ('pos', ctypes.c_uint32),
    ('fdump', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ndump', POINTER_T(ctypes.c_char)),
    ('expire', ctypes.c_uint64),
    ('last', ctypes.c_uint64),
    ('options', ctypes.c_int32),
    ('ns_lock', ctypes.c_int32),
    ('ns', POINTER_T(struct_ls_t)),
    ('hooks', POINTER_T(struct_ls_t)),
    ('tmpkv', struct_sdb_kv),
    ('depth', ctypes.c_uint32),
    ('timestamped', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('mht', struct_c__SA_dict),
]

class struct__IO_FILE(ctypes.Structure):
    pass

class struct__IO_codecvt(ctypes.Structure):
    pass

class struct__IO_marker(ctypes.Structure):
    pass

class struct__IO_wide_data(ctypes.Structure):
    pass

struct__IO_FILE._pack_ = True # source:False
struct__IO_FILE._fields_ = [
    ('_flags', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_IO_read_ptr', POINTER_T(ctypes.c_char)),
    ('_IO_read_end', POINTER_T(ctypes.c_char)),
    ('_IO_read_base', POINTER_T(ctypes.c_char)),
    ('_IO_write_base', POINTER_T(ctypes.c_char)),
    ('_IO_write_ptr', POINTER_T(ctypes.c_char)),
    ('_IO_write_end', POINTER_T(ctypes.c_char)),
    ('_IO_buf_base', POINTER_T(ctypes.c_char)),
    ('_IO_buf_end', POINTER_T(ctypes.c_char)),
    ('_IO_save_base', POINTER_T(ctypes.c_char)),
    ('_IO_backup_base', POINTER_T(ctypes.c_char)),
    ('_IO_save_end', POINTER_T(ctypes.c_char)),
    ('_markers', POINTER_T(struct__IO_marker)),
    ('_chain', POINTER_T(struct__IO_FILE)),
    ('_fileno', ctypes.c_int32),
    ('_flags2', ctypes.c_int32),
    ('_old_offset', ctypes.c_int64),
    ('_cur_column', ctypes.c_uint16),
    ('_vtable_offset', ctypes.c_byte),
    ('_shortbuf', ctypes.c_char * 1),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('_lock', POINTER_T(None)),
    ('_offset', ctypes.c_int64),
    ('_codecvt', POINTER_T(struct__IO_codecvt)),
    ('_wide_data', POINTER_T(struct__IO_wide_data)),
    ('_freeres_list', POINTER_T(struct__IO_FILE)),
    ('_freeres_buf', POINTER_T(None)),
    ('__pad5', ctypes.c_uint64),
    ('_mode', ctypes.c_int32),
    ('_unused2', ctypes.c_char * 20),
]

struct_r_syscall_t._pack_ = True # source:False
struct_r_syscall_t._fields_ = [
    ('fd', POINTER_T(struct__IO_FILE)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('os', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('cpu', POINTER_T(ctypes.c_char)),
    ('sysptr', POINTER_T(struct_r_syscall_item_t)),
    ('sysport', POINTER_T(struct_r_syscall_port_t)),
    ('db', POINTER_T(struct_sdb_t)),
    ('srdb', POINTER_T(struct_sdb_t)),
    ('refs', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

RSyscall = struct_r_syscall_t
class struct_r_syscall_plugin_t(ctypes.Structure):
    pass

class struct_r_syscall_args_t(ctypes.Structure):
    pass

struct_r_syscall_plugin_t._pack_ = True # source:False
struct_r_syscall_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('os', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('nargs', ctypes.c_int32),
    ('args', POINTER_T(struct_r_syscall_args_t)),
]

RSyscallPlugin = struct_r_syscall_plugin_t
class struct_r_syscall_arch_plugin_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('bits', POINTER_T(ctypes.c_int32)),
    ('nargs', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('args', POINTER_T(POINTER_T(struct_r_syscall_args_t))),
     ]

RSyscallArchPlugin = struct_r_syscall_arch_plugin_t
r_syscall_item_new_from_string = _libr_syscall.r_syscall_item_new_from_string
r_syscall_item_new_from_string.restype = POINTER_T(struct_r_syscall_item_t)
r_syscall_item_new_from_string.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_syscall_item_free = _libr_syscall.r_syscall_item_free
r_syscall_item_free.restype = None
r_syscall_item_free.argtypes = [POINTER_T(struct_r_syscall_item_t)]
r_syscall_new = _libr_syscall.r_syscall_new
r_syscall_new.restype = POINTER_T(struct_r_syscall_t)
r_syscall_new.argtypes = []
r_syscall_free = _libr_syscall.r_syscall_free
r_syscall_free.restype = None
r_syscall_free.argtypes = [POINTER_T(struct_r_syscall_t)]
r_syscall_ref = _libr_syscall.r_syscall_ref
r_syscall_ref.restype = POINTER_T(struct_r_syscall_t)
r_syscall_ref.argtypes = [POINTER_T(struct_r_syscall_t)]
r_syscall_setup = _libr_syscall.r_syscall_setup
r_syscall_setup.restype = ctypes.c_bool
r_syscall_setup.argtypes = [POINTER_T(struct_r_syscall_t), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_syscall_get = _libr_syscall.r_syscall_get
r_syscall_get.restype = POINTER_T(struct_r_syscall_item_t)
r_syscall_get.argtypes = [POINTER_T(struct_r_syscall_t), ctypes.c_int32, ctypes.c_int32]
r_syscall_get_num = _libr_syscall.r_syscall_get_num
r_syscall_get_num.restype = ctypes.c_int32
r_syscall_get_num.argtypes = [POINTER_T(struct_r_syscall_t), POINTER_T(ctypes.c_char)]
r_syscall_get_i = _libr_syscall.r_syscall_get_i
r_syscall_get_i.restype = POINTER_T(ctypes.c_char)
r_syscall_get_i.argtypes = [POINTER_T(struct_r_syscall_t), ctypes.c_int32, ctypes.c_int32]
r_syscall_sysreg = _libr_syscall.r_syscall_sysreg
r_syscall_sysreg.restype = POINTER_T(ctypes.c_char)
r_syscall_sysreg.argtypes = [POINTER_T(struct_r_syscall_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_syscall_list = _libr_syscall.r_syscall_list
r_syscall_list.restype = POINTER_T(struct_r_list_t)
r_syscall_list.argtypes = [POINTER_T(struct_r_syscall_t)]
r_syscall_get_swi = _libr_syscall.r_syscall_get_swi
r_syscall_get_swi.restype = ctypes.c_int32
r_syscall_get_swi.argtypes = [POINTER_T(struct_r_syscall_t)]
r_syscall_get_io = _libr_syscall.r_syscall_get_io
r_syscall_get_io.restype = POINTER_T(ctypes.c_char)
r_syscall_get_io.argtypes = [POINTER_T(struct_r_syscall_t), ctypes.c_int32]
__all__ = \
    ['RSyscall', 'RSyscallArchPlugin', 'RSyscallItem',
    'RSyscallPlugin', 'RSyscallPort', 'r_syscall_free',
    'r_syscall_get', 'r_syscall_get_i', 'r_syscall_get_io',
    'r_syscall_get_num', 'r_syscall_get_swi', 'r_syscall_item_free',
    'r_syscall_item_new_from_string', 'r_syscall_list',
    'r_syscall_new', 'r_syscall_ref', 'r_syscall_setup',
    'r_syscall_sysreg', 'r_syscall_version', 'struct__IO_FILE',
    'struct__IO_codecvt', 'struct__IO_marker', 'struct__IO_wide_data',
    'struct_buffer', 'struct_c__SA_dict', 'struct_cdb',
    'struct_cdb_hp', 'struct_cdb_hplist', 'struct_cdb_make',
    'struct_ht_pp_bucket_t', 'struct_ht_pp_kv',
    'struct_ht_pp_options_t', 'struct_ht_pp_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_r_list_iter_t', 'struct_r_list_t',
    'struct_r_syscall_arch_plugin_t', 'struct_r_syscall_args_t',
    'struct_r_syscall_item_t', 'struct_r_syscall_plugin_t',
    'struct_r_syscall_port_t', 'struct_r_syscall_t', 'struct_sdb_kv',
    'struct_sdb_t']

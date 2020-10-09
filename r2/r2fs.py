# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_fs as _libr_fs


c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16

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



class struct_r_core_bind_t(ctypes.Structure):
    pass

struct_r_core_bind_t._pack_ = True # source:False
struct_r_core_bind_t._fields_ = [
    ('core', POINTER_T(None)),
    ('cmd', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmdf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmdstr', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmdstrf', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('puts', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char)))),
    ('bphit', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
    ('syshit', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('setab', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('getName', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('getNameDelta', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('archbits', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_uint64))),
    ('cfggeti', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cfgGet', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('numGet', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('isMapped', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), ctypes.c_uint64, ctypes.c_int32))),
    ('syncDebugMaps', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None)))),
]

class struct_r_cons_bind_t(ctypes.Structure):
    pass

struct_r_cons_bind_t._pack_ = True # source:False
struct_r_cons_bind_t._fields_ = [
    ('get_size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))),
    ('get_cursor', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('is_breaked', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool))),
    ('cb_flush', POINTER_T(ctypes.CFUNCTYPE(None))),
    ('cb_grep', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char)))),
]

r_fs_version = _libr_fs.r_fs_version
r_fs_version.restype = POINTER_T(ctypes.c_char)
r_fs_version.argtypes = []
class struct_r_fs_t(ctypes.Structure):
    pass

class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_io_desc_t(ctypes.Structure):
    pass

class struct_r_list_t(ctypes.Structure):
    pass


# values for enumeration '__ptrace_request'
__ptrace_request__enumvalues = {
    0: 'PTRACE_TRACEME',
    1: 'PTRACE_PEEKTEXT',
    2: 'PTRACE_PEEKDATA',
    3: 'PTRACE_PEEKUSER',
    4: 'PTRACE_POKETEXT',
    5: 'PTRACE_POKEDATA',
    6: 'PTRACE_POKEUSER',
    7: 'PTRACE_CONT',
    8: 'PTRACE_KILL',
    9: 'PTRACE_SINGLESTEP',
    12: 'PTRACE_GETREGS',
    13: 'PTRACE_SETREGS',
    14: 'PTRACE_GETFPREGS',
    15: 'PTRACE_SETFPREGS',
    16: 'PTRACE_ATTACH',
    17: 'PTRACE_DETACH',
    18: 'PTRACE_GETFPXREGS',
    19: 'PTRACE_SETFPXREGS',
    24: 'PTRACE_SYSCALL',
    25: 'PTRACE_GET_THREAD_AREA',
    26: 'PTRACE_SET_THREAD_AREA',
    30: 'PTRACE_ARCH_PRCTL',
    31: 'PTRACE_SYSEMU',
    32: 'PTRACE_SYSEMU_SINGLESTEP',
    33: 'PTRACE_SINGLEBLOCK',
    16896: 'PTRACE_SETOPTIONS',
    16897: 'PTRACE_GETEVENTMSG',
    16898: 'PTRACE_GETSIGINFO',
    16899: 'PTRACE_SETSIGINFO',
    16900: 'PTRACE_GETREGSET',
    16901: 'PTRACE_SETREGSET',
    16902: 'PTRACE_SEIZE',
    16903: 'PTRACE_INTERRUPT',
    16904: 'PTRACE_LISTEN',
    16905: 'PTRACE_PEEKSIGINFO',
    16906: 'PTRACE_GETSIGMASK',
    16907: 'PTRACE_SETSIGMASK',
    16908: 'PTRACE_SECCOMP_GET_FILTER',
    16909: 'PTRACE_SECCOMP_GET_METADATA',
}
PTRACE_TRACEME = 0
PTRACE_PEEKTEXT = 1
PTRACE_PEEKDATA = 2
PTRACE_PEEKUSER = 3
PTRACE_POKETEXT = 4
PTRACE_POKEDATA = 5
PTRACE_POKEUSER = 6
PTRACE_CONT = 7
PTRACE_KILL = 8
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_GETFPREGS = 14
PTRACE_SETFPREGS = 15
PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_GETFPXREGS = 18
PTRACE_SETFPXREGS = 19
PTRACE_SYSCALL = 24
PTRACE_GET_THREAD_AREA = 25
PTRACE_SET_THREAD_AREA = 26
PTRACE_ARCH_PRCTL = 30
PTRACE_SYSEMU = 31
PTRACE_SYSEMU_SINGLESTEP = 32
PTRACE_SINGLEBLOCK = 33
PTRACE_SETOPTIONS = 16896
PTRACE_GETEVENTMSG = 16897
PTRACE_GETSIGINFO = 16898
PTRACE_SETSIGINFO = 16899
PTRACE_GETREGSET = 16900
PTRACE_SETREGSET = 16901
PTRACE_SEIZE = 16902
PTRACE_INTERRUPT = 16903
PTRACE_LISTEN = 16904
PTRACE_PEEKSIGINFO = 16905
PTRACE_GETSIGMASK = 16906
PTRACE_SETSIGMASK = 16907
PTRACE_SECCOMP_GET_FILTER = 16908
PTRACE_SECCOMP_GET_METADATA = 16909
__ptrace_request = ctypes.c_int # enum
class struct_r_io_map_t(ctypes.Structure):
    pass

class struct_r_id_pool_t(ctypes.Structure):
    pass

class struct_r_queue_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('elems', POINTER_T(POINTER_T(None))),
    ('capacity', ctypes.c_uint32),
    ('front', ctypes.c_uint32),
    ('rear', ctypes.c_int32),
    ('size', ctypes.c_uint32),
     ]

struct_r_id_pool_t._pack_ = True # source:False
struct_r_id_pool_t._fields_ = [
    ('start_id', ctypes.c_uint32),
    ('last_id', ctypes.c_uint32),
    ('next_id', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('freed_ids', POINTER_T(struct_r_queue_t)),
]

class struct_r_id_storage_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pool', POINTER_T(struct_r_id_pool_t)),
    ('data', POINTER_T(POINTER_T(None))),
    ('top_id', ctypes.c_uint32),
    ('size', ctypes.c_uint32),
     ]

class struct_r_pvector_t(ctypes.Structure):
    pass

class struct_r_vector_t(ctypes.Structure):
    pass

struct_r_vector_t._pack_ = True # source:False
struct_r_vector_t._fields_ = [
    ('a', POINTER_T(None)),
    ('len', ctypes.c_uint64),
    ('capacity', ctypes.c_uint64),
    ('elem_size', ctypes.c_uint64),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None)))),
    ('free_user', POINTER_T(None)),
]

struct_r_pvector_t._pack_ = True # source:False
struct_r_pvector_t._fields_ = [
    ('v', struct_r_vector_t),
]

class struct_ptrace_wrap_instance_t(ctypes.Structure):
    pass

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

class struct_r_io_plugin_t(ctypes.Structure):
    pass

class struct_r_io_undo_t(ctypes.Structure):
    pass

class struct_r_io_undos_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('off', ctypes.c_uint64),
    ('cursor', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

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

struct_r_io_undo_t._pack_ = True # source:False
struct_r_io_undo_t._fields_ = [
    ('s_enable', ctypes.c_int32),
    ('w_enable', ctypes.c_int32),
    ('w_list', POINTER_T(struct_r_list_t)),
    ('w_init', ctypes.c_int32),
    ('idx', ctypes.c_int32),
    ('undos', ctypes.c_int32),
    ('redos', ctypes.c_int32),
    ('seek', struct_r_io_undos_t * 64),
]

struct_r_io_plugin_t._pack_ = True # source:False
struct_r_io_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('widget', POINTER_T(None)),
    ('uris', POINTER_T(ctypes.c_char)),
    ('listener', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_desc_t)))),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32))),
    ('undo', struct_r_io_undo_t),
    ('isdbg', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('system', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_char)))),
    ('open', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('open_many', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('lseek', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, ctypes.c_int32))),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('close', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_desc_t)))),
    ('is_blockdevice', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_desc_t)))),
    ('is_chardevice', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_desc_t)))),
    ('getpid', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_desc_t)))),
    ('gettid', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_desc_t)))),
    ('getbase', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_uint64)))),
    ('resize', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), ctypes.c_uint64))),
    ('extend', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), ctypes.c_uint64))),
    ('accept', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t), ctypes.c_int32))),
    ('create', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('check', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_bool))),
]

class struct_ht_up_t(ctypes.Structure):
    pass

class struct_ht_up_options_t(ctypes.Structure):
    pass

class struct_ht_up_kv(ctypes.Structure):
    pass

struct_ht_up_options_t._pack_ = True # source:False
struct_ht_up_options_t._fields_ = [
    ('cmp', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64))),
    ('hashfn', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_uint64))),
    ('dupkey', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64))),
    ('dupvalue', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None)))),
    ('calcsizeK', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_uint64))),
    ('calcsizeV', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(None)))),
    ('freefn', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_ht_up_kv)))),
    ('elem_size', ctypes.c_uint64),
]

class struct_ht_up_bucket_t(ctypes.Structure):
    pass

struct_ht_up_kv._pack_ = True # source:False
struct_ht_up_kv._fields_ = [
    ('key', ctypes.c_uint64),
    ('value', POINTER_T(None)),
    ('key_len', ctypes.c_uint32),
    ('value_len', ctypes.c_uint32),
]

struct_ht_up_bucket_t._pack_ = True # source:False
struct_ht_up_bucket_t._fields_ = [
    ('arr', POINTER_T(struct_ht_up_kv)),
    ('count', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct_ht_up_t._pack_ = True # source:False
struct_ht_up_t._fields_ = [
    ('size', ctypes.c_uint32),
    ('count', ctypes.c_uint32),
    ('table', POINTER_T(struct_ht_up_bucket_t)),
    ('prime_idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('opt', struct_ht_up_options_t),
]

struct_r_io_desc_t._pack_ = True # source:False
struct_r_io_desc_t._fields_ = [
    ('fd', ctypes.c_int32),
    ('perm', ctypes.c_int32),
    ('uri', POINTER_T(ctypes.c_char)),
    ('name', POINTER_T(ctypes.c_char)),
    ('referer', POINTER_T(ctypes.c_char)),
    ('cache', POINTER_T(struct_ht_up_t)),
    ('data', POINTER_T(None)),
    ('plugin', POINTER_T(struct_r_io_plugin_t)),
    ('io', POINTER_T(struct_r_io_t)),
]

class struct_r_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', ctypes.c_uint64),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_uint64),
     ]

class struct_r_rb_node_t(ctypes.Structure):
    pass

struct_r_rb_node_t._pack_ = True # source:False
struct_r_rb_node_t._fields_ = [
    ('child', POINTER_T(struct_r_rb_node_t) * 2),
    ('red', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

struct_r_io_t._pack_ = True # source:False
struct_r_io_t._fields_ = [
    ('desc', POINTER_T(struct_r_io_desc_t)),
    ('off', ctypes.c_uint64),
    ('bits', ctypes.c_int32),
    ('va', ctypes.c_int32),
    ('ff', ctypes.c_int32),
    ('Oxff', ctypes.c_int32),
    ('addrbytes', ctypes.c_uint64),
    ('aslr', ctypes.c_int32),
    ('autofd', ctypes.c_int32),
    ('cached', ctypes.c_int32),
    ('cachemode', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('p_cache', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('map_ids', POINTER_T(struct_r_id_pool_t)),
    ('maps', struct_r_pvector_t),
    ('map_skyline', struct_r_pvector_t),
    ('files', POINTER_T(struct_r_id_storage_t)),
    ('buffer', POINTER_T(struct_r_cache_t)),
    ('cache', POINTER_T(struct_r_list_t)),
    ('cacheTree', struct_r_rb_node_t),
    ('write_mask', POINTER_T(ctypes.c_ubyte)),
    ('write_mask_len', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('undo', struct_r_io_undo_t),
    ('plugins', POINTER_T(struct_ls_t)),
    ('runprofile', POINTER_T(ctypes.c_char)),
    ('envprofile', POINTER_T(ctypes.c_char)),
    ('ptrace_wrap', POINTER_T(struct_ptrace_wrap_instance_t)),
    ('args', POINTER_T(ctypes.c_char)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('corebind', struct_r_core_bind_t),
]

struct_r_io_bind_t._pack_ = True # source:False
struct_r_io_bind_t._fields_ = [
    ('init', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('io', POINTER_T(struct_r_io_t)),
    ('desc_use', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('desc_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('desc_size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_desc_t)))),
    ('open', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('open_at', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64))),
    ('close', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('read_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('write_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('system', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char)))),
    ('fd_open', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('fd_close', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('fd_seek', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32))),
    ('fd_size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('fd_resize', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64))),
    ('fd_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('fd_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('fd_read_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('fd_write_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('fd_is_dbg', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('fd_get_name', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('fd_get_map', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_io_t), ctypes.c_int32))),
    ('fd_remap', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64))),
    ('is_valid_offset', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_int32))),
    ('addr_is_mapped', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64))),
    ('map_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_uint64))),
    ('map_get_paddr', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_uint64))),
    ('map_add', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64))),
    ('v2p', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_uint64))),
    ('p2v', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_uint64))),
    ('ptrace', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_io_t), __ptrace_request, ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
    ('ptrace_func', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(struct_r_io_t), POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None))), POINTER_T(None)))),
]

struct_r_fs_t._pack_ = True # source:False
struct_r_fs_t._fields_ = [
    ('iob', struct_r_io_bind_t),
    ('cob', struct_r_core_bind_t),
    ('csb', struct_r_cons_bind_t),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('roots', POINTER_T(struct_r_list_t)),
    ('view', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ptr', POINTER_T(None)),
]

RFS = struct_r_fs_t
class struct_r_fs_partition_plugin_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
     ]

RFSPartitionPlugin = struct_r_fs_partition_plugin_t
class struct_r_fs_file_t(ctypes.Structure):
    pass

class struct_r_fs_root_t(ctypes.Structure):
    pass

class struct_r_fs_plugin_t(ctypes.Structure):
    pass

struct_r_fs_plugin_t._pack_ = True # source:False
struct_r_fs_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('slurp', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_fs_file_t), POINTER_T(struct_r_fs_root_t), POINTER_T(ctypes.c_char)))),
    ('open', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_fs_file_t), POINTER_T(struct_r_fs_root_t), POINTER_T(ctypes.c_char), ctypes.c_bool))),
    ('unlink', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_fs_root_t), POINTER_T(ctypes.c_char)))),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_fs_file_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_fs_file_t), ctypes.c_uint64, ctypes.c_int32))),
    ('close', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_fs_file_t)))),
    ('dir', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_fs_root_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('init', POINTER_T(ctypes.CFUNCTYPE(None))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(None))),
    ('mount', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_fs_root_t)))),
    ('umount', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_fs_root_t)))),
]

struct_r_fs_root_t._pack_ = True # source:False
struct_r_fs_root_t._fields_ = [
    ('path', POINTER_T(ctypes.c_char)),
    ('delta', ctypes.c_uint64),
    ('p', POINTER_T(struct_r_fs_plugin_t)),
    ('ptr', POINTER_T(None)),
    ('iob', struct_r_io_bind_t),
    ('cob', struct_r_core_bind_t),
]

struct_r_fs_file_t._pack_ = True # source:False
struct_r_fs_file_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('path', POINTER_T(ctypes.c_char)),
    ('off', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('data', POINTER_T(ctypes.c_ubyte)),
    ('ctx', POINTER_T(None)),
    ('type', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('time', ctypes.c_uint64),
    ('p', POINTER_T(struct_r_fs_plugin_t)),
    ('root', POINTER_T(struct_r_fs_root_t)),
    ('ptr', POINTER_T(None)),
]

RFSFile = struct_r_fs_file_t
RFSRoot = struct_r_fs_root_t
RFSPlugin = struct_r_fs_plugin_t
class struct_r_fs_partition_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('number', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('start', ctypes.c_uint64),
    ('length', ctypes.c_uint64),
    ('index', ctypes.c_int32),
    ('type', ctypes.c_int32),
     ]

RFSPartition = struct_r_fs_partition_t
class struct_r_fs_shell_t(ctypes.Structure):
    pass

struct_r_fs_shell_t._pack_ = True # source:False
struct_r_fs_shell_t._fields_ = [
    ('cwd', POINTER_T(POINTER_T(ctypes.c_char))),
    ('set_prompt', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char)))),
    ('readline', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char)))),
    ('hist_add', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
]

RFSShell = struct_r_fs_shell_t
RFSPartitionIterator = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None), POINTER_T(None)))
class struct_r_fs_partition_type_t(ctypes.Structure):
    pass

struct_r_fs_partition_type_t._pack_ = True # source:False
struct_r_fs_partition_type_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('ptr', POINTER_T(None)),
    ('iterate', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None), POINTER_T(None)))),
]

RFSPartitionType = struct_r_fs_partition_type_t

# values for enumeration 'c__Ea_R_FS_VIEW_NORMAL'
c__Ea_R_FS_VIEW_NORMAL__enumvalues = {
    0: 'R_FS_VIEW_NORMAL',
    1: 'R_FS_VIEW_DELETED',
    2: 'R_FS_VIEW_SPECIAL',
    255: 'R_FS_VIEW_ALL',
}
R_FS_VIEW_NORMAL = 0
R_FS_VIEW_DELETED = 1
R_FS_VIEW_SPECIAL = 2
R_FS_VIEW_ALL = 255
c__Ea_R_FS_VIEW_NORMAL = ctypes.c_int # enum
r_fs_new = _libr_fs.r_fs_new
r_fs_new.restype = POINTER_T(struct_r_fs_t)
r_fs_new.argtypes = []
r_fs_view = _libr_fs.r_fs_view
r_fs_view.restype = None
r_fs_view.argtypes = [POINTER_T(struct_r_fs_t), ctypes.c_int32]
r_fs_free = _libr_fs.r_fs_free
r_fs_free.restype = None
r_fs_free.argtypes = [POINTER_T(struct_r_fs_t)]
r_fs_add = _libr_fs.r_fs_add
r_fs_add.restype = None
r_fs_add.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(struct_r_fs_plugin_t)]
r_fs_del = _libr_fs.r_fs_del
r_fs_del.restype = None
r_fs_del.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(struct_r_fs_plugin_t)]
r_fs_mount = _libr_fs.r_fs_mount
r_fs_mount.restype = POINTER_T(struct_r_fs_root_t)
r_fs_mount.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_fs_umount = _libr_fs.r_fs_umount
r_fs_umount.restype = ctypes.c_bool
r_fs_umount.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_root = _libr_fs.r_fs_root
r_fs_root.restype = POINTER_T(struct_r_list_t)
r_fs_root.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_open = _libr_fs.r_fs_open
r_fs_open.restype = POINTER_T(struct_r_fs_file_t)
r_fs_open.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_fs_close = _libr_fs.r_fs_close
r_fs_close.restype = None
r_fs_close.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(struct_r_fs_file_t)]
r_fs_read = _libr_fs.r_fs_read
r_fs_read.restype = ctypes.c_int32
r_fs_read.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(struct_r_fs_file_t), ctypes.c_uint64, ctypes.c_int32]
r_fs_write = _libr_fs.r_fs_write
r_fs_write.restype = ctypes.c_int32
r_fs_write.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(struct_r_fs_file_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_fs_slurp = _libr_fs.r_fs_slurp
r_fs_slurp.restype = POINTER_T(struct_r_fs_file_t)
r_fs_slurp.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_dir = _libr_fs.r_fs_dir
r_fs_dir.restype = POINTER_T(struct_r_list_t)
r_fs_dir.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_dir_dump = _libr_fs.r_fs_dir_dump
r_fs_dir_dump.restype = ctypes.c_int32
r_fs_dir_dump.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_fs_find_name = _libr_fs.r_fs_find_name
r_fs_find_name.restype = POINTER_T(struct_r_list_t)
r_fs_find_name.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_fs_find_off = _libr_fs.r_fs_find_off
r_fs_find_off.restype = POINTER_T(struct_r_list_t)
r_fs_find_off.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_fs_partitions = _libr_fs.r_fs_partitions
r_fs_partitions.restype = POINTER_T(struct_r_list_t)
r_fs_partitions.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_fs_name = _libr_fs.r_fs_name
r_fs_name.restype = POINTER_T(ctypes.c_char)
r_fs_name.argtypes = [POINTER_T(struct_r_fs_t), ctypes.c_uint64]
r_fs_check = _libr_fs.r_fs_check
r_fs_check.restype = ctypes.c_bool
r_fs_check.argtypes = [POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_shell_prompt = _libr_fs.r_fs_shell_prompt
r_fs_shell_prompt.restype = ctypes.c_int32
r_fs_shell_prompt.argtypes = [POINTER_T(struct_r_fs_shell_t), POINTER_T(struct_r_fs_t), POINTER_T(ctypes.c_char)]
r_fs_file_new = _libr_fs.r_fs_file_new
r_fs_file_new.restype = POINTER_T(struct_r_fs_file_t)
r_fs_file_new.argtypes = [POINTER_T(struct_r_fs_root_t), POINTER_T(ctypes.c_char)]
r_fs_file_free = _libr_fs.r_fs_file_free
r_fs_file_free.restype = None
r_fs_file_free.argtypes = [POINTER_T(struct_r_fs_file_t)]
r_fs_file_copy_abs_path = _libr_fs.r_fs_file_copy_abs_path
r_fs_file_copy_abs_path.restype = POINTER_T(ctypes.c_char)
r_fs_file_copy_abs_path.argtypes = [POINTER_T(struct_r_fs_file_t)]
r_fs_root_new = _libr_fs.r_fs_root_new
r_fs_root_new.restype = POINTER_T(struct_r_fs_root_t)
r_fs_root_new.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_fs_root_free = _libr_fs.r_fs_root_free
r_fs_root_free.restype = None
r_fs_root_free.argtypes = [POINTER_T(struct_r_fs_root_t)]
r_fs_partition_new = _libr_fs.r_fs_partition_new
r_fs_partition_new.restype = POINTER_T(struct_r_fs_partition_t)
r_fs_partition_new.argtypes = [ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64]
r_fs_partition_free = _libr_fs.r_fs_partition_free
r_fs_partition_free.restype = None
r_fs_partition_free.argtypes = [POINTER_T(struct_r_fs_partition_t)]
r_fs_partition_type = _libr_fs.r_fs_partition_type
r_fs_partition_type.restype = POINTER_T(ctypes.c_char)
r_fs_partition_type.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_fs_partition_type_get = _libr_fs.r_fs_partition_type_get
r_fs_partition_type_get.restype = POINTER_T(ctypes.c_char)
r_fs_partition_type_get.argtypes = [ctypes.c_int32]
r_fs_partition_get_size = _libr_fs.r_fs_partition_get_size
r_fs_partition_get_size.restype = ctypes.c_int32
r_fs_partition_get_size.argtypes = []
r_fs_plugin_io = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_r2 = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_ext2 = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_fat = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_ntfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_hfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_hfsplus = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_reiserfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_tar = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_iso9660 = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_udf = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_ufs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_ufs2 = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_sfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_btrfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_jfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_afs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_affs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_cpio = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_xfs = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_fb = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_minix = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
r_fs_plugin_posix = struct_r_fs_plugin_t # Variable struct_r_fs_plugin_t
class struct_r_interval_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
     ]

struct_r_io_map_t._pack_ = True # source:False
struct_r_io_map_t._fields_ = [
    ('fd', ctypes.c_int32),
    ('perm', ctypes.c_int32),
    ('id', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('itv', struct_r_interval_t),
    ('delta', ctypes.c_uint64),
    ('name', POINTER_T(ctypes.c_char)),
]

__all__ = \
    ['PTRACE_ARCH_PRCTL', 'PTRACE_ATTACH', 'PTRACE_CONT',
    'PTRACE_DETACH', 'PTRACE_GETEVENTMSG', 'PTRACE_GETFPREGS',
    'PTRACE_GETFPXREGS', 'PTRACE_GETREGS', 'PTRACE_GETREGSET',
    'PTRACE_GETSIGINFO', 'PTRACE_GETSIGMASK',
    'PTRACE_GET_THREAD_AREA', 'PTRACE_INTERRUPT', 'PTRACE_KILL',
    'PTRACE_LISTEN', 'PTRACE_PEEKDATA', 'PTRACE_PEEKSIGINFO',
    'PTRACE_PEEKTEXT', 'PTRACE_PEEKUSER', 'PTRACE_POKEDATA',
    'PTRACE_POKETEXT', 'PTRACE_POKEUSER', 'PTRACE_SECCOMP_GET_FILTER',
    'PTRACE_SECCOMP_GET_METADATA', 'PTRACE_SEIZE', 'PTRACE_SETFPREGS',
    'PTRACE_SETFPXREGS', 'PTRACE_SETOPTIONS', 'PTRACE_SETREGS',
    'PTRACE_SETREGSET', 'PTRACE_SETSIGINFO', 'PTRACE_SETSIGMASK',
    'PTRACE_SET_THREAD_AREA', 'PTRACE_SINGLEBLOCK',
    'PTRACE_SINGLESTEP', 'PTRACE_SYSCALL', 'PTRACE_SYSEMU',
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'RFS', 'RFSFile',
    'RFSPartition', 'RFSPartitionIterator', 'RFSPartitionPlugin',
    'RFSPartitionType', 'RFSPlugin', 'RFSRoot', 'RFSShell',
    'R_FS_VIEW_ALL', 'R_FS_VIEW_DELETED', 'R_FS_VIEW_NORMAL',
    'R_FS_VIEW_SPECIAL', '__ptrace_request', 'c__Ea_R_FS_VIEW_NORMAL',
    'r_fs_add', 'r_fs_check', 'r_fs_close', 'r_fs_del', 'r_fs_dir',
    'r_fs_dir_dump', 'r_fs_file_copy_abs_path', 'r_fs_file_free',
    'r_fs_file_new', 'r_fs_find_name', 'r_fs_find_off', 'r_fs_free',
    'r_fs_mount', 'r_fs_name', 'r_fs_new', 'r_fs_open',
    'r_fs_partition_free', 'r_fs_partition_get_size',
    'r_fs_partition_new', 'r_fs_partition_type',
    'r_fs_partition_type_get', 'r_fs_partitions', 'r_fs_plugin_affs',
    'r_fs_plugin_afs', 'r_fs_plugin_btrfs', 'r_fs_plugin_cpio',
    'r_fs_plugin_ext2', 'r_fs_plugin_fat', 'r_fs_plugin_fb',
    'r_fs_plugin_hfs', 'r_fs_plugin_hfsplus', 'r_fs_plugin_io',
    'r_fs_plugin_iso9660', 'r_fs_plugin_jfs', 'r_fs_plugin_minix',
    'r_fs_plugin_ntfs', 'r_fs_plugin_posix', 'r_fs_plugin_r2',
    'r_fs_plugin_reiserfs', 'r_fs_plugin_sfs', 'r_fs_plugin_tar',
    'r_fs_plugin_udf', 'r_fs_plugin_ufs', 'r_fs_plugin_ufs2',
    'r_fs_plugin_xfs', 'r_fs_read', 'r_fs_root', 'r_fs_root_free',
    'r_fs_root_new', 'r_fs_shell_prompt', 'r_fs_slurp', 'r_fs_umount',
    'r_fs_version', 'r_fs_view', 'r_fs_write',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_ptrace_wrap_instance_t',
    'struct_r_cache_t', 'struct_r_cons_bind_t',
    'struct_r_core_bind_t', 'struct_r_fs_file_t',
    'struct_r_fs_partition_plugin_t', 'struct_r_fs_partition_t',
    'struct_r_fs_partition_type_t', 'struct_r_fs_plugin_t',
    'struct_r_fs_root_t', 'struct_r_fs_shell_t', 'struct_r_fs_t',
    'struct_r_id_pool_t', 'struct_r_id_storage_t',
    'struct_r_interval_t', 'struct_r_io_bind_t', 'struct_r_io_desc_t',
    'struct_r_io_map_t', 'struct_r_io_plugin_t', 'struct_r_io_t',
    'struct_r_io_undo_t', 'struct_r_io_undos_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_pvector_t',
    'struct_r_queue_t', 'struct_r_rb_node_t', 'struct_r_vector_t']

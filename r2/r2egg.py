# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_egg as _libr_egg


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



class struct_r_anal_range_t(ctypes.Structure):
    pass

class struct_r_rb_node_t(ctypes.Structure):
    pass

struct_r_rb_node_t._pack_ = True # source:False
struct_r_rb_node_t._fields_ = [
    ('child', POINTER_T(struct_r_rb_node_t) * 2),
    ('red', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

struct_r_anal_range_t._pack_ = True # source:False
struct_r_anal_range_t._fields_ = [
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('rb_max_addr', ctypes.c_uint64),
    ('rb', struct_r_rb_node_t),
]

class struct_r_anal_diff_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('addr', ctypes.c_uint64),
    ('dist', ctypes.c_double),
    ('name', POINTER_T(ctypes.c_char)),
    ('size', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

class struct_r_anal_fcn_meta_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('_min', ctypes.c_uint64),
    ('_max', ctypes.c_uint64),
    ('numrefs', ctypes.c_int32),
    ('numcallrefs', ctypes.c_int32),
     ]

class struct_r_anal_function_t(ctypes.Structure):
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

class struct_ht_up_t(ctypes.Structure):
    pass

class struct_ht_up_bucket_t(ctypes.Structure):
    pass

class struct_ht_up_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

class struct_ht_up_options_t(ctypes.Structure):
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

struct_ht_up_t._pack_ = True # source:False
struct_ht_up_t._fields_ = [
    ('size', ctypes.c_uint32),
    ('count', ctypes.c_uint32),
    ('table', POINTER_T(struct_ht_up_bucket_t)),
    ('prime_idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('opt', struct_ht_up_options_t),
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

class struct_r_anal_t(ctypes.Structure):
    pass

class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_io_desc_t(ctypes.Structure):
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

class struct_ptrace_wrap_instance_t(ctypes.Structure):
    pass

class struct_r_id_storage_t(ctypes.Structure):
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

struct_r_id_storage_t._pack_ = True # source:False
struct_r_id_storage_t._fields_ = [
    ('pool', POINTER_T(struct_r_id_pool_t)),
    ('data', POINTER_T(POINTER_T(None))),
    ('top_id', ctypes.c_uint32),
    ('size', ctypes.c_uint32),
]

class struct_r_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', ctypes.c_uint64),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_uint64),
     ]

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

class struct_r_anal_plugin_t(ctypes.Structure):
    pass

class struct_r_anal_esil_t(ctypes.Structure):
    pass

class struct_r_anal_op_t(ctypes.Structure):
    pass


# values for enumeration 'c__EA_RAnalOpMask'
c__EA_RAnalOpMask__enumvalues = {
    0: 'R_ANAL_OP_MASK_BASIC',
    1: 'R_ANAL_OP_MASK_ESIL',
    2: 'R_ANAL_OP_MASK_VAL',
    4: 'R_ANAL_OP_MASK_HINT',
    8: 'R_ANAL_OP_MASK_OPEX',
    16: 'R_ANAL_OP_MASK_DISASM',
    31: 'R_ANAL_OP_MASK_ALL',
}
R_ANAL_OP_MASK_BASIC = 0
R_ANAL_OP_MASK_ESIL = 1
R_ANAL_OP_MASK_VAL = 2
R_ANAL_OP_MASK_HINT = 4
R_ANAL_OP_MASK_OPEX = 8
R_ANAL_OP_MASK_DISASM = 16
R_ANAL_OP_MASK_ALL = 31
c__EA_RAnalOpMask = ctypes.c_int # enum
class struct_r_anal_bb_t(ctypes.Structure):
    pass

struct_r_anal_plugin_t._pack_ = True # source:False
struct_r_anal_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('esil', ctypes.c_int32),
    ('fileformat_type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('archinfo', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), ctypes.c_int32))),
    ('anal_mask', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_ubyte), POINTER_T(struct_r_anal_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_uint64))),
    ('preludes', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_anal_t)))),
    ('op', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, c__EA_RAnalOpMask))),
    ('cmd_ext', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)))),
    ('set_reg_profile', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_t)))),
    ('get_reg_profile', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_t)))),
    ('fingerprint_bb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_bb_t)))),
    ('fingerprint_fcn', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)))),
    ('diff_bb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_function_t)))),
    ('diff_fcn', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_list_t), POINTER_T(struct_r_list_t)))),
    ('diff_eval', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t)))),
    ('esil_init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t)))),
    ('esil_post_loop', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_op_t)))),
    ('esil_trap', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_int32, ctypes.c_int32))),
    ('esil_fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t)))),
]

class struct_r_flag_item_t(ctypes.Structure):
    pass

class struct_r_flag_t(ctypes.Structure):
    pass

class struct_r_anal_hint_cb_t(ctypes.Structure):
    pass

struct_r_anal_hint_cb_t._pack_ = True # source:False
struct_r_anal_hint_cb_t._fields_ = [
    ('on_bits', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_bool))),
]

class struct_r_str_constpool_t(ctypes.Structure):
    pass

class struct_ht_pp_t(ctypes.Structure):
    pass

class struct_ht_pp_options_t(ctypes.Structure):
    pass

class struct_ht_pp_kv(ctypes.Structure):
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

class struct_ht_pp_bucket_t(ctypes.Structure):
    pass

struct_ht_pp_kv._pack_ = True # source:False
struct_ht_pp_kv._fields_ = [
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

struct_ht_pp_t._pack_ = True # source:False
struct_ht_pp_t._fields_ = [
    ('size', ctypes.c_uint32),
    ('count', ctypes.c_uint32),
    ('table', POINTER_T(struct_ht_pp_bucket_t)),
    ('prime_idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('opt', struct_ht_pp_options_t),
]

struct_r_str_constpool_t._pack_ = True # source:False
struct_r_str_constpool_t._fields_ = [
    ('ht', POINTER_T(struct_ht_pp_t)),
]

class struct_r_anal_callbacks_t(ctypes.Structure):
    pass

struct_r_anal_callbacks_t._pack_ = True # source:False
struct_r_anal_callbacks_t._fields_ = [
    ('on_fcn_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_delete', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_rename', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)))),
    ('on_fcn_bb_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t)))),
]

class struct_r_reg_t(ctypes.Structure):
    pass

class struct_r_reg_set_t(ctypes.Structure):
    pass

class struct_r_reg_arena_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', POINTER_T(ctypes.c_ubyte)),
    ('size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

struct_r_reg_set_t._pack_ = True # source:False
struct_r_reg_set_t._fields_ = [
    ('arena', POINTER_T(struct_r_reg_arena_t)),
    ('pool', POINTER_T(struct_r_list_t)),
    ('regs', POINTER_T(struct_r_list_t)),
    ('ht_regs', POINTER_T(struct_ht_pp_t)),
    ('cur', POINTER_T(struct_r_list_iter_t)),
    ('maskregstype', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct_r_reg_t._pack_ = True # source:False
struct_r_reg_t._fields_ = [
    ('profile', POINTER_T(ctypes.c_char)),
    ('reg_profile_cmt', POINTER_T(ctypes.c_char)),
    ('reg_profile_str', POINTER_T(ctypes.c_char)),
    ('name', POINTER_T(ctypes.c_char) * 24),
    ('regset', struct_r_reg_set_t * 8),
    ('allregs', POINTER_T(struct_r_list_t)),
    ('roregs', POINTER_T(struct_r_list_t)),
    ('iters', ctypes.c_int32),
    ('arch', ctypes.c_int32),
    ('bits', ctypes.c_int32),
    ('size', ctypes.c_int32),
    ('is_thumb', ctypes.c_bool),
    ('big_endian', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

class struct_r_flag_bind_t(ctypes.Structure):
    pass

class struct_r_space_t(ctypes.Structure):
    pass

class struct_sdb_t(ctypes.Structure):
    pass

class struct_c__SA_dict(ctypes.Structure):
    pass

struct_c__SA_dict._pack_ = True # source:False
struct_c__SA_dict._fields_ = [
    ('table', POINTER_T(POINTER_T(None))),
    ('f', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('size', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
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

class struct_sdb_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', struct_ht_pp_kv),
    ('cas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('expire', ctypes.c_uint64),
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

class struct_r_num_t(ctypes.Structure):
    pass

class struct_r_num_calc_t(ctypes.Structure):
    pass

class struct_c__SA_RNumCalcValue(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('d', ctypes.c_double),
    ('n', ctypes.c_uint64),
     ]


# values for enumeration 'c__EA_RNumCalcToken'
c__EA_RNumCalcToken__enumvalues = {
    0: 'RNCNAME',
    1: 'RNCNUMBER',
    2: 'RNCEND',
    3: 'RNCINC',
    4: 'RNCDEC',
    43: 'RNCPLUS',
    45: 'RNCMINUS',
    42: 'RNCMUL',
    47: 'RNCDIV',
    37: 'RNCMOD',
    126: 'RNCNEG',
    38: 'RNCAND',
    124: 'RNCORR',
    94: 'RNCXOR',
    59: 'RNCPRINT',
    61: 'RNCASSIGN',
    40: 'RNCLEFTP',
    41: 'RNCRIGHTP',
    60: 'RNCSHL',
    62: 'RNCSHR',
    35: 'RNCROL',
    36: 'RNCROR',
}
RNCNAME = 0
RNCNUMBER = 1
RNCEND = 2
RNCINC = 3
RNCDEC = 4
RNCPLUS = 43
RNCMINUS = 45
RNCMUL = 42
RNCDIV = 47
RNCMOD = 37
RNCNEG = 126
RNCAND = 38
RNCORR = 124
RNCXOR = 94
RNCPRINT = 59
RNCASSIGN = 61
RNCLEFTP = 40
RNCRIGHTP = 41
RNCSHL = 60
RNCSHR = 62
RNCROL = 35
RNCROR = 36
c__EA_RNumCalcToken = ctypes.c_int # enum
struct_r_num_calc_t._pack_ = True # source:False
struct_r_num_calc_t._fields_ = [
    ('curr_tok', c__EA_RNumCalcToken),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('number_value', struct_c__SA_RNumCalcValue),
    ('string_value', ctypes.c_char * 1024),
    ('errors', ctypes.c_int32),
    ('oc', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('calc_err', POINTER_T(ctypes.c_char)),
    ('calc_i', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('calc_buf', POINTER_T(ctypes.c_char)),
    ('calc_len', ctypes.c_int32),
    ('under_calc', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 3),
]

struct_r_num_t._pack_ = True # source:False
struct_r_num_t._fields_ = [
    ('callback', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_num_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_int32)))),
    ('cb_from_value', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_num_t), ctypes.c_uint64, POINTER_T(ctypes.c_int32)))),
    ('value', ctypes.c_uint64),
    ('fvalue', ctypes.c_double),
    ('userptr', POINTER_T(None)),
    ('dbz', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('nc', struct_r_num_calc_t),
]

class struct_r_spaces_t(ctypes.Structure):
    pass

class struct_r_event_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('user', POINTER_T(None)),
    ('incall', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('callbacks', POINTER_T(struct_ht_up_t)),
    ('all_callbacks', struct_r_vector_t),
    ('next_handle', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

struct_r_space_t._pack_ = True # source:False
struct_r_space_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('rb', struct_r_rb_node_t),
]

struct_r_spaces_t._pack_ = True # source:False
struct_r_spaces_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('current', POINTER_T(struct_r_space_t)),
    ('spaces', POINTER_T(struct_r_rb_node_t)),
    ('spacestack', POINTER_T(struct_r_list_t)),
    ('event', POINTER_T(struct_r_event_t)),
]

class struct_r_skiplist_t(ctypes.Structure):
    pass

class struct_r_skiplist_node_t(ctypes.Structure):
    pass

struct_r_skiplist_node_t._pack_ = True # source:False
struct_r_skiplist_node_t._fields_ = [
    ('data', POINTER_T(None)),
    ('forward', POINTER_T(POINTER_T(struct_r_skiplist_node_t))),
]

struct_r_skiplist_t._pack_ = True # source:False
struct_r_skiplist_t._fields_ = [
    ('head', POINTER_T(struct_r_skiplist_node_t)),
    ('list_level', ctypes.c_int32),
    ('size', ctypes.c_int32),
    ('freefn', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('compare', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
]

struct_r_flag_t._pack_ = True # source:False
struct_r_flag_t._fields_ = [
    ('spaces', struct_r_spaces_t),
    ('base', ctypes.c_int64),
    ('realnames', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('tags', POINTER_T(struct_sdb_t)),
    ('num', POINTER_T(struct_r_num_t)),
    ('by_off', POINTER_T(struct_r_skiplist_t)),
    ('ht_name', POINTER_T(struct_ht_pp_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('zones', POINTER_T(struct_r_list_t)),
]

struct_r_flag_bind_t._pack_ = True # source:False
struct_r_flag_bind_t._fields_ = [
    ('init', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('f', POINTER_T(struct_r_flag_t)),
    ('exist_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint16, ctypes.c_uint64))),
    ('get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))),
    ('get_at', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_bool))),
    ('get_list', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64))),
    ('set', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32))),
    ('unset', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(struct_r_flag_item_t)))),
    ('unset_name', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))),
    ('unset_off', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), ctypes.c_uint64))),
    ('set_fs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_space_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))),
    ('push_fs', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))),
    ('pop_fs', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t)))),
]

class struct_r_bin_bind_t(ctypes.Structure):
    pass

class struct_r_bin_t(ctypes.Structure):
    pass

class struct_r_bin_file_t(ctypes.Structure):
    pass

class struct_r_bin_object_t(ctypes.Structure):
    pass

class struct_r_bin_info_t(ctypes.Structure):
    pass

class struct_r_bin_hash_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('len', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('buf', ctypes.c_ubyte * 32),
    ('cmd', POINTER_T(ctypes.c_char)),
     ]

struct_r_bin_info_t._pack_ = True # source:False
struct_r_bin_info_t._fields_ = [
    ('file', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('bclass', POINTER_T(ctypes.c_char)),
    ('rclass', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('cpu', POINTER_T(ctypes.c_char)),
    ('machine', POINTER_T(ctypes.c_char)),
    ('head_flag', POINTER_T(ctypes.c_char)),
    ('features', POINTER_T(ctypes.c_char)),
    ('os', POINTER_T(ctypes.c_char)),
    ('subsystem', POINTER_T(ctypes.c_char)),
    ('rpath', POINTER_T(ctypes.c_char)),
    ('guid', POINTER_T(ctypes.c_char)),
    ('debug_file_name', POINTER_T(ctypes.c_char)),
    ('lang', POINTER_T(ctypes.c_char)),
    ('default_cc', POINTER_T(ctypes.c_char)),
    ('file_hashes', POINTER_T(struct_r_list_t)),
    ('bits', ctypes.c_int32),
    ('has_va', ctypes.c_int32),
    ('has_pi', ctypes.c_int32),
    ('has_canary', ctypes.c_int32),
    ('has_retguard', ctypes.c_int32),
    ('has_sanitizers', ctypes.c_int32),
    ('has_crypto', ctypes.c_int32),
    ('has_nx', ctypes.c_int32),
    ('big_endian', ctypes.c_int32),
    ('has_lit', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('actual_checksum', POINTER_T(ctypes.c_char)),
    ('claimed_checksum', POINTER_T(ctypes.c_char)),
    ('pe_overlay', ctypes.c_int32),
    ('signature', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('dbg_info', ctypes.c_uint64),
    ('sum', struct_r_bin_hash_t * 3),
    ('baddr', ctypes.c_uint64),
    ('intrp', POINTER_T(ctypes.c_char)),
    ('compiler', POINTER_T(ctypes.c_char)),
]

class struct_r_bin_addr_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('hvaddr', ctypes.c_uint64),
    ('hpaddr', ctypes.c_uint64),
    ('type', ctypes.c_int32),
    ('bits', ctypes.c_int32),
     ]

class struct_r_bin_plugin_t(ctypes.Structure):
    pass

class struct_r_buf_t(ctypes.Structure):
    pass

class struct_r_bin_arch_options_t(ctypes.Structure):
    pass

class struct_r_bin_write_t(ctypes.Structure):
    pass

struct_r_bin_write_t._pack_ = True # source:False
struct_r_bin_write_t._fields_ = [
    ('scn_resize', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), ctypes.c_uint64))),
    ('scn_perms', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('rpath_del', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_file_t)))),
    ('entry', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), ctypes.c_uint64))),
    ('addlib', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char)))),
]

class struct_r_bin_dbginfo_t(ctypes.Structure):
    pass

struct_r_bin_dbginfo_t._pack_ = True # source:False
struct_r_bin_dbginfo_t._fields_ = [
    ('get_line', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), ctypes.c_uint64, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_int32)))),
]

struct_r_bin_plugin_t._pack_ = True # source:False
struct_r_bin_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('get_sdb', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_sdb_t), POINTER_T(struct_r_bin_file_t)))),
    ('load_buffer', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), POINTER_T(POINTER_T(None)), POINTER_T(struct_r_buf_t), ctypes.c_uint64, POINTER_T(struct_sdb_t)))),
    ('size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_bin_file_t)))),
    ('destroy', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_bin_file_t)))),
    ('check_bytes', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(ctypes.c_ubyte), ctypes.c_uint64))),
    ('check_buffer', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_buf_t)))),
    ('baddr', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_bin_file_t)))),
    ('boffset', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_bin_file_t)))),
    ('binsym', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_addr_t), POINTER_T(struct_r_bin_file_t), ctypes.c_int32))),
    ('entries', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('sections', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('lines', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('symbols', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('imports', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('strings', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('info', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_info_t), POINTER_T(struct_r_bin_file_t)))),
    ('fields', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('libs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('relocs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('trycatch', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('classes', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('mem', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('patch_relocs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t)))),
    ('maps', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('hashes', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_file_t)))),
    ('header', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_bin_file_t)))),
    ('signature', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_file_t), ctypes.c_bool))),
    ('demangle_type', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('dbginfo', POINTER_T(struct_r_bin_dbginfo_t)),
    ('write', POINTER_T(struct_r_bin_write_t)),
    ('get_offset', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_file_t), ctypes.c_int32, ctypes.c_int32))),
    ('get_name', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_file_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_bool))),
    ('get_vaddr', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_bin_file_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64))),
    ('create', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_buf_t), POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(struct_r_bin_arch_options_t)))),
    ('demangle', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('regstate', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_file_t)))),
    ('file_type', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_file_t)))),
    ('minstrlen', ctypes.c_int32),
    ('strfilter', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('user', POINTER_T(None)),
]

struct_r_bin_object_t._pack_ = True # source:False
struct_r_bin_object_t._fields_ = [
    ('baddr', ctypes.c_uint64),
    ('baddr_shift', ctypes.c_int64),
    ('loadaddr', ctypes.c_uint64),
    ('boffset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('obj_size', ctypes.c_uint64),
    ('sections', POINTER_T(struct_r_list_t)),
    ('imports', POINTER_T(struct_r_list_t)),
    ('symbols', POINTER_T(struct_r_list_t)),
    ('entries', POINTER_T(struct_r_list_t)),
    ('fields', POINTER_T(struct_r_list_t)),
    ('libs', POINTER_T(struct_r_list_t)),
    ('relocs', POINTER_T(struct_r_rb_node_t)),
    ('strings', POINTER_T(struct_r_list_t)),
    ('classes', POINTER_T(struct_r_list_t)),
    ('classes_ht', POINTER_T(struct_ht_pp_t)),
    ('methods_ht', POINTER_T(struct_ht_pp_t)),
    ('lines', POINTER_T(struct_r_list_t)),
    ('strings_db', POINTER_T(struct_ht_up_t)),
    ('mem', POINTER_T(struct_r_list_t)),
    ('maps', POINTER_T(struct_r_list_t)),
    ('regstate', POINTER_T(ctypes.c_char)),
    ('info', POINTER_T(struct_r_bin_info_t)),
    ('binsym', POINTER_T(struct_r_bin_addr_t) * 4),
    ('plugin', POINTER_T(struct_r_bin_plugin_t)),
    ('lang', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('kv', POINTER_T(struct_sdb_t)),
    ('addr2klassmethod', POINTER_T(struct_sdb_t)),
    ('bin_obj', POINTER_T(None)),
]

class struct_r_bin_xtr_plugin_t(ctypes.Structure):
    pass

class struct_r_bin_xtr_extract_t(ctypes.Structure):
    pass

struct_r_bin_xtr_plugin_t._pack_ = True # source:False
struct_r_bin_xtr_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('check_buffer', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_buf_t)))),
    ('extract_from_bytes', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_xtr_extract_t), POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_ubyte), ctypes.c_uint64, ctypes.c_int32))),
    ('extract_from_buffer', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_xtr_extract_t), POINTER_T(struct_r_bin_t), POINTER_T(struct_r_buf_t), ctypes.c_int32))),
    ('extractall_from_bytes', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_ubyte), ctypes.c_uint64))),
    ('extractall_from_buffer', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t), POINTER_T(struct_r_buf_t)))),
    ('extract', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_xtr_extract_t), POINTER_T(struct_r_bin_t), ctypes.c_int32))),
    ('extractall', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t)))),
    ('load', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_t)))),
    ('size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_t)))),
    ('destroy', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_bin_t)))),
    ('free_xtr', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

class struct_r_buffer_methods_t(ctypes.Structure):
    pass

struct_r_buffer_methods_t._pack_ = True # source:False
struct_r_buffer_methods_t._fields_ = [
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_buf_t), POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_buf_t)))),
    ('read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_buf_t), POINTER_T(ctypes.c_ubyte), ctypes.c_uint64))),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_buf_t), POINTER_T(ctypes.c_ubyte), ctypes.c_uint64))),
    ('get_size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_buf_t)))),
    ('resize', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_buf_t), ctypes.c_uint64))),
    ('seek', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_buf_t), ctypes.c_int64, ctypes.c_int32))),
    ('get_whole_buf', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_ubyte), POINTER_T(struct_r_buf_t), POINTER_T(ctypes.c_uint64)))),
    ('free_whole_buf', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_buf_t)))),
    ('nonempty_list', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_buf_t)))),
]

struct_r_buf_t._pack_ = True # source:False
struct_r_buf_t._fields_ = [
    ('methods', POINTER_T(struct_r_buffer_methods_t)),
    ('priv', POINTER_T(None)),
    ('whole_buf', POINTER_T(ctypes.c_ubyte)),
    ('readonly', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('Oxff_priv', ctypes.c_int32),
    ('refctr', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

struct_r_bin_file_t._pack_ = True # source:False
struct_r_bin_file_t._fields_ = [
    ('file', POINTER_T(ctypes.c_char)),
    ('fd', ctypes.c_int32),
    ('size', ctypes.c_int32),
    ('rawstr', ctypes.c_int32),
    ('strmode', ctypes.c_int32),
    ('id', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('buf', POINTER_T(struct_r_buf_t)),
    ('offset', ctypes.c_uint64),
    ('o', POINTER_T(struct_r_bin_object_t)),
    ('xtr_obj', POINTER_T(None)),
    ('loadaddr', ctypes.c_uint64),
    ('minstrlen', ctypes.c_int32),
    ('maxstrlen', ctypes.c_int32),
    ('narch', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('curxtr', POINTER_T(struct_r_bin_xtr_plugin_t)),
    ('xtr_data', POINTER_T(struct_r_list_t)),
    ('sdb', POINTER_T(struct_sdb_t)),
    ('sdb_info', POINTER_T(struct_sdb_t)),
    ('sdb_addrinfo', POINTER_T(struct_sdb_t)),
    ('rbin', POINTER_T(struct_r_bin_t)),
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

struct_r_bin_t._pack_ = True # source:False
struct_r_bin_t._fields_ = [
    ('file', POINTER_T(ctypes.c_char)),
    ('cur', POINTER_T(struct_r_bin_file_t)),
    ('narch', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('user', POINTER_T(None)),
    ('debase64', ctypes.c_int32),
    ('minstrlen', ctypes.c_int32),
    ('maxstrlen', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('maxstrbuf', ctypes.c_uint64),
    ('rawstr', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('sdb', POINTER_T(struct_sdb_t)),
    ('ids', POINTER_T(struct_r_id_storage_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('binxtrs', POINTER_T(struct_r_list_t)),
    ('binldrs', POINTER_T(struct_r_list_t)),
    ('binfiles', POINTER_T(struct_r_list_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('loadany', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('iob', struct_r_io_bind_t),
    ('consb', struct_r_cons_bind_t),
    ('force', POINTER_T(ctypes.c_char)),
    ('is_debugger', ctypes.c_int32),
    ('want_dbginfo', ctypes.c_bool),
    ('PADDING_4', ctypes.c_ubyte * 3),
    ('filter', ctypes.c_int32),
    ('strfilter', ctypes.c_char),
    ('PADDING_5', ctypes.c_ubyte * 3),
    ('strpurge', POINTER_T(ctypes.c_char)),
    ('srcdir', POINTER_T(ctypes.c_char)),
    ('prefix', POINTER_T(ctypes.c_char)),
    ('strenc', POINTER_T(ctypes.c_char)),
    ('filter_rules', ctypes.c_uint64),
    ('demanglercmd', ctypes.c_bool),
    ('verbose', ctypes.c_bool),
    ('use_xtr', ctypes.c_bool),
    ('use_ldr', ctypes.c_bool),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('constpool', struct_r_str_constpool_t),
    ('is_reloc_patched', ctypes.c_bool),
    ('PADDING_7', ctypes.c_ubyte * 7),
]

class struct_r_bin_section_t(ctypes.Structure):
    pass

struct_r_bin_bind_t._pack_ = True # source:False
struct_r_bin_bind_t._fields_ = [
    ('bin', POINTER_T(struct_r_bin_t)),
    ('get_offset', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_t), ctypes.c_int32, ctypes.c_int32))),
    ('get_name', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_bool))),
    ('get_sections', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t)))),
    ('get_vsect_at', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_section_t), POINTER_T(struct_r_bin_t), ctypes.c_uint64))),
    ('demangle', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_bool))),
    ('visibility', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct_r_anal_esil_callbacks_t(ctypes.Structure):
    pass

struct_r_anal_esil_callbacks_t._pack_ = True # source:False
struct_r_anal_esil_callbacks_t._fields_ = [
    ('user', POINTER_T(None)),
    ('hook_flag_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64)))),
    ('hook_command', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)))),
    ('hook_mem_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('mem_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('hook_mem_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('mem_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('hook_reg_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64), POINTER_T(ctypes.c_int32)))),
    ('reg_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64), POINTER_T(ctypes.c_int32)))),
    ('hook_reg_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64)))),
    ('reg_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), ctypes.c_uint64))),
]

class struct_r_anal_esil_trace_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('idx', ctypes.c_int32),
    ('end_idx', ctypes.c_int32),
    ('registers', POINTER_T(struct_ht_up_t)),
    ('memory', POINTER_T(struct_ht_up_t)),
    ('arena', POINTER_T(struct_r_reg_arena_t) * 8),
    ('stack_addr', ctypes.c_uint64),
    ('stack_size', ctypes.c_uint64),
    ('stack_data', POINTER_T(ctypes.c_ubyte)),
    ('db', POINTER_T(struct_sdb_t)),
     ]

class struct_r_anal_reil(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('old', ctypes.c_char * 32),
    ('cur', ctypes.c_char * 32),
    ('lastsz', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('reilNextTemp', ctypes.c_uint64),
    ('addr', ctypes.c_uint64),
    ('seq_num', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('skip', ctypes.c_int32),
    ('cmd_count', ctypes.c_int32),
    ('if_buf', ctypes.c_char * 64),
    ('pc', ctypes.c_char * 8),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]

class struct_r_anal_esil_interrupt_t(ctypes.Structure):
    pass

class struct_r_anal_esil_interrupt_handler_t(ctypes.Structure):
    pass

struct_r_anal_esil_interrupt_handler_t._pack_ = True # source:False
struct_r_anal_esil_interrupt_handler_t._fields_ = [
    ('num', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(struct_r_anal_esil_t)))),
    ('cb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

struct_r_anal_esil_interrupt_t._pack_ = True # source:False
struct_r_anal_esil_interrupt_t._fields_ = [
    ('handler', POINTER_T(struct_r_anal_esil_interrupt_handler_t)),
    ('user', POINTER_T(None)),
    ('src_id', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct_r_anal_esil_t._pack_ = True # source:False
struct_r_anal_esil_t._fields_ = [
    ('anal', POINTER_T(struct_r_anal_t)),
    ('stack', POINTER_T(POINTER_T(ctypes.c_char))),
    ('addrmask', ctypes.c_uint64),
    ('stacksize', ctypes.c_int32),
    ('stackptr', ctypes.c_int32),
    ('skip', ctypes.c_uint32),
    ('nowrite', ctypes.c_int32),
    ('iotrap', ctypes.c_int32),
    ('exectrap', ctypes.c_int32),
    ('repeat', ctypes.c_int32),
    ('parse_stop', ctypes.c_int32),
    ('parse_goto', ctypes.c_int32),
    ('parse_goto_count', ctypes.c_int32),
    ('verbose', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('flags', ctypes.c_uint64),
    ('address', ctypes.c_uint64),
    ('stack_addr', ctypes.c_uint64),
    ('stack_size', ctypes.c_uint32),
    ('delay', ctypes.c_int32),
    ('jump_target', ctypes.c_uint64),
    ('jump_target_set', ctypes.c_int32),
    ('trap', ctypes.c_int32),
    ('trap_code', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('old', ctypes.c_uint64),
    ('cur', ctypes.c_uint64),
    ('lastsz', ctypes.c_ubyte),
    ('PADDING_2', ctypes.c_ubyte * 7),
    ('ops', POINTER_T(struct_ht_pp_t)),
    ('current_opstr', POINTER_T(ctypes.c_char)),
    ('sources', POINTER_T(struct_r_id_storage_t)),
    ('interrupts', POINTER_T(struct_c__SA_dict)),
    ('intr0', POINTER_T(struct_r_anal_esil_interrupt_t)),
    ('stats', POINTER_T(struct_sdb_t)),
    ('trace', POINTER_T(struct_r_anal_esil_trace_t)),
    ('cb', struct_r_anal_esil_callbacks_t),
    ('Reil', POINTER_T(struct_r_anal_reil)),
    ('cmd_step', POINTER_T(ctypes.c_char)),
    ('cmd_step_out', POINTER_T(ctypes.c_char)),
    ('cmd_intr', POINTER_T(ctypes.c_char)),
    ('cmd_trap', POINTER_T(ctypes.c_char)),
    ('cmd_mdev', POINTER_T(ctypes.c_char)),
    ('cmd_todo', POINTER_T(ctypes.c_char)),
    ('cmd_ioer', POINTER_T(ctypes.c_char)),
    ('mdev_range', POINTER_T(ctypes.c_char)),
    ('cmd', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64))),
    ('user', POINTER_T(None)),
    ('stack_fd', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
]

class struct_r_anal_options_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('depth', ctypes.c_int32),
    ('graph_depth', ctypes.c_int32),
    ('vars', ctypes.c_bool),
    ('varname_stack', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('cjmpref', ctypes.c_int32),
    ('jmpref', ctypes.c_int32),
    ('jmpabove', ctypes.c_int32),
    ('ijmp', ctypes.c_bool),
    ('jmpmid', ctypes.c_bool),
    ('loads', ctypes.c_bool),
    ('ignbithints', ctypes.c_bool),
    ('followdatarefs', ctypes.c_int32),
    ('searchstringrefs', ctypes.c_int32),
    ('followbrokenfcnsrefs', ctypes.c_int32),
    ('bb_max_size', ctypes.c_int32),
    ('trycatch', ctypes.c_bool),
    ('norevisit', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('afterjmp', ctypes.c_int32),
    ('recont', ctypes.c_int32),
    ('noncode', ctypes.c_int32),
    ('nopskip', ctypes.c_int32),
    ('hpskip', ctypes.c_int32),
    ('jmptbl', ctypes.c_int32),
    ('nonull', ctypes.c_int32),
    ('pushret', ctypes.c_bool),
    ('armthumb', ctypes.c_bool),
    ('endsize', ctypes.c_bool),
    ('delay', ctypes.c_bool),
    ('tailcall', ctypes.c_int32),
    ('retpoline', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 3),
     ]

class struct_r_syscall_t(ctypes.Structure):
    pass

class struct__IO_FILE(ctypes.Structure):
    pass

class struct__IO_codecvt(ctypes.Structure):
    pass

class struct__IO_wide_data(ctypes.Structure):
    pass

class struct__IO_marker(ctypes.Structure):
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

class struct_r_syscall_port_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('port', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
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


# values for enumeration 'c__EA_RAnalCPPABI'
c__EA_RAnalCPPABI__enumvalues = {
    0: 'R_ANAL_CPP_ABI_ITANIUM',
    1: 'R_ANAL_CPP_ABI_MSVC',
}
R_ANAL_CPP_ABI_ITANIUM = 0
R_ANAL_CPP_ABI_MSVC = 1
c__EA_RAnalCPPABI = ctypes.c_int # enum
class struct_r_interval_tree_t(ctypes.Structure):
    pass

class struct_r_interval_node_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('node', struct_r_rb_node_t),
    ('start', ctypes.c_uint64),
    ('end', ctypes.c_uint64),
    ('max_end', ctypes.c_uint64),
    ('data', POINTER_T(None)),
     ]

struct_r_interval_tree_t._pack_ = True # source:False
struct_r_interval_tree_t._fields_ = [
    ('root', POINTER_T(struct_r_interval_node_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

struct_r_anal_t._pack_ = True # source:False
struct_r_anal_t._fields_ = [
    ('cpu', POINTER_T(ctypes.c_char)),
    ('os', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('lineswidth', ctypes.c_int32),
    ('big_endian', ctypes.c_int32),
    ('sleep', ctypes.c_int32),
    ('cpp_abi', c__EA_RAnalCPPABI),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('user', POINTER_T(None)),
    ('gp', ctypes.c_uint64),
    ('bb_tree', POINTER_T(struct_r_rb_node_t)),
    ('fcns', POINTER_T(struct_r_list_t)),
    ('ht_addr_fun', POINTER_T(struct_ht_up_t)),
    ('ht_name_fun', POINTER_T(struct_ht_pp_t)),
    ('reg', POINTER_T(struct_r_reg_t)),
    ('last_disasm_reg', POINTER_T(ctypes.c_ubyte)),
    ('syscall', POINTER_T(struct_r_syscall_t)),
    ('diff_ops', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('diff_thbb', ctypes.c_double),
    ('diff_thfcn', ctypes.c_double),
    ('iob', struct_r_io_bind_t),
    ('flb', struct_r_flag_bind_t),
    ('flg_class_set', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32))),
    ('flg_class_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))),
    ('flg_fcn_set', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32))),
    ('binb', struct_r_bin_bind_t),
    ('coreb', struct_r_core_bind_t),
    ('maxreflines', ctypes.c_int32),
    ('esil_goto_limit', ctypes.c_int32),
    ('pcalign', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('esil', POINTER_T(struct_r_anal_esil_t)),
    ('cur', POINTER_T(struct_r_anal_plugin_t)),
    ('limit', POINTER_T(struct_r_anal_range_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('sdb_types', POINTER_T(struct_sdb_t)),
    ('sdb_fmts', POINTER_T(struct_sdb_t)),
    ('sdb_zigns', POINTER_T(struct_sdb_t)),
    ('dict_refs', POINTER_T(struct_ht_up_t)),
    ('dict_xrefs', POINTER_T(struct_ht_up_t)),
    ('recursive_noreturn', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 7),
    ('zign_spaces', struct_r_spaces_t),
    ('zign_path', POINTER_T(ctypes.c_char)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('sdb', POINTER_T(struct_sdb_t)),
    ('sdb_pins', POINTER_T(struct_sdb_t)),
    ('addr_hints', POINTER_T(struct_ht_up_t)),
    ('arch_hints', POINTER_T(struct_r_rb_node_t)),
    ('bits_hints', POINTER_T(struct_r_rb_node_t)),
    ('hint_cbs', struct_r_anal_hint_cb_t),
    ('meta', struct_r_interval_tree_t),
    ('meta_spaces', struct_r_spaces_t),
    ('sdb_cc', POINTER_T(struct_sdb_t)),
    ('sdb_classes', POINTER_T(struct_sdb_t)),
    ('sdb_classes_attrs', POINTER_T(struct_sdb_t)),
    ('cb', struct_r_anal_callbacks_t),
    ('opt', struct_r_anal_options_t),
    ('reflines', POINTER_T(struct_r_list_t)),
    ('columnSort', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(None)))),
    ('stackptr', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('log', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)))),
    ('read_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('verbose', ctypes.c_bool),
    ('PADDING_5', ctypes.c_ubyte * 3),
    ('seggrn', ctypes.c_int32),
    ('flag_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64))),
    ('ev', POINTER_T(struct_r_event_t)),
    ('imports', POINTER_T(struct_r_list_t)),
    ('visited', POINTER_T(struct_ht_up_t)),
    ('constpool', struct_r_str_constpool_t),
    ('leaddrs', POINTER_T(struct_r_list_t)),
]

struct_r_anal_function_t._pack_ = True # source:False
struct_r_anal_function_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('type', ctypes.c_int32),
    ('cc', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('labels', POINTER_T(struct_ht_up_t)),
    ('label_addrs', POINTER_T(struct_ht_pp_t)),
    ('vars', struct_r_pvector_t),
    ('inst_vars', POINTER_T(struct_ht_up_t)),
    ('reg_save_area', ctypes.c_uint64),
    ('bp_off', ctypes.c_int64),
    ('stack', ctypes.c_int64),
    ('maxstack', ctypes.c_int32),
    ('ninstr', ctypes.c_int32),
    ('folded', ctypes.c_bool),
    ('is_pure', ctypes.c_bool),
    ('is_variadic', ctypes.c_bool),
    ('has_changed', ctypes.c_bool),
    ('bp_frame', ctypes.c_bool),
    ('is_noreturn', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('fingerprint', POINTER_T(ctypes.c_ubyte)),
    ('fingerprint_size', ctypes.c_uint64),
    ('diff', POINTER_T(struct_r_anal_diff_t)),
    ('bbs', POINTER_T(struct_r_list_t)),
    ('meta', struct_r_anal_fcn_meta_t),
    ('imports', POINTER_T(struct_r_list_t)),
    ('anal', POINTER_T(struct_r_anal_t)),
]


# values for enumeration 'c__EA_RAnalOpFamily'
c__EA_RAnalOpFamily__enumvalues = {
    -1: 'R_ANAL_OP_FAMILY_UNKNOWN',
    0: 'R_ANAL_OP_FAMILY_CPU',
    1: 'R_ANAL_OP_FAMILY_FPU',
    2: 'R_ANAL_OP_FAMILY_MMX',
    3: 'R_ANAL_OP_FAMILY_SSE',
    4: 'R_ANAL_OP_FAMILY_PRIV',
    5: 'R_ANAL_OP_FAMILY_CRYPTO',
    6: 'R_ANAL_OP_FAMILY_THREAD',
    7: 'R_ANAL_OP_FAMILY_VIRT',
    8: 'R_ANAL_OP_FAMILY_SECURITY',
    9: 'R_ANAL_OP_FAMILY_IO',
    10: 'R_ANAL_OP_FAMILY_LAST',
}
R_ANAL_OP_FAMILY_UNKNOWN = -1
R_ANAL_OP_FAMILY_CPU = 0
R_ANAL_OP_FAMILY_FPU = 1
R_ANAL_OP_FAMILY_MMX = 2
R_ANAL_OP_FAMILY_SSE = 3
R_ANAL_OP_FAMILY_PRIV = 4
R_ANAL_OP_FAMILY_CRYPTO = 5
R_ANAL_OP_FAMILY_THREAD = 6
R_ANAL_OP_FAMILY_VIRT = 7
R_ANAL_OP_FAMILY_SECURITY = 8
R_ANAL_OP_FAMILY_IO = 9
R_ANAL_OP_FAMILY_LAST = 10
c__EA_RAnalOpFamily = ctypes.c_int # enum

# values for enumeration 'c__EA_RAnalOpPrefix'
c__EA_RAnalOpPrefix__enumvalues = {
    1: 'R_ANAL_OP_PREFIX_COND',
    2: 'R_ANAL_OP_PREFIX_REP',
    4: 'R_ANAL_OP_PREFIX_REPNE',
    8: 'R_ANAL_OP_PREFIX_LOCK',
    16: 'R_ANAL_OP_PREFIX_LIKELY',
    32: 'R_ANAL_OP_PREFIX_UNLIKELY',
}
R_ANAL_OP_PREFIX_COND = 1
R_ANAL_OP_PREFIX_REP = 2
R_ANAL_OP_PREFIX_REPNE = 4
R_ANAL_OP_PREFIX_LOCK = 8
R_ANAL_OP_PREFIX_LIKELY = 16
R_ANAL_OP_PREFIX_UNLIKELY = 32
c__EA_RAnalOpPrefix = ctypes.c_int # enum

# values for enumeration 'c__EA__RAnalCond'
c__EA__RAnalCond__enumvalues = {
    0: 'R_ANAL_COND_AL',
    1: 'R_ANAL_COND_EQ',
    2: 'R_ANAL_COND_NE',
    3: 'R_ANAL_COND_GE',
    4: 'R_ANAL_COND_GT',
    5: 'R_ANAL_COND_LE',
    6: 'R_ANAL_COND_LT',
    7: 'R_ANAL_COND_NV',
    8: 'R_ANAL_COND_HS',
    9: 'R_ANAL_COND_LO',
    10: 'R_ANAL_COND_MI',
    11: 'R_ANAL_COND_PL',
    12: 'R_ANAL_COND_VS',
    13: 'R_ANAL_COND_VC',
    14: 'R_ANAL_COND_HI',
    15: 'R_ANAL_COND_LS',
}
R_ANAL_COND_AL = 0
R_ANAL_COND_EQ = 1
R_ANAL_COND_NE = 2
R_ANAL_COND_GE = 3
R_ANAL_COND_GT = 4
R_ANAL_COND_LE = 5
R_ANAL_COND_LT = 6
R_ANAL_COND_NV = 7
R_ANAL_COND_HS = 8
R_ANAL_COND_LO = 9
R_ANAL_COND_MI = 10
R_ANAL_COND_PL = 11
R_ANAL_COND_VS = 12
R_ANAL_COND_VC = 13
R_ANAL_COND_HI = 14
R_ANAL_COND_LS = 15
c__EA__RAnalCond = ctypes.c_int # enum

# values for enumeration 'c__EA_RAnalStackOp'
c__EA_RAnalStackOp__enumvalues = {
    0: 'R_ANAL_STACK_NULL',
    1: 'R_ANAL_STACK_NOP',
    2: 'R_ANAL_STACK_INC',
    3: 'R_ANAL_STACK_GET',
    4: 'R_ANAL_STACK_SET',
    5: 'R_ANAL_STACK_RESET',
    6: 'R_ANAL_STACK_ALIGN',
}
R_ANAL_STACK_NULL = 0
R_ANAL_STACK_NOP = 1
R_ANAL_STACK_INC = 2
R_ANAL_STACK_GET = 3
R_ANAL_STACK_SET = 4
R_ANAL_STACK_RESET = 5
R_ANAL_STACK_ALIGN = 6
c__EA_RAnalStackOp = ctypes.c_int # enum
class struct_r_anal_switch_obj_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('min_val', ctypes.c_uint64),
    ('def_val', ctypes.c_uint64),
    ('max_val', ctypes.c_uint64),
    ('cases', POINTER_T(struct_r_list_t)),
     ]

class struct_r_anal_hint_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('ptr', ctypes.c_uint64),
    ('val', ctypes.c_uint64),
    ('jump', ctypes.c_uint64),
    ('fail', ctypes.c_uint64),
    ('ret', ctypes.c_uint64),
    ('arch', POINTER_T(ctypes.c_char)),
    ('opcode', POINTER_T(ctypes.c_char)),
    ('syntax', POINTER_T(ctypes.c_char)),
    ('esil', POINTER_T(ctypes.c_char)),
    ('offset', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('size', ctypes.c_uint64),
    ('bits', ctypes.c_int32),
    ('new_bits', ctypes.c_int32),
    ('immbase', ctypes.c_int32),
    ('high', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('nword', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('stackframe', ctypes.c_uint64),
     ]

class struct_r_anal_bind_t(ctypes.Structure):
    pass

struct_r_anal_bind_t._pack_ = True # source:False
struct_r_anal_bind_t._fields_ = [
    ('anal', POINTER_T(struct_r_anal_t)),
    ('get_fcn_in', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32))),
    ('get_hint', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_hint_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64))),
]


# values for enumeration 'c__EA_RAnalValueAccess'
c__EA_RAnalValueAccess__enumvalues = {
    0: 'R_ANAL_ACC_UNKNOWN',
    1: 'R_ANAL_ACC_R',
    2: 'R_ANAL_ACC_W',
}
R_ANAL_ACC_UNKNOWN = 0
R_ANAL_ACC_R = 1
R_ANAL_ACC_W = 2
c__EA_RAnalValueAccess = ctypes.c_int # enum

# values for enumeration 'c__EA_RAnalValueType'
c__EA_RAnalValueType__enumvalues = {
    0: 'R_ANAL_VAL_REG',
    1: 'R_ANAL_VAL_MEM',
    2: 'R_ANAL_VAL_IMM',
}
R_ANAL_VAL_REG = 0
R_ANAL_VAL_MEM = 1
R_ANAL_VAL_IMM = 2
c__EA_RAnalValueType = ctypes.c_int # enum
class struct_r_anal_value_t(ctypes.Structure):
    pass

class struct_r_reg_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_int32),
    ('size', ctypes.c_int32),
    ('offset', ctypes.c_int32),
    ('packed_size', ctypes.c_int32),
    ('is_float', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('flags', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
    ('index', ctypes.c_int32),
    ('arena', ctypes.c_int32),
     ]

struct_r_anal_value_t._pack_ = True # source:False
struct_r_anal_value_t._fields_ = [
    ('type', c__EA_RAnalValueType),
    ('access', c__EA_RAnalValueAccess),
    ('absolute', ctypes.c_int32),
    ('memref', ctypes.c_int32),
    ('base', ctypes.c_uint64),
    ('delta', ctypes.c_int64),
    ('imm', ctypes.c_int64),
    ('mul', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('seg', POINTER_T(struct_r_reg_item_t)),
    ('reg', POINTER_T(struct_r_reg_item_t)),
    ('regdelta', POINTER_T(struct_r_reg_item_t)),
]


# values for enumeration 'c__EA_RAnalOpDirection'
c__EA_RAnalOpDirection__enumvalues = {
    1: 'R_ANAL_OP_DIR_READ',
    2: 'R_ANAL_OP_DIR_WRITE',
    4: 'R_ANAL_OP_DIR_EXEC',
    8: 'R_ANAL_OP_DIR_REF',
}
R_ANAL_OP_DIR_READ = 1
R_ANAL_OP_DIR_WRITE = 2
R_ANAL_OP_DIR_EXEC = 4
R_ANAL_OP_DIR_REF = 8
c__EA_RAnalOpDirection = ctypes.c_int # enum

# values for enumeration 'r_anal_data_type_t'
r_anal_data_type_t__enumvalues = {
    0: 'R_ANAL_DATATYPE_NULL',
    1: 'R_ANAL_DATATYPE_ARRAY',
    2: 'R_ANAL_DATATYPE_OBJECT',
    3: 'R_ANAL_DATATYPE_STRING',
    4: 'R_ANAL_DATATYPE_CLASS',
    5: 'R_ANAL_DATATYPE_BOOLEAN',
    6: 'R_ANAL_DATATYPE_INT16',
    7: 'R_ANAL_DATATYPE_INT32',
    8: 'R_ANAL_DATATYPE_INT64',
    9: 'R_ANAL_DATATYPE_FLOAT',
}
R_ANAL_DATATYPE_NULL = 0
R_ANAL_DATATYPE_ARRAY = 1
R_ANAL_DATATYPE_OBJECT = 2
R_ANAL_DATATYPE_STRING = 3
R_ANAL_DATATYPE_CLASS = 4
R_ANAL_DATATYPE_BOOLEAN = 5
R_ANAL_DATATYPE_INT16 = 6
R_ANAL_DATATYPE_INT32 = 7
R_ANAL_DATATYPE_INT64 = 8
R_ANAL_DATATYPE_FLOAT = 9
r_anal_data_type_t = ctypes.c_int # enum
class struct_c__SA_RStrBuf(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('buf', ctypes.c_char * 32),
    ('len', ctypes.c_uint64),
    ('ptr', POINTER_T(ctypes.c_char)),
    ('ptrlen', ctypes.c_uint64),
    ('weakref', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
     ]

struct_r_anal_op_t._pack_ = True # source:False
struct_r_anal_op_t._fields_ = [
    ('mnemonic', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('type', ctypes.c_uint32),
    ('prefix', c__EA_RAnalOpPrefix),
    ('type2', ctypes.c_uint32),
    ('stackop', c__EA_RAnalStackOp),
    ('cond', c__EA__RAnalCond),
    ('size', ctypes.c_int32),
    ('nopcode', ctypes.c_int32),
    ('cycles', ctypes.c_int32),
    ('failcycles', ctypes.c_int32),
    ('family', c__EA_RAnalOpFamily),
    ('id', ctypes.c_int32),
    ('eob', ctypes.c_bool),
    ('sign', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('delay', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('jump', ctypes.c_uint64),
    ('fail', ctypes.c_uint64),
    ('direction', c__EA_RAnalOpDirection),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('ptr', ctypes.c_int64),
    ('val', ctypes.c_uint64),
    ('ptrsize', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('stackptr', ctypes.c_int64),
    ('refptr', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('src', POINTER_T(struct_r_anal_value_t) * 3),
    ('dst', POINTER_T(struct_r_anal_value_t)),
    ('access', POINTER_T(struct_r_list_t)),
    ('esil', struct_c__SA_RStrBuf),
    ('opex', struct_c__SA_RStrBuf),
    ('reg', POINTER_T(ctypes.c_char)),
    ('ireg', POINTER_T(ctypes.c_char)),
    ('scale', ctypes.c_int32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('disp', ctypes.c_uint64),
    ('switch_op', POINTER_T(struct_r_anal_switch_obj_t)),
    ('hint', struct_r_anal_hint_t),
    ('datatype', r_anal_data_type_t),
    ('PADDING_6', ctypes.c_ubyte * 4),
]

class struct_r_anal_cond_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arg', POINTER_T(struct_r_anal_value_t) * 2),
     ]

struct_r_anal_bb_t._pack_ = True # source:False
struct_r_anal_bb_t._fields_ = [
    ('_rb', struct_r_rb_node_t),
    ('_max_end', ctypes.c_uint64),
    ('addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('jump', ctypes.c_uint64),
    ('fail', ctypes.c_uint64),
    ('traced', ctypes.c_bool),
    ('folded', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('colorize', ctypes.c_uint32),
    ('fingerprint', POINTER_T(ctypes.c_ubyte)),
    ('diff', POINTER_T(struct_r_anal_diff_t)),
    ('cond', POINTER_T(struct_r_anal_cond_t)),
    ('switch_op', POINTER_T(struct_r_anal_switch_obj_t)),
    ('op_pos', POINTER_T(ctypes.c_uint16)),
    ('op_bytes', POINTER_T(ctypes.c_ubyte)),
    ('parent_reg_arena', POINTER_T(ctypes.c_ubyte)),
    ('op_pos_size', ctypes.c_int32),
    ('ninstr', ctypes.c_int32),
    ('stackptr', ctypes.c_int32),
    ('parent_stackptr', ctypes.c_int32),
    ('cmpval', ctypes.c_uint64),
    ('cmpreg', POINTER_T(ctypes.c_char)),
    ('fcns', POINTER_T(struct_r_list_t)),
    ('anal', POINTER_T(struct_r_anal_t)),
    ('ref', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

class struct_r_asm_op_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('size', ctypes.c_int32),
    ('bitsize', ctypes.c_int32),
    ('payload', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('buf', struct_c__SA_RStrBuf),
    ('buf_asm', struct_c__SA_RStrBuf),
    ('buf_inc', POINTER_T(struct_r_buf_t)),
     ]

class struct_r_asm_t(ctypes.Structure):
    pass

class struct_r_asm_plugin_t(ctypes.Structure):
    pass

struct_r_asm_plugin_t._pack_ = True # source:False
struct_r_asm_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('cpus', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('user', POINTER_T(None)),
    ('bits', ctypes.c_int32),
    ('endian', ctypes.c_int32),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None)))),
    ('disassemble', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_asm_t), POINTER_T(struct_r_asm_op_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('assemble', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_asm_t), POINTER_T(struct_r_asm_op_t), POINTER_T(ctypes.c_char)))),
    ('modify', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_asm_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_uint64))),
    ('mnemonics', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_asm_t), ctypes.c_int32, ctypes.c_bool))),
    ('features', POINTER_T(ctypes.c_char)),
]

class struct_r_parse_t(ctypes.Structure):
    pass

class struct_r_parse_plugin_t(ctypes.Structure):
    pass

struct_r_parse_plugin_t._pack_ = True # source:False
struct_r_parse_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_parse_t), POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_parse_t), POINTER_T(None)))),
    ('parse', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_parse_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('assemble', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_parse_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('filter', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_parse_t), ctypes.c_uint64, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_bool))),
    ('varsub', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_parse_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('replace', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char)), POINTER_T(ctypes.c_char)))),
]

struct_r_parse_t._pack_ = True # source:False
struct_r_parse_t._fields_ = [
    ('user', POINTER_T(None)),
    ('flagspace', POINTER_T(struct_r_space_t)),
    ('notin_flagspace', POINTER_T(struct_r_space_t)),
    ('pseudo', ctypes.c_bool),
    ('subreg', ctypes.c_bool),
    ('subrel', ctypes.c_bool),
    ('subtail', ctypes.c_bool),
    ('localvar_only', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('subrel_addr', ctypes.c_uint64),
    ('maxflagnamelen', ctypes.c_int32),
    ('minval', ctypes.c_int32),
    ('retleave_asm', POINTER_T(ctypes.c_char)),
    ('cur', POINTER_T(struct_r_parse_plugin_t)),
    ('parsers', POINTER_T(struct_r_list_t)),
    ('varlist', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_anal_function_t), ctypes.c_int32))),
    ('get_ptr_at', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_anal_function_t), ctypes.c_int64, ctypes.c_uint64))),
    ('get_reg_at', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_function_t), ctypes.c_int64, ctypes.c_uint64))),
    ('get_op_ireg', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('analb', struct_r_anal_bind_t),
    ('flag_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64))),
    ('label_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64))),
]

struct_r_asm_t._pack_ = True # source:False
struct_r_asm_t._fields_ = [
    ('cpu', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('big_endian', ctypes.c_int32),
    ('syntax', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pc', ctypes.c_uint64),
    ('user', POINTER_T(None)),
    ('cur', POINTER_T(struct_r_asm_plugin_t)),
    ('acur', POINTER_T(struct_r_asm_plugin_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('binb', struct_r_bin_bind_t),
    ('ifilter', POINTER_T(struct_r_parse_t)),
    ('ofilter', POINTER_T(struct_r_parse_t)),
    ('pair', POINTER_T(struct_sdb_t)),
    ('syscall', POINTER_T(struct_r_syscall_t)),
    ('num', POINTER_T(struct_r_num_t)),
    ('features', POINTER_T(ctypes.c_char)),
    ('invhex', ctypes.c_int32),
    ('pcalign', ctypes.c_int32),
    ('dataalign', ctypes.c_int32),
    ('bitshift', ctypes.c_int32),
    ('immdisp', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('flags', POINTER_T(struct_ht_pp_t)),
    ('seggrn', ctypes.c_int32),
    ('pseudo', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 3),
]

class struct_r_bin_xtr_metadata_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('arch', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('libname', POINTER_T(ctypes.c_char)),
    ('machine', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('xtr_type', POINTER_T(ctypes.c_char)),
     ]

struct_r_bin_xtr_extract_t._pack_ = True # source:False
struct_r_bin_xtr_extract_t._fields_ = [
    ('file', POINTER_T(ctypes.c_char)),
    ('buf', POINTER_T(struct_r_buf_t)),
    ('size', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('baddr', ctypes.c_uint64),
    ('laddr', ctypes.c_uint64),
    ('file_count', ctypes.c_int32),
    ('loaded', ctypes.c_int32),
    ('metadata', POINTER_T(struct_r_bin_xtr_metadata_t)),
]

struct_r_bin_arch_options_t._pack_ = True # source:False
struct_r_bin_arch_options_t._fields_ = [
    ('arch', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct_r_bin_section_t._pack_ = True # source:False
struct_r_bin_section_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('size', ctypes.c_uint64),
    ('vsize', ctypes.c_uint64),
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('perm', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arch', POINTER_T(ctypes.c_char)),
    ('format', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('has_strings', ctypes.c_bool),
    ('add', ctypes.c_bool),
    ('is_data', ctypes.c_bool),
    ('is_segment', ctypes.c_bool),
]

r_egg_version = _libr_egg.r_egg_version
r_egg_version.restype = POINTER_T(ctypes.c_char)
r_egg_version.argtypes = []
class struct_r_egg_plugin_t(ctypes.Structure):
    pass

struct_r_egg_plugin_t._pack_ = True # source:False
struct_r_egg_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('build', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_buf_t), POINTER_T(None)))),
]

REggPlugin = struct_r_egg_plugin_t
class struct_r_egg_lang_t(ctypes.Structure):
    pass

class struct_r_egg_lang_t_1(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arg', POINTER_T(ctypes.c_char)),
     ]

class struct_r_egg_lang_t_2(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('content', POINTER_T(ctypes.c_char)),
     ]

class struct_r_egg_lang_t_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('body', POINTER_T(ctypes.c_char)),
     ]

struct_r_egg_lang_t._pack_ = True # source:False
struct_r_egg_lang_t._fields_ = [
    ('pushargs', ctypes.c_int32),
    ('nalias', ctypes.c_int32),
    ('nsyscalls', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('conditionstr', POINTER_T(ctypes.c_char)),
    ('syscallbody', POINTER_T(ctypes.c_char)),
    ('includefile', POINTER_T(ctypes.c_char)),
    ('setenviron', POINTER_T(ctypes.c_char)),
    ('mathline', POINTER_T(ctypes.c_char)),
    ('commentmode', ctypes.c_int32),
    ('varsize', ctypes.c_int32),
    ('varxs', ctypes.c_int32),
    ('lastctxdelta', ctypes.c_int32),
    ('nargs', ctypes.c_int32),
    ('docall', ctypes.c_int32),
    ('nfunctions', ctypes.c_int32),
    ('nbrackets', ctypes.c_int32),
    ('slurpin', ctypes.c_int32),
    ('slurp', ctypes.c_int32),
    ('line', ctypes.c_int32),
    ('elem', ctypes.c_char * 1024),
    ('attsyntax', ctypes.c_int32),
    ('elem_n', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('callname', POINTER_T(ctypes.c_char)),
    ('endframe', POINTER_T(ctypes.c_char)),
    ('ctxpush', POINTER_T(ctypes.c_char) * 32),
    ('file', POINTER_T(ctypes.c_char)),
    ('dstvar', POINTER_T(ctypes.c_char)),
    ('dstval', POINTER_T(ctypes.c_char)),
    ('includedir', POINTER_T(ctypes.c_char)),
    ('ifelse_table', POINTER_T(ctypes.c_char) * 32 * 32),
    ('ndstval', ctypes.c_int32),
    ('skipline', ctypes.c_int32),
    ('quoteline', ctypes.c_int32),
    ('quotelinevar', ctypes.c_int32),
    ('stackframe', ctypes.c_int32),
    ('stackfixed', ctypes.c_int32),
    ('oc', ctypes.c_int32),
    ('mode', ctypes.c_int32),
    ('inlinectr', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('inlines', struct_r_egg_lang_t_0 * 256),
    ('ninlines', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('syscalls', struct_r_egg_lang_t_1 * 256),
    ('aliases', struct_r_egg_lang_t_2 * 256),
    ('nested', POINTER_T(ctypes.c_char) * 32),
    ('nested_callname', POINTER_T(ctypes.c_char) * 32),
    ('nestedi', ctypes.c_int32 * 32),
]

REggLang = struct_r_egg_lang_t
class struct_r_egg_t(ctypes.Structure):
    pass

class struct_r_egg_emit_t(ctypes.Structure):
    pass

struct_r_egg_emit_t._pack_ = True # source:False
struct_r_egg_emit_t._fields_ = [
    ('arch', POINTER_T(ctypes.c_char)),
    ('size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('retvar', POINTER_T(ctypes.c_char)),
    ('regs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_egg_t), ctypes.c_int32))),
    ('init', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t)))),
    ('call', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('jmp', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('frame', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32))),
    ('syscall', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_egg_t), ctypes.c_int32))),
    ('trap', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t)))),
    ('frame_end', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32, ctypes.c_int32))),
    ('comment', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)))),
    ('push_arg', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('set_string', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('equ', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('get_result', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)))),
    ('restore_stack', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32))),
    ('syscall_args', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32))),
    ('get_var', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('get_ar', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('while_end', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)))),
    ('load', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('load_ptr', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)))),
    ('branch', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('mathop', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('get_while_end', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
]

struct_r_egg_t._pack_ = True # source:False
struct_r_egg_t._fields_ = [
    ('src', POINTER_T(struct_r_buf_t)),
    ('buf', POINTER_T(struct_r_buf_t)),
    ('bin', POINTER_T(struct_r_buf_t)),
    ('list', POINTER_T(struct_r_list_t)),
    ('rasm', POINTER_T(struct_r_asm_t)),
    ('syscall', POINTER_T(struct_r_syscall_t)),
    ('lang', REggLang),
    ('db', POINTER_T(struct_sdb_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('patches', POINTER_T(struct_r_list_t)),
    ('remit', POINTER_T(struct_r_egg_emit_t)),
    ('arch', ctypes.c_int32),
    ('endian', ctypes.c_int32),
    ('bits', ctypes.c_int32),
    ('os', ctypes.c_uint32),
    ('context', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

REgg = struct_r_egg_t
REggEmit = struct_r_egg_emit_t
r_egg_new = _libr_egg.r_egg_new
r_egg_new.restype = POINTER_T(struct_r_egg_t)
r_egg_new.argtypes = []
r_egg_lang_init = _libr_egg.r_egg_lang_init
r_egg_lang_init.restype = None
r_egg_lang_init.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_lang_free = _libr_egg.r_egg_lang_free
r_egg_lang_free.restype = None
r_egg_lang_free.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_to_string = _libr_egg.r_egg_to_string
r_egg_to_string.restype = POINTER_T(ctypes.c_char)
r_egg_to_string.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_free = _libr_egg.r_egg_free
r_egg_free.restype = None
r_egg_free.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_add = _libr_egg.r_egg_add
r_egg_add.restype = ctypes.c_int32
r_egg_add.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(struct_r_egg_plugin_t)]
r_egg_reset = _libr_egg.r_egg_reset
r_egg_reset.restype = None
r_egg_reset.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_setup = _libr_egg.r_egg_setup
r_egg_setup.restype = ctypes.c_int32
r_egg_setup.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_egg_include = _libr_egg.r_egg_include
r_egg_include.restype = ctypes.c_int32
r_egg_include.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_egg_load = _libr_egg.r_egg_load
r_egg_load.restype = None
r_egg_load.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_egg_syscall = _libr_egg.r_egg_syscall
r_egg_syscall.restype = None
r_egg_syscall.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_alloc = _libr_egg.r_egg_alloc
r_egg_alloc.restype = None
r_egg_alloc.argtypes = [POINTER_T(struct_r_egg_t), ctypes.c_int32]
r_egg_label = _libr_egg.r_egg_label
r_egg_label.restype = None
r_egg_label.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_raw = _libr_egg.r_egg_raw
r_egg_raw.restype = ctypes.c_int32
r_egg_raw.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_egg_encode = _libr_egg.r_egg_encode
r_egg_encode.restype = ctypes.c_int32
r_egg_encode.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_shellcode = _libr_egg.r_egg_shellcode
r_egg_shellcode.restype = ctypes.c_int32
r_egg_shellcode.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_option_set = _libr_egg.r_egg_option_set
r_egg_option_set.restype = None
r_egg_option_set.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_egg_option_get = _libr_egg.r_egg_option_get
r_egg_option_get.restype = POINTER_T(ctypes.c_char)
r_egg_option_get.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_if = _libr_egg.r_egg_if
r_egg_if.restype = None
r_egg_if.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), ctypes.c_char, ctypes.c_int32]
r_egg_printf = _libr_egg.r_egg_printf
r_egg_printf.restype = None
r_egg_printf.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_compile = _libr_egg.r_egg_compile
r_egg_compile.restype = ctypes.c_int32
r_egg_compile.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_padding = _libr_egg.r_egg_padding
r_egg_padding.restype = ctypes.c_int32
r_egg_padding.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_assemble = _libr_egg.r_egg_assemble
r_egg_assemble.restype = ctypes.c_bool
r_egg_assemble.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_assemble_asm = _libr_egg.r_egg_assemble_asm
r_egg_assemble_asm.restype = ctypes.c_bool
r_egg_assemble_asm.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(POINTER_T(ctypes.c_char))]
r_egg_pattern = _libr_egg.r_egg_pattern
r_egg_pattern.restype = None
r_egg_pattern.argtypes = [POINTER_T(struct_r_egg_t), ctypes.c_int32]
r_egg_get_bin = _libr_egg.r_egg_get_bin
r_egg_get_bin.restype = POINTER_T(struct_r_buf_t)
r_egg_get_bin.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_get_source = _libr_egg.r_egg_get_source
r_egg_get_source.restype = POINTER_T(ctypes.c_char)
r_egg_get_source.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_get_assembly = _libr_egg.r_egg_get_assembly
r_egg_get_assembly.restype = POINTER_T(ctypes.c_char)
r_egg_get_assembly.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_append = _libr_egg.r_egg_append
r_egg_append.restype = None
r_egg_append.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_run = _libr_egg.r_egg_run
r_egg_run.restype = ctypes.c_int32
r_egg_run.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_run_rop = _libr_egg.r_egg_run_rop
r_egg_run_rop.restype = ctypes.c_int32
r_egg_run_rop.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_patch = _libr_egg.r_egg_patch
r_egg_patch.restype = ctypes.c_int32
r_egg_patch.argtypes = [POINTER_T(struct_r_egg_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_egg_finalize = _libr_egg.r_egg_finalize
r_egg_finalize.restype = None
r_egg_finalize.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_Cfile_parser = _libr_egg.r_egg_Cfile_parser
r_egg_Cfile_parser.restype = POINTER_T(ctypes.c_char)
r_egg_Cfile_parser.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_egg_mkvar = _libr_egg.r_egg_mkvar
r_egg_mkvar.restype = POINTER_T(ctypes.c_char)
r_egg_mkvar.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_egg_lang_parsechar = _libr_egg.r_egg_lang_parsechar
r_egg_lang_parsechar.restype = ctypes.c_int32
r_egg_lang_parsechar.argtypes = [POINTER_T(struct_r_egg_t), ctypes.c_char]
r_egg_lang_include_path = _libr_egg.r_egg_lang_include_path
r_egg_lang_include_path.restype = None
r_egg_lang_include_path.argtypes = [POINTER_T(struct_r_egg_t), POINTER_T(ctypes.c_char)]
r_egg_lang_include_init = _libr_egg.r_egg_lang_include_init
r_egg_lang_include_init.restype = None
r_egg_lang_include_init.argtypes = [POINTER_T(struct_r_egg_t)]
r_egg_plugin_xor = struct_r_egg_plugin_t # Variable struct_r_egg_plugin_t
r_egg_plugin_shya = struct_r_egg_plugin_t # Variable struct_r_egg_plugin_t
r_egg_plugin_exec = struct_r_egg_plugin_t # Variable struct_r_egg_plugin_t
struct_r_flag_item_t._pack_ = True # source:False
struct_r_flag_item_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('realname', POINTER_T(ctypes.c_char)),
    ('demangled', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('space', POINTER_T(struct_r_space_t)),
    ('color', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
    ('alias', POINTER_T(ctypes.c_char)),
]

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
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'REgg', 'REggEmit',
    'REggLang', 'REggPlugin', 'RNCAND', 'RNCASSIGN', 'RNCDEC',
    'RNCDIV', 'RNCEND', 'RNCINC', 'RNCLEFTP', 'RNCMINUS', 'RNCMOD',
    'RNCMUL', 'RNCNAME', 'RNCNEG', 'RNCNUMBER', 'RNCORR', 'RNCPLUS',
    'RNCPRINT', 'RNCRIGHTP', 'RNCROL', 'RNCROR', 'RNCSHL', 'RNCSHR',
    'RNCXOR', 'R_ANAL_ACC_R', 'R_ANAL_ACC_UNKNOWN', 'R_ANAL_ACC_W',
    'R_ANAL_COND_AL', 'R_ANAL_COND_EQ', 'R_ANAL_COND_GE',
    'R_ANAL_COND_GT', 'R_ANAL_COND_HI', 'R_ANAL_COND_HS',
    'R_ANAL_COND_LE', 'R_ANAL_COND_LO', 'R_ANAL_COND_LS',
    'R_ANAL_COND_LT', 'R_ANAL_COND_MI', 'R_ANAL_COND_NE',
    'R_ANAL_COND_NV', 'R_ANAL_COND_PL', 'R_ANAL_COND_VC',
    'R_ANAL_COND_VS', 'R_ANAL_CPP_ABI_ITANIUM', 'R_ANAL_CPP_ABI_MSVC',
    'R_ANAL_DATATYPE_ARRAY', 'R_ANAL_DATATYPE_BOOLEAN',
    'R_ANAL_DATATYPE_CLASS', 'R_ANAL_DATATYPE_FLOAT',
    'R_ANAL_DATATYPE_INT16', 'R_ANAL_DATATYPE_INT32',
    'R_ANAL_DATATYPE_INT64', 'R_ANAL_DATATYPE_NULL',
    'R_ANAL_DATATYPE_OBJECT', 'R_ANAL_DATATYPE_STRING',
    'R_ANAL_OP_DIR_EXEC', 'R_ANAL_OP_DIR_READ', 'R_ANAL_OP_DIR_REF',
    'R_ANAL_OP_DIR_WRITE', 'R_ANAL_OP_FAMILY_CPU',
    'R_ANAL_OP_FAMILY_CRYPTO', 'R_ANAL_OP_FAMILY_FPU',
    'R_ANAL_OP_FAMILY_IO', 'R_ANAL_OP_FAMILY_LAST',
    'R_ANAL_OP_FAMILY_MMX', 'R_ANAL_OP_FAMILY_PRIV',
    'R_ANAL_OP_FAMILY_SECURITY', 'R_ANAL_OP_FAMILY_SSE',
    'R_ANAL_OP_FAMILY_THREAD', 'R_ANAL_OP_FAMILY_UNKNOWN',
    'R_ANAL_OP_FAMILY_VIRT', 'R_ANAL_OP_MASK_ALL',
    'R_ANAL_OP_MASK_BASIC', 'R_ANAL_OP_MASK_DISASM',
    'R_ANAL_OP_MASK_ESIL', 'R_ANAL_OP_MASK_HINT',
    'R_ANAL_OP_MASK_OPEX', 'R_ANAL_OP_MASK_VAL',
    'R_ANAL_OP_PREFIX_COND', 'R_ANAL_OP_PREFIX_LIKELY',
    'R_ANAL_OP_PREFIX_LOCK', 'R_ANAL_OP_PREFIX_REP',
    'R_ANAL_OP_PREFIX_REPNE', 'R_ANAL_OP_PREFIX_UNLIKELY',
    'R_ANAL_STACK_ALIGN', 'R_ANAL_STACK_GET', 'R_ANAL_STACK_INC',
    'R_ANAL_STACK_NOP', 'R_ANAL_STACK_NULL', 'R_ANAL_STACK_RESET',
    'R_ANAL_STACK_SET', 'R_ANAL_VAL_IMM', 'R_ANAL_VAL_MEM',
    'R_ANAL_VAL_REG', '__ptrace_request', 'c__EA_RAnalCPPABI',
    'c__EA_RAnalOpDirection', 'c__EA_RAnalOpFamily',
    'c__EA_RAnalOpMask', 'c__EA_RAnalOpPrefix', 'c__EA_RAnalStackOp',
    'c__EA_RAnalValueAccess', 'c__EA_RAnalValueType',
    'c__EA_RNumCalcToken', 'c__EA__RAnalCond', 'r_anal_data_type_t',
    'r_egg_Cfile_parser', 'r_egg_add', 'r_egg_alloc', 'r_egg_append',
    'r_egg_assemble', 'r_egg_assemble_asm', 'r_egg_compile',
    'r_egg_encode', 'r_egg_finalize', 'r_egg_free',
    'r_egg_get_assembly', 'r_egg_get_bin', 'r_egg_get_source',
    'r_egg_if', 'r_egg_include', 'r_egg_label', 'r_egg_lang_free',
    'r_egg_lang_include_init', 'r_egg_lang_include_path',
    'r_egg_lang_init', 'r_egg_lang_parsechar', 'r_egg_load',
    'r_egg_mkvar', 'r_egg_new', 'r_egg_option_get',
    'r_egg_option_set', 'r_egg_padding', 'r_egg_patch',
    'r_egg_pattern', 'r_egg_plugin_exec', 'r_egg_plugin_shya',
    'r_egg_plugin_xor', 'r_egg_printf', 'r_egg_raw', 'r_egg_reset',
    'r_egg_run', 'r_egg_run_rop', 'r_egg_setup', 'r_egg_shellcode',
    'r_egg_syscall', 'r_egg_to_string', 'r_egg_version',
    'struct__IO_FILE', 'struct__IO_codecvt', 'struct__IO_marker',
    'struct__IO_wide_data', 'struct_buffer',
    'struct_c__SA_RNumCalcValue', 'struct_c__SA_RStrBuf',
    'struct_c__SA_dict', 'struct_cdb', 'struct_cdb_hp',
    'struct_cdb_hplist', 'struct_cdb_make', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_ptrace_wrap_instance_t',
    'struct_r_anal_bb_t', 'struct_r_anal_bind_t',
    'struct_r_anal_callbacks_t', 'struct_r_anal_cond_t',
    'struct_r_anal_diff_t', 'struct_r_anal_esil_callbacks_t',
    'struct_r_anal_esil_interrupt_handler_t',
    'struct_r_anal_esil_interrupt_t', 'struct_r_anal_esil_t',
    'struct_r_anal_esil_trace_t', 'struct_r_anal_fcn_meta_t',
    'struct_r_anal_function_t', 'struct_r_anal_hint_cb_t',
    'struct_r_anal_hint_t', 'struct_r_anal_op_t',
    'struct_r_anal_options_t', 'struct_r_anal_plugin_t',
    'struct_r_anal_range_t', 'struct_r_anal_reil',
    'struct_r_anal_switch_obj_t', 'struct_r_anal_t',
    'struct_r_anal_value_t', 'struct_r_asm_op_t',
    'struct_r_asm_plugin_t', 'struct_r_asm_t', 'struct_r_bin_addr_t',
    'struct_r_bin_arch_options_t', 'struct_r_bin_bind_t',
    'struct_r_bin_dbginfo_t', 'struct_r_bin_file_t',
    'struct_r_bin_hash_t', 'struct_r_bin_info_t',
    'struct_r_bin_object_t', 'struct_r_bin_plugin_t',
    'struct_r_bin_section_t', 'struct_r_bin_t',
    'struct_r_bin_write_t', 'struct_r_bin_xtr_extract_t',
    'struct_r_bin_xtr_metadata_t', 'struct_r_bin_xtr_plugin_t',
    'struct_r_buf_t', 'struct_r_buffer_methods_t', 'struct_r_cache_t',
    'struct_r_cons_bind_t', 'struct_r_core_bind_t',
    'struct_r_egg_emit_t', 'struct_r_egg_lang_t',
    'struct_r_egg_lang_t_0', 'struct_r_egg_lang_t_1',
    'struct_r_egg_lang_t_2', 'struct_r_egg_plugin_t',
    'struct_r_egg_t', 'struct_r_event_t', 'struct_r_flag_bind_t',
    'struct_r_flag_item_t', 'struct_r_flag_t', 'struct_r_id_pool_t',
    'struct_r_id_storage_t', 'struct_r_interval_node_t',
    'struct_r_interval_t', 'struct_r_interval_tree_t',
    'struct_r_io_bind_t', 'struct_r_io_desc_t', 'struct_r_io_map_t',
    'struct_r_io_plugin_t', 'struct_r_io_t', 'struct_r_io_undo_t',
    'struct_r_io_undos_t', 'struct_r_list_iter_t', 'struct_r_list_t',
    'struct_r_num_calc_t', 'struct_r_num_t',
    'struct_r_parse_plugin_t', 'struct_r_parse_t',
    'struct_r_pvector_t', 'struct_r_queue_t', 'struct_r_rb_node_t',
    'struct_r_reg_arena_t', 'struct_r_reg_item_t',
    'struct_r_reg_set_t', 'struct_r_reg_t',
    'struct_r_skiplist_node_t', 'struct_r_skiplist_t',
    'struct_r_space_t', 'struct_r_spaces_t',
    'struct_r_str_constpool_t', 'struct_r_syscall_item_t',
    'struct_r_syscall_port_t', 'struct_r_syscall_t',
    'struct_r_vector_t', 'struct_sdb_kv', 'struct_sdb_t']

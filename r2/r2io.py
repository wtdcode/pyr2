# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_io as _libr_io


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
r_ptrace_request_t = __ptrace_request
r_ptrace_request_t__enumvalues = __ptrace_request__enumvalues
r_ptrace_data_t = POINTER_T(None)
r_io_version = _libr_io.r_io_version
r_io_version.restype = POINTER_T(ctypes.c_char)
r_io_version.argtypes = []
class struct_r_io_undos_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('off', ctypes.c_uint64),
    ('cursor', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RIOUndos = struct_r_io_undos_t
class struct_r_io_undo_t(ctypes.Structure):
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

RIOUndo = struct_r_io_undo_t
class struct_r_io_undo_w_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('set', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('off', ctypes.c_uint64),
    ('o', POINTER_T(ctypes.c_ubyte)),
    ('n', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

RIOUndoWrite = struct_r_io_undo_w_t
class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', ctypes.c_uint64),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_uint64),
     ]

class struct_r_io_desc_t(ctypes.Structure):
    pass

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

class struct_r_io_plugin_t(ctypes.Structure):
    pass

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
    ('undo', RIOUndo),
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

class struct_ptrace_wrap_instance_t(ctypes.Structure):
    pass

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
    ('undo', RIOUndo),
    ('plugins', POINTER_T(struct_ls_t)),
    ('runprofile', POINTER_T(ctypes.c_char)),
    ('envprofile', POINTER_T(ctypes.c_char)),
    ('ptrace_wrap', POINTER_T(struct_ptrace_wrap_instance_t)),
    ('args', POINTER_T(ctypes.c_char)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('corebind', struct_r_core_bind_t),
]

RIO = struct_r_io_t
RIODesc = struct_r_io_desc_t
class struct_c__SA_RIODescData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('magic', ctypes.c_uint32),
    ('pid', ctypes.c_int32),
    ('tid', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('data', POINTER_T(None)),
     ]

RIODescData = struct_c__SA_RIODescData
class struct_c__SA_RIORap(ctypes.Structure):
    pass

class struct_r_socket_t(ctypes.Structure):
    pass

class struct_sockaddr_in(ctypes.Structure):
    pass

class struct_in_addr(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('s_addr', ctypes.c_uint32),
     ]

struct_sockaddr_in._pack_ = True # source:False
struct_sockaddr_in._fields_ = [
    ('sin_family', ctypes.c_uint16),
    ('sin_port', ctypes.c_uint16),
    ('sin_addr', struct_in_addr),
    ('sin_zero', ctypes.c_ubyte * 8),
]

struct_r_socket_t._pack_ = True # source:False
struct_r_socket_t._fields_ = [
    ('fd', ctypes.c_int32),
    ('is_ssl', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('proto', ctypes.c_int32),
    ('local', ctypes.c_int32),
    ('port', ctypes.c_int32),
    ('sa', struct_sockaddr_in),
]

struct_c__SA_RIORap._pack_ = True # source:False
struct_c__SA_RIORap._fields_ = [
    ('fd', POINTER_T(struct_r_socket_t)),
    ('client', POINTER_T(struct_r_socket_t)),
    ('listener', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

RIORap = struct_c__SA_RIORap
RIOPlugin = struct_r_io_plugin_t
class struct_r_io_map_t(ctypes.Structure):
    pass

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

RIOMap = struct_r_io_map_t
class struct_r_io_map_skyline_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('map', POINTER_T(struct_r_io_map_t)),
    ('itv', struct_r_interval_t),
     ]

RIOMapSkyline = struct_r_io_map_skyline_t
class struct_r_io_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('itv', struct_r_interval_t),
    ('data', POINTER_T(ctypes.c_ubyte)),
    ('odata', POINTER_T(ctypes.c_ubyte)),
    ('written', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RIOCache = struct_r_io_cache_t
class struct_r_io_desc_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cached', ctypes.c_uint64),
    ('cdata', ctypes.c_ubyte * 64),
     ]

RIODescCache = struct_r_io_desc_cache_t
RIODescUse = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))
RIODescGet = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), ctypes.c_int32))
RIODescSize = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_desc_t)))
RIOOpen = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))
RIOOpenAt = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_desc_t), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64))
RIOClose = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOReadAt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOWriteAt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOSystem = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char)))
RIOFdOpen = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))
RIOFdClose = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOFdSeek = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32))
RIOFdSize = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOFdResize = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64))
RIOP2V = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_uint64))
RIOV2P = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_io_t), ctypes.c_uint64))
RIOFdRead = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOFdWrite = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOFdReadAt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOFdWriteAt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
RIOFdIsDbg = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOFdGetName = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOFdGetMap = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_io_t), ctypes.c_int32))
RIOFdRemap = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64))
RIOIsValidOff = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_int32))
RIOMapGet = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_uint64))
RIOMapGetPaddr = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_uint64))
RIOAddrIsMapped = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_io_t), ctypes.c_uint64))
RIOMapAdd = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_io_map_t), POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64))
RIOPtraceFn = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int64, POINTER_T(struct_r_io_t), __ptrace_request, ctypes.c_int32, POINTER_T(None), POINTER_T(None)))
RIOPtraceFuncFn = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(struct_r_io_t), POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None))), POINTER_T(None)))
class struct_r_io_bind_t(ctypes.Structure):
    pass

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

RIOBind = struct_r_io_bind_t
r_io_map_new = _libr_io.r_io_map_new
r_io_map_new.restype = POINTER_T(struct_r_io_map_t)
r_io_map_new.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_io_map_init = _libr_io.r_io_map_init
r_io_map_init.restype = None
r_io_map_init.argtypes = [POINTER_T(struct_r_io_t)]
r_io_map_remap = _libr_io.r_io_map_remap
r_io_map_remap.restype = ctypes.c_bool
r_io_map_remap.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32, ctypes.c_uint64]
r_io_map_remap_fd = _libr_io.r_io_map_remap_fd
r_io_map_remap_fd.restype = ctypes.c_bool
r_io_map_remap_fd.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64]
r_io_map_location = _libr_io.r_io_map_location
r_io_map_location.restype = ctypes.c_uint64
r_io_map_location.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_map_exists = _libr_io.r_io_map_exists
r_io_map_exists.restype = ctypes.c_bool
r_io_map_exists.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_map_t)]
r_io_map_exists_for_id = _libr_io.r_io_map_exists_for_id
r_io_map_exists_for_id.restype = ctypes.c_bool
r_io_map_exists_for_id.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32]
r_io_map_resolve = _libr_io.r_io_map_resolve
r_io_map_resolve.restype = POINTER_T(struct_r_io_map_t)
r_io_map_resolve.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32]
r_io_map_add = _libr_io.r_io_map_add
r_io_map_add.restype = POINTER_T(struct_r_io_map_t)
r_io_map_add.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_io_map_add_batch = _libr_io.r_io_map_add_batch
r_io_map_add_batch.restype = POINTER_T(struct_r_io_map_t)
r_io_map_add_batch.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_io_map_get = _libr_io.r_io_map_get
r_io_map_get.restype = POINTER_T(struct_r_io_map_t)
r_io_map_get.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_update = _libr_io.r_io_update
r_io_update.restype = None
r_io_update.argtypes = [POINTER_T(struct_r_io_t)]
r_io_map_is_mapped = _libr_io.r_io_map_is_mapped
r_io_map_is_mapped.restype = ctypes.c_bool
r_io_map_is_mapped.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_map_get_paddr = _libr_io.r_io_map_get_paddr
r_io_map_get_paddr.restype = POINTER_T(struct_r_io_map_t)
r_io_map_get_paddr.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_map_reset = _libr_io.r_io_map_reset
r_io_map_reset.restype = None
r_io_map_reset.argtypes = [POINTER_T(struct_r_io_t)]
r_io_map_del = _libr_io.r_io_map_del
r_io_map_del.restype = ctypes.c_bool
r_io_map_del.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32]
r_io_map_del_for_fd = _libr_io.r_io_map_del_for_fd
r_io_map_del_for_fd.restype = ctypes.c_bool
r_io_map_del_for_fd.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_map_depriorize = _libr_io.r_io_map_depriorize
r_io_map_depriorize.restype = ctypes.c_bool
r_io_map_depriorize.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32]
r_io_map_priorize = _libr_io.r_io_map_priorize
r_io_map_priorize.restype = ctypes.c_bool
r_io_map_priorize.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32]
r_io_map_priorize_for_fd = _libr_io.r_io_map_priorize_for_fd
r_io_map_priorize_for_fd.restype = ctypes.c_bool
r_io_map_priorize_for_fd.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_map_cleanup = _libr_io.r_io_map_cleanup
r_io_map_cleanup.restype = None
r_io_map_cleanup.argtypes = [POINTER_T(struct_r_io_t)]
r_io_map_fini = _libr_io.r_io_map_fini
r_io_map_fini.restype = None
r_io_map_fini.argtypes = [POINTER_T(struct_r_io_t)]
r_io_map_set_name = _libr_io.r_io_map_set_name
r_io_map_set_name.restype = None
r_io_map_set_name.argtypes = [POINTER_T(struct_r_io_map_t), POINTER_T(ctypes.c_char)]
r_io_map_del_name = _libr_io.r_io_map_del_name
r_io_map_del_name.restype = None
r_io_map_del_name.argtypes = [POINTER_T(struct_r_io_map_t)]
r_io_map_get_for_fd = _libr_io.r_io_map_get_for_fd
r_io_map_get_for_fd.restype = POINTER_T(struct_r_list_t)
r_io_map_get_for_fd.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_map_resize = _libr_io.r_io_map_resize
r_io_map_resize.restype = ctypes.c_bool
r_io_map_resize.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint32, ctypes.c_uint64]
r_io_map_next_available = _libr_io.r_io_map_next_available
r_io_map_next_available.restype = ctypes.c_uint64
r_io_map_next_available.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_io_map_next_address = _libr_io.r_io_map_next_address
r_io_map_next_address.restype = ctypes.c_uint64
r_io_map_next_address.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_p2v = _libr_io.r_io_p2v
r_io_p2v.restype = ctypes.c_uint64
r_io_p2v.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_v2p = _libr_io.r_io_v2p
r_io_v2p.restype = ctypes.c_uint64
r_io_v2p.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_new = _libr_io.r_io_new
r_io_new.restype = POINTER_T(struct_r_io_t)
r_io_new.argtypes = []
r_io_init = _libr_io.r_io_init
r_io_init.restype = POINTER_T(struct_r_io_t)
r_io_init.argtypes = [POINTER_T(struct_r_io_t)]
r_io_open_nomap = _libr_io.r_io_open_nomap
r_io_open_nomap.restype = POINTER_T(struct_r_io_desc_t)
r_io_open_nomap.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_io_open = _libr_io.r_io_open
r_io_open.restype = POINTER_T(struct_r_io_desc_t)
r_io_open.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_io_open_at = _libr_io.r_io_open_at
r_io_open_at.restype = POINTER_T(struct_r_io_desc_t)
r_io_open_at.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64]
r_io_open_many = _libr_io.r_io_open_many
r_io_open_many.restype = POINTER_T(struct_r_list_t)
r_io_open_many.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
class struct_r_buf_t(ctypes.Structure):
    pass

r_io_open_buffer = _libr_io.r_io_open_buffer
r_io_open_buffer.restype = POINTER_T(struct_r_io_desc_t)
r_io_open_buffer.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_buf_t), ctypes.c_int32, ctypes.c_int32]
r_io_close = _libr_io.r_io_close
r_io_close.restype = ctypes.c_bool
r_io_close.argtypes = [POINTER_T(struct_r_io_t)]
r_io_reopen = _libr_io.r_io_reopen
r_io_reopen.restype = ctypes.c_bool
r_io_reopen.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_io_close_all = _libr_io.r_io_close_all
r_io_close_all.restype = ctypes.c_int32
r_io_close_all.argtypes = [POINTER_T(struct_r_io_t)]
r_io_pread_at = _libr_io.r_io_pread_at
r_io_pread_at.restype = ctypes.c_int32
r_io_pread_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_pwrite_at = _libr_io.r_io_pwrite_at
r_io_pwrite_at.restype = ctypes.c_int32
r_io_pwrite_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_vread_at_mapped = _libr_io.r_io_vread_at_mapped
r_io_vread_at_mapped.restype = ctypes.c_bool
r_io_vread_at_mapped.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_read_at = _libr_io.r_io_read_at
r_io_read_at.restype = ctypes.c_bool
r_io_read_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_read_at_mapped = _libr_io.r_io_read_at_mapped
r_io_read_at_mapped.restype = ctypes.c_bool
r_io_read_at_mapped.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_nread_at = _libr_io.r_io_nread_at
r_io_nread_at.restype = ctypes.c_int32
r_io_nread_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_write_at = _libr_io.r_io_write_at
r_io_write_at.restype = ctypes.c_bool
r_io_write_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_read = _libr_io.r_io_read
r_io_read.restype = ctypes.c_bool
r_io_read.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_write = _libr_io.r_io_write
r_io_write.restype = ctypes.c_bool
r_io_write.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_size = _libr_io.r_io_size
r_io_size.restype = ctypes.c_uint64
r_io_size.argtypes = [POINTER_T(struct_r_io_t)]
r_io_is_listener = _libr_io.r_io_is_listener
r_io_is_listener.restype = ctypes.c_bool
r_io_is_listener.argtypes = [POINTER_T(struct_r_io_t)]
r_io_system = _libr_io.r_io_system
r_io_system.restype = POINTER_T(ctypes.c_char)
r_io_system.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char)]
r_io_resize = _libr_io.r_io_resize
r_io_resize.restype = ctypes.c_bool
r_io_resize.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_extend_at = _libr_io.r_io_extend_at
r_io_extend_at.restype = ctypes.c_int32
r_io_extend_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_uint64]
r_io_set_write_mask = _libr_io.r_io_set_write_mask
r_io_set_write_mask.restype = ctypes.c_bool
r_io_set_write_mask.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_bind = _libr_io.r_io_bind
r_io_bind.restype = None
r_io_bind.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_bind_t)]
r_io_shift = _libr_io.r_io_shift
r_io_shift.restype = ctypes.c_bool
r_io_shift.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int64]
r_io_seek = _libr_io.r_io_seek
r_io_seek.restype = ctypes.c_uint64
r_io_seek.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_int32]
r_io_fini = _libr_io.r_io_fini
r_io_fini.restype = ctypes.c_int32
r_io_fini.argtypes = [POINTER_T(struct_r_io_t)]
r_io_free = _libr_io.r_io_free
r_io_free.restype = None
r_io_free.argtypes = [POINTER_T(struct_r_io_t)]
r_io_plugin_init = _libr_io.r_io_plugin_init
r_io_plugin_init.restype = ctypes.c_bool
r_io_plugin_init.argtypes = [POINTER_T(struct_r_io_t)]
r_io_plugin_add = _libr_io.r_io_plugin_add
r_io_plugin_add.restype = ctypes.c_bool
r_io_plugin_add.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_plugin_t)]
r_io_plugin_list = _libr_io.r_io_plugin_list
r_io_plugin_list.restype = ctypes.c_int32
r_io_plugin_list.argtypes = [POINTER_T(struct_r_io_t)]
r_io_plugin_list_json = _libr_io.r_io_plugin_list_json
r_io_plugin_list_json.restype = ctypes.c_int32
r_io_plugin_list_json.argtypes = [POINTER_T(struct_r_io_t)]
r_io_plugin_read = _libr_io.r_io_plugin_read
r_io_plugin_read.restype = ctypes.c_int32
r_io_plugin_read.argtypes = [POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_plugin_write = _libr_io.r_io_plugin_write
r_io_plugin_write.restype = ctypes.c_int32
r_io_plugin_write.argtypes = [POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_plugin_read_at = _libr_io.r_io_plugin_read_at
r_io_plugin_read_at.restype = ctypes.c_int32
r_io_plugin_read_at.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_plugin_write_at = _libr_io.r_io_plugin_write_at
r_io_plugin_write_at.restype = ctypes.c_int32
r_io_plugin_write_at.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_plugin_resolve = _libr_io.r_io_plugin_resolve
r_io_plugin_resolve.restype = POINTER_T(struct_r_io_plugin_t)
r_io_plugin_resolve.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_io_plugin_get_default = _libr_io.r_io_plugin_get_default
r_io_plugin_get_default.restype = POINTER_T(struct_r_io_plugin_t)
r_io_plugin_get_default.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_io_undo_init = _libr_io.r_io_undo_init
r_io_undo_init.restype = ctypes.c_int32
r_io_undo_init.argtypes = [POINTER_T(struct_r_io_t)]
r_io_undo_enable = _libr_io.r_io_undo_enable
r_io_undo_enable.restype = None
r_io_undo_enable.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32]
r_io_sundo = _libr_io.r_io_sundo
r_io_sundo.restype = POINTER_T(struct_r_io_undos_t)
r_io_sundo.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_sundo_redo = _libr_io.r_io_sundo_redo
r_io_sundo_redo.restype = POINTER_T(struct_r_io_undos_t)
r_io_sundo_redo.argtypes = [POINTER_T(struct_r_io_t)]
r_io_sundo_push = _libr_io.r_io_sundo_push
r_io_sundo_push.restype = None
r_io_sundo_push.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_int32]
r_io_sundo_reset = _libr_io.r_io_sundo_reset
r_io_sundo_reset.restype = None
r_io_sundo_reset.argtypes = [POINTER_T(struct_r_io_t)]
r_io_sundo_list = _libr_io.r_io_sundo_list
r_io_sundo_list.restype = POINTER_T(struct_r_list_t)
r_io_sundo_list.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_wundo_new = _libr_io.r_io_wundo_new
r_io_wundo_new.restype = None
r_io_wundo_new.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_wundo_apply_all = _libr_io.r_io_wundo_apply_all
r_io_wundo_apply_all.restype = None
r_io_wundo_apply_all.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_wundo_apply = _libr_io.r_io_wundo_apply
r_io_wundo_apply.restype = ctypes.c_int32
r_io_wundo_apply.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_undo_w_t), ctypes.c_int32]
r_io_wundo_clear = _libr_io.r_io_wundo_clear
r_io_wundo_clear.restype = None
r_io_wundo_clear.argtypes = [POINTER_T(struct_r_io_t)]
r_io_wundo_size = _libr_io.r_io_wundo_size
r_io_wundo_size.restype = ctypes.c_int32
r_io_wundo_size.argtypes = [POINTER_T(struct_r_io_t)]
r_io_wundo_list = _libr_io.r_io_wundo_list
r_io_wundo_list.restype = None
r_io_wundo_list.argtypes = [POINTER_T(struct_r_io_t)]
r_io_wundo_set = _libr_io.r_io_wundo_set
r_io_wundo_set.restype = ctypes.c_int32
r_io_wundo_set.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32]
r_io_desc_new = _libr_io.r_io_desc_new
r_io_desc_new.restype = POINTER_T(struct_r_io_desc_t)
r_io_desc_new.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_plugin_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, POINTER_T(None)]
r_io_desc_open = _libr_io.r_io_desc_open
r_io_desc_open.restype = POINTER_T(struct_r_io_desc_t)
r_io_desc_open.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_io_desc_open_plugin = _libr_io.r_io_desc_open_plugin
r_io_desc_open_plugin.restype = POINTER_T(struct_r_io_desc_t)
r_io_desc_open_plugin.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_plugin_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_io_desc_close = _libr_io.r_io_desc_close
r_io_desc_close.restype = ctypes.c_bool
r_io_desc_close.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_read = _libr_io.r_io_desc_read
r_io_desc_read.restype = ctypes.c_int32
r_io_desc_read.argtypes = [POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_write = _libr_io.r_io_desc_write
r_io_desc_write.restype = ctypes.c_int32
r_io_desc_write.argtypes = [POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_free = _libr_io.r_io_desc_free
r_io_desc_free.restype = None
r_io_desc_free.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_add = _libr_io.r_io_desc_add
r_io_desc_add.restype = ctypes.c_bool
r_io_desc_add.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(struct_r_io_desc_t)]
r_io_desc_del = _libr_io.r_io_desc_del
r_io_desc_del.restype = ctypes.c_bool
r_io_desc_del.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_desc_get = _libr_io.r_io_desc_get
r_io_desc_get.restype = POINTER_T(struct_r_io_desc_t)
r_io_desc_get.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_desc_seek = _libr_io.r_io_desc_seek
r_io_desc_seek.restype = ctypes.c_uint64
r_io_desc_seek.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, ctypes.c_int32]
r_io_desc_resize = _libr_io.r_io_desc_resize
r_io_desc_resize.restype = ctypes.c_bool
r_io_desc_resize.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64]
r_io_desc_size = _libr_io.r_io_desc_size
r_io_desc_size.restype = ctypes.c_uint64
r_io_desc_size.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_is_blockdevice = _libr_io.r_io_desc_is_blockdevice
r_io_desc_is_blockdevice.restype = ctypes.c_bool
r_io_desc_is_blockdevice.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_is_chardevice = _libr_io.r_io_desc_is_chardevice
r_io_desc_is_chardevice.restype = ctypes.c_bool
r_io_desc_is_chardevice.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_exchange = _libr_io.r_io_desc_exchange
r_io_desc_exchange.restype = ctypes.c_bool
r_io_desc_exchange.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_int32]
r_io_desc_is_dbg = _libr_io.r_io_desc_is_dbg
r_io_desc_is_dbg.restype = ctypes.c_bool
r_io_desc_is_dbg.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_get_pid = _libr_io.r_io_desc_get_pid
r_io_desc_get_pid.restype = ctypes.c_int32
r_io_desc_get_pid.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_get_tid = _libr_io.r_io_desc_get_tid
r_io_desc_get_tid.restype = ctypes.c_int32
r_io_desc_get_tid.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_get_base = _libr_io.r_io_desc_get_base
r_io_desc_get_base.restype = ctypes.c_bool
r_io_desc_get_base.argtypes = [POINTER_T(struct_r_io_desc_t), POINTER_T(ctypes.c_uint64)]
r_io_desc_read_at = _libr_io.r_io_desc_read_at
r_io_desc_read_at.restype = ctypes.c_int32
r_io_desc_read_at.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_write_at = _libr_io.r_io_desc_write_at
r_io_desc_write_at.restype = ctypes.c_int32
r_io_desc_write_at.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_cache_invalidate = _libr_io.r_io_cache_invalidate
r_io_cache_invalidate.restype = ctypes.c_int32
r_io_cache_invalidate.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_uint64]
r_io_cache_at = _libr_io.r_io_cache_at
r_io_cache_at.restype = ctypes.c_bool
r_io_cache_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_cache_commit = _libr_io.r_io_cache_commit
r_io_cache_commit.restype = None
r_io_cache_commit.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_uint64]
r_io_cache_init = _libr_io.r_io_cache_init
r_io_cache_init.restype = None
r_io_cache_init.argtypes = [POINTER_T(struct_r_io_t)]
r_io_cache_fini = _libr_io.r_io_cache_fini
r_io_cache_fini.restype = None
r_io_cache_fini.argtypes = [POINTER_T(struct_r_io_t)]
r_io_cache_list = _libr_io.r_io_cache_list
r_io_cache_list.restype = ctypes.c_int32
r_io_cache_list.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_cache_reset = _libr_io.r_io_cache_reset
r_io_cache_reset.restype = None
r_io_cache_reset.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_cache_write = _libr_io.r_io_cache_write
r_io_cache_write.restype = ctypes.c_bool
r_io_cache_write.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_cache_read = _libr_io.r_io_cache_read
r_io_cache_read.restype = ctypes.c_bool
r_io_cache_read.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_cache_init = _libr_io.r_io_desc_cache_init
r_io_desc_cache_init.restype = ctypes.c_bool
r_io_desc_cache_init.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_cache_write = _libr_io.r_io_desc_cache_write
r_io_desc_cache_write.restype = ctypes.c_int32
r_io_desc_cache_write.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_cache_read = _libr_io.r_io_desc_cache_read
r_io_desc_cache_read.restype = ctypes.c_int32
r_io_desc_cache_read.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_desc_cache_commit = _libr_io.r_io_desc_cache_commit
r_io_desc_cache_commit.restype = ctypes.c_bool
r_io_desc_cache_commit.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_cache_cleanup = _libr_io.r_io_desc_cache_cleanup
r_io_desc_cache_cleanup.restype = None
r_io_desc_cache_cleanup.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_cache_fini = _libr_io.r_io_desc_cache_fini
r_io_desc_cache_fini.restype = None
r_io_desc_cache_fini.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_cache_fini_all = _libr_io.r_io_desc_cache_fini_all
r_io_desc_cache_fini_all.restype = None
r_io_desc_cache_fini_all.argtypes = [POINTER_T(struct_r_io_t)]
r_io_desc_cache_list = _libr_io.r_io_desc_cache_list
r_io_desc_cache_list.restype = POINTER_T(struct_r_list_t)
r_io_desc_cache_list.argtypes = [POINTER_T(struct_r_io_desc_t)]
r_io_desc_extend = _libr_io.r_io_desc_extend
r_io_desc_extend.restype = ctypes.c_int32
r_io_desc_extend.argtypes = [POINTER_T(struct_r_io_desc_t), ctypes.c_uint64]
r_io_fd_open = _libr_io.r_io_fd_open
r_io_fd_open.restype = ctypes.c_int32
r_io_fd_open.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_io_fd_close = _libr_io.r_io_fd_close
r_io_fd_close.restype = ctypes.c_bool
r_io_fd_close.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_read = _libr_io.r_io_fd_read
r_io_fd_read.restype = ctypes.c_int32
r_io_fd_read.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_fd_write = _libr_io.r_io_fd_write
r_io_fd_write.restype = ctypes.c_int32
r_io_fd_write.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_fd_seek = _libr_io.r_io_fd_seek
r_io_fd_seek.restype = ctypes.c_uint64
r_io_fd_seek.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32]
r_io_fd_size = _libr_io.r_io_fd_size
r_io_fd_size.restype = ctypes.c_uint64
r_io_fd_size.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_resize = _libr_io.r_io_fd_resize
r_io_fd_resize.restype = ctypes.c_bool
r_io_fd_resize.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64]
r_io_fd_is_blockdevice = _libr_io.r_io_fd_is_blockdevice
r_io_fd_is_blockdevice.restype = ctypes.c_bool
r_io_fd_is_blockdevice.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_is_chardevice = _libr_io.r_io_fd_is_chardevice
r_io_fd_is_chardevice.restype = ctypes.c_bool
r_io_fd_is_chardevice.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_read_at = _libr_io.r_io_fd_read_at
r_io_fd_read_at.restype = ctypes.c_int32
r_io_fd_read_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_fd_write_at = _libr_io.r_io_fd_write_at
r_io_fd_write_at.restype = ctypes.c_int32
r_io_fd_write_at.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_io_fd_is_dbg = _libr_io.r_io_fd_is_dbg
r_io_fd_is_dbg.restype = ctypes.c_bool
r_io_fd_is_dbg.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_get_pid = _libr_io.r_io_fd_get_pid
r_io_fd_get_pid.restype = ctypes.c_int32
r_io_fd_get_pid.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_get_tid = _libr_io.r_io_fd_get_tid
r_io_fd_get_tid.restype = ctypes.c_int32
r_io_fd_get_tid.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_get_base = _libr_io.r_io_fd_get_base
r_io_fd_get_base.restype = ctypes.c_bool
r_io_fd_get_base.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32, POINTER_T(ctypes.c_uint64)]
r_io_fd_get_name = _libr_io.r_io_fd_get_name
r_io_fd_get_name.restype = POINTER_T(ctypes.c_char)
r_io_fd_get_name.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_fd_get_current = _libr_io.r_io_fd_get_current
r_io_fd_get_current.restype = ctypes.c_int32
r_io_fd_get_current.argtypes = [POINTER_T(struct_r_io_t)]
r_io_use_fd = _libr_io.r_io_use_fd
r_io_use_fd.restype = ctypes.c_bool
r_io_use_fd.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_int32]
r_io_is_valid_offset = _libr_io.r_io_is_valid_offset
r_io_is_valid_offset.restype = ctypes.c_bool
r_io_is_valid_offset.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, ctypes.c_int32]
r_io_addr_is_mapped = _libr_io.r_io_addr_is_mapped
r_io_addr_is_mapped.restype = ctypes.c_bool
r_io_addr_is_mapped.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64]
r_io_read_i = _libr_io.r_io_read_i
r_io_read_i.restype = ctypes.c_bool
r_io_read_i.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_uint64), ctypes.c_int32, ctypes.c_bool]
r_io_write_i = _libr_io.r_io_write_i
r_io_write_i.restype = ctypes.c_bool
r_io_write_i.argtypes = [POINTER_T(struct_r_io_t), ctypes.c_uint64, POINTER_T(ctypes.c_uint64), ctypes.c_int32, ctypes.c_bool]
pid_t = ctypes.c_int32
r_io_ptrace = _libr_io.r_io_ptrace
r_io_ptrace.restype = ctypes.c_int64
r_io_ptrace.argtypes = [POINTER_T(struct_r_io_t), r_ptrace_request_t, pid_t, POINTER_T(None), r_ptrace_data_t]
r_io_ptrace_fork = _libr_io.r_io_ptrace_fork
r_io_ptrace_fork.restype = pid_t
r_io_ptrace_fork.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None))), POINTER_T(None)]
r_io_ptrace_func = _libr_io.r_io_ptrace_func
r_io_ptrace_func.restype = POINTER_T(None)
r_io_ptrace_func.argtypes = [POINTER_T(struct_r_io_t), POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None))), POINTER_T(None)]
r_io_plugin_procpid = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_malloc = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_sparse = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_ptrace = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_w32dbg = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_windbg = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_mach = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_debug = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_shm = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_gdb = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_rap = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_http = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_bfdbg = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_w32 = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_zip = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_mmap = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_default = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_ihex = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_self = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_gzip = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_winkd = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_r2pipe = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_r2web = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_qnx = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_r2k = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_tcp = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_bochs = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_null = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_ar = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_rbuf = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_winedbg = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_gprobe = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
r_io_plugin_fd = struct_r_io_plugin_t # Variable struct_r_io_plugin_t
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
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'RIO',
    'RIOAddrIsMapped', 'RIOBind', 'RIOCache', 'RIOClose', 'RIODesc',
    'RIODescCache', 'RIODescData', 'RIODescGet', 'RIODescSize',
    'RIODescUse', 'RIOFdClose', 'RIOFdGetMap', 'RIOFdGetName',
    'RIOFdIsDbg', 'RIOFdOpen', 'RIOFdRead', 'RIOFdReadAt',
    'RIOFdRemap', 'RIOFdResize', 'RIOFdSeek', 'RIOFdSize',
    'RIOFdWrite', 'RIOFdWriteAt', 'RIOIsValidOff', 'RIOMap',
    'RIOMapAdd', 'RIOMapGet', 'RIOMapGetPaddr', 'RIOMapSkyline',
    'RIOOpen', 'RIOOpenAt', 'RIOP2V', 'RIOPlugin', 'RIOPtraceFn',
    'RIOPtraceFuncFn', 'RIORap', 'RIOReadAt', 'RIOSystem', 'RIOUndo',
    'RIOUndoWrite', 'RIOUndos', 'RIOV2P', 'RIOWriteAt',
    '__ptrace_request', 'pid_t', 'r_io_addr_is_mapped', 'r_io_bind',
    'r_io_cache_at', 'r_io_cache_commit', 'r_io_cache_fini',
    'r_io_cache_init', 'r_io_cache_invalidate', 'r_io_cache_list',
    'r_io_cache_read', 'r_io_cache_reset', 'r_io_cache_write',
    'r_io_close', 'r_io_close_all', 'r_io_desc_add',
    'r_io_desc_cache_cleanup', 'r_io_desc_cache_commit',
    'r_io_desc_cache_fini', 'r_io_desc_cache_fini_all',
    'r_io_desc_cache_init', 'r_io_desc_cache_list',
    'r_io_desc_cache_read', 'r_io_desc_cache_write',
    'r_io_desc_close', 'r_io_desc_del', 'r_io_desc_exchange',
    'r_io_desc_extend', 'r_io_desc_free', 'r_io_desc_get',
    'r_io_desc_get_base', 'r_io_desc_get_pid', 'r_io_desc_get_tid',
    'r_io_desc_is_blockdevice', 'r_io_desc_is_chardevice',
    'r_io_desc_is_dbg', 'r_io_desc_new', 'r_io_desc_open',
    'r_io_desc_open_plugin', 'r_io_desc_read', 'r_io_desc_read_at',
    'r_io_desc_resize', 'r_io_desc_seek', 'r_io_desc_size',
    'r_io_desc_write', 'r_io_desc_write_at', 'r_io_extend_at',
    'r_io_fd_close', 'r_io_fd_get_base', 'r_io_fd_get_current',
    'r_io_fd_get_name', 'r_io_fd_get_pid', 'r_io_fd_get_tid',
    'r_io_fd_is_blockdevice', 'r_io_fd_is_chardevice',
    'r_io_fd_is_dbg', 'r_io_fd_open', 'r_io_fd_read',
    'r_io_fd_read_at', 'r_io_fd_resize', 'r_io_fd_seek',
    'r_io_fd_size', 'r_io_fd_write', 'r_io_fd_write_at', 'r_io_fini',
    'r_io_free', 'r_io_init', 'r_io_is_listener',
    'r_io_is_valid_offset', 'r_io_map_add', 'r_io_map_add_batch',
    'r_io_map_cleanup', 'r_io_map_del', 'r_io_map_del_for_fd',
    'r_io_map_del_name', 'r_io_map_depriorize', 'r_io_map_exists',
    'r_io_map_exists_for_id', 'r_io_map_fini', 'r_io_map_get',
    'r_io_map_get_for_fd', 'r_io_map_get_paddr', 'r_io_map_init',
    'r_io_map_is_mapped', 'r_io_map_location', 'r_io_map_new',
    'r_io_map_next_address', 'r_io_map_next_available',
    'r_io_map_priorize', 'r_io_map_priorize_for_fd', 'r_io_map_remap',
    'r_io_map_remap_fd', 'r_io_map_reset', 'r_io_map_resize',
    'r_io_map_resolve', 'r_io_map_set_name', 'r_io_new',
    'r_io_nread_at', 'r_io_open', 'r_io_open_at', 'r_io_open_buffer',
    'r_io_open_many', 'r_io_open_nomap', 'r_io_p2v',
    'r_io_plugin_add', 'r_io_plugin_ar', 'r_io_plugin_bfdbg',
    'r_io_plugin_bochs', 'r_io_plugin_debug', 'r_io_plugin_default',
    'r_io_plugin_fd', 'r_io_plugin_gdb', 'r_io_plugin_get_default',
    'r_io_plugin_gprobe', 'r_io_plugin_gzip', 'r_io_plugin_http',
    'r_io_plugin_ihex', 'r_io_plugin_init', 'r_io_plugin_list',
    'r_io_plugin_list_json', 'r_io_plugin_mach', 'r_io_plugin_malloc',
    'r_io_plugin_mmap', 'r_io_plugin_null', 'r_io_plugin_procpid',
    'r_io_plugin_ptrace', 'r_io_plugin_qnx', 'r_io_plugin_r2k',
    'r_io_plugin_r2pipe', 'r_io_plugin_r2web', 'r_io_plugin_rap',
    'r_io_plugin_rbuf', 'r_io_plugin_read', 'r_io_plugin_read_at',
    'r_io_plugin_resolve', 'r_io_plugin_self', 'r_io_plugin_shm',
    'r_io_plugin_sparse', 'r_io_plugin_tcp', 'r_io_plugin_w32',
    'r_io_plugin_w32dbg', 'r_io_plugin_windbg', 'r_io_plugin_winedbg',
    'r_io_plugin_winkd', 'r_io_plugin_write', 'r_io_plugin_write_at',
    'r_io_plugin_zip', 'r_io_pread_at', 'r_io_ptrace',
    'r_io_ptrace_fork', 'r_io_ptrace_func', 'r_io_pwrite_at',
    'r_io_read', 'r_io_read_at', 'r_io_read_at_mapped', 'r_io_read_i',
    'r_io_reopen', 'r_io_resize', 'r_io_seek', 'r_io_set_write_mask',
    'r_io_shift', 'r_io_size', 'r_io_sundo', 'r_io_sundo_list',
    'r_io_sundo_push', 'r_io_sundo_redo', 'r_io_sundo_reset',
    'r_io_system', 'r_io_undo_enable', 'r_io_undo_init',
    'r_io_update', 'r_io_use_fd', 'r_io_v2p', 'r_io_version',
    'r_io_vread_at_mapped', 'r_io_write', 'r_io_write_at',
    'r_io_write_i', 'r_io_wundo_apply', 'r_io_wundo_apply_all',
    'r_io_wundo_clear', 'r_io_wundo_list', 'r_io_wundo_new',
    'r_io_wundo_set', 'r_io_wundo_size', 'r_ptrace_data_t',
    'r_ptrace_request_t', 'r_ptrace_request_t__enumvalues',
    'struct_c__SA_RIODescData', 'struct_c__SA_RIORap',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_in_addr',
    'struct_ls_iter_t', 'struct_ls_t',
    'struct_ptrace_wrap_instance_t', 'struct_r_buf_t',
    'struct_r_buffer_methods_t', 'struct_r_cache_t',
    'struct_r_core_bind_t', 'struct_r_id_pool_t',
    'struct_r_id_storage_t', 'struct_r_interval_t',
    'struct_r_io_bind_t', 'struct_r_io_cache_t',
    'struct_r_io_desc_cache_t', 'struct_r_io_desc_t',
    'struct_r_io_map_skyline_t', 'struct_r_io_map_t',
    'struct_r_io_plugin_t', 'struct_r_io_t', 'struct_r_io_undo_t',
    'struct_r_io_undo_w_t', 'struct_r_io_undos_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_pvector_t',
    'struct_r_queue_t', 'struct_r_rb_node_t', 'struct_r_socket_t',
    'struct_r_vector_t', 'struct_sockaddr_in']

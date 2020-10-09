# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_bp as _libr_bp


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

r_bp_version = _libr_bp.r_bp_version
r_bp_version.restype = POINTER_T(ctypes.c_char)
r_bp_version.argtypes = []
class struct_r_bp_arch_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bits', ctypes.c_int32),
    ('length', ctypes.c_int32),
    ('endian', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('bytes', POINTER_T(ctypes.c_ubyte)),
     ]

RBreakpointArch = struct_r_bp_arch_t

# values for enumeration 'c__Ea_R_BP_TYPE_SW'
c__Ea_R_BP_TYPE_SW__enumvalues = {
    0: 'R_BP_TYPE_SW',
    1: 'R_BP_TYPE_HW',
    2: 'R_BP_TYPE_COND',
    3: 'R_BP_TYPE_FAULT',
    4: 'R_BP_TYPE_DELETE',
}
R_BP_TYPE_SW = 0
R_BP_TYPE_HW = 1
R_BP_TYPE_COND = 2
R_BP_TYPE_FAULT = 3
R_BP_TYPE_DELETE = 4
c__Ea_R_BP_TYPE_SW = ctypes.c_int # enum
class struct_r_bp_plugin_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_int32),
    ('nbps', ctypes.c_int32),
    ('bps', POINTER_T(struct_r_bp_arch_t)),
     ]

RBreakpointPlugin = struct_r_bp_plugin_t
class struct_r_bp_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('module_name', POINTER_T(ctypes.c_char)),
    ('module_delta', ctypes.c_int64),
    ('addr', ctypes.c_uint64),
    ('delta', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('recoil', ctypes.c_int32),
    ('swstep', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('perm', ctypes.c_int32),
    ('hw', ctypes.c_int32),
    ('trace', ctypes.c_int32),
    ('internal', ctypes.c_int32),
    ('enabled', ctypes.c_int32),
    ('togglehits', ctypes.c_int32),
    ('hits', ctypes.c_int32),
    ('obytes', POINTER_T(ctypes.c_ubyte)),
    ('bbytes', POINTER_T(ctypes.c_ubyte)),
    ('pids', ctypes.c_int32 * 10),
    ('data', POINTER_T(ctypes.c_char)),
    ('cond', POINTER_T(ctypes.c_char)),
    ('expr', POINTER_T(ctypes.c_char)),
     ]

RBreakpointItem = struct_r_bp_item_t
class struct_r_bp_t(ctypes.Structure):
    pass

RBreakpointCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_item_t), ctypes.c_bool))
class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_io_map_t(ctypes.Structure):
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
class struct_r_io_undo_t(ctypes.Structure):
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

class struct_r_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', ctypes.c_uint64),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_uint64),
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

struct_r_bp_t._pack_ = True # source:False
struct_r_bp_t._fields_ = [
    ('user', POINTER_T(None)),
    ('stepcont', ctypes.c_int32),
    ('endian', ctypes.c_int32),
    ('bits', ctypes.c_int32),
    ('bpinmaps', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('corebind', struct_r_core_bind_t),
    ('iob', struct_r_io_bind_t),
    ('cur', POINTER_T(struct_r_bp_plugin_t)),
    ('traces', POINTER_T(struct_r_list_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('breakpoint', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_item_t), ctypes.c_bool))),
    ('nbps', ctypes.c_int32),
    ('nhwbps', ctypes.c_int32),
    ('bps', POINTER_T(struct_r_list_t)),
    ('bps_idx', POINTER_T(POINTER_T(struct_r_bp_item_t))),
    ('bps_idx_count', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('delta', ctypes.c_int64),
    ('baddr', ctypes.c_uint64),
]

RBreakpoint = struct_r_bp_t

# values for enumeration 'c__Ea_R_BP_PROT_EXEC'
c__Ea_R_BP_PROT_EXEC__enumvalues = {
    1: 'R_BP_PROT_EXEC',
    2: 'R_BP_PROT_WRITE',
    4: 'R_BP_PROT_READ',
    8: 'R_BP_PROT_ACCESS',
}
R_BP_PROT_EXEC = 1
R_BP_PROT_WRITE = 2
R_BP_PROT_READ = 4
R_BP_PROT_ACCESS = 8
c__Ea_R_BP_PROT_EXEC = ctypes.c_int # enum
class struct_r_bp_trace_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('addr_end', ctypes.c_uint64),
    ('traps', POINTER_T(ctypes.c_ubyte)),
    ('buffer', POINTER_T(ctypes.c_ubyte)),
    ('bits', POINTER_T(ctypes.c_ubyte)),
    ('length', ctypes.c_int32),
    ('bitlen', ctypes.c_int32),
     ]

RBreakpointTrace = struct_r_bp_trace_t
r_bp_new = _libr_bp.r_bp_new
r_bp_new.restype = POINTER_T(struct_r_bp_t)
r_bp_new.argtypes = []
r_bp_free = _libr_bp.r_bp_free
r_bp_free.restype = POINTER_T(struct_r_bp_t)
r_bp_free.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_del = _libr_bp.r_bp_del
r_bp_del.restype = ctypes.c_int32
r_bp_del.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64]
r_bp_del_all = _libr_bp.r_bp_del_all
r_bp_del_all.restype = ctypes.c_int32
r_bp_del_all.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_plugin_add = _libr_bp.r_bp_plugin_add
r_bp_plugin_add.restype = ctypes.c_int32
r_bp_plugin_add.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_plugin_t)]
r_bp_use = _libr_bp.r_bp_use
r_bp_use.restype = ctypes.c_int32
r_bp_use.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bp_plugin_del = _libr_bp.r_bp_plugin_del
r_bp_plugin_del.restype = ctypes.c_int32
r_bp_plugin_del.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(ctypes.c_char)]
r_bp_plugin_list = _libr_bp.r_bp_plugin_list
r_bp_plugin_list.restype = None
r_bp_plugin_list.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_list = _libr_bp.r_bp_list
r_bp_list.restype = ctypes.c_int32
r_bp_list.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_size = _libr_bp.r_bp_size
r_bp_size.restype = ctypes.c_int32
r_bp_size.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_get_bytes = _libr_bp.r_bp_get_bytes
r_bp_get_bytes.restype = ctypes.c_int32
r_bp_get_bytes.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_bp_set_trace = _libr_bp.r_bp_set_trace
r_bp_set_trace.restype = ctypes.c_int32
r_bp_set_trace.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32]
r_bp_set_trace_all = _libr_bp.r_bp_set_trace_all
r_bp_set_trace_all.restype = ctypes.c_int32
r_bp_set_trace_all.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_enable = _libr_bp.r_bp_enable
r_bp_enable.restype = POINTER_T(struct_r_bp_item_t)
r_bp_enable.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_bp_enable_all = _libr_bp.r_bp_enable_all
r_bp_enable_all.restype = ctypes.c_int32
r_bp_enable_all.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_del_index = _libr_bp.r_bp_del_index
r_bp_del_index.restype = ctypes.c_int32
r_bp_del_index.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_get_index = _libr_bp.r_bp_get_index
r_bp_get_index.restype = POINTER_T(struct_r_bp_item_t)
r_bp_get_index.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_get_index_at = _libr_bp.r_bp_get_index_at
r_bp_get_index_at.restype = ctypes.c_int32
r_bp_get_index_at.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64]
r_bp_item_new = _libr_bp.r_bp_item_new
r_bp_item_new.restype = POINTER_T(struct_r_bp_item_t)
r_bp_item_new.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_get_at = _libr_bp.r_bp_get_at
r_bp_get_at.restype = POINTER_T(struct_r_bp_item_t)
r_bp_get_at.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64]
r_bp_get_in = _libr_bp.r_bp_get_in
r_bp_get_in.restype = POINTER_T(struct_r_bp_item_t)
r_bp_get_in.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32]
r_bp_is_valid = _libr_bp.r_bp_is_valid
r_bp_is_valid.restype = ctypes.c_bool
r_bp_is_valid.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_item_t)]
r_bp_add_fault = _libr_bp.r_bp_add_fault
r_bp_add_fault.restype = ctypes.c_int32
r_bp_add_fault.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_bp_add_sw = _libr_bp.r_bp_add_sw
r_bp_add_sw.restype = POINTER_T(struct_r_bp_item_t)
r_bp_add_sw.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_bp_add_hw = _libr_bp.r_bp_add_hw
r_bp_add_hw.restype = POINTER_T(struct_r_bp_item_t)
r_bp_add_hw.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_bp_restore_one = _libr_bp.r_bp_restore_one
r_bp_restore_one.restype = None
r_bp_restore_one.argtypes = [POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_item_t), ctypes.c_bool]
r_bp_restore = _libr_bp.r_bp_restore
r_bp_restore.restype = ctypes.c_int32
r_bp_restore.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_bool]
r_bp_restore_except = _libr_bp.r_bp_restore_except
r_bp_restore_except.restype = ctypes.c_bool
r_bp_restore_except.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_bool, ctypes.c_uint64]
r_bp_traptrace_free = _libr_bp.r_bp_traptrace_free
r_bp_traptrace_free.restype = None
r_bp_traptrace_free.argtypes = [POINTER_T(None)]
r_bp_traptrace_enable = _libr_bp.r_bp_traptrace_enable
r_bp_traptrace_enable.restype = None
r_bp_traptrace_enable.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_traptrace_reset = _libr_bp.r_bp_traptrace_reset
r_bp_traptrace_reset.restype = None
r_bp_traptrace_reset.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_int32]
r_bp_traptrace_next = _libr_bp.r_bp_traptrace_next
r_bp_traptrace_next.restype = ctypes.c_uint64
r_bp_traptrace_next.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64]
r_bp_traptrace_add = _libr_bp.r_bp_traptrace_add
r_bp_traptrace_add.restype = ctypes.c_int32
r_bp_traptrace_add.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_uint64]
r_bp_traptrace_free_at = _libr_bp.r_bp_traptrace_free_at
r_bp_traptrace_free_at.restype = ctypes.c_int32
r_bp_traptrace_free_at.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64]
r_bp_traptrace_list = _libr_bp.r_bp_traptrace_list
r_bp_traptrace_list.restype = None
r_bp_traptrace_list.argtypes = [POINTER_T(struct_r_bp_t)]
r_bp_traptrace_at = _libr_bp.r_bp_traptrace_at
r_bp_traptrace_at.restype = ctypes.c_int32
r_bp_traptrace_at.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32]
r_bp_traptrace_new = _libr_bp.r_bp_traptrace_new
r_bp_traptrace_new.restype = POINTER_T(struct_r_list_t)
r_bp_traptrace_new.argtypes = []
r_bp_watch_add = _libr_bp.r_bp_watch_add
r_bp_watch_add.restype = POINTER_T(struct_r_bp_item_t)
r_bp_watch_add.argtypes = [POINTER_T(struct_r_bp_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_bp_plugin_x86 = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
r_bp_plugin_arm = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
r_bp_plugin_mips = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
r_bp_plugin_ppc = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
r_bp_plugin_sh = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
r_bp_plugin_bf = struct_r_bp_plugin_t # Variable struct_r_bp_plugin_t
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
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'RBreakpoint',
    'RBreakpointArch', 'RBreakpointCallback', 'RBreakpointItem',
    'RBreakpointPlugin', 'RBreakpointTrace', 'R_BP_PROT_ACCESS',
    'R_BP_PROT_EXEC', 'R_BP_PROT_READ', 'R_BP_PROT_WRITE',
    'R_BP_TYPE_COND', 'R_BP_TYPE_DELETE', 'R_BP_TYPE_FAULT',
    'R_BP_TYPE_HW', 'R_BP_TYPE_SW', '__ptrace_request',
    'c__Ea_R_BP_PROT_EXEC', 'c__Ea_R_BP_TYPE_SW', 'r_bp_add_fault',
    'r_bp_add_hw', 'r_bp_add_sw', 'r_bp_del', 'r_bp_del_all',
    'r_bp_del_index', 'r_bp_enable', 'r_bp_enable_all', 'r_bp_free',
    'r_bp_get_at', 'r_bp_get_bytes', 'r_bp_get_in', 'r_bp_get_index',
    'r_bp_get_index_at', 'r_bp_is_valid', 'r_bp_item_new',
    'r_bp_list', 'r_bp_new', 'r_bp_plugin_add', 'r_bp_plugin_arm',
    'r_bp_plugin_bf', 'r_bp_plugin_del', 'r_bp_plugin_list',
    'r_bp_plugin_mips', 'r_bp_plugin_ppc', 'r_bp_plugin_sh',
    'r_bp_plugin_x86', 'r_bp_restore', 'r_bp_restore_except',
    'r_bp_restore_one', 'r_bp_set_trace', 'r_bp_set_trace_all',
    'r_bp_size', 'r_bp_traptrace_add', 'r_bp_traptrace_at',
    'r_bp_traptrace_enable', 'r_bp_traptrace_free',
    'r_bp_traptrace_free_at', 'r_bp_traptrace_list',
    'r_bp_traptrace_new', 'r_bp_traptrace_next',
    'r_bp_traptrace_reset', 'r_bp_use', 'r_bp_version',
    'r_bp_watch_add', 'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_ptrace_wrap_instance_t',
    'struct_r_bp_arch_t', 'struct_r_bp_item_t',
    'struct_r_bp_plugin_t', 'struct_r_bp_t', 'struct_r_bp_trace_t',
    'struct_r_cache_t', 'struct_r_core_bind_t', 'struct_r_id_pool_t',
    'struct_r_id_storage_t', 'struct_r_interval_t',
    'struct_r_io_bind_t', 'struct_r_io_desc_t', 'struct_r_io_map_t',
    'struct_r_io_plugin_t', 'struct_r_io_t', 'struct_r_io_undo_t',
    'struct_r_io_undos_t', 'struct_r_list_iter_t', 'struct_r_list_t',
    'struct_r_pvector_t', 'struct_r_queue_t', 'struct_r_rb_node_t',
    'struct_r_vector_t']

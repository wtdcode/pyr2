# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_config as _libr_config


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



RConfigCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(None)))
class struct_r_config_node_t(ctypes.Structure):
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

struct_r_config_node_t._pack_ = True # source:False
struct_r_config_node_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('flags', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('value', POINTER_T(ctypes.c_char)),
    ('i_value', ctypes.c_uint64),
    ('cb_ptr_q', POINTER_T(ctypes.c_uint64)),
    ('cb_ptr_i', POINTER_T(ctypes.c_int32)),
    ('cb_ptr_s', POINTER_T(POINTER_T(ctypes.c_char))),
    ('getter', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(None)))),
    ('setter', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(None)))),
    ('desc', POINTER_T(ctypes.c_char)),
    ('options', POINTER_T(struct_r_list_t)),
]

RConfigNode = struct_r_config_node_t
r_config_node_type = _libr_config.r_config_node_type
r_config_node_type.restype = POINTER_T(ctypes.c_char)
r_config_node_type.argtypes = [POINTER_T(struct_r_config_node_t)]
class struct_r_config_t(ctypes.Structure):
    pass

class struct_r_num_t(ctypes.Structure):
    pass

class struct_r_num_calc_t(ctypes.Structure):
    pass


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
class struct_c__SA_RNumCalcValue(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('d', ctypes.c_double),
    ('n', ctypes.c_uint64),
     ]

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

struct_r_config_t._pack_ = True # source:False
struct_r_config_t._fields_ = [
    ('lock', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('user', POINTER_T(None)),
    ('num', POINTER_T(struct_r_num_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('nodes', POINTER_T(struct_r_list_t)),
    ('ht', POINTER_T(struct_ht_pp_t)),
]

RConfig = struct_r_config_t
class struct_r_config_hold_num_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('key', POINTER_T(ctypes.c_char)),
    ('value', ctypes.c_uint64),
     ]

RConfigHoldNum = struct_r_config_hold_num_t
class struct_r_config_hold_char_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('key', POINTER_T(ctypes.c_char)),
    ('value', POINTER_T(ctypes.c_char)),
     ]

RConfigHoldChar = struct_r_config_hold_char_t
class struct_r_config_hold_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cfg', POINTER_T(struct_r_config_t)),
    ('list_num', POINTER_T(struct_r_list_t)),
    ('list_char', POINTER_T(struct_r_list_t)),
     ]

RConfigHold = struct_r_config_hold_t
r_config_hold_new = _libr_config.r_config_hold_new
r_config_hold_new.restype = POINTER_T(struct_r_config_hold_t)
r_config_hold_new.argtypes = [POINTER_T(struct_r_config_t)]
r_config_hold_free = _libr_config.r_config_hold_free
r_config_hold_free.restype = None
r_config_hold_free.argtypes = [POINTER_T(struct_r_config_hold_t)]
r_config_hold_i = _libr_config.r_config_hold_i
r_config_hold_i.restype = ctypes.c_bool
r_config_hold_i.argtypes = [POINTER_T(struct_r_config_hold_t)]
r_config_hold_s = _libr_config.r_config_hold_s
r_config_hold_s.restype = ctypes.c_bool
r_config_hold_s.argtypes = [POINTER_T(struct_r_config_hold_t)]
r_config_hold_restore = _libr_config.r_config_hold_restore
r_config_hold_restore.restype = None
r_config_hold_restore.argtypes = [POINTER_T(struct_r_config_hold_t)]
r_config_new = _libr_config.r_config_new
r_config_new.restype = POINTER_T(struct_r_config_t)
r_config_new.argtypes = [POINTER_T(None)]
r_config_clone = _libr_config.r_config_clone
r_config_clone.restype = POINTER_T(struct_r_config_t)
r_config_clone.argtypes = [POINTER_T(struct_r_config_t)]
r_config_free = _libr_config.r_config_free
r_config_free.restype = None
r_config_free.argtypes = [POINTER_T(struct_r_config_t)]
r_config_lock = _libr_config.r_config_lock
r_config_lock.restype = None
r_config_lock.argtypes = [POINTER_T(struct_r_config_t), ctypes.c_int32]
r_config_eval = _libr_config.r_config_eval
r_config_eval.restype = ctypes.c_bool
r_config_eval.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_config_bump = _libr_config.r_config_bump
r_config_bump.restype = None
r_config_bump.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_set_i = _libr_config.r_config_set_i
r_config_set_i.restype = POINTER_T(struct_r_config_node_t)
r_config_set_i.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_config_set_cb = _libr_config.r_config_set_cb
r_config_set_cb.restype = POINTER_T(struct_r_config_node_t)
r_config_set_cb.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(None)))]
r_config_set_i_cb = _libr_config.r_config_set_i_cb
r_config_set_i_cb.restype = POINTER_T(struct_r_config_node_t)
r_config_set_i_cb.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(None)))]
r_config_set = _libr_config.r_config_set
r_config_set.restype = POINTER_T(struct_r_config_node_t)
r_config_set.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_config_rm = _libr_config.r_config_rm
r_config_rm.restype = ctypes.c_bool
r_config_rm.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_get_i = _libr_config.r_config_get_i
r_config_get_i.restype = ctypes.c_uint64
r_config_get_i.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_get = _libr_config.r_config_get
r_config_get.restype = POINTER_T(ctypes.c_char)
r_config_get.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_desc = _libr_config.r_config_desc
r_config_desc.restype = POINTER_T(ctypes.c_char)
r_config_desc.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_config_node_desc = _libr_config.r_config_node_desc
r_config_node_desc.restype = POINTER_T(ctypes.c_char)
r_config_node_desc.argtypes = [POINTER_T(struct_r_config_node_t), POINTER_T(ctypes.c_char)]
r_config_list = _libr_config.r_config_list
r_config_list.restype = None
r_config_list.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_config_node_get = _libr_config.r_config_node_get
r_config_node_get.restype = POINTER_T(struct_r_config_node_t)
r_config_node_get.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_node_new = _libr_config.r_config_node_new
r_config_node_new.restype = POINTER_T(struct_r_config_node_t)
r_config_node_new.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_config_node_free = _libr_config.r_config_node_free
r_config_node_free.restype = None
r_config_node_free.argtypes = [POINTER_T(None)]
size_t = ctypes.c_uint64
r_config_node_value_format_i = _libr_config.r_config_node_value_format_i
r_config_node_value_format_i.restype = None
r_config_node_value_format_i.argtypes = [POINTER_T(ctypes.c_char), size_t, ctypes.c_uint64, POINTER_T(struct_r_config_node_t)]
r_config_toggle = _libr_config.r_config_toggle
r_config_toggle.restype = ctypes.c_bool
r_config_toggle.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_readonly = _libr_config.r_config_readonly
r_config_readonly.restype = ctypes.c_bool
r_config_readonly.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char)]
r_config_set_setter = _libr_config.r_config_set_setter
r_config_set_setter.restype = ctypes.c_bool
r_config_set_setter.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), RConfigCallback]
r_config_set_getter = _libr_config.r_config_set_getter
r_config_set_getter.restype = ctypes.c_bool
r_config_set_getter.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(ctypes.c_char), RConfigCallback]
class struct_sdb_t(ctypes.Structure):
    pass

r_config_serialize = _libr_config.r_config_serialize
r_config_serialize.restype = None
r_config_serialize.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(struct_sdb_t)]
r_config_unserialize = _libr_config.r_config_unserialize
r_config_unserialize.restype = ctypes.c_bool
r_config_unserialize.argtypes = [POINTER_T(struct_r_config_t), POINTER_T(struct_sdb_t), POINTER_T(POINTER_T(ctypes.c_char))]
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

class struct_cdb_hp(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('h', ctypes.c_uint32),
    ('p', ctypes.c_uint32),
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

class struct_cdb_make(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

class struct_ls_iter_t(ctypes.Structure):
    pass

struct_ls_iter_t._pack_ = True # source:False
struct_ls_iter_t._fields_ = [
    ('data', POINTER_T(None)),
    ('n', POINTER_T(struct_ls_iter_t)),
    ('p', POINTER_T(struct_ls_iter_t)),
]

class struct_ls_t(ctypes.Structure):
    pass

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

__all__ = \
    ['RConfig', 'RConfigCallback', 'RConfigHold', 'RConfigHoldChar',
    'RConfigHoldNum', 'RConfigNode', 'RNCAND', 'RNCASSIGN', 'RNCDEC',
    'RNCDIV', 'RNCEND', 'RNCINC', 'RNCLEFTP', 'RNCMINUS', 'RNCMOD',
    'RNCMUL', 'RNCNAME', 'RNCNEG', 'RNCNUMBER', 'RNCORR', 'RNCPLUS',
    'RNCPRINT', 'RNCRIGHTP', 'RNCROL', 'RNCROR', 'RNCSHL', 'RNCSHR',
    'RNCXOR', 'c__EA_RNumCalcToken', 'r_config_bump',
    'r_config_clone', 'r_config_desc', 'r_config_eval',
    'r_config_free', 'r_config_get', 'r_config_get_i',
    'r_config_hold_free', 'r_config_hold_i', 'r_config_hold_new',
    'r_config_hold_restore', 'r_config_hold_s', 'r_config_list',
    'r_config_lock', 'r_config_new', 'r_config_node_desc',
    'r_config_node_free', 'r_config_node_get', 'r_config_node_new',
    'r_config_node_type', 'r_config_node_value_format_i',
    'r_config_readonly', 'r_config_rm', 'r_config_serialize',
    'r_config_set', 'r_config_set_cb', 'r_config_set_getter',
    'r_config_set_i', 'r_config_set_i_cb', 'r_config_set_setter',
    'r_config_toggle', 'r_config_unserialize', 'size_t',
    'struct_buffer', 'struct_c__SA_RNumCalcValue',
    'struct_c__SA_dict', 'struct_cdb', 'struct_cdb_hp',
    'struct_cdb_hplist', 'struct_cdb_make', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ls_iter_t', 'struct_ls_t', 'struct_r_config_hold_char_t',
    'struct_r_config_hold_num_t', 'struct_r_config_hold_t',
    'struct_r_config_node_t', 'struct_r_config_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_num_calc_t',
    'struct_r_num_t', 'struct_sdb_kv', 'struct_sdb_t']

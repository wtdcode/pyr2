# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_flag as _libr_flag


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



r_flag_version = _libr_flag.r_flag_version
r_flag_version.restype = POINTER_T(ctypes.c_char)
r_flag_version.argtypes = []
class struct_r_flag_zone_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('name', POINTER_T(ctypes.c_char)),
     ]

RFlagZoneItem = struct_r_flag_zone_item_t
class struct_r_flags_at_offset_t(ctypes.Structure):
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

struct_r_flags_at_offset_t._pack_ = True # source:False
struct_r_flags_at_offset_t._fields_ = [
    ('off', ctypes.c_uint64),
    ('flags', POINTER_T(struct_r_list_t)),
]

RFlagsAtOffset = struct_r_flags_at_offset_t
class struct_r_flag_item_t(ctypes.Structure):
    pass

class struct_r_space_t(ctypes.Structure):
    pass

class struct_r_rb_node_t(ctypes.Structure):
    pass

struct_r_rb_node_t._pack_ = True # source:False
struct_r_rb_node_t._fields_ = [
    ('child', POINTER_T(struct_r_rb_node_t) * 2),
    ('red', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

struct_r_space_t._pack_ = True # source:False
struct_r_space_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('rb', struct_r_rb_node_t),
]

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

RFlagItem = struct_r_flag_item_t
class struct_r_flag_t(ctypes.Structure):
    pass

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

class struct_r_spaces_t(ctypes.Structure):
    pass

class struct_r_event_t(ctypes.Structure):
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

struct_r_event_t._pack_ = True # source:False
struct_r_event_t._fields_ = [
    ('user', POINTER_T(None)),
    ('incall', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('callbacks', POINTER_T(struct_ht_up_t)),
    ('all_callbacks', struct_r_vector_t),
    ('next_handle', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

struct_r_spaces_t._pack_ = True # source:False
struct_r_spaces_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('current', POINTER_T(struct_r_space_t)),
    ('spaces', POINTER_T(struct_r_rb_node_t)),
    ('spacestack', POINTER_T(struct_r_list_t)),
    ('event', POINTER_T(struct_r_event_t)),
]

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

class struct_cdb_hplist(ctypes.Structure):
    pass

struct_cdb_hplist._pack_ = True # source:False
struct_cdb_hplist._fields_ = [
    ('hp', struct_cdb_hp * 1000),
    ('next', POINTER_T(struct_cdb_hplist)),
    ('num', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
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

class struct_sdb_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', struct_ht_pp_kv),
    ('cas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('expire', ctypes.c_uint64),
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

RFlag = struct_r_flag_t
RFlagExistAt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint16, ctypes.c_uint64))
RFlagGet = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))
RFlagGetAtAddr = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64))
RFlagGetAt = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_bool))
RFlagGetList = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_flag_t), ctypes.c_uint64))
RFlagSet = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_flag_item_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32))
RFlagUnset = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(struct_r_flag_item_t)))
RFlagUnsetName = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))
RFlagUnsetOff = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), ctypes.c_uint64))
RFlagSetSpace = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_space_t), POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))
RFlagPopSpace = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t)))
RFlagPushSpace = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)))
RFlagItemCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_flag_item_t), POINTER_T(None)))
class struct_r_flag_bind_t(ctypes.Structure):
    pass

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

RFlagBind = struct_r_flag_bind_t
r_flag_bind = _libr_flag.r_flag_bind
r_flag_bind.restype = None
r_flag_bind.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(struct_r_flag_bind_t)]
r_flag_new = _libr_flag.r_flag_new
r_flag_new.restype = POINTER_T(struct_r_flag_t)
r_flag_new.argtypes = []
r_flag_free = _libr_flag.r_flag_free
r_flag_free.restype = POINTER_T(struct_r_flag_t)
r_flag_free.argtypes = [POINTER_T(struct_r_flag_t)]
r_flag_list = _libr_flag.r_flag_list
r_flag_list.restype = None
r_flag_list.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_flag_exist_at = _libr_flag.r_flag_exist_at
r_flag_exist_at.restype = ctypes.c_bool
r_flag_exist_at.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint16, ctypes.c_uint64]
r_flag_get = _libr_flag.r_flag_get
r_flag_get.restype = POINTER_T(struct_r_flag_item_t)
r_flag_get.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_get_i = _libr_flag.r_flag_get_i
r_flag_get_i.restype = POINTER_T(struct_r_flag_item_t)
r_flag_get_i.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_flag_get_by_spaces = _libr_flag.r_flag_get_by_spaces
r_flag_get_by_spaces.restype = POINTER_T(struct_r_flag_item_t)
r_flag_get_by_spaces.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_flag_get_at = _libr_flag.r_flag_get_at
r_flag_get_at.restype = POINTER_T(struct_r_flag_item_t)
r_flag_get_at.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_bool]
r_flag_all_list = _libr_flag.r_flag_all_list
r_flag_all_list.restype = POINTER_T(struct_r_list_t)
r_flag_all_list.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_bool]
r_flag_get_list = _libr_flag.r_flag_get_list
r_flag_get_list.restype = POINTER_T(struct_r_list_t)
r_flag_get_list.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_flag_get_liststr = _libr_flag.r_flag_get_liststr
r_flag_get_liststr.restype = POINTER_T(ctypes.c_char)
r_flag_get_liststr.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_flag_unset = _libr_flag.r_flag_unset
r_flag_unset.restype = ctypes.c_bool
r_flag_unset.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(struct_r_flag_item_t)]
r_flag_unset_name = _libr_flag.r_flag_unset_name
r_flag_unset_name.restype = ctypes.c_bool
r_flag_unset_name.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_unset_off = _libr_flag.r_flag_unset_off
r_flag_unset_off.restype = ctypes.c_bool
r_flag_unset_off.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_flag_unset_all = _libr_flag.r_flag_unset_all
r_flag_unset_all.restype = None
r_flag_unset_all.argtypes = [POINTER_T(struct_r_flag_t)]
r_flag_set = _libr_flag.r_flag_set
r_flag_set.restype = POINTER_T(struct_r_flag_item_t)
r_flag_set.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32]
r_flag_set_next = _libr_flag.r_flag_set_next
r_flag_set_next.restype = POINTER_T(struct_r_flag_item_t)
r_flag_set_next.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint32]
r_flag_item_set_alias = _libr_flag.r_flag_item_set_alias
r_flag_item_set_alias.restype = None
r_flag_item_set_alias.argtypes = [POINTER_T(struct_r_flag_item_t), POINTER_T(ctypes.c_char)]
r_flag_item_free = _libr_flag.r_flag_item_free
r_flag_item_free.restype = None
r_flag_item_free.argtypes = [POINTER_T(struct_r_flag_item_t)]
r_flag_item_set_comment = _libr_flag.r_flag_item_set_comment
r_flag_item_set_comment.restype = None
r_flag_item_set_comment.argtypes = [POINTER_T(struct_r_flag_item_t), POINTER_T(ctypes.c_char)]
r_flag_item_set_realname = _libr_flag.r_flag_item_set_realname
r_flag_item_set_realname.restype = None
r_flag_item_set_realname.argtypes = [POINTER_T(struct_r_flag_item_t), POINTER_T(ctypes.c_char)]
r_flag_item_set_color = _libr_flag.r_flag_item_set_color
r_flag_item_set_color.restype = POINTER_T(ctypes.c_char)
r_flag_item_set_color.argtypes = [POINTER_T(struct_r_flag_item_t), POINTER_T(ctypes.c_char)]
r_flag_item_clone = _libr_flag.r_flag_item_clone
r_flag_item_clone.restype = POINTER_T(struct_r_flag_item_t)
r_flag_item_clone.argtypes = [POINTER_T(struct_r_flag_item_t)]
r_flag_unset_glob = _libr_flag.r_flag_unset_glob
r_flag_unset_glob.restype = ctypes.c_int32
r_flag_unset_glob.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_rename = _libr_flag.r_flag_rename
r_flag_rename.restype = ctypes.c_int32
r_flag_rename.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(struct_r_flag_item_t), POINTER_T(ctypes.c_char)]
r_flag_relocate = _libr_flag.r_flag_relocate
r_flag_relocate.restype = ctypes.c_int32
r_flag_relocate.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_flag_move = _libr_flag.r_flag_move
r_flag_move.restype = ctypes.c_bool
r_flag_move.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_uint64]
r_flag_count = _libr_flag.r_flag_count
r_flag_count.restype = ctypes.c_int32
r_flag_count.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_foreach = _libr_flag.r_flag_foreach
r_flag_foreach.restype = None
r_flag_foreach.argtypes = [POINTER_T(struct_r_flag_t), RFlagItemCb, POINTER_T(None)]
r_flag_foreach_prefix = _libr_flag.r_flag_foreach_prefix
r_flag_foreach_prefix.restype = None
r_flag_foreach_prefix.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_int32, RFlagItemCb, POINTER_T(None)]
r_flag_foreach_range = _libr_flag.r_flag_foreach_range
r_flag_foreach_range.restype = None
r_flag_foreach_range.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_uint64, RFlagItemCb, POINTER_T(None)]
r_flag_foreach_glob = _libr_flag.r_flag_foreach_glob
r_flag_foreach_glob.restype = None
r_flag_foreach_glob.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), RFlagItemCb, POINTER_T(None)]
r_flag_foreach_space = _libr_flag.r_flag_foreach_space
r_flag_foreach_space.restype = None
r_flag_foreach_space.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(struct_r_space_t), RFlagItemCb, POINTER_T(None)]
r_flag_foreach_space_glob = _libr_flag.r_flag_foreach_space_glob
r_flag_foreach_space_glob.restype = None
r_flag_foreach_space_glob.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_space_t), RFlagItemCb, POINTER_T(None)]
r_flag_tags_list = _libr_flag.r_flag_tags_list
r_flag_tags_list.restype = POINTER_T(struct_r_list_t)
r_flag_tags_list.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_tags_set = _libr_flag.r_flag_tags_set
r_flag_tags_set.restype = POINTER_T(struct_r_list_t)
r_flag_tags_set.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_flag_tags_reset = _libr_flag.r_flag_tags_reset
r_flag_tags_reset.restype = None
r_flag_tags_reset.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_tags_get = _libr_flag.r_flag_tags_get
r_flag_tags_get.restype = POINTER_T(struct_r_list_t)
r_flag_tags_get.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_zone_item_free = _libr_flag.r_flag_zone_item_free
r_flag_zone_item_free.restype = None
r_flag_zone_item_free.argtypes = [POINTER_T(None)]
r_flag_zone_add = _libr_flag.r_flag_zone_add
r_flag_zone_add.restype = ctypes.c_bool
r_flag_zone_add.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_flag_zone_del = _libr_flag.r_flag_zone_del
r_flag_zone_del.restype = ctypes.c_bool
r_flag_zone_del.argtypes = [POINTER_T(struct_r_flag_t), POINTER_T(ctypes.c_char)]
r_flag_zone_around = _libr_flag.r_flag_zone_around
r_flag_zone_around.restype = ctypes.c_bool
r_flag_zone_around.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, POINTER_T(POINTER_T(ctypes.c_char)), POINTER_T(POINTER_T(ctypes.c_char))]
r_flag_zone_list = _libr_flag.r_flag_zone_list
r_flag_zone_list.restype = ctypes.c_bool
r_flag_zone_list.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_int32]
r_flag_zone_reset = _libr_flag.r_flag_zone_reset
r_flag_zone_reset.restype = ctypes.c_bool
r_flag_zone_reset.argtypes = [POINTER_T(struct_r_flag_t)]
r_flag_zone_barlist = _libr_flag.r_flag_zone_barlist
r_flag_zone_barlist.restype = POINTER_T(struct_r_list_t)
r_flag_zone_barlist.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
__all__ = \
    ['RFlag', 'RFlagBind', 'RFlagExistAt', 'RFlagGet', 'RFlagGetAt',
    'RFlagGetAtAddr', 'RFlagGetList', 'RFlagItem', 'RFlagItemCb',
    'RFlagPopSpace', 'RFlagPushSpace', 'RFlagSet', 'RFlagSetSpace',
    'RFlagUnset', 'RFlagUnsetName', 'RFlagUnsetOff', 'RFlagZoneItem',
    'RFlagsAtOffset', 'RNCAND', 'RNCASSIGN', 'RNCDEC', 'RNCDIV',
    'RNCEND', 'RNCINC', 'RNCLEFTP', 'RNCMINUS', 'RNCMOD', 'RNCMUL',
    'RNCNAME', 'RNCNEG', 'RNCNUMBER', 'RNCORR', 'RNCPLUS', 'RNCPRINT',
    'RNCRIGHTP', 'RNCROL', 'RNCROR', 'RNCSHL', 'RNCSHR', 'RNCXOR',
    'c__EA_RNumCalcToken', 'r_flag_all_list', 'r_flag_bind',
    'r_flag_count', 'r_flag_exist_at', 'r_flag_foreach',
    'r_flag_foreach_glob', 'r_flag_foreach_prefix',
    'r_flag_foreach_range', 'r_flag_foreach_space',
    'r_flag_foreach_space_glob', 'r_flag_free', 'r_flag_get',
    'r_flag_get_at', 'r_flag_get_by_spaces', 'r_flag_get_i',
    'r_flag_get_list', 'r_flag_get_liststr', 'r_flag_item_clone',
    'r_flag_item_free', 'r_flag_item_set_alias',
    'r_flag_item_set_color', 'r_flag_item_set_comment',
    'r_flag_item_set_realname', 'r_flag_list', 'r_flag_move',
    'r_flag_new', 'r_flag_relocate', 'r_flag_rename', 'r_flag_set',
    'r_flag_set_next', 'r_flag_tags_get', 'r_flag_tags_list',
    'r_flag_tags_reset', 'r_flag_tags_set', 'r_flag_unset',
    'r_flag_unset_all', 'r_flag_unset_glob', 'r_flag_unset_name',
    'r_flag_unset_off', 'r_flag_version', 'r_flag_zone_add',
    'r_flag_zone_around', 'r_flag_zone_barlist', 'r_flag_zone_del',
    'r_flag_zone_item_free', 'r_flag_zone_list', 'r_flag_zone_reset',
    'struct_buffer', 'struct_c__SA_RNumCalcValue',
    'struct_c__SA_dict', 'struct_cdb', 'struct_cdb_hp',
    'struct_cdb_hplist', 'struct_cdb_make', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_r_event_t', 'struct_r_flag_bind_t',
    'struct_r_flag_item_t', 'struct_r_flag_t',
    'struct_r_flag_zone_item_t', 'struct_r_flags_at_offset_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_num_calc_t',
    'struct_r_num_t', 'struct_r_rb_node_t',
    'struct_r_skiplist_node_t', 'struct_r_skiplist_t',
    'struct_r_space_t', 'struct_r_spaces_t', 'struct_r_vector_t',
    'struct_sdb_kv', 'struct_sdb_t']

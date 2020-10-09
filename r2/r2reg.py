# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_reg as _libr_reg


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

r_reg_version = _libr_reg.r_reg_version
r_reg_version.restype = POINTER_T(ctypes.c_char)
r_reg_version.argtypes = []

# values for enumeration 'c__EA_RRegisterType'
c__EA_RRegisterType__enumvalues = {
    0: 'R_REG_TYPE_GPR',
    1: 'R_REG_TYPE_DRX',
    2: 'R_REG_TYPE_FPU',
    3: 'R_REG_TYPE_MMX',
    4: 'R_REG_TYPE_XMM',
    5: 'R_REG_TYPE_YMM',
    6: 'R_REG_TYPE_FLG',
    7: 'R_REG_TYPE_SEG',
    8: 'R_REG_TYPE_LAST',
    -1: 'R_REG_TYPE_ALL',
}
R_REG_TYPE_GPR = 0
R_REG_TYPE_DRX = 1
R_REG_TYPE_FPU = 2
R_REG_TYPE_MMX = 3
R_REG_TYPE_XMM = 4
R_REG_TYPE_YMM = 5
R_REG_TYPE_FLG = 6
R_REG_TYPE_SEG = 7
R_REG_TYPE_LAST = 8
R_REG_TYPE_ALL = -1
c__EA_RRegisterType = ctypes.c_int # enum
RRegisterType = c__EA_RRegisterType
RRegisterType__enumvalues = c__EA_RRegisterType__enumvalues

# values for enumeration 'c__EA_RRegisterId'
c__EA_RRegisterId__enumvalues = {
    0: 'R_REG_NAME_PC',
    1: 'R_REG_NAME_SP',
    2: 'R_REG_NAME_SR',
    3: 'R_REG_NAME_BP',
    4: 'R_REG_NAME_LR',
    5: 'R_REG_NAME_A0',
    6: 'R_REG_NAME_A1',
    7: 'R_REG_NAME_A2',
    8: 'R_REG_NAME_A3',
    9: 'R_REG_NAME_A4',
    10: 'R_REG_NAME_A5',
    11: 'R_REG_NAME_A6',
    12: 'R_REG_NAME_A7',
    13: 'R_REG_NAME_A8',
    14: 'R_REG_NAME_A9',
    15: 'R_REG_NAME_R0',
    16: 'R_REG_NAME_R1',
    17: 'R_REG_NAME_R2',
    18: 'R_REG_NAME_R3',
    19: 'R_REG_NAME_ZF',
    20: 'R_REG_NAME_SF',
    21: 'R_REG_NAME_CF',
    22: 'R_REG_NAME_OF',
    23: 'R_REG_NAME_SN',
    24: 'R_REG_NAME_LAST',
}
R_REG_NAME_PC = 0
R_REG_NAME_SP = 1
R_REG_NAME_SR = 2
R_REG_NAME_BP = 3
R_REG_NAME_LR = 4
R_REG_NAME_A0 = 5
R_REG_NAME_A1 = 6
R_REG_NAME_A2 = 7
R_REG_NAME_A3 = 8
R_REG_NAME_A4 = 9
R_REG_NAME_A5 = 10
R_REG_NAME_A6 = 11
R_REG_NAME_A7 = 12
R_REG_NAME_A8 = 13
R_REG_NAME_A9 = 14
R_REG_NAME_R0 = 15
R_REG_NAME_R1 = 16
R_REG_NAME_R2 = 17
R_REG_NAME_R3 = 18
R_REG_NAME_ZF = 19
R_REG_NAME_SF = 20
R_REG_NAME_CF = 21
R_REG_NAME_OF = 22
R_REG_NAME_SN = 23
R_REG_NAME_LAST = 24
c__EA_RRegisterId = ctypes.c_int # enum
RRegisterId = c__EA_RRegisterId
RRegisterId__enumvalues = c__EA_RRegisterId__enumvalues
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

RRegItem = struct_r_reg_item_t
class struct_r_reg_arena_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', POINTER_T(ctypes.c_ubyte)),
    ('size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RRegArena = struct_r_reg_arena_t
class struct_r_reg_set_t(ctypes.Structure):
    pass

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

RRegSet = struct_r_reg_set_t
class struct_r_reg_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

RReg = struct_r_reg_t
class struct_r_reg_flags_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('s', ctypes.c_bool),
    ('z', ctypes.c_bool),
    ('a', ctypes.c_bool),
    ('c', ctypes.c_bool),
    ('o', ctypes.c_bool),
    ('p', ctypes.c_bool),
     ]

RRegFlags = struct_r_reg_flags_t
r_reg_free = _libr_reg.r_reg_free
r_reg_free.restype = None
r_reg_free.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_free_internal = _libr_reg.r_reg_free_internal
r_reg_free_internal.restype = None
r_reg_free_internal.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_bool]
r_reg_new = _libr_reg.r_reg_new
r_reg_new.restype = POINTER_T(struct_r_reg_t)
r_reg_new.argtypes = []
r_reg_set_name = _libr_reg.r_reg_set_name
r_reg_set_name.restype = ctypes.c_bool
r_reg_set_name.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_reg_set_profile_string = _libr_reg.r_reg_set_profile_string
r_reg_set_profile_string.restype = ctypes.c_bool
r_reg_set_profile_string.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_profile_to_cc = _libr_reg.r_reg_profile_to_cc
r_reg_profile_to_cc.restype = POINTER_T(ctypes.c_char)
r_reg_profile_to_cc.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_set_profile = _libr_reg.r_reg_set_profile
r_reg_set_profile.restype = ctypes.c_bool
r_reg_set_profile.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_parse_gdb_profile = _libr_reg.r_reg_parse_gdb_profile
r_reg_parse_gdb_profile.restype = POINTER_T(ctypes.c_char)
r_reg_parse_gdb_profile.argtypes = [POINTER_T(ctypes.c_char)]
r_reg_is_readonly = _libr_reg.r_reg_is_readonly
r_reg_is_readonly.restype = ctypes.c_bool
r_reg_is_readonly.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
r_reg_regset_get = _libr_reg.r_reg_regset_get
r_reg_regset_get.restype = POINTER_T(struct_r_reg_set_t)
r_reg_regset_get.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_getv = _libr_reg.r_reg_getv
r_reg_getv.restype = ctypes.c_uint64
r_reg_getv.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_setv = _libr_reg.r_reg_setv
r_reg_setv.restype = ctypes.c_uint64
r_reg_setv.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_reg_32_to_64 = _libr_reg.r_reg_32_to_64
r_reg_32_to_64.restype = POINTER_T(ctypes.c_char)
r_reg_32_to_64.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_64_to_32 = _libr_reg.r_reg_64_to_32
r_reg_64_to_32.restype = POINTER_T(ctypes.c_char)
r_reg_64_to_32.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_get_name_by_type = _libr_reg.r_reg_get_name_by_type
r_reg_get_name_by_type.restype = POINTER_T(ctypes.c_char)
r_reg_get_name_by_type.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_get_type = _libr_reg.r_reg_get_type
r_reg_get_type.restype = POINTER_T(ctypes.c_char)
r_reg_get_type.argtypes = [ctypes.c_int32]
r_reg_get_name = _libr_reg.r_reg_get_name
r_reg_get_name.restype = POINTER_T(ctypes.c_char)
r_reg_get_name.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_get_role = _libr_reg.r_reg_get_role
r_reg_get_role.restype = POINTER_T(ctypes.c_char)
r_reg_get_role.argtypes = [ctypes.c_int32]
r_reg_get = _libr_reg.r_reg_get
r_reg_get.restype = POINTER_T(struct_r_reg_item_t)
r_reg_get.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_reg_get_list = _libr_reg.r_reg_get_list
r_reg_get_list.restype = POINTER_T(struct_r_list_t)
r_reg_get_list.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_get_at = _libr_reg.r_reg_get_at
r_reg_get_at.restype = POINTER_T(struct_r_reg_item_t)
r_reg_get_at.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_reg_next_diff = _libr_reg.r_reg_next_diff
r_reg_next_diff.restype = POINTER_T(struct_r_reg_item_t)
r_reg_next_diff.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(struct_r_reg_item_t), ctypes.c_int32]
r_reg_reindex = _libr_reg.r_reg_reindex
r_reg_reindex.restype = None
r_reg_reindex.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_index_get = _libr_reg.r_reg_index_get
r_reg_index_get.restype = POINTER_T(struct_r_reg_item_t)
r_reg_index_get.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_item_free = _libr_reg.r_reg_item_free
r_reg_item_free.restype = None
r_reg_item_free.argtypes = [POINTER_T(struct_r_reg_item_t)]
r_reg_type_by_name = _libr_reg.r_reg_type_by_name
r_reg_type_by_name.restype = ctypes.c_int32
r_reg_type_by_name.argtypes = [POINTER_T(ctypes.c_char)]
r_reg_get_name_idx = _libr_reg.r_reg_get_name_idx
r_reg_get_name_idx.restype = ctypes.c_int32
r_reg_get_name_idx.argtypes = [POINTER_T(ctypes.c_char)]
r_reg_cond_get = _libr_reg.r_reg_cond_get
r_reg_cond_get.restype = POINTER_T(struct_r_reg_item_t)
r_reg_cond_get.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_cond_apply = _libr_reg.r_reg_cond_apply
r_reg_cond_apply.restype = None
r_reg_cond_apply.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_flags_t)]
r_reg_cond_set = _libr_reg.r_reg_cond_set
r_reg_cond_set.restype = ctypes.c_bool
r_reg_cond_set.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_reg_cond_get_value = _libr_reg.r_reg_cond_get_value
r_reg_cond_get_value.restype = ctypes.c_int32
r_reg_cond_get_value.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_cond_bits_set = _libr_reg.r_reg_cond_bits_set
r_reg_cond_bits_set.restype = ctypes.c_bool
r_reg_cond_bits_set.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(struct_r_reg_flags_t), ctypes.c_bool]
r_reg_cond_bits = _libr_reg.r_reg_cond_bits
r_reg_cond_bits.restype = ctypes.c_int32
r_reg_cond_bits.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(struct_r_reg_flags_t)]
r_reg_cond_retrieve = _libr_reg.r_reg_cond_retrieve
r_reg_cond_retrieve.restype = POINTER_T(struct_r_reg_flags_t)
r_reg_cond_retrieve.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_flags_t)]
r_reg_cond = _libr_reg.r_reg_cond
r_reg_cond.restype = ctypes.c_int32
r_reg_cond.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_get_value = _libr_reg.r_reg_get_value
r_reg_get_value.restype = ctypes.c_uint64
r_reg_get_value.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
class struct__utX(ctypes.Structure):
    pass

r_reg_get_value_big = _libr_reg.r_reg_get_value_big
r_reg_get_value_big.restype = ctypes.c_uint64
r_reg_get_value_big.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), POINTER_T(struct__utX)]
r_reg_get_value_by_role = _libr_reg.r_reg_get_value_by_role
r_reg_get_value_by_role.restype = ctypes.c_uint64
r_reg_get_value_by_role.argtypes = [POINTER_T(struct_r_reg_t), RRegisterId]
r_reg_set_value = _libr_reg.r_reg_set_value
r_reg_set_value.restype = ctypes.c_bool
r_reg_set_value.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), ctypes.c_uint64]
r_reg_set_value_by_role = _libr_reg.r_reg_set_value_by_role
r_reg_set_value_by_role.restype = ctypes.c_bool
r_reg_set_value_by_role.argtypes = [POINTER_T(struct_r_reg_t), RRegisterId, ctypes.c_uint64]
r_reg_get_float = _libr_reg.r_reg_get_float
r_reg_get_float.restype = ctypes.c_float
r_reg_get_float.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
r_reg_set_float = _libr_reg.r_reg_set_float
r_reg_set_float.restype = ctypes.c_bool
r_reg_set_float.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), ctypes.c_float]
r_reg_get_double = _libr_reg.r_reg_get_double
r_reg_get_double.restype = ctypes.c_double
r_reg_get_double.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
r_reg_set_double = _libr_reg.r_reg_set_double
r_reg_set_double.restype = ctypes.c_bool
r_reg_set_double.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), ctypes.c_double]
r_reg_get_longdouble = _libr_reg.r_reg_get_longdouble
r_reg_get_longdouble.restype = c_long_double_t
r_reg_get_longdouble.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
r_reg_set_longdouble = _libr_reg.r_reg_set_longdouble
r_reg_set_longdouble.restype = ctypes.c_bool
r_reg_set_longdouble.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), c_long_double_t]
r_reg_get_bvalue = _libr_reg.r_reg_get_bvalue
r_reg_get_bvalue.restype = POINTER_T(ctypes.c_char)
r_reg_get_bvalue.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)]
r_reg_set_bvalue = _libr_reg.r_reg_set_bvalue
r_reg_set_bvalue.restype = ctypes.c_uint64
r_reg_set_bvalue.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), POINTER_T(ctypes.c_char)]
r_reg_set_pack = _libr_reg.r_reg_set_pack
r_reg_set_pack.restype = ctypes.c_int32
r_reg_set_pack.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64]
r_reg_get_pack = _libr_reg.r_reg_get_pack
r_reg_get_pack.restype = ctypes.c_uint64
r_reg_get_pack.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t), ctypes.c_int32, ctypes.c_int32]
r_reg_get_bytes = _libr_reg.r_reg_get_bytes
r_reg_get_bytes.restype = POINTER_T(ctypes.c_ubyte)
r_reg_get_bytes.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(ctypes.c_int32)]
r_reg_set_bytes = _libr_reg.r_reg_set_bytes
r_reg_set_bytes.restype = ctypes.c_bool
r_reg_set_bytes.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_reg_read_regs = _libr_reg.r_reg_read_regs
r_reg_read_regs.restype = ctypes.c_bool
r_reg_read_regs.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_reg_arena_set_bytes = _libr_reg.r_reg_arena_set_bytes
r_reg_arena_set_bytes.restype = ctypes.c_int32
r_reg_arena_set_bytes.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char)]
r_reg_arena_new = _libr_reg.r_reg_arena_new
r_reg_arena_new.restype = POINTER_T(struct_r_reg_arena_t)
r_reg_arena_new.argtypes = [ctypes.c_int32]
r_reg_arena_free = _libr_reg.r_reg_arena_free
r_reg_arena_free.restype = None
r_reg_arena_free.argtypes = [POINTER_T(struct_r_reg_arena_t)]
r_reg_fit_arena = _libr_reg.r_reg_fit_arena
r_reg_fit_arena.restype = ctypes.c_int32
r_reg_fit_arena.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_arena_swap = _libr_reg.r_reg_arena_swap
r_reg_arena_swap.restype = None
r_reg_arena_swap.argtypes = [POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_reg_arena_push = _libr_reg.r_reg_arena_push
r_reg_arena_push.restype = ctypes.c_int32
r_reg_arena_push.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_arena_pop = _libr_reg.r_reg_arena_pop
r_reg_arena_pop.restype = None
r_reg_arena_pop.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_arena_zero = _libr_reg.r_reg_arena_zero
r_reg_arena_zero.restype = None
r_reg_arena_zero.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_arena_peek = _libr_reg.r_reg_arena_peek
r_reg_arena_peek.restype = POINTER_T(ctypes.c_ubyte)
r_reg_arena_peek.argtypes = [POINTER_T(struct_r_reg_t)]
r_reg_arena_poke = _libr_reg.r_reg_arena_poke
r_reg_arena_poke.restype = None
r_reg_arena_poke.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_ubyte)]
r_reg_arena_dup = _libr_reg.r_reg_arena_dup
r_reg_arena_dup.restype = POINTER_T(ctypes.c_ubyte)
r_reg_arena_dup.argtypes = [POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_ubyte)]
r_reg_cond_to_string = _libr_reg.r_reg_cond_to_string
r_reg_cond_to_string.restype = POINTER_T(ctypes.c_char)
r_reg_cond_to_string.argtypes = [ctypes.c_int32]
r_reg_cond_from_string = _libr_reg.r_reg_cond_from_string
r_reg_cond_from_string.restype = ctypes.c_int32
r_reg_cond_from_string.argtypes = [POINTER_T(ctypes.c_char)]
r_reg_arena_shrink = _libr_reg.r_reg_arena_shrink
r_reg_arena_shrink.restype = None
r_reg_arena_shrink.argtypes = [POINTER_T(struct_r_reg_t)]
class struct__ut80(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Low', ctypes.c_uint64),
    ('High', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

class struct__ut96(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Low', ctypes.c_uint64),
    ('High', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

class struct__ut128(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Low', ctypes.c_uint64),
    ('High', ctypes.c_int64),
     ]

class struct__ut256(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Low', struct__ut128),
    ('High', struct__ut128),
     ]

struct__utX._pack_ = True # source:False
struct__utX._fields_ = [
    ('v80', struct__ut80),
    ('v96', struct__ut96),
    ('v128', struct__ut128),
    ('v256', struct__ut256),
]

__all__ = \
    ['RReg', 'RRegArena', 'RRegFlags', 'RRegItem', 'RRegSet',
    'RRegisterId', 'RRegisterId__enumvalues', 'RRegisterType',
    'RRegisterType__enumvalues', 'R_REG_NAME_A0', 'R_REG_NAME_A1',
    'R_REG_NAME_A2', 'R_REG_NAME_A3', 'R_REG_NAME_A4',
    'R_REG_NAME_A5', 'R_REG_NAME_A6', 'R_REG_NAME_A7',
    'R_REG_NAME_A8', 'R_REG_NAME_A9', 'R_REG_NAME_BP',
    'R_REG_NAME_CF', 'R_REG_NAME_LAST', 'R_REG_NAME_LR',
    'R_REG_NAME_OF', 'R_REG_NAME_PC', 'R_REG_NAME_R0',
    'R_REG_NAME_R1', 'R_REG_NAME_R2', 'R_REG_NAME_R3',
    'R_REG_NAME_SF', 'R_REG_NAME_SN', 'R_REG_NAME_SP',
    'R_REG_NAME_SR', 'R_REG_NAME_ZF', 'R_REG_TYPE_ALL',
    'R_REG_TYPE_DRX', 'R_REG_TYPE_FLG', 'R_REG_TYPE_FPU',
    'R_REG_TYPE_GPR', 'R_REG_TYPE_LAST', 'R_REG_TYPE_MMX',
    'R_REG_TYPE_SEG', 'R_REG_TYPE_XMM', 'R_REG_TYPE_YMM',
    'c__EA_RRegisterId', 'c__EA_RRegisterType', 'r_reg_32_to_64',
    'r_reg_64_to_32', 'r_reg_arena_dup', 'r_reg_arena_free',
    'r_reg_arena_new', 'r_reg_arena_peek', 'r_reg_arena_poke',
    'r_reg_arena_pop', 'r_reg_arena_push', 'r_reg_arena_set_bytes',
    'r_reg_arena_shrink', 'r_reg_arena_swap', 'r_reg_arena_zero',
    'r_reg_cond', 'r_reg_cond_apply', 'r_reg_cond_bits',
    'r_reg_cond_bits_set', 'r_reg_cond_from_string', 'r_reg_cond_get',
    'r_reg_cond_get_value', 'r_reg_cond_retrieve', 'r_reg_cond_set',
    'r_reg_cond_to_string', 'r_reg_fit_arena', 'r_reg_free',
    'r_reg_free_internal', 'r_reg_get', 'r_reg_get_at',
    'r_reg_get_bvalue', 'r_reg_get_bytes', 'r_reg_get_double',
    'r_reg_get_float', 'r_reg_get_list', 'r_reg_get_longdouble',
    'r_reg_get_name', 'r_reg_get_name_by_type', 'r_reg_get_name_idx',
    'r_reg_get_pack', 'r_reg_get_role', 'r_reg_get_type',
    'r_reg_get_value', 'r_reg_get_value_big',
    'r_reg_get_value_by_role', 'r_reg_getv', 'r_reg_index_get',
    'r_reg_is_readonly', 'r_reg_item_free', 'r_reg_new',
    'r_reg_next_diff', 'r_reg_parse_gdb_profile',
    'r_reg_profile_to_cc', 'r_reg_read_regs', 'r_reg_regset_get',
    'r_reg_reindex', 'r_reg_set_bvalue', 'r_reg_set_bytes',
    'r_reg_set_double', 'r_reg_set_float', 'r_reg_set_longdouble',
    'r_reg_set_name', 'r_reg_set_pack', 'r_reg_set_profile',
    'r_reg_set_profile_string', 'r_reg_set_value',
    'r_reg_set_value_by_role', 'r_reg_setv', 'r_reg_type_by_name',
    'r_reg_version', 'struct__ut128', 'struct__ut256', 'struct__ut80',
    'struct__ut96', 'struct__utX', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_reg_arena_t',
    'struct_r_reg_flags_t', 'struct_r_reg_item_t',
    'struct_r_reg_set_t', 'struct_r_reg_t']

# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_bin as _libr_bin


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



class struct_r_bin_t(ctypes.Structure):
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

class struct_r_bin_file_t(ctypes.Structure):
    pass

class struct_r_bin_object_t(ctypes.Structure):
    pass

class struct_r_rb_node_t(ctypes.Structure):
    pass

struct_r_rb_node_t._pack_ = True # source:False
struct_r_rb_node_t._fields_ = [
    ('child', POINTER_T(struct_r_rb_node_t) * 2),
    ('red', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

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

class struct_r_bin_plugin_t(ctypes.Structure):
    pass

class struct_r_bin_dbginfo_t(ctypes.Structure):
    pass

struct_r_bin_dbginfo_t._pack_ = True # source:False
struct_r_bin_dbginfo_t._fields_ = [
    ('get_line', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_file_t), ctypes.c_uint64, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_int32)))),
]

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

class struct_r_buf_t(ctypes.Structure):
    pass

class struct_r_bin_arch_options_t(ctypes.Structure):
    pass

class struct_sdb_t(ctypes.Structure):
    pass

class struct_r_bin_addr_t(ctypes.Structure):
    pass

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
    pass

class struct_ht_pp_kv(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('key', POINTER_T(None)),
    ('value', POINTER_T(None)),
    ('key_len', ctypes.c_uint32),
    ('value_len', ctypes.c_uint32),
     ]

struct_sdb_kv._pack_ = True # source:False
struct_sdb_kv._fields_ = [
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

class struct_ht_pp_t(ctypes.Structure):
    pass

class struct_ht_pp_bucket_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

struct_r_bin_addr_t._pack_ = True # source:False
struct_r_bin_addr_t._fields_ = [
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('hvaddr', ctypes.c_uint64),
    ('hpaddr', ctypes.c_uint64),
    ('type', ctypes.c_int32),
    ('bits', ctypes.c_int32),
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

class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_io_desc_t(ctypes.Structure):
    pass

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

class struct_r_str_constpool_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ht', POINTER_T(struct_ht_pp_t)),
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

RBin = struct_r_bin_t
r_bin_version = _libr_bin.r_bin_version
r_bin_version.restype = POINTER_T(ctypes.c_char)
r_bin_version.argtypes = []

# values for enumeration 'c__Ea_R_BIN_SYM_ENTRY'
c__Ea_R_BIN_SYM_ENTRY__enumvalues = {
    0: 'R_BIN_SYM_ENTRY',
    1: 'R_BIN_SYM_INIT',
    2: 'R_BIN_SYM_MAIN',
    3: 'R_BIN_SYM_FINI',
    4: 'R_BIN_SYM_LAST',
}
R_BIN_SYM_ENTRY = 0
R_BIN_SYM_INIT = 1
R_BIN_SYM_MAIN = 2
R_BIN_SYM_FINI = 3
R_BIN_SYM_LAST = 4
c__Ea_R_BIN_SYM_ENTRY = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_BIN_NM_NONE'
c__Ea_R_BIN_NM_NONE__enumvalues = {
    0: 'R_BIN_NM_NONE',
    1: 'R_BIN_NM_JAVA',
    2: 'R_BIN_NM_C',
    4: 'R_BIN_NM_GO',
    8: 'R_BIN_NM_CXX',
    16: 'R_BIN_NM_OBJC',
    32: 'R_BIN_NM_SWIFT',
    64: 'R_BIN_NM_DLANG',
    128: 'R_BIN_NM_MSVC',
    256: 'R_BIN_NM_RUST',
    512: 'R_BIN_NM_KOTLIN',
    -2147483648: 'R_BIN_NM_BLOCKS',
    -1: 'R_BIN_NM_ANY',
}
R_BIN_NM_NONE = 0
R_BIN_NM_JAVA = 1
R_BIN_NM_C = 2
R_BIN_NM_GO = 4
R_BIN_NM_CXX = 8
R_BIN_NM_OBJC = 16
R_BIN_NM_SWIFT = 32
R_BIN_NM_DLANG = 64
R_BIN_NM_MSVC = 128
R_BIN_NM_RUST = 256
R_BIN_NM_KOTLIN = 512
R_BIN_NM_BLOCKS = -2147483648
R_BIN_NM_ANY = -1
c__Ea_R_BIN_NM_NONE = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_STRING_TYPE_DETECT'
c__Ea_R_STRING_TYPE_DETECT__enumvalues = {
    63: 'R_STRING_TYPE_DETECT',
    97: 'R_STRING_TYPE_ASCII',
    117: 'R_STRING_TYPE_UTF8',
    119: 'R_STRING_TYPE_WIDE',
    87: 'R_STRING_TYPE_WIDE32',
    98: 'R_STRING_TYPE_BASE64',
}
R_STRING_TYPE_DETECT = 63
R_STRING_TYPE_ASCII = 97
R_STRING_TYPE_UTF8 = 117
R_STRING_TYPE_WIDE = 119
R_STRING_TYPE_WIDE32 = 87
R_STRING_TYPE_BASE64 = 98
c__Ea_R_STRING_TYPE_DETECT = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_BIN_CLASS_PRIVATE'
c__Ea_R_BIN_CLASS_PRIVATE__enumvalues = {
    0: 'R_BIN_CLASS_PRIVATE',
    1: 'R_BIN_CLASS_PUBLIC',
    2: 'R_BIN_CLASS_FRIENDLY',
    3: 'R_BIN_CLASS_PROTECTED',
}
R_BIN_CLASS_PRIVATE = 0
R_BIN_CLASS_PUBLIC = 1
R_BIN_CLASS_FRIENDLY = 2
R_BIN_CLASS_PROTECTED = 3
c__Ea_R_BIN_CLASS_PRIVATE = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_BIN_RELOC_8'
c__Ea_R_BIN_RELOC_8__enumvalues = {
    8: 'R_BIN_RELOC_8',
    16: 'R_BIN_RELOC_16',
    32: 'R_BIN_RELOC_32',
    64: 'R_BIN_RELOC_64',
}
R_BIN_RELOC_8 = 8
R_BIN_RELOC_16 = 16
R_BIN_RELOC_32 = 32
R_BIN_RELOC_64 = 64
c__Ea_R_BIN_RELOC_8 = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_BIN_TYPE_DEFAULT'
c__Ea_R_BIN_TYPE_DEFAULT__enumvalues = {
    0: 'R_BIN_TYPE_DEFAULT',
    1: 'R_BIN_TYPE_CORE',
}
R_BIN_TYPE_DEFAULT = 0
R_BIN_TYPE_CORE = 1
c__Ea_R_BIN_TYPE_DEFAULT = ctypes.c_int # enum
RBinAddr = struct_r_bin_addr_t
RBinHash = struct_r_bin_hash_t
class struct_r_bin_file_hash_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', POINTER_T(ctypes.c_char)),
    ('hex', POINTER_T(ctypes.c_char)),
     ]

RBinFileHash = struct_r_bin_file_hash_t
RBinInfo = struct_r_bin_info_t
RBinObject = struct_r_bin_object_t
RBinFile = struct_r_bin_file_t
class struct_r_bin_file_options_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('rawstr', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('baddr', ctypes.c_uint64),
    ('laddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('plugname', POINTER_T(ctypes.c_char)),
     ]

RBinFileOptions = struct_r_bin_file_options_t
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

RBinXtrMetadata = struct_r_bin_xtr_metadata_t
FREE_XTR = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))
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

RBinXtrData = struct_r_bin_xtr_extract_t
r_bin_xtrdata_new = _libr_bin.r_bin_xtrdata_new
r_bin_xtrdata_new.restype = POINTER_T(struct_r_bin_xtr_extract_t)
r_bin_xtrdata_new.argtypes = [POINTER_T(struct_r_buf_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint32, POINTER_T(struct_r_bin_xtr_metadata_t)]
r_bin_xtrdata_free = _libr_bin.r_bin_xtrdata_free
r_bin_xtrdata_free.restype = None
r_bin_xtrdata_free.argtypes = [POINTER_T(None)]
RBinXtrPlugin = struct_r_bin_xtr_plugin_t
class struct_r_bin_ldr_plugin_t(ctypes.Structure):
    pass

struct_r_bin_ldr_plugin_t._pack_ = True # source:False
struct_r_bin_ldr_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('load', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_bin_t)))),
]

RBinLdrPlugin = struct_r_bin_ldr_plugin_t
struct_r_bin_arch_options_t._pack_ = True # source:False
struct_r_bin_arch_options_t._fields_ = [
    ('arch', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

RBinArchOptions = struct_r_bin_arch_options_t
class struct_r_bin_trycatch_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('source', ctypes.c_uint64),
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('handler', ctypes.c_uint64),
    ('filter', ctypes.c_uint64),
     ]

RBinTrycatch = struct_r_bin_trycatch_t
r_bin_trycatch_new = _libr_bin.r_bin_trycatch_new
r_bin_trycatch_new.restype = POINTER_T(struct_r_bin_trycatch_t)
r_bin_trycatch_new.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_bin_trycatch_free = _libr_bin.r_bin_trycatch_free
r_bin_trycatch_free.restype = None
r_bin_trycatch_free.argtypes = [POINTER_T(struct_r_bin_trycatch_t)]
RBinPlugin = struct_r_bin_plugin_t
RBinSymbollCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_bin_object_t), POINTER_T(None)))
class struct_r_bin_section_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

RBinSection = struct_r_bin_section_t
class struct_r_bin_class_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('super', POINTER_T(ctypes.c_char)),
    ('visibility_str', POINTER_T(ctypes.c_char)),
    ('index', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('addr', ctypes.c_uint64),
    ('methods', POINTER_T(struct_r_list_t)),
    ('fields', POINTER_T(struct_r_list_t)),
    ('visibility', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

RBinClass = struct_r_bin_class_t
class struct_r_bin_symbol_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('dname', POINTER_T(ctypes.c_char)),
    ('libname', POINTER_T(ctypes.c_char)),
    ('classname', POINTER_T(ctypes.c_char)),
    ('forwarder', POINTER_T(ctypes.c_char)),
    ('bind', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('rtype', POINTER_T(ctypes.c_char)),
    ('is_imported', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('visibility_str', POINTER_T(ctypes.c_char)),
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('ordinal', ctypes.c_uint32),
    ('visibility', ctypes.c_uint32),
    ('bits', ctypes.c_int32),
    ('method_flags', ctypes.c_uint64),
    ('dup_count', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

RBinSymbol = struct_r_bin_symbol_t
class struct_r_bin_import_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('libname', POINTER_T(ctypes.c_char)),
    ('bind', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('classname', POINTER_T(ctypes.c_char)),
    ('descriptor', POINTER_T(ctypes.c_char)),
    ('ordinal', ctypes.c_uint32),
    ('visibility', ctypes.c_uint32),
     ]

RBinImport = struct_r_bin_import_t
class struct_r_bin_reloc_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_ubyte),
    ('additive', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('symbol', POINTER_T(struct_r_bin_symbol_t)),
    ('import', POINTER_T(struct_r_bin_import_t)),
    ('addend', ctypes.c_int64),
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('visibility', ctypes.c_uint32),
    ('is_ifunc', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('vrb', struct_r_rb_node_t),
     ]

RBinReloc = struct_r_bin_reloc_t
class struct_r_bin_string_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('string', POINTER_T(ctypes.c_char)),
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('ordinal', ctypes.c_uint32),
    ('size', ctypes.c_uint32),
    ('length', ctypes.c_uint32),
    ('type', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

RBinString = struct_r_bin_string_t
class struct_r_bin_field_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('vaddr', ctypes.c_uint64),
    ('paddr', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('offset', ctypes.c_int32),
    ('visibility', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
    ('format', POINTER_T(ctypes.c_char)),
    ('format_named', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('flags', ctypes.c_uint64),
     ]

RBinField = struct_r_bin_field_t
r_bin_field_new = _libr_bin.r_bin_field_new
r_bin_field_new.restype = POINTER_T(struct_r_bin_field_t)
r_bin_field_new.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_bin_field_free = _libr_bin.r_bin_field_free
r_bin_field_free.restype = None
r_bin_field_free.argtypes = [POINTER_T(None)]
class struct_r_bin_mem_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('perms', ctypes.c_int32),
    ('mirrors', POINTER_T(struct_r_list_t)),
     ]

RBinMem = struct_r_bin_mem_t
class struct_r_bin_map_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('perms', ctypes.c_int32),
    ('file', POINTER_T(ctypes.c_char)),
     ]

RBinMap = struct_r_bin_map_t
RBinDbgInfo = struct_r_bin_dbginfo_t
RBinWrite = struct_r_bin_write_t
RBinGetOffset = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bin_t), ctypes.c_int32, ctypes.c_int32))
RBinGetName = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_bool))
RBinGetSections = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_bin_t)))
RBinGetSectionAt = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_bin_section_t), POINTER_T(struct_r_bin_t), ctypes.c_uint64))
RBinDemangle = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_bool))
class struct_r_bin_bind_t(ctypes.Structure):
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

RBinBind = struct_r_bin_bind_t
r_bin_info_free = _libr_bin.r_bin_info_free
r_bin_info_free.restype = None
r_bin_info_free.argtypes = [POINTER_T(struct_r_bin_info_t)]
r_bin_import_free = _libr_bin.r_bin_import_free
r_bin_import_free.restype = None
r_bin_import_free.argtypes = [POINTER_T(None)]
r_bin_symbol_free = _libr_bin.r_bin_symbol_free
r_bin_symbol_free.restype = None
r_bin_symbol_free.argtypes = [POINTER_T(None)]
r_bin_symbol_new = _libr_bin.r_bin_symbol_new
r_bin_symbol_new.restype = POINTER_T(struct_r_bin_symbol_t)
r_bin_symbol_new.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64]
r_bin_string_free = _libr_bin.r_bin_string_free
r_bin_string_free.restype = None
r_bin_string_free.argtypes = [POINTER_T(None)]
class struct_r_bin_options_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pluginname', POINTER_T(ctypes.c_char)),
    ('baseaddr', ctypes.c_uint64),
    ('loadaddr', ctypes.c_uint64),
    ('sz', ctypes.c_uint64),
    ('xtr_idx', ctypes.c_int32),
    ('rawstr', ctypes.c_int32),
    ('fd', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('filename', POINTER_T(ctypes.c_char)),
     ]

RBinOptions = struct_r_bin_options_t
r_bin_import_clone = _libr_bin.r_bin_import_clone
r_bin_import_clone.restype = POINTER_T(struct_r_bin_import_t)
r_bin_import_clone.argtypes = [POINTER_T(struct_r_bin_import_t)]
r_bin_symbol_name = _libr_bin.r_bin_symbol_name
r_bin_symbol_name.restype = POINTER_T(ctypes.c_char)
r_bin_symbol_name.argtypes = [POINTER_T(struct_r_bin_symbol_t)]
RBinSymbolCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_bin_object_t), POINTER_T(struct_r_bin_symbol_t)))
r_bin_options_init = _libr_bin.r_bin_options_init
r_bin_options_init.restype = None
r_bin_options_init.argtypes = [POINTER_T(struct_r_bin_options_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_bin_arch_options_init = _libr_bin.r_bin_arch_options_init
r_bin_arch_options_init.restype = None
r_bin_arch_options_init.argtypes = [POINTER_T(struct_r_bin_arch_options_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_new = _libr_bin.r_bin_new
r_bin_new.restype = POINTER_T(struct_r_bin_t)
r_bin_new.argtypes = []
r_bin_free = _libr_bin.r_bin_free
r_bin_free.restype = None
r_bin_free.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_open = _libr_bin.r_bin_open
r_bin_open.restype = ctypes.c_bool
r_bin_open.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_bin_options_t)]
r_bin_open_io = _libr_bin.r_bin_open_io
r_bin_open_io.restype = ctypes.c_bool
r_bin_open_io.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_options_t)]
r_bin_open_buf = _libr_bin.r_bin_open_buf
r_bin_open_buf.restype = ctypes.c_bool
r_bin_open_buf.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_buf_t), POINTER_T(struct_r_bin_options_t)]
r_bin_reload = _libr_bin.r_bin_reload
r_bin_reload.restype = ctypes.c_bool
r_bin_reload.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32, ctypes.c_uint64]
r_bin_bind = _libr_bin.r_bin_bind
r_bin_bind.restype = None
r_bin_bind.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_bind_t)]
r_bin_add = _libr_bin.r_bin_add
r_bin_add.restype = ctypes.c_bool
r_bin_add.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_plugin_t)]
r_bin_xtr_add = _libr_bin.r_bin_xtr_add
r_bin_xtr_add.restype = ctypes.c_bool
r_bin_xtr_add.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_xtr_plugin_t)]
r_bin_ldr_add = _libr_bin.r_bin_ldr_add
r_bin_ldr_add.restype = ctypes.c_bool
r_bin_ldr_add.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_ldr_plugin_t)]
r_bin_list = _libr_bin.r_bin_list
r_bin_list.restype = None
r_bin_list.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_int32]
r_bin_list_plugin = _libr_bin.r_bin_list_plugin
r_bin_list_plugin.restype = ctypes.c_bool
r_bin_list_plugin.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_get_binplugin_by_buffer = _libr_bin.r_bin_get_binplugin_by_buffer
r_bin_get_binplugin_by_buffer.restype = POINTER_T(struct_r_bin_plugin_t)
r_bin_get_binplugin_by_buffer.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_buf_t)]
r_bin_force_plugin = _libr_bin.r_bin_force_plugin
r_bin_force_plugin.restype = None
r_bin_force_plugin.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char)]
r_bin_get_baddr = _libr_bin.r_bin_get_baddr
r_bin_get_baddr.restype = ctypes.c_uint64
r_bin_get_baddr.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_file_get_baddr = _libr_bin.r_bin_file_get_baddr
r_bin_file_get_baddr.restype = ctypes.c_uint64
r_bin_file_get_baddr.argtypes = [POINTER_T(struct_r_bin_file_t)]
r_bin_set_user_ptr = _libr_bin.r_bin_set_user_ptr
r_bin_set_user_ptr.restype = None
r_bin_set_user_ptr.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(None)]
r_bin_get_info = _libr_bin.r_bin_get_info
r_bin_get_info.restype = POINTER_T(struct_r_bin_info_t)
r_bin_get_info.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_set_baddr = _libr_bin.r_bin_set_baddr
r_bin_set_baddr.restype = None
r_bin_set_baddr.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_get_laddr = _libr_bin.r_bin_get_laddr
r_bin_get_laddr.restype = ctypes.c_uint64
r_bin_get_laddr.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_size = _libr_bin.r_bin_get_size
r_bin_get_size.restype = ctypes.c_uint64
r_bin_get_size.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_sym = _libr_bin.r_bin_get_sym
r_bin_get_sym.restype = POINTER_T(struct_r_bin_addr_t)
r_bin_get_sym.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_int32]
r_bin_raw_strings = _libr_bin.r_bin_raw_strings
r_bin_raw_strings.restype = POINTER_T(struct_r_list_t)
r_bin_raw_strings.argtypes = [POINTER_T(struct_r_bin_file_t), ctypes.c_int32]
r_bin_dump_strings = _libr_bin.r_bin_dump_strings
r_bin_dump_strings.restype = POINTER_T(struct_r_list_t)
r_bin_dump_strings.argtypes = [POINTER_T(struct_r_bin_file_t), ctypes.c_int32, ctypes.c_int32]
r_bin_get_entries = _libr_bin.r_bin_get_entries
r_bin_get_entries.restype = POINTER_T(struct_r_list_t)
r_bin_get_entries.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_fields = _libr_bin.r_bin_get_fields
r_bin_get_fields.restype = POINTER_T(struct_r_list_t)
r_bin_get_fields.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_imports = _libr_bin.r_bin_get_imports
r_bin_get_imports.restype = POINTER_T(struct_r_list_t)
r_bin_get_imports.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_libs = _libr_bin.r_bin_get_libs
r_bin_get_libs.restype = POINTER_T(struct_r_list_t)
r_bin_get_libs.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_patch_relocs = _libr_bin.r_bin_patch_relocs
r_bin_patch_relocs.restype = POINTER_T(struct_r_rb_node_t)
r_bin_patch_relocs.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_patch_relocs_list = _libr_bin.r_bin_patch_relocs_list
r_bin_patch_relocs_list.restype = POINTER_T(struct_r_list_t)
r_bin_patch_relocs_list.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_relocs = _libr_bin.r_bin_get_relocs
r_bin_get_relocs.restype = POINTER_T(struct_r_rb_node_t)
r_bin_get_relocs.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_relocs_list = _libr_bin.r_bin_get_relocs_list
r_bin_get_relocs_list.restype = POINTER_T(struct_r_list_t)
r_bin_get_relocs_list.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_sections = _libr_bin.r_bin_get_sections
r_bin_get_sections.restype = POINTER_T(struct_r_list_t)
r_bin_get_sections.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_classes = _libr_bin.r_bin_get_classes
r_bin_get_classes.restype = POINTER_T(struct_r_list_t)
r_bin_get_classes.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_strings = _libr_bin.r_bin_get_strings
r_bin_get_strings.restype = POINTER_T(struct_r_list_t)
r_bin_get_strings.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_file_get_trycatch = _libr_bin.r_bin_file_get_trycatch
r_bin_file_get_trycatch.restype = POINTER_T(struct_r_list_t)
r_bin_file_get_trycatch.argtypes = [POINTER_T(struct_r_bin_file_t)]
r_bin_get_symbols = _libr_bin.r_bin_get_symbols
r_bin_get_symbols.restype = POINTER_T(struct_r_list_t)
r_bin_get_symbols.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_reset_strings = _libr_bin.r_bin_reset_strings
r_bin_reset_strings.restype = POINTER_T(struct_r_list_t)
r_bin_reset_strings.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_is_string = _libr_bin.r_bin_is_string
r_bin_is_string.restype = ctypes.c_int32
r_bin_is_string.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_is_big_endian = _libr_bin.r_bin_is_big_endian
r_bin_is_big_endian.restype = ctypes.c_int32
r_bin_is_big_endian.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_is_static = _libr_bin.r_bin_is_static
r_bin_is_static.restype = ctypes.c_int32
r_bin_is_static.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_get_vaddr = _libr_bin.r_bin_get_vaddr
r_bin_get_vaddr.restype = ctypes.c_uint64
r_bin_get_vaddr.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64, ctypes.c_uint64]
r_bin_file_get_vaddr = _libr_bin.r_bin_file_get_vaddr
r_bin_file_get_vaddr.restype = ctypes.c_uint64
r_bin_file_get_vaddr.argtypes = [POINTER_T(struct_r_bin_file_t), ctypes.c_uint64, ctypes.c_uint64]
r_bin_a2b = _libr_bin.r_bin_a2b
r_bin_a2b.restype = ctypes.c_uint64
r_bin_a2b.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_load_languages = _libr_bin.r_bin_load_languages
r_bin_load_languages.restype = ctypes.c_int32
r_bin_load_languages.argtypes = [POINTER_T(struct_r_bin_file_t)]
r_bin_cur = _libr_bin.r_bin_cur
r_bin_cur.restype = POINTER_T(struct_r_bin_file_t)
r_bin_cur.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_cur_object = _libr_bin.r_bin_cur_object
r_bin_cur_object.restype = POINTER_T(struct_r_bin_object_t)
r_bin_cur_object.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_select = _libr_bin.r_bin_select
r_bin_select.restype = ctypes.c_bool
r_bin_select.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_bin_select_bfid = _libr_bin.r_bin_select_bfid
r_bin_select_bfid.restype = ctypes.c_bool
r_bin_select_bfid.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_use_arch = _libr_bin.r_bin_use_arch
r_bin_use_arch.restype = ctypes.c_bool
r_bin_use_arch.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_bin_list_archs = _libr_bin.r_bin_list_archs
r_bin_list_archs.restype = None
r_bin_list_archs.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_int32]
r_bin_create = _libr_bin.r_bin_create
r_bin_create.restype = POINTER_T(struct_r_buf_t)
r_bin_create.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(struct_r_bin_arch_options_t)]
r_bin_package = _libr_bin.r_bin_package
r_bin_package.restype = POINTER_T(struct_r_buf_t)
r_bin_package.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(struct_r_list_t)]
r_bin_string_type = _libr_bin.r_bin_string_type
r_bin_string_type.restype = POINTER_T(ctypes.c_char)
r_bin_string_type.argtypes = [ctypes.c_int32]
r_bin_entry_type_string = _libr_bin.r_bin_entry_type_string
r_bin_entry_type_string.restype = POINTER_T(ctypes.c_char)
r_bin_entry_type_string.argtypes = [ctypes.c_int32]
r_bin_file_object_new_from_xtr_data = _libr_bin.r_bin_file_object_new_from_xtr_data
r_bin_file_object_new_from_xtr_data.restype = ctypes.c_bool
r_bin_file_object_new_from_xtr_data.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_file_t), ctypes.c_uint64, ctypes.c_uint64, POINTER_T(struct_r_bin_xtr_extract_t)]
r_bin_file_close = _libr_bin.r_bin_file_close
r_bin_file_close.restype = ctypes.c_bool
r_bin_file_close.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_int32]
r_bin_file_free = _libr_bin.r_bin_file_free
r_bin_file_free.restype = None
r_bin_file_free.argtypes = [POINTER_T(None)]
r_bin_file_at = _libr_bin.r_bin_file_at
r_bin_file_at.restype = POINTER_T(struct_r_bin_file_t)
r_bin_file_at.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_file_get_symbols = _libr_bin.r_bin_file_get_symbols
r_bin_file_get_symbols.restype = POINTER_T(struct_r_list_t)
r_bin_file_get_symbols.argtypes = [POINTER_T(struct_r_bin_file_t)]
r_bin_file_add_class = _libr_bin.r_bin_file_add_class
r_bin_file_add_class.restype = POINTER_T(struct_r_bin_class_t)
r_bin_file_add_class.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_file_add_method = _libr_bin.r_bin_file_add_method
r_bin_file_add_method.restype = POINTER_T(struct_r_bin_symbol_t)
r_bin_file_add_method.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_file_add_field = _libr_bin.r_bin_file_add_field
r_bin_file_add_field.restype = POINTER_T(struct_r_bin_field_t)
r_bin_file_add_field.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_bin_file_find_by_arch_bits = _libr_bin.r_bin_file_find_by_arch_bits
r_bin_file_find_by_arch_bits.restype = POINTER_T(struct_r_bin_file_t)
r_bin_file_find_by_arch_bits.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_file_find_by_id = _libr_bin.r_bin_file_find_by_id
r_bin_file_find_by_id.restype = POINTER_T(struct_r_bin_file_t)
r_bin_file_find_by_id.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_file_find_by_fd = _libr_bin.r_bin_file_find_by_fd
r_bin_file_find_by_fd.restype = POINTER_T(struct_r_bin_file_t)
r_bin_file_find_by_fd.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_file_find_by_name = _libr_bin.r_bin_file_find_by_name
r_bin_file_find_by_name.restype = POINTER_T(struct_r_bin_file_t)
r_bin_file_find_by_name.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char)]
r_bin_file_set_cur_binfile = _libr_bin.r_bin_file_set_cur_binfile
r_bin_file_set_cur_binfile.restype = ctypes.c_bool
r_bin_file_set_cur_binfile.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_file_t)]
r_bin_file_set_cur_by_name = _libr_bin.r_bin_file_set_cur_by_name
r_bin_file_set_cur_by_name.restype = ctypes.c_bool
r_bin_file_set_cur_by_name.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char)]
r_bin_file_deref = _libr_bin.r_bin_file_deref
r_bin_file_deref.restype = ctypes.c_bool
r_bin_file_deref.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_bin_file_t)]
r_bin_file_set_cur_by_fd = _libr_bin.r_bin_file_set_cur_by_fd
r_bin_file_set_cur_by_fd.restype = ctypes.c_bool
r_bin_file_set_cur_by_fd.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_file_set_cur_by_id = _libr_bin.r_bin_file_set_cur_by_id
r_bin_file_set_cur_by_id.restype = ctypes.c_bool
r_bin_file_set_cur_by_id.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_file_delete_all = _libr_bin.r_bin_file_delete_all
r_bin_file_delete_all.restype = ctypes.c_uint64
r_bin_file_delete_all.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_file_delete = _libr_bin.r_bin_file_delete
r_bin_file_delete.restype = ctypes.c_bool
r_bin_file_delete.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_file_compute_hashes = _libr_bin.r_bin_file_compute_hashes
r_bin_file_compute_hashes.restype = POINTER_T(struct_r_list_t)
r_bin_file_compute_hashes.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_file_set_hashes = _libr_bin.r_bin_file_set_hashes
r_bin_file_set_hashes.restype = POINTER_T(struct_r_list_t)
r_bin_file_set_hashes.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(struct_r_list_t)]
r_bin_file_cur_plugin = _libr_bin.r_bin_file_cur_plugin
r_bin_file_cur_plugin.restype = POINTER_T(struct_r_bin_plugin_t)
r_bin_file_cur_plugin.argtypes = [POINTER_T(struct_r_bin_file_t)]
r_bin_file_hash_free = _libr_bin.r_bin_file_hash_free
r_bin_file_hash_free.restype = None
r_bin_file_hash_free.argtypes = [POINTER_T(struct_r_bin_file_hash_t)]
r_bin_object_set_items = _libr_bin.r_bin_object_set_items
r_bin_object_set_items.restype = ctypes.c_int32
r_bin_object_set_items.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(struct_r_bin_object_t)]
r_bin_object_delete = _libr_bin.r_bin_object_delete
r_bin_object_delete.restype = ctypes.c_bool
r_bin_object_delete.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint32]
r_bin_mem_free = _libr_bin.r_bin_mem_free
r_bin_mem_free.restype = None
r_bin_mem_free.argtypes = [POINTER_T(None)]
r_bin_demangle = _libr_bin.r_bin_demangle
r_bin_demangle.restype = POINTER_T(ctypes.c_char)
r_bin_demangle.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_bool]
r_bin_demangle_java = _libr_bin.r_bin_demangle_java
r_bin_demangle_java.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_java.argtypes = [POINTER_T(ctypes.c_char)]
r_bin_demangle_cxx = _libr_bin.r_bin_demangle_cxx
r_bin_demangle_cxx.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_cxx.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_bin_demangle_msvc = _libr_bin.r_bin_demangle_msvc
r_bin_demangle_msvc.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_msvc.argtypes = [POINTER_T(ctypes.c_char)]
r_bin_demangle_swift = _libr_bin.r_bin_demangle_swift
r_bin_demangle_swift.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_swift.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_bool]
r_bin_demangle_objc = _libr_bin.r_bin_demangle_objc
r_bin_demangle_objc.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_objc.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char)]
r_bin_demangle_rust = _libr_bin.r_bin_demangle_rust
r_bin_demangle_rust.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_rust.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_bin_demangle_type = _libr_bin.r_bin_demangle_type
r_bin_demangle_type.restype = ctypes.c_int32
r_bin_demangle_type.argtypes = [POINTER_T(ctypes.c_char)]
r_bin_demangle_list = _libr_bin.r_bin_demangle_list
r_bin_demangle_list.restype = None
r_bin_demangle_list.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_demangle_plugin = _libr_bin.r_bin_demangle_plugin
r_bin_demangle_plugin.restype = POINTER_T(ctypes.c_char)
r_bin_demangle_plugin.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_bin_get_meth_flag_string = _libr_bin.r_bin_get_meth_flag_string
r_bin_get_meth_flag_string.restype = POINTER_T(ctypes.c_char)
r_bin_get_meth_flag_string.argtypes = [ctypes.c_uint64, ctypes.c_bool]
r_bin_get_section_at = _libr_bin.r_bin_get_section_at
r_bin_get_section_at.restype = POINTER_T(struct_r_bin_section_t)
r_bin_get_section_at.argtypes = [POINTER_T(struct_r_bin_object_t), ctypes.c_uint64, ctypes.c_int32]
r_bin_addr2line = _libr_bin.r_bin_addr2line
r_bin_addr2line.restype = ctypes.c_bool
r_bin_addr2line.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_int32)]
r_bin_addr2text = _libr_bin.r_bin_addr2text
r_bin_addr2text.restype = POINTER_T(ctypes.c_char)
r_bin_addr2text.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64, ctypes.c_int32]
r_bin_addr2fileline = _libr_bin.r_bin_addr2fileline
r_bin_addr2fileline.restype = POINTER_T(ctypes.c_char)
r_bin_addr2fileline.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_wr_addlib = _libr_bin.r_bin_wr_addlib
r_bin_wr_addlib.restype = ctypes.c_bool
r_bin_wr_addlib.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char)]
r_bin_wr_scn_resize = _libr_bin.r_bin_wr_scn_resize
r_bin_wr_scn_resize.restype = ctypes.c_uint64
r_bin_wr_scn_resize.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_bin_wr_scn_perms = _libr_bin.r_bin_wr_scn_perms
r_bin_wr_scn_perms.restype = ctypes.c_bool
r_bin_wr_scn_perms.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_bin_wr_rpath_del = _libr_bin.r_bin_wr_rpath_del
r_bin_wr_rpath_del.restype = ctypes.c_bool
r_bin_wr_rpath_del.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_wr_entry = _libr_bin.r_bin_wr_entry
r_bin_wr_entry.restype = ctypes.c_bool
r_bin_wr_entry.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_wr_output = _libr_bin.r_bin_wr_output
r_bin_wr_output.restype = ctypes.c_bool
r_bin_wr_output.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char)]
r_bin_get_mem = _libr_bin.r_bin_get_mem
r_bin_get_mem.restype = POINTER_T(struct_r_list_t)
r_bin_get_mem.argtypes = [POINTER_T(struct_r_bin_t)]
r_bin_load_filter = _libr_bin.r_bin_load_filter
r_bin_load_filter.restype = None
r_bin_load_filter.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_uint64]
r_bin_filter_symbols = _libr_bin.r_bin_filter_symbols
r_bin_filter_symbols.restype = None
r_bin_filter_symbols.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(struct_r_list_t)]
r_bin_filter_sections = _libr_bin.r_bin_filter_sections
r_bin_filter_sections.restype = None
r_bin_filter_sections.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(struct_r_list_t)]
r_bin_filter_name = _libr_bin.r_bin_filter_name
r_bin_filter_name.restype = POINTER_T(ctypes.c_char)
r_bin_filter_name.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(struct_sdb_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_bin_filter_sym = _libr_bin.r_bin_filter_sym
r_bin_filter_sym.restype = None
r_bin_filter_sym.argtypes = [POINTER_T(struct_r_bin_file_t), POINTER_T(struct_ht_pp_t), ctypes.c_uint64, POINTER_T(struct_r_bin_symbol_t)]
r_bin_strpurge = _libr_bin.r_bin_strpurge
r_bin_strpurge.restype = ctypes.c_bool
r_bin_strpurge.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_bin_string_filter = _libr_bin.r_bin_string_filter
r_bin_string_filter.restype = ctypes.c_bool
r_bin_string_filter.argtypes = [POINTER_T(struct_r_bin_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_bin_plugin_any = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_fs = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_cgc = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_elf = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_elf64 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_p9 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_ne = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_le = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_pe = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_mz = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_pe64 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_pebble = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_bios = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_bf = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_te = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_symbols = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_mach0 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_mach064 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_mdmp = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_java = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_dex = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_coff = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_ningb = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_ningba = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_ninds = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_nin3ds = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_xbe = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_bflt = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_xtr_plugin_xtr_fatmach0 = struct_r_bin_xtr_plugin_t # Variable struct_r_bin_xtr_plugin_t
r_bin_xtr_plugin_xtr_dyldcache = struct_r_bin_xtr_plugin_t # Variable struct_r_bin_xtr_plugin_t
r_bin_xtr_plugin_xtr_pemixed = struct_r_bin_xtr_plugin_t # Variable struct_r_bin_xtr_plugin_t
r_bin_xtr_plugin_xtr_sep64 = struct_r_bin_xtr_plugin_t # Variable struct_r_bin_xtr_plugin_t
r_bin_ldr_plugin_ldr_linux = struct_r_bin_ldr_plugin_t # Variable struct_r_bin_ldr_plugin_t
r_bin_plugin_zimg = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_omf = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_art = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_bootimg = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_dol = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_nes = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_qnx = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_mbn = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_smd = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_sms = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_psxexe = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_spc700 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_vsf = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_dyldcache = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_xnu_kernelcache = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_avr = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_menuet = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_wasm = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_nro = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_nso = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_sfc = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_z64 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_prg = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_dmp64 = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
r_bin_plugin_pyc = struct_r_bin_plugin_t # Variable struct_r_bin_plugin_t
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
    ['FREE_XTR', 'PTRACE_ARCH_PRCTL', 'PTRACE_ATTACH', 'PTRACE_CONT',
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
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'RBin', 'RBinAddr',
    'RBinArchOptions', 'RBinBind', 'RBinClass', 'RBinDbgInfo',
    'RBinDemangle', 'RBinField', 'RBinFile', 'RBinFileHash',
    'RBinFileOptions', 'RBinGetName', 'RBinGetOffset',
    'RBinGetSectionAt', 'RBinGetSections', 'RBinHash', 'RBinImport',
    'RBinInfo', 'RBinLdrPlugin', 'RBinMap', 'RBinMem', 'RBinObject',
    'RBinOptions', 'RBinPlugin', 'RBinReloc', 'RBinSection',
    'RBinString', 'RBinSymbol', 'RBinSymbolCallback',
    'RBinSymbollCallback', 'RBinTrycatch', 'RBinWrite', 'RBinXtrData',
    'RBinXtrMetadata', 'RBinXtrPlugin', 'R_BIN_CLASS_FRIENDLY',
    'R_BIN_CLASS_PRIVATE', 'R_BIN_CLASS_PROTECTED',
    'R_BIN_CLASS_PUBLIC', 'R_BIN_NM_ANY', 'R_BIN_NM_BLOCKS',
    'R_BIN_NM_C', 'R_BIN_NM_CXX', 'R_BIN_NM_DLANG', 'R_BIN_NM_GO',
    'R_BIN_NM_JAVA', 'R_BIN_NM_KOTLIN', 'R_BIN_NM_MSVC',
    'R_BIN_NM_NONE', 'R_BIN_NM_OBJC', 'R_BIN_NM_RUST',
    'R_BIN_NM_SWIFT', 'R_BIN_RELOC_16', 'R_BIN_RELOC_32',
    'R_BIN_RELOC_64', 'R_BIN_RELOC_8', 'R_BIN_SYM_ENTRY',
    'R_BIN_SYM_FINI', 'R_BIN_SYM_INIT', 'R_BIN_SYM_LAST',
    'R_BIN_SYM_MAIN', 'R_BIN_TYPE_CORE', 'R_BIN_TYPE_DEFAULT',
    'R_STRING_TYPE_ASCII', 'R_STRING_TYPE_BASE64',
    'R_STRING_TYPE_DETECT', 'R_STRING_TYPE_UTF8',
    'R_STRING_TYPE_WIDE', 'R_STRING_TYPE_WIDE32', '__ptrace_request',
    'c__Ea_R_BIN_CLASS_PRIVATE', 'c__Ea_R_BIN_NM_NONE',
    'c__Ea_R_BIN_RELOC_8', 'c__Ea_R_BIN_SYM_ENTRY',
    'c__Ea_R_BIN_TYPE_DEFAULT', 'c__Ea_R_STRING_TYPE_DETECT',
    'r_bin_a2b', 'r_bin_add', 'r_bin_addr2fileline',
    'r_bin_addr2line', 'r_bin_addr2text', 'r_bin_arch_options_init',
    'r_bin_bind', 'r_bin_create', 'r_bin_cur', 'r_bin_cur_object',
    'r_bin_demangle', 'r_bin_demangle_cxx', 'r_bin_demangle_java',
    'r_bin_demangle_list', 'r_bin_demangle_msvc',
    'r_bin_demangle_objc', 'r_bin_demangle_plugin',
    'r_bin_demangle_rust', 'r_bin_demangle_swift',
    'r_bin_demangle_type', 'r_bin_dump_strings',
    'r_bin_entry_type_string', 'r_bin_field_free', 'r_bin_field_new',
    'r_bin_file_add_class', 'r_bin_file_add_field',
    'r_bin_file_add_method', 'r_bin_file_at', 'r_bin_file_close',
    'r_bin_file_compute_hashes', 'r_bin_file_cur_plugin',
    'r_bin_file_delete', 'r_bin_file_delete_all', 'r_bin_file_deref',
    'r_bin_file_find_by_arch_bits', 'r_bin_file_find_by_fd',
    'r_bin_file_find_by_id', 'r_bin_file_find_by_name',
    'r_bin_file_free', 'r_bin_file_get_baddr',
    'r_bin_file_get_symbols', 'r_bin_file_get_trycatch',
    'r_bin_file_get_vaddr', 'r_bin_file_hash_free',
    'r_bin_file_object_new_from_xtr_data',
    'r_bin_file_set_cur_binfile', 'r_bin_file_set_cur_by_fd',
    'r_bin_file_set_cur_by_id', 'r_bin_file_set_cur_by_name',
    'r_bin_file_set_hashes', 'r_bin_filter_name',
    'r_bin_filter_sections', 'r_bin_filter_sym',
    'r_bin_filter_symbols', 'r_bin_force_plugin', 'r_bin_free',
    'r_bin_get_baddr', 'r_bin_get_binplugin_by_buffer',
    'r_bin_get_classes', 'r_bin_get_entries', 'r_bin_get_fields',
    'r_bin_get_imports', 'r_bin_get_info', 'r_bin_get_laddr',
    'r_bin_get_libs', 'r_bin_get_mem', 'r_bin_get_meth_flag_string',
    'r_bin_get_relocs', 'r_bin_get_relocs_list',
    'r_bin_get_section_at', 'r_bin_get_sections', 'r_bin_get_size',
    'r_bin_get_strings', 'r_bin_get_sym', 'r_bin_get_symbols',
    'r_bin_get_vaddr', 'r_bin_import_clone', 'r_bin_import_free',
    'r_bin_info_free', 'r_bin_is_big_endian', 'r_bin_is_static',
    'r_bin_is_string', 'r_bin_ldr_add', 'r_bin_ldr_plugin_ldr_linux',
    'r_bin_list', 'r_bin_list_archs', 'r_bin_list_plugin',
    'r_bin_load_filter', 'r_bin_load_languages', 'r_bin_mem_free',
    'r_bin_new', 'r_bin_object_delete', 'r_bin_object_set_items',
    'r_bin_open', 'r_bin_open_buf', 'r_bin_open_io',
    'r_bin_options_init', 'r_bin_package', 'r_bin_patch_relocs',
    'r_bin_patch_relocs_list', 'r_bin_plugin_any', 'r_bin_plugin_art',
    'r_bin_plugin_avr', 'r_bin_plugin_bf', 'r_bin_plugin_bflt',
    'r_bin_plugin_bios', 'r_bin_plugin_bootimg', 'r_bin_plugin_cgc',
    'r_bin_plugin_coff', 'r_bin_plugin_dex', 'r_bin_plugin_dmp64',
    'r_bin_plugin_dol', 'r_bin_plugin_dyldcache', 'r_bin_plugin_elf',
    'r_bin_plugin_elf64', 'r_bin_plugin_fs', 'r_bin_plugin_java',
    'r_bin_plugin_le', 'r_bin_plugin_mach0', 'r_bin_plugin_mach064',
    'r_bin_plugin_mbn', 'r_bin_plugin_mdmp', 'r_bin_plugin_menuet',
    'r_bin_plugin_mz', 'r_bin_plugin_ne', 'r_bin_plugin_nes',
    'r_bin_plugin_nin3ds', 'r_bin_plugin_ninds', 'r_bin_plugin_ningb',
    'r_bin_plugin_ningba', 'r_bin_plugin_nro', 'r_bin_plugin_nso',
    'r_bin_plugin_omf', 'r_bin_plugin_p9', 'r_bin_plugin_pe',
    'r_bin_plugin_pe64', 'r_bin_plugin_pebble', 'r_bin_plugin_prg',
    'r_bin_plugin_psxexe', 'r_bin_plugin_pyc', 'r_bin_plugin_qnx',
    'r_bin_plugin_sfc', 'r_bin_plugin_smd', 'r_bin_plugin_sms',
    'r_bin_plugin_spc700', 'r_bin_plugin_symbols', 'r_bin_plugin_te',
    'r_bin_plugin_vsf', 'r_bin_plugin_wasm', 'r_bin_plugin_xbe',
    'r_bin_plugin_xnu_kernelcache', 'r_bin_plugin_z64',
    'r_bin_plugin_zimg', 'r_bin_raw_strings', 'r_bin_reload',
    'r_bin_reset_strings', 'r_bin_select', 'r_bin_select_bfid',
    'r_bin_set_baddr', 'r_bin_set_user_ptr', 'r_bin_string_filter',
    'r_bin_string_free', 'r_bin_string_type', 'r_bin_strpurge',
    'r_bin_symbol_free', 'r_bin_symbol_name', 'r_bin_symbol_new',
    'r_bin_trycatch_free', 'r_bin_trycatch_new', 'r_bin_use_arch',
    'r_bin_version', 'r_bin_wr_addlib', 'r_bin_wr_entry',
    'r_bin_wr_output', 'r_bin_wr_rpath_del', 'r_bin_wr_scn_perms',
    'r_bin_wr_scn_resize', 'r_bin_xtr_add',
    'r_bin_xtr_plugin_xtr_dyldcache', 'r_bin_xtr_plugin_xtr_fatmach0',
    'r_bin_xtr_plugin_xtr_pemixed', 'r_bin_xtr_plugin_xtr_sep64',
    'r_bin_xtrdata_free', 'r_bin_xtrdata_new', 'struct_buffer',
    'struct_c__SA_dict', 'struct_cdb', 'struct_cdb_hp',
    'struct_cdb_hplist', 'struct_cdb_make', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_ptrace_wrap_instance_t',
    'struct_r_bin_addr_t', 'struct_r_bin_arch_options_t',
    'struct_r_bin_bind_t', 'struct_r_bin_class_t',
    'struct_r_bin_dbginfo_t', 'struct_r_bin_field_t',
    'struct_r_bin_file_hash_t', 'struct_r_bin_file_options_t',
    'struct_r_bin_file_t', 'struct_r_bin_hash_t',
    'struct_r_bin_import_t', 'struct_r_bin_info_t',
    'struct_r_bin_ldr_plugin_t', 'struct_r_bin_map_t',
    'struct_r_bin_mem_t', 'struct_r_bin_object_t',
    'struct_r_bin_options_t', 'struct_r_bin_plugin_t',
    'struct_r_bin_reloc_t', 'struct_r_bin_section_t',
    'struct_r_bin_string_t', 'struct_r_bin_symbol_t',
    'struct_r_bin_t', 'struct_r_bin_trycatch_t',
    'struct_r_bin_write_t', 'struct_r_bin_xtr_extract_t',
    'struct_r_bin_xtr_metadata_t', 'struct_r_bin_xtr_plugin_t',
    'struct_r_buf_t', 'struct_r_buffer_methods_t', 'struct_r_cache_t',
    'struct_r_cons_bind_t', 'struct_r_core_bind_t',
    'struct_r_id_pool_t', 'struct_r_id_storage_t',
    'struct_r_interval_t', 'struct_r_io_bind_t', 'struct_r_io_desc_t',
    'struct_r_io_map_t', 'struct_r_io_plugin_t', 'struct_r_io_t',
    'struct_r_io_undo_t', 'struct_r_io_undos_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_pvector_t',
    'struct_r_queue_t', 'struct_r_rb_node_t',
    'struct_r_str_constpool_t', 'struct_r_vector_t', 'struct_sdb_kv',
    'struct_sdb_t']

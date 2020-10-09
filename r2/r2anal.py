# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-I/home/mio/pyr2/radare2/installdir/usr/local/include/libr', '-I/home/mio/pyr2/radare2/installdir/usr/local/include/libr/sdb']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_anal as _r_anal

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

class struct_r_bin_info_t(ctypes.Structure):
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

class struct_r_bin_object_t(ctypes.Structure):
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

class struct_cdb_make(ctypes.Structure):
    pass

class struct_cdb_hplist(ctypes.Structure):
    pass

class struct_cdb_hp(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('h', ctypes.c_uint32),
    ('p', ctypes.c_uint32),
     ]

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

class struct_r_bin_plugin_t(ctypes.Structure):
    pass

class struct_r_bin_file_t(ctypes.Structure):
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

class struct_r_bin_t(ctypes.Structure):
    pass

class struct_r_buf_t(ctypes.Structure):
    pass

class struct_r_bin_arch_options_t(ctypes.Structure):
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

class struct_r_rb_node_t(ctypes.Structure):
    pass

struct_r_rb_node_t._pack_ = True # source:False
struct_r_rb_node_t._fields_ = [
    ('child', POINTER_T(struct_r_rb_node_t) * 2),
    ('red', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
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

class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

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

class struct_ptrace_wrap_instance_t(ctypes.Structure):
    pass

class struct_r_io_desc_t(ctypes.Structure):
    pass

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
class struct_r_io_map_t(ctypes.Structure):
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

class struct_c__SA_RBinDwarfBlock(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint64),
    ('data', POINTER_T(ctypes.c_ubyte)),
     ]


# values for enumeration 'c__EA_RBinDwarfAttrKind'
c__EA_RBinDwarfAttrKind__enumvalues = {
    0: 'DW_AT_KIND_ADDRESS',
    1: 'DW_AT_KIND_BLOCK',
    2: 'DW_AT_KIND_CONSTANT',
    3: 'DW_AT_KIND_EXPRLOC',
    4: 'DW_AT_KIND_FLAG',
    5: 'DW_AT_KIND_LINEPTR',
    6: 'DW_AT_KIND_LOCLISTPTR',
    7: 'DW_AT_KIND_MACPTR',
    8: 'DW_AT_KIND_RANGELISTPTR',
    9: 'DW_AT_KIND_REFERENCE',
    10: 'DW_AT_KIND_STRING',
}
DW_AT_KIND_ADDRESS = 0
DW_AT_KIND_BLOCK = 1
DW_AT_KIND_CONSTANT = 2
DW_AT_KIND_EXPRLOC = 3
DW_AT_KIND_FLAG = 4
DW_AT_KIND_LINEPTR = 5
DW_AT_KIND_LOCLISTPTR = 6
DW_AT_KIND_MACPTR = 7
DW_AT_KIND_RANGELISTPTR = 8
DW_AT_KIND_REFERENCE = 9
DW_AT_KIND_STRING = 10
c__EA_RBinDwarfAttrKind = ctypes.c_int # enum
class struct_dwarf_attr_kind(ctypes.Structure):
    pass

class union_dwarf_attr_kind_0(ctypes.Union):
    pass

class struct_dwarf_attr_kind_0_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('content', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_uint64),
     ]

union_dwarf_attr_kind_0._pack_ = True # source:False
union_dwarf_attr_kind_0._fields_ = [
    ('address', ctypes.c_uint64),
    ('block', struct_c__SA_RBinDwarfBlock),
    ('uconstant', ctypes.c_uint64),
    ('sconstant', ctypes.c_int64),
    ('flag', ctypes.c_ubyte),
    ('reference', ctypes.c_uint64),
    ('_6', struct_dwarf_attr_kind_0_0),
]

struct_dwarf_attr_kind._pack_ = True # source:False
struct_dwarf_attr_kind._fields_ = [
    ('attr_name', ctypes.c_uint64),
    ('attr_form', ctypes.c_uint64),
    ('kind', c__EA_RBinDwarfAttrKind),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_3', union_dwarf_attr_kind_0),
]

class struct_c__SA_RBinDwarfCompUnitHdr(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint64),
    ('version', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('abbrev_offset', ctypes.c_uint64),
    ('address_size', ctypes.c_ubyte),
    ('unit_type', ctypes.c_ubyte),
    ('dwo_id', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 5),
    ('type_sig', ctypes.c_uint64),
    ('type_offset', ctypes.c_uint64),
    ('header_size', ctypes.c_uint64),
    ('unit_offset', ctypes.c_uint64),
    ('is_64bit', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 7),
     ]

class struct_c__SA_RBinDwarfDie(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tag', ctypes.c_uint64),
    ('abbrev_code', ctypes.c_uint64),
    ('count', ctypes.c_uint64),
    ('capacity', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('has_children', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('attr_values', POINTER_T(struct_dwarf_attr_kind)),
     ]

class struct_c__SA_RBinDwarfCompUnit(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('hdr', struct_c__SA_RBinDwarfCompUnitHdr),
    ('offset', ctypes.c_uint64),
    ('count', ctypes.c_uint64),
    ('capacity', ctypes.c_uint64),
    ('dies', POINTER_T(struct_c__SA_RBinDwarfDie)),
     ]

class struct_c__SA_RBinDwarfDebugInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('count', ctypes.c_uint64),
    ('capacity', ctypes.c_uint64),
    ('comp_units', POINTER_T(struct_c__SA_RBinDwarfCompUnit)),
    ('lookup_table', POINTER_T(struct_ht_up_t)),
     ]

class struct_r_cons_printable_palette_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('b0x00', POINTER_T(ctypes.c_char)),
    ('b0x7f', POINTER_T(ctypes.c_char)),
    ('b0xff', POINTER_T(ctypes.c_char)),
    ('args', POINTER_T(ctypes.c_char)),
    ('bin', POINTER_T(ctypes.c_char)),
    ('btext', POINTER_T(ctypes.c_char)),
    ('call', POINTER_T(ctypes.c_char)),
    ('cjmp', POINTER_T(ctypes.c_char)),
    ('cmp', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
    ('usercomment', POINTER_T(ctypes.c_char)),
    ('creg', POINTER_T(ctypes.c_char)),
    ('flag', POINTER_T(ctypes.c_char)),
    ('fline', POINTER_T(ctypes.c_char)),
    ('floc', POINTER_T(ctypes.c_char)),
    ('flow', POINTER_T(ctypes.c_char)),
    ('flow2', POINTER_T(ctypes.c_char)),
    ('fname', POINTER_T(ctypes.c_char)),
    ('help', POINTER_T(ctypes.c_char)),
    ('input', POINTER_T(ctypes.c_char)),
    ('invalid', POINTER_T(ctypes.c_char)),
    ('jmp', POINTER_T(ctypes.c_char)),
    ('label', POINTER_T(ctypes.c_char)),
    ('math', POINTER_T(ctypes.c_char)),
    ('mov', POINTER_T(ctypes.c_char)),
    ('nop', POINTER_T(ctypes.c_char)),
    ('num', POINTER_T(ctypes.c_char)),
    ('offset', POINTER_T(ctypes.c_char)),
    ('other', POINTER_T(ctypes.c_char)),
    ('pop', POINTER_T(ctypes.c_char)),
    ('prompt', POINTER_T(ctypes.c_char)),
    ('push', POINTER_T(ctypes.c_char)),
    ('crypto', POINTER_T(ctypes.c_char)),
    ('reg', POINTER_T(ctypes.c_char)),
    ('reset', POINTER_T(ctypes.c_char)),
    ('ret', POINTER_T(ctypes.c_char)),
    ('swi', POINTER_T(ctypes.c_char)),
    ('trap', POINTER_T(ctypes.c_char)),
    ('ucall', POINTER_T(ctypes.c_char)),
    ('ujmp', POINTER_T(ctypes.c_char)),
    ('ai_read', POINTER_T(ctypes.c_char)),
    ('ai_write', POINTER_T(ctypes.c_char)),
    ('ai_exec', POINTER_T(ctypes.c_char)),
    ('ai_seq', POINTER_T(ctypes.c_char)),
    ('ai_ascii', POINTER_T(ctypes.c_char)),
    ('ai_unmap', POINTER_T(ctypes.c_char)),
    ('gui_cflow', POINTER_T(ctypes.c_char)),
    ('gui_dataoffset', POINTER_T(ctypes.c_char)),
    ('gui_background', POINTER_T(ctypes.c_char)),
    ('gui_alt_background', POINTER_T(ctypes.c_char)),
    ('gui_border', POINTER_T(ctypes.c_char)),
    ('wordhl', POINTER_T(ctypes.c_char)),
    ('linehl', POINTER_T(ctypes.c_char)),
    ('func_var', POINTER_T(ctypes.c_char)),
    ('func_var_type', POINTER_T(ctypes.c_char)),
    ('func_var_addr', POINTER_T(ctypes.c_char)),
    ('widget_bg', POINTER_T(ctypes.c_char)),
    ('widget_sel', POINTER_T(ctypes.c_char)),
    ('graph_box', POINTER_T(ctypes.c_char)),
    ('graph_box2', POINTER_T(ctypes.c_char)),
    ('graph_box3', POINTER_T(ctypes.c_char)),
    ('graph_box4', POINTER_T(ctypes.c_char)),
    ('graph_diff_match', POINTER_T(ctypes.c_char)),
    ('graph_diff_unmatch', POINTER_T(ctypes.c_char)),
    ('graph_diff_unknown', POINTER_T(ctypes.c_char)),
    ('graph_diff_new', POINTER_T(ctypes.c_char)),
    ('graph_true', POINTER_T(ctypes.c_char)),
    ('graph_false', POINTER_T(ctypes.c_char)),
    ('graph_trufae', POINTER_T(ctypes.c_char)),
    ('graph_traced', POINTER_T(ctypes.c_char)),
    ('graph_current', POINTER_T(ctypes.c_char)),
    ('rainbow', POINTER_T(POINTER_T(ctypes.c_char))),
    ('rainbow_sz', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

class struct_r_flag_item_t(ctypes.Structure):
    pass

class struct_r_space_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

class struct_r_flag_t(ctypes.Structure):
    pass

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

struct_r_spaces_t._pack_ = True # source:False
struct_r_spaces_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('current', POINTER_T(struct_r_space_t)),
    ('spaces', POINTER_T(struct_r_rb_node_t)),
    ('spacestack', POINTER_T(struct_r_list_t)),
    ('event', POINTER_T(struct_r_event_t)),
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

class struct_r_list_range_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('h', POINTER_T(struct_ht_pp_t)),
    ('l', POINTER_T(struct_r_list_t)),
     ]

class struct_R_PDB7_ROOT_STREAM(ctypes.Structure):
    pass

class struct_r_pdb_t(ctypes.Structure):
    pass

class struct_pj_t(ctypes.Structure):
    pass

struct_r_pdb_t._pack_ = True # source:False
struct_r_pdb_t._fields_ = [
    ('pdb_parse', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_pdb_t)))),
    ('finish_pdb_parse', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_pdb_t)))),
    ('print_types', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_pdb_t), POINTER_T(struct_pj_t), ctypes.c_int32))),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('root_stream', POINTER_T(struct_R_PDB7_ROOT_STREAM)),
    ('stream_map', POINTER_T(None)),
    ('pdb_streams', POINTER_T(struct_r_list_t)),
    ('pdb_streams2', POINTER_T(struct_r_list_t)),
    ('buf', POINTER_T(struct_r_buf_t)),
    ('print_gvars', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_pdb_t), ctypes.c_uint64, POINTER_T(struct_pj_t), ctypes.c_int32))),
]

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

class struct_r_reg_arena_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', POINTER_T(ctypes.c_ubyte)),
    ('size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

class struct_r_reg_set_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('arena', POINTER_T(struct_r_reg_arena_t)),
    ('pool', POINTER_T(struct_r_list_t)),
    ('regs', POINTER_T(struct_r_list_t)),
    ('ht_regs', POINTER_T(struct_ht_pp_t)),
    ('cur', POINTER_T(struct_r_list_iter_t)),
    ('maskregstype', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

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

struct_pj_t._pack_ = True # source:False
struct_pj_t._fields_ = [
    ('sb', struct_c__SA_RStrBuf),
    ('is_first', ctypes.c_bool),
    ('is_key', ctypes.c_bool),
    ('braces', ctypes.c_char * 128),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('level', ctypes.c_int32),
]

class struct_r_graph_node_t(ctypes.Structure):
    pass

struct_r_graph_node_t._pack_ = True # source:False
struct_r_graph_node_t._fields_ = [
    ('idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('data', POINTER_T(None)),
    ('out_nodes', POINTER_T(struct_r_list_t)),
    ('in_nodes', POINTER_T(struct_r_list_t)),
    ('all_neighbours', POINTER_T(struct_r_list_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

class struct_r_graph_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('n_nodes', ctypes.c_uint32),
    ('n_edges', ctypes.c_uint32),
    ('last_index', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('nodes', POINTER_T(struct_r_list_t)),
     ]

class struct_r_interval_node_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('node', struct_r_rb_node_t),
    ('start', ctypes.c_uint64),
    ('end', ctypes.c_uint64),
    ('max_end', ctypes.c_uint64),
    ('data', POINTER_T(None)),
     ]

class struct_r_interval_tree_t(ctypes.Structure):
    pass

struct_r_interval_tree_t._pack_ = True # source:False
struct_r_interval_tree_t._fields_ = [
    ('root', POINTER_T(struct_r_interval_node_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

class struct_r_containing_rb_node_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('node', struct_r_rb_node_t),
    ('data', POINTER_T(None)),
     ]

class struct_r_containing_rb_tree_t(ctypes.Structure):
    pass

struct_r_containing_rb_tree_t._pack_ = True # source:False
struct_r_containing_rb_tree_t._fields_ = [
    ('root', POINTER_T(struct_r_containing_rb_node_t)),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]

SdbForeachCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))
size_t = ctypes.c_uint64
r_anal_version = _r_anal.r_anal_version
r_anal_version.restype = POINTER_T(ctypes.c_char)
r_anal_version.argtypes = []
class struct_r_anal_dwarf_context(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('info', POINTER_T(struct_c__SA_RBinDwarfDebugInfo)),
    ('loc', POINTER_T(struct_ht_up_t)),
     ]

RAnalDwarfContext = struct_r_anal_dwarf_context
class struct_c__SA_RAnalMetaUserItem(ctypes.Structure):
    pass

class struct_r_anal_function_t(ctypes.Structure):
    pass

class struct_r_anal_t(ctypes.Structure):
    pass


# values for enumeration 'c__EA_RAnalCPPABI'
c__EA_RAnalCPPABI__enumvalues = {
    0: 'R_ANAL_CPP_ABI_ITANIUM',
    1: 'R_ANAL_CPP_ABI_MSVC',
}
R_ANAL_CPP_ABI_ITANIUM = 0
R_ANAL_CPP_ABI_MSVC = 1
c__EA_RAnalCPPABI = ctypes.c_int # enum
class struct_r_anal_esil_t(ctypes.Structure):
    pass

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

class struct_r_anal_range_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('bits', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('rb_max_addr', ctypes.c_uint64),
    ('rb', struct_r_rb_node_t),
     ]

class struct_r_anal_hint_cb_t(ctypes.Structure):
    pass

struct_r_anal_hint_cb_t._pack_ = True # source:False
struct_r_anal_hint_cb_t._fields_ = [
    ('on_bits', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_bool))),
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

class struct_r_anal_plugin_t(ctypes.Structure):
    pass

class struct_r_anal_bb_t(ctypes.Structure):
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

class struct_r_anal_callbacks_t(ctypes.Structure):
    pass

struct_r_anal_callbacks_t._pack_ = True # source:False
struct_r_anal_callbacks_t._fields_ = [
    ('on_fcn_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_delete', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_rename', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)))),
    ('on_fcn_bb_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t)))),
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

class struct_r_anal_fcn_meta_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('_min', ctypes.c_uint64),
    ('_max', ctypes.c_uint64),
    ('numrefs', ctypes.c_int32),
    ('numcallrefs', ctypes.c_int32),
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

struct_c__SA_RAnalMetaUserItem._pack_ = True # source:False
struct_c__SA_RAnalMetaUserItem._fields_ = [
    ('anal', POINTER_T(struct_r_anal_t)),
    ('type', ctypes.c_int32),
    ('rad', ctypes.c_int32),
    ('cb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(None), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('user', POINTER_T(None)),
    ('count', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('fcn', POINTER_T(struct_r_anal_function_t)),
    ('pj', POINTER_T(struct_pj_t)),
]

RAnalMetaUserItem = struct_c__SA_RAnalMetaUserItem
RAnalRange = struct_r_anal_range_t

# values for enumeration 'c__Ea_R_ANAL_DATA_TYPE_NULL'
c__Ea_R_ANAL_DATA_TYPE_NULL__enumvalues = {
    0: 'R_ANAL_DATA_TYPE_NULL',
    1: 'R_ANAL_DATA_TYPE_UNKNOWN',
    2: 'R_ANAL_DATA_TYPE_STRING',
    3: 'R_ANAL_DATA_TYPE_WIDE_STRING',
    4: 'R_ANAL_DATA_TYPE_POINTER',
    5: 'R_ANAL_DATA_TYPE_NUMBER',
    6: 'R_ANAL_DATA_TYPE_INVALID',
    7: 'R_ANAL_DATA_TYPE_HEADER',
    8: 'R_ANAL_DATA_TYPE_SEQUENCE',
    9: 'R_ANAL_DATA_TYPE_PATTERN',
}
R_ANAL_DATA_TYPE_NULL = 0
R_ANAL_DATA_TYPE_UNKNOWN = 1
R_ANAL_DATA_TYPE_STRING = 2
R_ANAL_DATA_TYPE_WIDE_STRING = 3
R_ANAL_DATA_TYPE_POINTER = 4
R_ANAL_DATA_TYPE_NUMBER = 5
R_ANAL_DATA_TYPE_INVALID = 6
R_ANAL_DATA_TYPE_HEADER = 7
R_ANAL_DATA_TYPE_SEQUENCE = 8
R_ANAL_DATA_TYPE_PATTERN = 9
c__Ea_R_ANAL_DATA_TYPE_NULL = ctypes.c_int # enum
class struct_r_anal_type_var_t(ctypes.Structure):
    pass

class union_r_anal_type_var_t_0(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('v8', ctypes.c_ubyte),
    ('v16', ctypes.c_uint16),
    ('v32', ctypes.c_uint32),
    ('v64', ctypes.c_uint64),
     ]

struct_r_anal_type_var_t._pack_ = True # source:False
struct_r_anal_type_var_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('index', ctypes.c_int32),
    ('scope', ctypes.c_int32),
    ('type', ctypes.c_uint16),
    ('size', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 5),
    ('_5', union_r_anal_type_var_t_0),
]

RAnalTypeVar = struct_r_anal_type_var_t
class struct_r_anal_type_ptr_t(ctypes.Structure):
    pass

class union_r_anal_type_ptr_t_0(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('v8', ctypes.c_ubyte),
    ('v16', ctypes.c_uint16),
    ('v32', ctypes.c_uint32),
    ('v64', ctypes.c_uint64),
     ]

struct_r_anal_type_ptr_t._pack_ = True # source:False
struct_r_anal_type_ptr_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_uint16),
    ('size', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 5),
    ('_3', union_r_anal_type_ptr_t_0),
]

RAnalTypePtr = struct_r_anal_type_ptr_t
class struct_r_anal_type_array_t(ctypes.Structure):
    pass

class union_r_anal_type_array_t_0(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('v8', POINTER_T(ctypes.c_ubyte)),
    ('v16', POINTER_T(ctypes.c_uint16)),
    ('v32', POINTER_T(ctypes.c_uint32)),
    ('v64', POINTER_T(ctypes.c_uint64)),
     ]

struct_r_anal_type_array_t._pack_ = True # source:False
struct_r_anal_type_array_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_uint16),
    ('size', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 5),
    ('count', ctypes.c_uint64),
    ('_4', union_r_anal_type_array_t_0),
]

RAnalTypeArray = struct_r_anal_type_array_t
class struct_r_anal_type_struct_t(ctypes.Structure):
    pass

class struct_r_anal_type_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_uint32),
    ('size', ctypes.c_uint32),
    ('content', POINTER_T(struct_r_list_t)),
     ]

struct_r_anal_type_struct_t._pack_ = True # source:False
struct_r_anal_type_struct_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('size', ctypes.c_uint32),
    ('parent', POINTER_T(None)),
    ('items', POINTER_T(struct_r_anal_type_t)),
]

RAnalTypeStruct = struct_r_anal_type_struct_t
RAnalType = struct_r_anal_type_t
class struct_r_anal_type_union_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('size', ctypes.c_uint32),
    ('parent', POINTER_T(None)),
    ('items', POINTER_T(struct_r_anal_type_t)),
     ]

RAnalTypeUnion = struct_r_anal_type_union_t
class struct_r_anal_type_alloca_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('address', ctypes.c_int64),
    ('size', ctypes.c_int64),
    ('parent', POINTER_T(None)),
    ('items', POINTER_T(struct_r_anal_type_t)),
     ]

RAnalTypeAlloca = struct_r_anal_type_alloca_t

# values for enumeration 'c__Ea_R_ANAL_FQUALIFIER_NONE'
c__Ea_R_ANAL_FQUALIFIER_NONE__enumvalues = {
    0: 'R_ANAL_FQUALIFIER_NONE',
    1: 'R_ANAL_FQUALIFIER_STATIC',
    2: 'R_ANAL_FQUALIFIER_VOLATILE',
    3: 'R_ANAL_FQUALIFIER_INLINE',
    4: 'R_ANAL_FQUALIFIER_NAKED',
    5: 'R_ANAL_FQUALIFIER_VIRTUAL',
}
R_ANAL_FQUALIFIER_NONE = 0
R_ANAL_FQUALIFIER_STATIC = 1
R_ANAL_FQUALIFIER_VOLATILE = 2
R_ANAL_FQUALIFIER_INLINE = 3
R_ANAL_FQUALIFIER_NAKED = 4
R_ANAL_FQUALIFIER_VIRTUAL = 5
c__Ea_R_ANAL_FQUALIFIER_NONE = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_ANAL_FCN_TYPE_NULL'
c__Ea_R_ANAL_FCN_TYPE_NULL__enumvalues = {
    0: 'R_ANAL_FCN_TYPE_NULL',
    1: 'R_ANAL_FCN_TYPE_FCN',
    2: 'R_ANAL_FCN_TYPE_LOC',
    4: 'R_ANAL_FCN_TYPE_SYM',
    8: 'R_ANAL_FCN_TYPE_IMP',
    16: 'R_ANAL_FCN_TYPE_INT',
    32: 'R_ANAL_FCN_TYPE_ROOT',
    -1: 'R_ANAL_FCN_TYPE_ANY',
}
R_ANAL_FCN_TYPE_NULL = 0
R_ANAL_FCN_TYPE_FCN = 1
R_ANAL_FCN_TYPE_LOC = 2
R_ANAL_FCN_TYPE_SYM = 4
R_ANAL_FCN_TYPE_IMP = 8
R_ANAL_FCN_TYPE_INT = 16
R_ANAL_FCN_TYPE_ROOT = 32
R_ANAL_FCN_TYPE_ANY = -1
c__Ea_R_ANAL_FCN_TYPE_NULL = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_ANAL_DIFF_TYPE_NULL'
c__Ea_R_ANAL_DIFF_TYPE_NULL__enumvalues = {
    0: 'R_ANAL_DIFF_TYPE_NULL',
    109: 'R_ANAL_DIFF_TYPE_MATCH',
    117: 'R_ANAL_DIFF_TYPE_UNMATCH',
}
R_ANAL_DIFF_TYPE_NULL = 0
R_ANAL_DIFF_TYPE_MATCH = 109
R_ANAL_DIFF_TYPE_UNMATCH = 117
c__Ea_R_ANAL_DIFF_TYPE_NULL = ctypes.c_int # enum
class struct_r_anal_enum_case_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('val', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RAnalEnumCase = struct_r_anal_enum_case_t
class struct_r_anal_struct_member_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
     ]

RAnalStructMember = struct_r_anal_struct_member_t
class struct_r_anal_union_member_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
     ]

RAnalUnionMember = struct_r_anal_union_member_t

# values for enumeration 'c__EA_RAnalBaseTypeKind'
c__EA_RAnalBaseTypeKind__enumvalues = {
    0: 'R_ANAL_BASE_TYPE_KIND_STRUCT',
    1: 'R_ANAL_BASE_TYPE_KIND_UNION',
    2: 'R_ANAL_BASE_TYPE_KIND_ENUM',
    3: 'R_ANAL_BASE_TYPE_KIND_TYPEDEF',
    4: 'R_ANAL_BASE_TYPE_KIND_ATOMIC',
}
R_ANAL_BASE_TYPE_KIND_STRUCT = 0
R_ANAL_BASE_TYPE_KIND_UNION = 1
R_ANAL_BASE_TYPE_KIND_ENUM = 2
R_ANAL_BASE_TYPE_KIND_TYPEDEF = 3
R_ANAL_BASE_TYPE_KIND_ATOMIC = 4
c__EA_RAnalBaseTypeKind = ctypes.c_int # enum
RAnalBaseTypeKind = c__EA_RAnalBaseTypeKind
RAnalBaseTypeKind__enumvalues = c__EA_RAnalBaseTypeKind__enumvalues
class struct_r_anal_base_type_struct_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('members', struct_r_vector_t),
     ]

RAnalBaseTypeStruct = struct_r_anal_base_type_struct_t
class struct_r_anal_base_type_union_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('members', struct_r_vector_t),
     ]

RAnalBaseTypeUnion = struct_r_anal_base_type_union_t
class struct_r_anal_base_type_enum_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cases', struct_r_vector_t),
     ]

RAnalBaseTypeEnum = struct_r_anal_base_type_enum_t
class struct_r_anal_base_type_t(ctypes.Structure):
    pass

class union_r_anal_base_type_t_0(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('struct_data', RAnalBaseTypeStruct),
    ('enum_data', RAnalBaseTypeEnum),
    ('union_data', RAnalBaseTypeUnion),
     ]

struct_r_anal_base_type_t._pack_ = True # source:False
struct_r_anal_base_type_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('size', ctypes.c_uint64),
    ('kind', RAnalBaseTypeKind),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_4', union_r_anal_base_type_t_0),
]

RAnalBaseType = struct_r_anal_base_type_t
RAnalDiff = struct_r_anal_diff_t
class struct_r_anal_attr_t(ctypes.Structure):
    pass

struct_r_anal_attr_t._pack_ = True # source:False
struct_r_anal_attr_t._fields_ = [
    ('key', POINTER_T(ctypes.c_char)),
    ('value', ctypes.c_int64),
    ('next', POINTER_T(struct_r_anal_attr_t)),
]

RAnalAttr = struct_r_anal_attr_t
RAnalFcnMeta = struct_r_anal_fcn_meta_t
RAnalFunction = struct_r_anal_function_t
class struct_r_anal_func_arg_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('fmt', POINTER_T(ctypes.c_char)),
    ('cc_source', POINTER_T(ctypes.c_char)),
    ('orig_c_type', POINTER_T(ctypes.c_char)),
    ('c_type', POINTER_T(ctypes.c_char)),
    ('size', ctypes.c_uint64),
    ('src', ctypes.c_uint64),
     ]

RAnalFuncArg = struct_r_anal_func_arg_t

# values for enumeration 'c__EA_RAnalMetaType'
c__EA_RAnalMetaType__enumvalues = {
    -1: 'R_META_TYPE_ANY',
    100: 'R_META_TYPE_DATA',
    99: 'R_META_TYPE_CODE',
    115: 'R_META_TYPE_STRING',
    102: 'R_META_TYPE_FORMAT',
    109: 'R_META_TYPE_MAGIC',
    104: 'R_META_TYPE_HIDE',
    67: 'R_META_TYPE_COMMENT',
    114: 'R_META_TYPE_RUN',
    72: 'R_META_TYPE_HIGHLIGHT',
    116: 'R_META_TYPE_VARTYPE',
}
R_META_TYPE_ANY = -1
R_META_TYPE_DATA = 100
R_META_TYPE_CODE = 99
R_META_TYPE_STRING = 115
R_META_TYPE_FORMAT = 102
R_META_TYPE_MAGIC = 109
R_META_TYPE_HIDE = 104
R_META_TYPE_COMMENT = 67
R_META_TYPE_RUN = 114
R_META_TYPE_HIGHLIGHT = 72
R_META_TYPE_VARTYPE = 116
c__EA_RAnalMetaType = ctypes.c_int # enum
RAnalMetaType = c__EA_RAnalMetaType
RAnalMetaType__enumvalues = c__EA_RAnalMetaType__enumvalues
class struct_r_anal_meta_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', RAnalMetaType),
    ('subtype', ctypes.c_int32),
    ('str', POINTER_T(ctypes.c_char)),
    ('space', POINTER_T(struct_r_space_t)),
     ]

RAnalMetaItem = struct_r_anal_meta_item_t

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
RAnalOpFamily = c__EA_RAnalOpFamily
RAnalOpFamily__enumvalues = c__EA_RAnalOpFamily__enumvalues

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
RAnalOpPrefix = c__EA_RAnalOpPrefix
RAnalOpPrefix__enumvalues = c__EA_RAnalOpPrefix__enumvalues

# values for enumeration 'c__EA__RAnalOpType'
c__EA__RAnalOpType__enumvalues = {
    2147483648: 'R_ANAL_OP_TYPE_COND',
    1073741824: 'R_ANAL_OP_TYPE_REP',
    536870912: 'R_ANAL_OP_TYPE_MEM',
    268435456: 'R_ANAL_OP_TYPE_REG',
    134217728: 'R_ANAL_OP_TYPE_IND',
    0: 'R_ANAL_OP_TYPE_NULL',
    1: 'R_ANAL_OP_TYPE_JMP',
    2: 'R_ANAL_OP_TYPE_UJMP',
    268435458: 'R_ANAL_OP_TYPE_RJMP',
    134217730: 'R_ANAL_OP_TYPE_IJMP',
    402653186: 'R_ANAL_OP_TYPE_IRJMP',
    2147483649: 'R_ANAL_OP_TYPE_CJMP',
    2415919105: 'R_ANAL_OP_TYPE_RCJMP',
    536870913: 'R_ANAL_OP_TYPE_MJMP',
    2684354561: 'R_ANAL_OP_TYPE_MCJMP',
    2147483650: 'R_ANAL_OP_TYPE_UCJMP',
    3: 'R_ANAL_OP_TYPE_CALL',
    4: 'R_ANAL_OP_TYPE_UCALL',
    268435460: 'R_ANAL_OP_TYPE_RCALL',
    134217732: 'R_ANAL_OP_TYPE_ICALL',
    402653188: 'R_ANAL_OP_TYPE_IRCALL',
    2147483651: 'R_ANAL_OP_TYPE_CCALL',
    2147483652: 'R_ANAL_OP_TYPE_UCCALL',
    5: 'R_ANAL_OP_TYPE_RET',
    2147483653: 'R_ANAL_OP_TYPE_CRET',
    6: 'R_ANAL_OP_TYPE_ILL',
    7: 'R_ANAL_OP_TYPE_UNK',
    8: 'R_ANAL_OP_TYPE_NOP',
    9: 'R_ANAL_OP_TYPE_MOV',
    2147483657: 'R_ANAL_OP_TYPE_CMOV',
    10: 'R_ANAL_OP_TYPE_TRAP',
    11: 'R_ANAL_OP_TYPE_SWI',
    2147483659: 'R_ANAL_OP_TYPE_CSWI',
    12: 'R_ANAL_OP_TYPE_UPUSH',
    268435468: 'R_ANAL_OP_TYPE_RPUSH',
    13: 'R_ANAL_OP_TYPE_PUSH',
    14: 'R_ANAL_OP_TYPE_POP',
    15: 'R_ANAL_OP_TYPE_CMP',
    16: 'R_ANAL_OP_TYPE_ACMP',
    17: 'R_ANAL_OP_TYPE_ADD',
    18: 'R_ANAL_OP_TYPE_SUB',
    19: 'R_ANAL_OP_TYPE_IO',
    20: 'R_ANAL_OP_TYPE_MUL',
    21: 'R_ANAL_OP_TYPE_DIV',
    22: 'R_ANAL_OP_TYPE_SHR',
    23: 'R_ANAL_OP_TYPE_SHL',
    24: 'R_ANAL_OP_TYPE_SAL',
    25: 'R_ANAL_OP_TYPE_SAR',
    26: 'R_ANAL_OP_TYPE_OR',
    27: 'R_ANAL_OP_TYPE_AND',
    28: 'R_ANAL_OP_TYPE_XOR',
    29: 'R_ANAL_OP_TYPE_NOR',
    30: 'R_ANAL_OP_TYPE_NOT',
    31: 'R_ANAL_OP_TYPE_STORE',
    32: 'R_ANAL_OP_TYPE_LOAD',
    33: 'R_ANAL_OP_TYPE_LEA',
    34: 'R_ANAL_OP_TYPE_LEAVE',
    35: 'R_ANAL_OP_TYPE_ROR',
    36: 'R_ANAL_OP_TYPE_ROL',
    37: 'R_ANAL_OP_TYPE_XCHG',
    38: 'R_ANAL_OP_TYPE_MOD',
    39: 'R_ANAL_OP_TYPE_SWITCH',
    40: 'R_ANAL_OP_TYPE_CASE',
    41: 'R_ANAL_OP_TYPE_LENGTH',
    42: 'R_ANAL_OP_TYPE_CAST',
    43: 'R_ANAL_OP_TYPE_NEW',
    44: 'R_ANAL_OP_TYPE_ABS',
    45: 'R_ANAL_OP_TYPE_CPL',
    46: 'R_ANAL_OP_TYPE_CRYPTO',
    47: 'R_ANAL_OP_TYPE_SYNC',
}
R_ANAL_OP_TYPE_COND = 2147483648
R_ANAL_OP_TYPE_REP = 1073741824
R_ANAL_OP_TYPE_MEM = 536870912
R_ANAL_OP_TYPE_REG = 268435456
R_ANAL_OP_TYPE_IND = 134217728
R_ANAL_OP_TYPE_NULL = 0
R_ANAL_OP_TYPE_JMP = 1
R_ANAL_OP_TYPE_UJMP = 2
R_ANAL_OP_TYPE_RJMP = 268435458
R_ANAL_OP_TYPE_IJMP = 134217730
R_ANAL_OP_TYPE_IRJMP = 402653186
R_ANAL_OP_TYPE_CJMP = 2147483649
R_ANAL_OP_TYPE_RCJMP = 2415919105
R_ANAL_OP_TYPE_MJMP = 536870913
R_ANAL_OP_TYPE_MCJMP = 2684354561
R_ANAL_OP_TYPE_UCJMP = 2147483650
R_ANAL_OP_TYPE_CALL = 3
R_ANAL_OP_TYPE_UCALL = 4
R_ANAL_OP_TYPE_RCALL = 268435460
R_ANAL_OP_TYPE_ICALL = 134217732
R_ANAL_OP_TYPE_IRCALL = 402653188
R_ANAL_OP_TYPE_CCALL = 2147483651
R_ANAL_OP_TYPE_UCCALL = 2147483652
R_ANAL_OP_TYPE_RET = 5
R_ANAL_OP_TYPE_CRET = 2147483653
R_ANAL_OP_TYPE_ILL = 6
R_ANAL_OP_TYPE_UNK = 7
R_ANAL_OP_TYPE_NOP = 8
R_ANAL_OP_TYPE_MOV = 9
R_ANAL_OP_TYPE_CMOV = 2147483657
R_ANAL_OP_TYPE_TRAP = 10
R_ANAL_OP_TYPE_SWI = 11
R_ANAL_OP_TYPE_CSWI = 2147483659
R_ANAL_OP_TYPE_UPUSH = 12
R_ANAL_OP_TYPE_RPUSH = 268435468
R_ANAL_OP_TYPE_PUSH = 13
R_ANAL_OP_TYPE_POP = 14
R_ANAL_OP_TYPE_CMP = 15
R_ANAL_OP_TYPE_ACMP = 16
R_ANAL_OP_TYPE_ADD = 17
R_ANAL_OP_TYPE_SUB = 18
R_ANAL_OP_TYPE_IO = 19
R_ANAL_OP_TYPE_MUL = 20
R_ANAL_OP_TYPE_DIV = 21
R_ANAL_OP_TYPE_SHR = 22
R_ANAL_OP_TYPE_SHL = 23
R_ANAL_OP_TYPE_SAL = 24
R_ANAL_OP_TYPE_SAR = 25
R_ANAL_OP_TYPE_OR = 26
R_ANAL_OP_TYPE_AND = 27
R_ANAL_OP_TYPE_XOR = 28
R_ANAL_OP_TYPE_NOR = 29
R_ANAL_OP_TYPE_NOT = 30
R_ANAL_OP_TYPE_STORE = 31
R_ANAL_OP_TYPE_LOAD = 32
R_ANAL_OP_TYPE_LEA = 33
R_ANAL_OP_TYPE_LEAVE = 34
R_ANAL_OP_TYPE_ROR = 35
R_ANAL_OP_TYPE_ROL = 36
R_ANAL_OP_TYPE_XCHG = 37
R_ANAL_OP_TYPE_MOD = 38
R_ANAL_OP_TYPE_SWITCH = 39
R_ANAL_OP_TYPE_CASE = 40
R_ANAL_OP_TYPE_LENGTH = 41
R_ANAL_OP_TYPE_CAST = 42
R_ANAL_OP_TYPE_NEW = 43
R_ANAL_OP_TYPE_ABS = 44
R_ANAL_OP_TYPE_CPL = 45
R_ANAL_OP_TYPE_CRYPTO = 46
R_ANAL_OP_TYPE_SYNC = 47
c__EA__RAnalOpType = ctypes.c_int # enum
_RAnalOpType = c__EA__RAnalOpType
_RAnalOpType__enumvalues = c__EA__RAnalOpType__enumvalues
RAnalOpMask = c__EA_RAnalOpMask
RAnalOpMask__enumvalues = c__EA_RAnalOpMask__enumvalues

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
_RAnalCond = c__EA__RAnalCond
_RAnalCond__enumvalues = c__EA__RAnalCond__enumvalues

# values for enumeration 'c__EA__RAnalVarScope'
c__EA__RAnalVarScope__enumvalues = {
    1: 'R_ANAL_VAR_SCOPE_LOCAL',
}
R_ANAL_VAR_SCOPE_LOCAL = 1
c__EA__RAnalVarScope = ctypes.c_int # enum
_RAnalVarScope = c__EA__RAnalVarScope
_RAnalVarScope__enumvalues = c__EA__RAnalVarScope__enumvalues

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
RAnalStackOp = c__EA_RAnalStackOp
RAnalStackOp__enumvalues = c__EA_RAnalStackOp__enumvalues

# values for enumeration 'c__Ea_R_ANAL_REFLINE_TYPE_UTF8'
c__Ea_R_ANAL_REFLINE_TYPE_UTF8__enumvalues = {
    1: 'R_ANAL_REFLINE_TYPE_UTF8',
    2: 'R_ANAL_REFLINE_TYPE_WIDE',
    4: 'R_ANAL_REFLINE_TYPE_MIDDLE_BEFORE',
    8: 'R_ANAL_REFLINE_TYPE_MIDDLE_AFTER',
}
R_ANAL_REFLINE_TYPE_UTF8 = 1
R_ANAL_REFLINE_TYPE_WIDE = 2
R_ANAL_REFLINE_TYPE_MIDDLE_BEFORE = 4
R_ANAL_REFLINE_TYPE_MIDDLE_AFTER = 8
c__Ea_R_ANAL_REFLINE_TYPE_UTF8 = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_ANAL_RET_NOP'
c__Ea_R_ANAL_RET_NOP__enumvalues = {
    0: 'R_ANAL_RET_NOP',
    -1: 'R_ANAL_RET_ERROR',
    -2: 'R_ANAL_RET_DUP',
    -3: 'R_ANAL_RET_NEW',
    -4: 'R_ANAL_RET_END',
}
R_ANAL_RET_NOP = 0
R_ANAL_RET_ERROR = -1
R_ANAL_RET_DUP = -2
R_ANAL_RET_NEW = -3
R_ANAL_RET_END = -4
c__Ea_R_ANAL_RET_NOP = ctypes.c_int # enum
class struct_r_anal_case_obj_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('jump', ctypes.c_uint64),
    ('value', ctypes.c_uint64),
     ]

RAnalCaseOp = struct_r_anal_case_obj_t
class struct_r_anal_switch_obj_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('min_val', ctypes.c_uint64),
    ('def_val', ctypes.c_uint64),
    ('max_val', ctypes.c_uint64),
    ('cases', POINTER_T(struct_r_list_t)),
     ]

RAnalSwitchOp = struct_r_anal_switch_obj_t
RAnalCallbacks = struct_r_anal_callbacks_t
RAnalOptions = struct_r_anal_options_t
RAnalCPPABI = c__EA_RAnalCPPABI
RAnalCPPABI__enumvalues = c__EA_RAnalCPPABI__enumvalues
RHintCb = struct_r_anal_hint_cb_t
RAnal = struct_r_anal_t

# values for enumeration 'r_anal_addr_hint_type_t'
r_anal_addr_hint_type_t__enumvalues = {
    0: 'R_ANAL_ADDR_HINT_TYPE_IMMBASE',
    1: 'R_ANAL_ADDR_HINT_TYPE_JUMP',
    2: 'R_ANAL_ADDR_HINT_TYPE_FAIL',
    3: 'R_ANAL_ADDR_HINT_TYPE_STACKFRAME',
    4: 'R_ANAL_ADDR_HINT_TYPE_PTR',
    5: 'R_ANAL_ADDR_HINT_TYPE_NWORD',
    6: 'R_ANAL_ADDR_HINT_TYPE_RET',
    7: 'R_ANAL_ADDR_HINT_TYPE_NEW_BITS',
    8: 'R_ANAL_ADDR_HINT_TYPE_SIZE',
    9: 'R_ANAL_ADDR_HINT_TYPE_SYNTAX',
    10: 'R_ANAL_ADDR_HINT_TYPE_OPTYPE',
    11: 'R_ANAL_ADDR_HINT_TYPE_OPCODE',
    12: 'R_ANAL_ADDR_HINT_TYPE_TYPE_OFFSET',
    13: 'R_ANAL_ADDR_HINT_TYPE_ESIL',
    14: 'R_ANAL_ADDR_HINT_TYPE_HIGH',
    15: 'R_ANAL_ADDR_HINT_TYPE_VAL',
}
R_ANAL_ADDR_HINT_TYPE_IMMBASE = 0
R_ANAL_ADDR_HINT_TYPE_JUMP = 1
R_ANAL_ADDR_HINT_TYPE_FAIL = 2
R_ANAL_ADDR_HINT_TYPE_STACKFRAME = 3
R_ANAL_ADDR_HINT_TYPE_PTR = 4
R_ANAL_ADDR_HINT_TYPE_NWORD = 5
R_ANAL_ADDR_HINT_TYPE_RET = 6
R_ANAL_ADDR_HINT_TYPE_NEW_BITS = 7
R_ANAL_ADDR_HINT_TYPE_SIZE = 8
R_ANAL_ADDR_HINT_TYPE_SYNTAX = 9
R_ANAL_ADDR_HINT_TYPE_OPTYPE = 10
R_ANAL_ADDR_HINT_TYPE_OPCODE = 11
R_ANAL_ADDR_HINT_TYPE_TYPE_OFFSET = 12
R_ANAL_ADDR_HINT_TYPE_ESIL = 13
R_ANAL_ADDR_HINT_TYPE_HIGH = 14
R_ANAL_ADDR_HINT_TYPE_VAL = 15
r_anal_addr_hint_type_t = ctypes.c_int # enum
RAnalAddrHintType = r_anal_addr_hint_type_t
RAnalAddrHintType__enumvalues = r_anal_addr_hint_type_t__enumvalues
class struct_r_anal_addr_hint_record_t(ctypes.Structure):
    pass

class union_r_anal_addr_hint_record_t_0(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('type_offset', POINTER_T(ctypes.c_char)),
    ('nword', ctypes.c_int32),
    ('jump', ctypes.c_uint64),
    ('fail', ctypes.c_uint64),
    ('newbits', ctypes.c_int32),
    ('immbase', ctypes.c_int32),
    ('ptr', ctypes.c_uint64),
    ('retval', ctypes.c_uint64),
    ('syntax', POINTER_T(ctypes.c_char)),
    ('opcode', POINTER_T(ctypes.c_char)),
    ('esil', POINTER_T(ctypes.c_char)),
    ('optype', ctypes.c_int32),
    ('size', ctypes.c_uint64),
    ('stackframe', ctypes.c_uint64),
    ('val', ctypes.c_uint64),
     ]

struct_r_anal_addr_hint_record_t._pack_ = True # source:False
struct_r_anal_addr_hint_record_t._fields_ = [
    ('type', RAnalAddrHintType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_1', union_r_anal_addr_hint_record_t_0),
]

RAnalAddrHintRecord = struct_r_anal_addr_hint_record_t
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

RAnalHint = struct_r_anal_hint_t
RAnalGetFcnIn = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32))
RAnalGetHint = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_hint_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64))
class struct_r_anal_bind_t(ctypes.Structure):
    pass

struct_r_anal_bind_t._pack_ = True # source:False
struct_r_anal_bind_t._fields_ = [
    ('anal', POINTER_T(struct_r_anal_t)),
    ('get_fcn_in', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32))),
    ('get_hint', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_anal_hint_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64))),
]

RAnalBind = struct_r_anal_bind_t
RAnalLabelAt = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64))

# values for enumeration 'c__EA_RAnalVarKind'
c__EA_RAnalVarKind__enumvalues = {
    114: 'R_ANAL_VAR_KIND_REG',
    98: 'R_ANAL_VAR_KIND_BPV',
    115: 'R_ANAL_VAR_KIND_SPV',
}
R_ANAL_VAR_KIND_REG = 114
R_ANAL_VAR_KIND_BPV = 98
R_ANAL_VAR_KIND_SPV = 115
c__EA_RAnalVarKind = ctypes.c_int # enum
RAnalVarKind = c__EA_RAnalVarKind
RAnalVarKind__enumvalues = c__EA_RAnalVarKind__enumvalues

# values for enumeration 'c__EA_RAnalVarAccessType'
c__EA_RAnalVarAccessType__enumvalues = {
    1: 'R_ANAL_VAR_ACCESS_TYPE_READ',
    2: 'R_ANAL_VAR_ACCESS_TYPE_WRITE',
}
R_ANAL_VAR_ACCESS_TYPE_READ = 1
R_ANAL_VAR_ACCESS_TYPE_WRITE = 2
c__EA_RAnalVarAccessType = ctypes.c_int # enum
RAnalVarAccessType = c__EA_RAnalVarAccessType
RAnalVarAccessType__enumvalues = c__EA_RAnalVarAccessType__enumvalues
class struct_r_anal_var_access_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reg', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_int64),
    ('stackptr', ctypes.c_int64),
    ('type', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
     ]

RAnalVarAccess = struct_r_anal_var_access_t
class struct_r_anal_var_constraint_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cond', _RAnalCond),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('val', ctypes.c_uint64),
     ]

RAnalVarConstraint = struct_r_anal_var_constraint_t
class struct_r_anal_var_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('fcn', POINTER_T(struct_r_anal_function_t)),
    ('name', POINTER_T(ctypes.c_char)),
    ('type', POINTER_T(ctypes.c_char)),
    ('kind', RAnalVarKind),
    ('isarg', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('delta', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('regname', POINTER_T(ctypes.c_char)),
    ('accesses', struct_r_vector_t),
    ('comment', POINTER_T(ctypes.c_char)),
    ('constraints', struct_r_vector_t),
    ('argnum', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]

RAnalVar = struct_r_anal_var_t
class struct_r_anal_var_field_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('delta', ctypes.c_int64),
    ('field', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
     ]

RAnalVarField = struct_r_anal_var_field_t

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
RAnalValueAccess = c__EA_RAnalValueAccess
RAnalValueAccess__enumvalues = c__EA_RAnalValueAccess__enumvalues

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
RAnalValueType = c__EA_RAnalValueType
RAnalValueType__enumvalues = c__EA_RAnalValueType__enumvalues
class struct_r_anal_value_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

RAnalValue = struct_r_anal_value_t

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
RAnalOpDirection = c__EA_RAnalOpDirection
RAnalOpDirection__enumvalues = c__EA_RAnalOpDirection__enumvalues

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
RAnalDataType = r_anal_data_type_t
RAnalDataType__enumvalues = r_anal_data_type_t__enumvalues
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

RAnalOp = struct_r_anal_op_t
class struct_r_anal_cond_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arg', POINTER_T(struct_r_anal_value_t) * 2),
     ]

RAnalCond = struct_r_anal_cond_t
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

RAnalBlock = struct_r_anal_bb_t

# values for enumeration 'c__EA_RAnalRefType'
c__EA_RAnalRefType__enumvalues = {
    0: 'R_ANAL_REF_TYPE_NULL',
    99: 'R_ANAL_REF_TYPE_CODE',
    67: 'R_ANAL_REF_TYPE_CALL',
    100: 'R_ANAL_REF_TYPE_DATA',
    115: 'R_ANAL_REF_TYPE_STRING',
}
R_ANAL_REF_TYPE_NULL = 0
R_ANAL_REF_TYPE_CODE = 99
R_ANAL_REF_TYPE_CALL = 67
R_ANAL_REF_TYPE_DATA = 100
R_ANAL_REF_TYPE_STRING = 115
c__EA_RAnalRefType = ctypes.c_int # enum
RAnalRefType = c__EA_RAnalRefType
RAnalRefType__enumvalues = c__EA_RAnalRefType__enumvalues
class struct_r_anal_ref_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('at', ctypes.c_uint64),
    ('type', RAnalRefType),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RAnalRef = struct_r_anal_ref_t
r_anal_ref_type_tostring = _r_anal.r_anal_ref_type_tostring
r_anal_ref_type_tostring.restype = POINTER_T(ctypes.c_char)
r_anal_ref_type_tostring.argtypes = [RAnalRefType]
class struct_r_anal_refline_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('index', ctypes.c_int32),
    ('level', ctypes.c_int32),
    ('type', ctypes.c_int32),
    ('direction', ctypes.c_int32),
     ]

RAnalRefline = struct_r_anal_refline_t
class struct_r_anal_cycle_frame_t(ctypes.Structure):
    pass

struct_r_anal_cycle_frame_t._pack_ = True # source:False
struct_r_anal_cycle_frame_t._fields_ = [
    ('naddr', ctypes.c_uint64),
    ('hooks', POINTER_T(struct_r_list_t)),
    ('prev', POINTER_T(struct_r_anal_cycle_frame_t)),
]

RAnalCycleFrame = struct_r_anal_cycle_frame_t
class struct_r_anal_cycle_hook_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('cycles', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RAnalCycleHook = struct_r_anal_cycle_hook_t
class struct_r_anal_esil_word_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('str', POINTER_T(ctypes.c_char)),
     ]

RAnalEsilWord = struct_r_anal_esil_word_t

# values for enumeration 'c__Ea_R_ANAL_ESIL_FLAG_ZERO'
c__Ea_R_ANAL_ESIL_FLAG_ZERO__enumvalues = {
    1: 'R_ANAL_ESIL_FLAG_ZERO',
    2: 'R_ANAL_ESIL_FLAG_CARRY',
    4: 'R_ANAL_ESIL_FLAG_OVERFLOW',
    8: 'R_ANAL_ESIL_FLAG_PARITY',
    16: 'R_ANAL_ESIL_FLAG_SIGN',
}
R_ANAL_ESIL_FLAG_ZERO = 1
R_ANAL_ESIL_FLAG_CARRY = 2
R_ANAL_ESIL_FLAG_OVERFLOW = 4
R_ANAL_ESIL_FLAG_PARITY = 8
R_ANAL_ESIL_FLAG_SIGN = 16
c__Ea_R_ANAL_ESIL_FLAG_ZERO = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_ANAL_TRAP_NONE'
c__Ea_R_ANAL_TRAP_NONE__enumvalues = {
    0: 'R_ANAL_TRAP_NONE',
    1: 'R_ANAL_TRAP_UNHANDLED',
    2: 'R_ANAL_TRAP_BREAKPOINT',
    3: 'R_ANAL_TRAP_DIVBYZERO',
    4: 'R_ANAL_TRAP_WRITE_ERR',
    5: 'R_ANAL_TRAP_READ_ERR',
    6: 'R_ANAL_TRAP_EXEC_ERR',
    7: 'R_ANAL_TRAP_INVALID',
    8: 'R_ANAL_TRAP_UNALIGNED',
    9: 'R_ANAL_TRAP_TODO',
    10: 'R_ANAL_TRAP_HALT',
}
R_ANAL_TRAP_NONE = 0
R_ANAL_TRAP_UNHANDLED = 1
R_ANAL_TRAP_BREAKPOINT = 2
R_ANAL_TRAP_DIVBYZERO = 3
R_ANAL_TRAP_WRITE_ERR = 4
R_ANAL_TRAP_READ_ERR = 5
R_ANAL_TRAP_EXEC_ERR = 6
R_ANAL_TRAP_INVALID = 7
R_ANAL_TRAP_UNALIGNED = 8
R_ANAL_TRAP_TODO = 9
R_ANAL_TRAP_HALT = 10
c__Ea_R_ANAL_TRAP_NONE = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_ANAL_ESIL_PARM_INVALID'
c__Ea_R_ANAL_ESIL_PARM_INVALID__enumvalues = {
    0: 'R_ANAL_ESIL_PARM_INVALID',
    1: 'R_ANAL_ESIL_PARM_REG',
    2: 'R_ANAL_ESIL_PARM_NUM',
}
R_ANAL_ESIL_PARM_INVALID = 0
R_ANAL_ESIL_PARM_REG = 1
R_ANAL_ESIL_PARM_NUM = 2
c__Ea_R_ANAL_ESIL_PARM_INVALID = ctypes.c_int # enum

# values for enumeration 'c__EA_RAnalReilOpcode'
c__EA_RAnalReilOpcode__enumvalues = {
    0: 'REIL_NOP',
    1: 'REIL_UNK',
    2: 'REIL_JCC',
    3: 'REIL_STR',
    4: 'REIL_STM',
    5: 'REIL_LDM',
    6: 'REIL_ADD',
    7: 'REIL_SUB',
    8: 'REIL_NEG',
    9: 'REIL_MUL',
    10: 'REIL_DIV',
    11: 'REIL_MOD',
    12: 'REIL_SMUL',
    13: 'REIL_SDIV',
    14: 'REIL_SMOD',
    15: 'REIL_SHL',
    16: 'REIL_SHR',
    17: 'REIL_AND',
    18: 'REIL_OR',
    19: 'REIL_XOR',
    20: 'REIL_NOT',
    21: 'REIL_EQ',
    22: 'REIL_LT',
}
REIL_NOP = 0
REIL_UNK = 1
REIL_JCC = 2
REIL_STR = 3
REIL_STM = 4
REIL_LDM = 5
REIL_ADD = 6
REIL_SUB = 7
REIL_NEG = 8
REIL_MUL = 9
REIL_DIV = 10
REIL_MOD = 11
REIL_SMUL = 12
REIL_SDIV = 13
REIL_SMOD = 14
REIL_SHL = 15
REIL_SHR = 16
REIL_AND = 17
REIL_OR = 18
REIL_XOR = 19
REIL_NOT = 20
REIL_EQ = 21
REIL_LT = 22
c__EA_RAnalReilOpcode = ctypes.c_int # enum
RAnalReilOpcode = c__EA_RAnalReilOpcode
RAnalReilOpcode__enumvalues = c__EA_RAnalReilOpcode__enumvalues

# values for enumeration 'c__EA_RAnalReilArgType'
c__EA_RAnalReilArgType__enumvalues = {
    0: 'ARG_REG',
    1: 'ARG_TEMP',
    2: 'ARG_CONST',
    3: 'ARG_ESIL_INTERNAL',
    4: 'ARG_NONE',
}
ARG_REG = 0
ARG_TEMP = 1
ARG_CONST = 2
ARG_ESIL_INTERNAL = 3
ARG_NONE = 4
c__EA_RAnalReilArgType = ctypes.c_int # enum
RAnalReilArgType = c__EA_RAnalReilArgType
RAnalReilArgType__enumvalues = c__EA_RAnalReilArgType__enumvalues
class struct_r_anal_reil_arg(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', RAnalReilArgType),
    ('size', ctypes.c_ubyte),
    ('name', ctypes.c_char * 32),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

RAnalReilArg = struct_r_anal_reil_arg
class struct_r_anal_ref_char(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('str', POINTER_T(ctypes.c_char)),
    ('cols', POINTER_T(ctypes.c_char)),
     ]

RAnalRefStr = struct_r_anal_ref_char
class struct_r_anal_reil_inst(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('opcode', RAnalReilOpcode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arg', POINTER_T(struct_r_anal_reil_arg) * 3),
     ]

RAnalReilInst = struct_r_anal_reil_inst
RAnalReil = struct_r_anal_reil
class struct_r_anal_esil_source_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('id', ctypes.c_uint32),
    ('claimed', ctypes.c_uint32),
    ('content', POINTER_T(None)),
     ]

RAnalEsilSource = struct_r_anal_esil_source_t
r_anal_esil_sources_init = _r_anal.r_anal_esil_sources_init
r_anal_esil_sources_init.restype = None
r_anal_esil_sources_init.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_load_source = _r_anal.r_anal_esil_load_source
r_anal_esil_load_source.restype = ctypes.c_uint32
r_anal_esil_load_source.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_get_source = _r_anal.r_anal_esil_get_source
r_anal_esil_get_source.restype = POINTER_T(None)
r_anal_esil_get_source.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32]
r_anal_esil_claim_source = _r_anal.r_anal_esil_claim_source
r_anal_esil_claim_source.restype = ctypes.c_bool
r_anal_esil_claim_source.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32]
r_anal_esil_release_source = _r_anal.r_anal_esil_release_source
r_anal_esil_release_source.restype = None
r_anal_esil_release_source.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32]
r_anal_esil_sources_fini = _r_anal.r_anal_esil_sources_fini
r_anal_esil_sources_fini.restype = None
r_anal_esil_sources_fini.argtypes = [POINTER_T(struct_r_anal_esil_t)]
RAnalEsilInterruptCB = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32, POINTER_T(None)))
RAnalEsilInterruptHandler = struct_r_anal_esil_interrupt_handler_t
RAnalEsilInterrupt = struct_r_anal_esil_interrupt_t
class struct_r_anal_esil_change_reg_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('idx', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('data', ctypes.c_uint64),
     ]

RAnalEsilRegChange = struct_r_anal_esil_change_reg_t
class struct_r_anal_esil_change_mem_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('idx', ctypes.c_int32),
    ('data', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

RAnalEsilMemChange = struct_r_anal_esil_change_mem_t
RAnalEsilTrace = struct_r_anal_esil_trace_t
RAnalEsilHookRegWriteCB = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64)))
RAnalEsilCallbacks = struct_r_anal_esil_callbacks_t
RAnalEsil = struct_r_anal_esil_t

# values for enumeration 'c__Ea_R_ANAL_ESIL_OP_TYPE_UNKNOWN'
c__Ea_R_ANAL_ESIL_OP_TYPE_UNKNOWN__enumvalues = {
    1: 'R_ANAL_ESIL_OP_TYPE_UNKNOWN',
    2: 'R_ANAL_ESIL_OP_TYPE_CONTROL_FLOW',
    4: 'R_ANAL_ESIL_OP_TYPE_MEM_READ',
    8: 'R_ANAL_ESIL_OP_TYPE_MEM_WRITE',
    16: 'R_ANAL_ESIL_OP_TYPE_REG_WRITE',
    32: 'R_ANAL_ESIL_OP_TYPE_MATH',
    64: 'R_ANAL_ESIL_OP_TYPE_CUSTOM',
}
R_ANAL_ESIL_OP_TYPE_UNKNOWN = 1
R_ANAL_ESIL_OP_TYPE_CONTROL_FLOW = 2
R_ANAL_ESIL_OP_TYPE_MEM_READ = 4
R_ANAL_ESIL_OP_TYPE_MEM_WRITE = 8
R_ANAL_ESIL_OP_TYPE_REG_WRITE = 16
R_ANAL_ESIL_OP_TYPE_MATH = 32
R_ANAL_ESIL_OP_TYPE_CUSTOM = 64
c__Ea_R_ANAL_ESIL_OP_TYPE_UNKNOWN = ctypes.c_int # enum
RAnalEsilOpCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_esil_t)))
class struct_r_anal_esil_operation_t(ctypes.Structure):
    pass

struct_r_anal_esil_operation_t._pack_ = True # source:False
struct_r_anal_esil_operation_t._fields_ = [
    ('code', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_esil_t)))),
    ('push', ctypes.c_uint32),
    ('pop', ctypes.c_uint32),
    ('type', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

RAnalEsilOp = struct_r_anal_esil_operation_t
class struct_r_anal_esil_expr_offset_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('off', ctypes.c_uint64),
    ('idx', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

RAnalEsilEOffset = struct_r_anal_esil_expr_offset_t

# values for enumeration 'c__EA_RAnalEsilBlockEnterType'
c__EA_RAnalEsilBlockEnterType__enumvalues = {
    0: 'R_ANAL_ESIL_BLOCK_ENTER_NORMAL',
    1: 'R_ANAL_ESIL_BLOCK_ENTER_TRUE',
    2: 'R_ANAL_ESIL_BLOCK_ENTER_FALSE',
    3: 'R_ANAL_ESIL_BLOCK_ENTER_GLUE',
}
R_ANAL_ESIL_BLOCK_ENTER_NORMAL = 0
R_ANAL_ESIL_BLOCK_ENTER_TRUE = 1
R_ANAL_ESIL_BLOCK_ENTER_FALSE = 2
R_ANAL_ESIL_BLOCK_ENTER_GLUE = 3
c__EA_RAnalEsilBlockEnterType = ctypes.c_int # enum
RAnalEsilBlockEnterType = c__EA_RAnalEsilBlockEnterType
RAnalEsilBlockEnterType__enumvalues = c__EA_RAnalEsilBlockEnterType__enumvalues
class struct_r_anal_esil_basic_block_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('first', RAnalEsilEOffset),
    ('last', RAnalEsilEOffset),
    ('expr', POINTER_T(ctypes.c_char)),
    ('enter', RAnalEsilBlockEnterType),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RAnalEsilBB = struct_r_anal_esil_basic_block_t
class struct_r_anal_esil_cfg_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('start', POINTER_T(struct_r_graph_node_t)),
    ('end', POINTER_T(struct_r_graph_node_t)),
    ('g', POINTER_T(struct_r_graph_t)),
     ]

RAnalEsilCFG = struct_r_anal_esil_cfg_t

# values for enumeration 'c__EA_RAnalEsilDFGBlockType'
c__EA_RAnalEsilDFGBlockType__enumvalues = {
    1: 'R_ANAL_ESIL_DFG_BLOCK_CONST',
    2: 'R_ANAL_ESIL_DFG_BLOCK_VAR',
    4: 'R_ANAL_ESIL_DFG_BLOCK_PTR',
    8: 'R_ANAL_ESIL_DFG_BLOCK_RESULT',
    16: 'R_ANAL_ESIL_DFG_BLOCK_GENERATIVE',
}
R_ANAL_ESIL_DFG_BLOCK_CONST = 1
R_ANAL_ESIL_DFG_BLOCK_VAR = 2
R_ANAL_ESIL_DFG_BLOCK_PTR = 4
R_ANAL_ESIL_DFG_BLOCK_RESULT = 8
R_ANAL_ESIL_DFG_BLOCK_GENERATIVE = 16
c__EA_RAnalEsilDFGBlockType = ctypes.c_int # enum
RAnalEsilDFGBlockType = c__EA_RAnalEsilDFGBlockType
RAnalEsilDFGBlockType__enumvalues = c__EA_RAnalEsilDFGBlockType__enumvalues
class struct_r_anal_esil_dfg_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('regs', POINTER_T(struct_sdb_t)),
    ('reg_vars', POINTER_T(struct_r_containing_rb_tree_t)),
    ('todo', POINTER_T(struct_r_queue_t)),
    ('insert', POINTER_T(None)),
    ('flow', POINTER_T(struct_r_graph_t)),
    ('cur', POINTER_T(struct_r_graph_node_t)),
    ('old', POINTER_T(struct_r_graph_node_t)),
    ('malloc_failed', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
     ]

RAnalEsilDFG = struct_r_anal_esil_dfg_t
class struct_r_anal_esil_dfg_node_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('idx', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('content', POINTER_T(struct_c__SA_RStrBuf)),
    ('type', RAnalEsilDFGBlockType),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

RAnalEsilDFGNode = struct_r_anal_esil_dfg_node_t
RAnalCmdExt = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)))
RAnalOpCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, c__EA_RAnalOpMask))
RAnalRegProfCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_t)))
RAnalRegProfGetCallback = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_t)))
RAnalFPBBCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_bb_t)))
RAnalFPFcnCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)))
RAnalDiffBBCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_function_t)))
RAnalDiffFcnCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(struct_r_list_t), POINTER_T(struct_r_list_t)))
RAnalDiffEvalCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t)))
RAnalEsilCB = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t)))
RAnalEsilLoopCB = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_op_t)))
RAnalEsilTrapCB = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_esil_t), ctypes.c_int32, ctypes.c_int32))
RAnalPlugin = struct_r_anal_plugin_t
r_anal_datatype_to_string = _r_anal.r_anal_datatype_to_string
r_anal_datatype_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_datatype_to_string.argtypes = [RAnalDataType]
r_anal_op_nonlinear = _r_anal.r_anal_op_nonlinear
r_anal_op_nonlinear.restype = ctypes.c_bool
r_anal_op_nonlinear.argtypes = [ctypes.c_int32]
r_anal_op_ismemref = _r_anal.r_anal_op_ismemref
r_anal_op_ismemref.restype = ctypes.c_bool
r_anal_op_ismemref.argtypes = [ctypes.c_int32]
r_anal_optype_to_string = _r_anal.r_anal_optype_to_string
r_anal_optype_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_optype_to_string.argtypes = [ctypes.c_int32]
r_anal_optype_from_string = _r_anal.r_anal_optype_from_string
r_anal_optype_from_string.restype = ctypes.c_int32
r_anal_optype_from_string.argtypes = [POINTER_T(ctypes.c_char)]
r_anal_op_family_to_string = _r_anal.r_anal_op_family_to_string
r_anal_op_family_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_op_family_to_string.argtypes = [ctypes.c_int32]
r_anal_op_family_from_string = _r_anal.r_anal_op_family_from_string
r_anal_op_family_from_string.restype = ctypes.c_int32
r_anal_op_family_from_string.argtypes = [POINTER_T(ctypes.c_char)]
r_anal_op_hint = _r_anal.r_anal_op_hint
r_anal_op_hint.restype = ctypes.c_int32
r_anal_op_hint.argtypes = [POINTER_T(struct_r_anal_op_t), POINTER_T(struct_r_anal_hint_t)]
RAnalBlockCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_bb_t), POINTER_T(None)))
RAnalAddrCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint64, POINTER_T(None)))
r_anal_block_ref = _r_anal.r_anal_block_ref
r_anal_block_ref.restype = None
r_anal_block_ref.argtypes = [POINTER_T(struct_r_anal_bb_t)]
r_anal_block_unref = _r_anal.r_anal_block_unref
r_anal_block_unref.restype = None
r_anal_block_unref.argtypes = [POINTER_T(struct_r_anal_bb_t)]
r_anal_create_block = _r_anal.r_anal_create_block
r_anal_create_block.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_create_block.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_block_split = _r_anal.r_anal_block_split
r_anal_block_split.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_block_split.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_block_merge = _r_anal.r_anal_block_merge
r_anal_block_merge.restype = ctypes.c_bool
r_anal_block_merge.argtypes = [POINTER_T(struct_r_anal_bb_t), POINTER_T(struct_r_anal_bb_t)]
r_anal_delete_block = _r_anal.r_anal_delete_block
r_anal_delete_block.restype = None
r_anal_delete_block.argtypes = [POINTER_T(struct_r_anal_bb_t)]
r_anal_block_set_size = _r_anal.r_anal_block_set_size
r_anal_block_set_size.restype = None
r_anal_block_set_size.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_block_relocate = _r_anal.r_anal_block_relocate
r_anal_block_relocate.restype = ctypes.c_bool
r_anal_block_relocate.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_get_block_at = _r_anal.r_anal_get_block_at
r_anal_get_block_at.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_get_block_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_blocks_foreach_in = _r_anal.r_anal_blocks_foreach_in
r_anal_blocks_foreach_in.restype = ctypes.c_bool
r_anal_blocks_foreach_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, RAnalBlockCb, POINTER_T(None)]
r_anal_get_blocks_in = _r_anal.r_anal_get_blocks_in
r_anal_get_blocks_in.restype = POINTER_T(struct_r_list_t)
r_anal_get_blocks_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_blocks_foreach_intersect = _r_anal.r_anal_blocks_foreach_intersect
r_anal_blocks_foreach_intersect.restype = None
r_anal_blocks_foreach_intersect.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64, RAnalBlockCb, POINTER_T(None)]
r_anal_get_blocks_intersect = _r_anal.r_anal_get_blocks_intersect
r_anal_get_blocks_intersect.restype = POINTER_T(struct_r_list_t)
r_anal_get_blocks_intersect.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_block_successor_addrs_foreach = _r_anal.r_anal_block_successor_addrs_foreach
r_anal_block_successor_addrs_foreach.restype = ctypes.c_bool
r_anal_block_successor_addrs_foreach.argtypes = [POINTER_T(struct_r_anal_bb_t), RAnalAddrCb, POINTER_T(None)]
r_anal_block_recurse = _r_anal.r_anal_block_recurse
r_anal_block_recurse.restype = ctypes.c_bool
r_anal_block_recurse.argtypes = [POINTER_T(struct_r_anal_bb_t), RAnalBlockCb, POINTER_T(None)]
r_anal_block_recurse_followthrough = _r_anal.r_anal_block_recurse_followthrough
r_anal_block_recurse_followthrough.restype = ctypes.c_bool
r_anal_block_recurse_followthrough.argtypes = [POINTER_T(struct_r_anal_bb_t), RAnalBlockCb, POINTER_T(None)]
r_anal_block_recurse_depth_first = _r_anal.r_anal_block_recurse_depth_first
r_anal_block_recurse_depth_first.restype = ctypes.c_bool
r_anal_block_recurse_depth_first.argtypes = [POINTER_T(struct_r_anal_bb_t), RAnalBlockCb, RAnalBlockCb, POINTER_T(None)]
r_anal_block_recurse_list = _r_anal.r_anal_block_recurse_list
r_anal_block_recurse_list.restype = POINTER_T(struct_r_list_t)
r_anal_block_recurse_list.argtypes = [POINTER_T(struct_r_anal_bb_t)]
r_anal_block_shortest_path = _r_anal.r_anal_block_shortest_path
r_anal_block_shortest_path.restype = POINTER_T(struct_r_list_t)
r_anal_block_shortest_path.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_block_add_switch_case = _r_anal.r_anal_block_add_switch_case
r_anal_block_add_switch_case.restype = None
r_anal_block_add_switch_case.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_anal_block_chop_noreturn = _r_anal.r_anal_block_chop_noreturn
r_anal_block_chop_noreturn.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_block_chop_noreturn.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_block_automerge = _r_anal.r_anal_block_automerge
r_anal_block_automerge.restype = None
r_anal_block_automerge.argtypes = [POINTER_T(struct_r_list_t)]
r_anal_block_op_starts_at = _r_anal.r_anal_block_op_starts_at
r_anal_block_op_starts_at.restype = ctypes.c_bool
r_anal_block_op_starts_at.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_function_new = _r_anal.r_anal_function_new
r_anal_function_new.restype = POINTER_T(struct_r_anal_function_t)
r_anal_function_new.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_function_free = _r_anal.r_anal_function_free
r_anal_function_free.restype = None
r_anal_function_free.argtypes = [POINTER_T(None)]
r_anal_add_function = _r_anal.r_anal_add_function
r_anal_add_function.restype = ctypes.c_bool
r_anal_add_function.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_create_function = _r_anal.r_anal_create_function
r_anal_create_function.restype = POINTER_T(struct_r_anal_function_t)
r_anal_create_function.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_int32, POINTER_T(struct_r_anal_diff_t)]
r_anal_get_functions_in = _r_anal.r_anal_get_functions_in
r_anal_get_functions_in.restype = POINTER_T(struct_r_list_t)
r_anal_get_functions_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_get_function_at = _r_anal.r_anal_get_function_at
r_anal_get_function_at.restype = POINTER_T(struct_r_anal_function_t)
r_anal_get_function_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_function_delete = _r_anal.r_anal_function_delete
r_anal_function_delete.restype = ctypes.c_bool
r_anal_function_delete.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_relocate = _r_anal.r_anal_function_relocate
r_anal_function_relocate.restype = ctypes.c_bool
r_anal_function_relocate.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_function_rename = _r_anal.r_anal_function_rename
r_anal_function_rename.restype = ctypes.c_bool
r_anal_function_rename.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)]
r_anal_function_add_block = _r_anal.r_anal_function_add_block
r_anal_function_add_block.restype = None
r_anal_function_add_block.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t)]
r_anal_function_remove_block = _r_anal.r_anal_function_remove_block
r_anal_function_remove_block.restype = None
r_anal_function_remove_block.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t)]
r_anal_function_linear_size = _r_anal.r_anal_function_linear_size
r_anal_function_linear_size.restype = ctypes.c_uint64
r_anal_function_linear_size.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_min_addr = _r_anal.r_anal_function_min_addr
r_anal_function_min_addr.restype = ctypes.c_uint64
r_anal_function_min_addr.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_max_addr = _r_anal.r_anal_function_max_addr
r_anal_function_max_addr.restype = ctypes.c_uint64
r_anal_function_max_addr.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_size_from_entry = _r_anal.r_anal_function_size_from_entry
r_anal_function_size_from_entry.restype = ctypes.c_uint64
r_anal_function_size_from_entry.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_realsize = _r_anal.r_anal_function_realsize
r_anal_function_realsize.restype = ctypes.c_uint64
r_anal_function_realsize.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_contains = _r_anal.r_anal_function_contains
r_anal_function_contains.restype = ctypes.c_bool
r_anal_function_contains.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_new = _r_anal.r_anal_new
r_anal_new.restype = POINTER_T(struct_r_anal_t)
r_anal_new.argtypes = []
r_anal_purge = _r_anal.r_anal_purge
r_anal_purge.restype = None
r_anal_purge.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_free = _r_anal.r_anal_free
r_anal_free.restype = POINTER_T(struct_r_anal_t)
r_anal_free.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_set_user_ptr = _r_anal.r_anal_set_user_ptr
r_anal_set_user_ptr.restype = None
r_anal_set_user_ptr.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(None)]
r_anal_plugin_free = _r_anal.r_anal_plugin_free
r_anal_plugin_free.restype = None
r_anal_plugin_free.argtypes = [POINTER_T(struct_r_anal_plugin_t)]
r_anal_add = _r_anal.r_anal_add
r_anal_add.restype = ctypes.c_int32
r_anal_add.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_plugin_t)]
r_anal_archinfo = _r_anal.r_anal_archinfo
r_anal_archinfo.restype = ctypes.c_int32
r_anal_archinfo.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_use = _r_anal.r_anal_use
r_anal_use.restype = ctypes.c_bool
r_anal_use.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_set_reg_profile = _r_anal.r_anal_set_reg_profile
r_anal_set_reg_profile.restype = ctypes.c_bool
r_anal_set_reg_profile.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_get_reg_profile = _r_anal.r_anal_get_reg_profile
r_anal_get_reg_profile.restype = POINTER_T(ctypes.c_char)
r_anal_get_reg_profile.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_get_bbaddr = _r_anal.r_anal_get_bbaddr
r_anal_get_bbaddr.restype = ctypes.c_uint64
r_anal_get_bbaddr.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_set_bits = _r_anal.r_anal_set_bits
r_anal_set_bits.restype = ctypes.c_bool
r_anal_set_bits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_set_os = _r_anal.r_anal_set_os
r_anal_set_os.restype = ctypes.c_bool
r_anal_set_os.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_set_cpu = _r_anal.r_anal_set_cpu
r_anal_set_cpu.restype = None
r_anal_set_cpu.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_set_big_endian = _r_anal.r_anal_set_big_endian
r_anal_set_big_endian.restype = ctypes.c_int32
r_anal_set_big_endian.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_mask = _r_anal.r_anal_mask
r_anal_mask.restype = POINTER_T(ctypes.c_ubyte)
r_anal_mask.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_anal_trace_bb = _r_anal.r_anal_trace_bb
r_anal_trace_bb.restype = None
r_anal_trace_bb.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_fcntype_tostring = _r_anal.r_anal_fcntype_tostring
r_anal_fcntype_tostring.restype = POINTER_T(ctypes.c_char)
r_anal_fcntype_tostring.argtypes = [ctypes.c_int32]
r_anal_fcn_bb = _r_anal.r_anal_fcn_bb
r_anal_fcn_bb.restype = ctypes.c_int32
r_anal_fcn_bb.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_bind = _r_anal.r_anal_bind
r_anal_bind.restype = None
r_anal_bind.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_bind_t)]
r_anal_set_triplet = _r_anal.r_anal_set_triplet
r_anal_set_triplet.restype = ctypes.c_bool
r_anal_set_triplet.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_anal_add_import = _r_anal.r_anal_add_import
r_anal_add_import.restype = None
r_anal_add_import.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_remove_import = _r_anal.r_anal_remove_import
r_anal_remove_import.restype = None
r_anal_remove_import.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_purge_imports = _r_anal.r_anal_purge_imports
r_anal_purge_imports.restype = None
r_anal_purge_imports.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_bb_from_offset = _r_anal.r_anal_bb_from_offset
r_anal_bb_from_offset.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_bb_from_offset.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_bb_set_offset = _r_anal.r_anal_bb_set_offset
r_anal_bb_set_offset.restype = ctypes.c_bool
r_anal_bb_set_offset.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_int32, ctypes.c_uint16]
r_anal_bb_offset_inst = _r_anal.r_anal_bb_offset_inst
r_anal_bb_offset_inst.restype = ctypes.c_uint16
r_anal_bb_offset_inst.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_int32]
r_anal_bb_opaddr_i = _r_anal.r_anal_bb_opaddr_i
r_anal_bb_opaddr_i.restype = ctypes.c_uint64
r_anal_bb_opaddr_i.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_int32]
r_anal_bb_opaddr_at = _r_anal.r_anal_bb_opaddr_at
r_anal_bb_opaddr_at.restype = ctypes.c_uint64
r_anal_bb_opaddr_at.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64]
r_anal_bb_size_i = _r_anal.r_anal_bb_size_i
r_anal_bb_size_i.restype = ctypes.c_uint64
r_anal_bb_size_i.argtypes = [POINTER_T(struct_r_anal_bb_t), ctypes.c_int32]
r_anal_stackop_tostring = _r_anal.r_anal_stackop_tostring
r_anal_stackop_tostring.restype = POINTER_T(ctypes.c_char)
r_anal_stackop_tostring.argtypes = [ctypes.c_int32]
r_anal_op_new = _r_anal.r_anal_op_new
r_anal_op_new.restype = POINTER_T(struct_r_anal_op_t)
r_anal_op_new.argtypes = []
r_anal_op_free = _r_anal.r_anal_op_free
r_anal_op_free.restype = None
r_anal_op_free.argtypes = [POINTER_T(None)]
r_anal_op_init = _r_anal.r_anal_op_init
r_anal_op_init.restype = None
r_anal_op_init.argtypes = [POINTER_T(struct_r_anal_op_t)]
r_anal_op_fini = _r_anal.r_anal_op_fini
r_anal_op_fini.restype = ctypes.c_bool
r_anal_op_fini.argtypes = [POINTER_T(struct_r_anal_op_t)]
r_anal_op_reg_delta = _r_anal.r_anal_op_reg_delta
r_anal_op_reg_delta.restype = ctypes.c_int32
r_anal_op_reg_delta.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_op_is_eob = _r_anal.r_anal_op_is_eob
r_anal_op_is_eob.restype = ctypes.c_bool
r_anal_op_is_eob.argtypes = [POINTER_T(struct_r_anal_op_t)]
r_anal_op_list_new = _r_anal.r_anal_op_list_new
r_anal_op_list_new.restype = POINTER_T(struct_r_list_t)
r_anal_op_list_new.argtypes = []
r_anal_op = _r_anal.r_anal_op
r_anal_op.restype = ctypes.c_int32
r_anal_op.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, RAnalOpMask]
r_anal_op_hexstr = _r_anal.r_anal_op_hexstr
r_anal_op_hexstr.restype = POINTER_T(struct_r_anal_op_t)
r_anal_op_hexstr.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_op_to_string = _r_anal.r_anal_op_to_string
r_anal_op_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_op_to_string.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t)]
r_anal_esil_new = _r_anal.r_anal_esil_new
r_anal_esil_new.restype = POINTER_T(struct_r_anal_esil_t)
r_anal_esil_new.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_uint32]
r_anal_esil_set_pc = _r_anal.r_anal_esil_set_pc
r_anal_esil_set_pc.restype = ctypes.c_bool
r_anal_esil_set_pc.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64]
r_anal_esil_setup = _r_anal.r_anal_esil_setup
r_anal_esil_setup.restype = ctypes.c_bool
r_anal_esil_setup.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_anal_esil_free = _r_anal.r_anal_esil_free
r_anal_esil_free.restype = None
r_anal_esil_free.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_runword = _r_anal.r_anal_esil_runword
r_anal_esil_runword.restype = ctypes.c_bool
r_anal_esil_runword.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_parse = _r_anal.r_anal_esil_parse
r_anal_esil_parse.restype = ctypes.c_bool
r_anal_esil_parse.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_dumpstack = _r_anal.r_anal_esil_dumpstack
r_anal_esil_dumpstack.restype = ctypes.c_bool
r_anal_esil_dumpstack.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_mem_read = _r_anal.r_anal_esil_mem_read
r_anal_esil_mem_read.restype = ctypes.c_int32
r_anal_esil_mem_read.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_anal_esil_mem_write = _r_anal.r_anal_esil_mem_write
r_anal_esil_mem_write.restype = ctypes.c_int32
r_anal_esil_mem_write.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_anal_esil_reg_read = _r_anal.r_anal_esil_reg_read
r_anal_esil_reg_read.restype = ctypes.c_int32
r_anal_esil_reg_read.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64), POINTER_T(ctypes.c_int32)]
r_anal_esil_reg_write = _r_anal.r_anal_esil_reg_write
r_anal_esil_reg_write.restype = ctypes.c_int32
r_anal_esil_reg_write.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_anal_esil_pushnum = _r_anal.r_anal_esil_pushnum
r_anal_esil_pushnum.restype = ctypes.c_bool
r_anal_esil_pushnum.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint64]
r_anal_esil_push = _r_anal.r_anal_esil_push
r_anal_esil_push.restype = ctypes.c_bool
r_anal_esil_push.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_pop = _r_anal.r_anal_esil_pop
r_anal_esil_pop.restype = POINTER_T(ctypes.c_char)
r_anal_esil_pop.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_set_op = _r_anal.r_anal_esil_set_op
r_anal_esil_set_op.restype = ctypes.c_bool
r_anal_esil_set_op.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), RAnalEsilOpCb, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]
r_anal_esil_stack_free = _r_anal.r_anal_esil_stack_free
r_anal_esil_stack_free.restype = None
r_anal_esil_stack_free.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_get_parm_type = _r_anal.r_anal_esil_get_parm_type
r_anal_esil_get_parm_type.restype = ctypes.c_int32
r_anal_esil_get_parm_type.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_get_parm = _r_anal.r_anal_esil_get_parm
r_anal_esil_get_parm.restype = ctypes.c_int32
r_anal_esil_get_parm.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64)]
r_anal_esil_condition = _r_anal.r_anal_esil_condition
r_anal_esil_condition.restype = ctypes.c_int32
r_anal_esil_condition.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_interrupts_init = _r_anal.r_anal_esil_interrupts_init
r_anal_esil_interrupts_init.restype = None
r_anal_esil_interrupts_init.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_interrupt_new = _r_anal.r_anal_esil_interrupt_new
r_anal_esil_interrupt_new.restype = POINTER_T(struct_r_anal_esil_interrupt_t)
r_anal_esil_interrupt_new.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32, POINTER_T(struct_r_anal_esil_interrupt_handler_t)]
r_anal_esil_interrupt_free = _r_anal.r_anal_esil_interrupt_free
r_anal_esil_interrupt_free.restype = None
r_anal_esil_interrupt_free.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_esil_interrupt_t)]
r_anal_esil_set_interrupt = _r_anal.r_anal_esil_set_interrupt
r_anal_esil_set_interrupt.restype = ctypes.c_bool
r_anal_esil_set_interrupt.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_esil_interrupt_t)]
r_anal_esil_fire_interrupt = _r_anal.r_anal_esil_fire_interrupt
r_anal_esil_fire_interrupt.restype = ctypes.c_int32
r_anal_esil_fire_interrupt.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_uint32]
r_anal_esil_load_interrupts = _r_anal.r_anal_esil_load_interrupts
r_anal_esil_load_interrupts.restype = ctypes.c_bool
r_anal_esil_load_interrupts.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(POINTER_T(struct_r_anal_esil_interrupt_handler_t)), ctypes.c_uint32]
r_anal_esil_load_interrupts_from_lib = _r_anal.r_anal_esil_load_interrupts_from_lib
r_anal_esil_load_interrupts_from_lib.restype = ctypes.c_bool
r_anal_esil_load_interrupts_from_lib.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char)]
r_anal_esil_interrupts_fini = _r_anal.r_anal_esil_interrupts_fini
r_anal_esil_interrupts_fini.restype = None
r_anal_esil_interrupts_fini.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_mem_ro = _r_anal.r_anal_esil_mem_ro
r_anal_esil_mem_ro.restype = None
r_anal_esil_mem_ro.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_int32]
r_anal_esil_stats = _r_anal.r_anal_esil_stats
r_anal_esil_stats.restype = None
r_anal_esil_stats.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_int32]
r_anal_esil_trace_new = _r_anal.r_anal_esil_trace_new
r_anal_esil_trace_new.restype = POINTER_T(struct_r_anal_esil_trace_t)
r_anal_esil_trace_new.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_trace_free = _r_anal.r_anal_esil_trace_free
r_anal_esil_trace_free.restype = None
r_anal_esil_trace_free.argtypes = [POINTER_T(struct_r_anal_esil_trace_t)]
r_anal_esil_trace_op = _r_anal.r_anal_esil_trace_op
r_anal_esil_trace_op.restype = None
r_anal_esil_trace_op.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_op_t)]
r_anal_esil_trace_list = _r_anal.r_anal_esil_trace_list
r_anal_esil_trace_list.restype = None
r_anal_esil_trace_list.argtypes = [POINTER_T(struct_r_anal_esil_t)]
r_anal_esil_trace_show = _r_anal.r_anal_esil_trace_show
r_anal_esil_trace_show.restype = None
r_anal_esil_trace_show.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_int32]
r_anal_esil_trace_restore = _r_anal.r_anal_esil_trace_restore
r_anal_esil_trace_restore.restype = None
r_anal_esil_trace_restore.argtypes = [POINTER_T(struct_r_anal_esil_t), ctypes.c_int32]
r_anal_pin_init = _r_anal.r_anal_pin_init
r_anal_pin_init.restype = None
r_anal_pin_init.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_pin_fini = _r_anal.r_anal_pin_fini
r_anal_pin_fini.restype = None
r_anal_pin_fini.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_pin = _r_anal.r_anal_pin
r_anal_pin.restype = None
r_anal_pin.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_pin_unset = _r_anal.r_anal_pin_unset
r_anal_pin_unset.restype = None
r_anal_pin_unset.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_pin_call = _r_anal.r_anal_pin_call
r_anal_pin_call.restype = POINTER_T(ctypes.c_char)
r_anal_pin_call.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_pin_list = _r_anal.r_anal_pin_list
r_anal_pin_list.restype = None
r_anal_pin_list.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_function_cost = _r_anal.r_anal_function_cost
r_anal_function_cost.restype = ctypes.c_uint32
r_anal_function_cost.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_count_edges = _r_anal.r_anal_function_count_edges
r_anal_function_count_edges.restype = ctypes.c_int32
r_anal_function_count_edges.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_int32)]
r_anal_get_fcn_in = _r_anal.r_anal_get_fcn_in
r_anal_get_fcn_in.restype = POINTER_T(struct_r_anal_function_t)
r_anal_get_fcn_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_get_fcn_in_bounds = _r_anal.r_anal_get_fcn_in_bounds
r_anal_get_fcn_in_bounds.restype = POINTER_T(struct_r_anal_function_t)
r_anal_get_fcn_in_bounds.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_get_function_byname = _r_anal.r_anal_get_function_byname
r_anal_get_function_byname.restype = POINTER_T(struct_r_anal_function_t)
r_anal_get_function_byname.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_fcn = _r_anal.r_anal_fcn
r_anal_fcn.restype = ctypes.c_int32
r_anal_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_anal_fcn_del = _r_anal.r_anal_fcn_del
r_anal_fcn_del.restype = ctypes.c_int32
r_anal_fcn_del.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_fcn_del_locs = _r_anal.r_anal_fcn_del_locs
r_anal_fcn_del_locs.restype = ctypes.c_int32
r_anal_fcn_del_locs.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_fcn_add_bb = _r_anal.r_anal_fcn_add_bb
r_anal_fcn_add_bb.restype = ctypes.c_bool
r_anal_fcn_add_bb.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, POINTER_T(struct_r_anal_diff_t)]
r_anal_check_fcn = _r_anal.r_anal_check_fcn
r_anal_check_fcn.restype = ctypes.c_bool
r_anal_check_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_ubyte), ctypes.c_uint16, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_anal_fcn_invalidate_read_ahead_cache = _r_anal.r_anal_fcn_invalidate_read_ahead_cache
r_anal_fcn_invalidate_read_ahead_cache.restype = None
r_anal_fcn_invalidate_read_ahead_cache.argtypes = []
r_anal_function_check_bp_use = _r_anal.r_anal_function_check_bp_use
r_anal_function_check_bp_use.restype = None
r_anal_function_check_bp_use.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_var_count = _r_anal.r_anal_var_count
r_anal_var_count.restype = ctypes.c_int32
r_anal_var_count.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_int32, ctypes.c_int32]
r_anal_var_display = _r_anal.r_anal_var_display
r_anal_var_display.restype = ctypes.c_bool
r_anal_var_display.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_var_t)]
r_anal_function_complexity = _r_anal.r_anal_function_complexity
r_anal_function_complexity.restype = ctypes.c_int32
r_anal_function_complexity.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_loops = _r_anal.r_anal_function_loops
r_anal_function_loops.restype = ctypes.c_int32
r_anal_function_loops.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_trim_jmprefs = _r_anal.r_anal_trim_jmprefs
r_anal_trim_jmprefs.restype = None
r_anal_trim_jmprefs.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_del_jmprefs = _r_anal.r_anal_del_jmprefs
r_anal_del_jmprefs.restype = None
r_anal_del_jmprefs.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_function_get_json = _r_anal.r_anal_function_get_json
r_anal_function_get_json.restype = POINTER_T(ctypes.c_char)
r_anal_function_get_json.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_fcn_next = _r_anal.r_anal_fcn_next
r_anal_fcn_next.restype = POINTER_T(struct_r_anal_function_t)
r_anal_fcn_next.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_function_get_signature = _r_anal.r_anal_function_get_signature
r_anal_function_get_signature.restype = POINTER_T(ctypes.c_char)
r_anal_function_get_signature.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_str_to_fcn = _r_anal.r_anal_str_to_fcn
r_anal_str_to_fcn.restype = ctypes.c_int32
r_anal_str_to_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)]
r_anal_fcn_count = _r_anal.r_anal_fcn_count
r_anal_fcn_count.restype = ctypes.c_int32
r_anal_fcn_count.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_fcn_bbget_in = _r_anal.r_anal_fcn_bbget_in
r_anal_fcn_bbget_in.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_fcn_bbget_in.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_fcn_bbget_at = _r_anal.r_anal_fcn_bbget_at
r_anal_fcn_bbget_at.restype = POINTER_T(struct_r_anal_bb_t)
r_anal_fcn_bbget_at.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_function_resize = _r_anal.r_anal_function_resize
r_anal_function_resize.restype = ctypes.c_int32
r_anal_function_resize.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_int32]
r_anal_function_purity = _r_anal.r_anal_function_purity
r_anal_function_purity.restype = ctypes.c_bool
r_anal_function_purity.argtypes = [POINTER_T(struct_r_anal_function_t)]
RAnalRefCmp = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_ref_t), POINTER_T(None)))
r_anal_ref_list_new = _r_anal.r_anal_ref_list_new
r_anal_ref_list_new.restype = POINTER_T(struct_r_list_t)
r_anal_ref_list_new.argtypes = []
r_anal_xrefs_count = _r_anal.r_anal_xrefs_count
r_anal_xrefs_count.restype = ctypes.c_uint64
r_anal_xrefs_count.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_xrefs_type_tostring = _r_anal.r_anal_xrefs_type_tostring
r_anal_xrefs_type_tostring.restype = POINTER_T(ctypes.c_char)
r_anal_xrefs_type_tostring.argtypes = [RAnalRefType]
r_anal_xrefs_type = _r_anal.r_anal_xrefs_type
r_anal_xrefs_type.restype = RAnalRefType
r_anal_xrefs_type.argtypes = [ctypes.c_char]
r_anal_xrefs_get = _r_anal.r_anal_xrefs_get
r_anal_xrefs_get.restype = POINTER_T(struct_r_list_t)
r_anal_xrefs_get.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_refs_get = _r_anal.r_anal_refs_get
r_anal_refs_get.restype = POINTER_T(struct_r_list_t)
r_anal_refs_get.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_xrefs_get_from = _r_anal.r_anal_xrefs_get_from
r_anal_xrefs_get_from.restype = POINTER_T(struct_r_list_t)
r_anal_xrefs_get_from.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_xrefs_list = _r_anal.r_anal_xrefs_list
r_anal_xrefs_list.restype = None
r_anal_xrefs_list.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_function_get_refs = _r_anal.r_anal_function_get_refs
r_anal_function_get_refs.restype = POINTER_T(struct_r_list_t)
r_anal_function_get_refs.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_get_xrefs = _r_anal.r_anal_function_get_xrefs
r_anal_function_get_xrefs.restype = POINTER_T(struct_r_list_t)
r_anal_function_get_xrefs.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_xrefs_from = _r_anal.r_anal_xrefs_from
r_anal_xrefs_from.restype = ctypes.c_int32
r_anal_xrefs_from.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_list_t), POINTER_T(ctypes.c_char), RAnalRefType, ctypes.c_uint64]
r_anal_xrefs_set = _r_anal.r_anal_xrefs_set
r_anal_xrefs_set.restype = ctypes.c_int32
r_anal_xrefs_set.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64, RAnalRefType]
r_anal_xrefs_deln = _r_anal.r_anal_xrefs_deln
r_anal_xrefs_deln.restype = ctypes.c_int32
r_anal_xrefs_deln.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64, RAnalRefType]
r_anal_xref_del = _r_anal.r_anal_xref_del
r_anal_xref_del.restype = ctypes.c_int32
r_anal_xref_del.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_get_fcns = _r_anal.r_anal_get_fcns
r_anal_get_fcns.restype = POINTER_T(struct_r_list_t)
r_anal_get_fcns.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_remove_parsed_type = _r_anal.r_anal_remove_parsed_type
r_anal_remove_parsed_type.restype = None
r_anal_remove_parsed_type.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_save_parsed_type = _r_anal.r_anal_save_parsed_type
r_anal_save_parsed_type.restype = None
r_anal_save_parsed_type.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_function_autoname_var = _r_anal.r_anal_function_autoname_var
r_anal_function_autoname_var.restype = POINTER_T(ctypes.c_char)
r_anal_function_autoname_var.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_char, POINTER_T(ctypes.c_char), ctypes.c_int32]
r_anal_function_set_var = _r_anal.r_anal_function_set_var
r_anal_function_set_var.restype = POINTER_T(struct_r_anal_var_t)
r_anal_function_set_var.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_int32, ctypes.c_char, POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_bool, POINTER_T(ctypes.c_char)]
r_anal_function_get_var = _r_anal.r_anal_function_get_var
r_anal_function_get_var.restype = POINTER_T(struct_r_anal_var_t)
r_anal_function_get_var.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_char, ctypes.c_int32]
r_anal_function_get_var_byname = _r_anal.r_anal_function_get_var_byname
r_anal_function_get_var_byname.restype = POINTER_T(struct_r_anal_var_t)
r_anal_function_get_var_byname.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)]
r_anal_function_delete_vars_by_kind = _r_anal.r_anal_function_delete_vars_by_kind
r_anal_function_delete_vars_by_kind.restype = None
r_anal_function_delete_vars_by_kind.argtypes = [POINTER_T(struct_r_anal_function_t), RAnalVarKind]
r_anal_function_delete_all_vars = _r_anal.r_anal_function_delete_all_vars
r_anal_function_delete_all_vars.restype = None
r_anal_function_delete_all_vars.argtypes = [POINTER_T(struct_r_anal_function_t)]
r_anal_function_delete_var = _r_anal.r_anal_function_delete_var
r_anal_function_delete_var.restype = None
r_anal_function_delete_var.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_var_t)]
r_anal_function_rebase_vars = _r_anal.r_anal_function_rebase_vars
r_anal_function_rebase_vars.restype = ctypes.c_bool
r_anal_function_rebase_vars.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_function_get_var_stackptr_at = _r_anal.r_anal_function_get_var_stackptr_at
r_anal_function_get_var_stackptr_at.restype = ctypes.c_int64
r_anal_function_get_var_stackptr_at.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_int64, ctypes.c_uint64]
r_anal_function_get_var_reg_at = _r_anal.r_anal_function_get_var_reg_at
r_anal_function_get_var_reg_at.restype = POINTER_T(ctypes.c_char)
r_anal_function_get_var_reg_at.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_int64, ctypes.c_uint64]
r_anal_function_get_vars_used_at = _r_anal.r_anal_function_get_vars_used_at
r_anal_function_get_vars_used_at.restype = POINTER_T(struct_r_pvector_t)
r_anal_function_get_vars_used_at.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_get_used_function_var = _r_anal.r_anal_get_used_function_var
r_anal_get_used_function_var.restype = POINTER_T(struct_r_anal_var_t)
r_anal_get_used_function_var.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_var_rename = _r_anal.r_anal_var_rename
r_anal_var_rename.restype = ctypes.c_bool
r_anal_var_rename.argtypes = [POINTER_T(struct_r_anal_var_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_anal_var_set_type = _r_anal.r_anal_var_set_type
r_anal_var_set_type.restype = None
r_anal_var_set_type.argtypes = [POINTER_T(struct_r_anal_var_t), POINTER_T(ctypes.c_char)]
r_anal_var_delete = _r_anal.r_anal_var_delete
r_anal_var_delete.restype = None
r_anal_var_delete.argtypes = [POINTER_T(struct_r_anal_var_t)]
r_anal_var_addr = _r_anal.r_anal_var_addr
r_anal_var_addr.restype = ctypes.c_uint64
r_anal_var_addr.argtypes = [POINTER_T(struct_r_anal_var_t)]
r_anal_var_set_access = _r_anal.r_anal_var_set_access
r_anal_var_set_access.restype = None
r_anal_var_set_access.argtypes = [POINTER_T(struct_r_anal_var_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int64]
r_anal_var_remove_access_at = _r_anal.r_anal_var_remove_access_at
r_anal_var_remove_access_at.restype = None
r_anal_var_remove_access_at.argtypes = [POINTER_T(struct_r_anal_var_t), ctypes.c_uint64]
r_anal_var_clear_accesses = _r_anal.r_anal_var_clear_accesses
r_anal_var_clear_accesses.restype = None
r_anal_var_clear_accesses.argtypes = [POINTER_T(struct_r_anal_var_t)]
r_anal_var_add_constraint = _r_anal.r_anal_var_add_constraint
r_anal_var_add_constraint.restype = None
r_anal_var_add_constraint.argtypes = [POINTER_T(struct_r_anal_var_t), POINTER_T(struct_r_anal_var_constraint_t)]
r_anal_var_get_constraints_readable = _r_anal.r_anal_var_get_constraints_readable
r_anal_var_get_constraints_readable.restype = POINTER_T(ctypes.c_char)
r_anal_var_get_constraints_readable.argtypes = [POINTER_T(struct_r_anal_var_t)]
r_anal_var_get_access_at = _r_anal.r_anal_var_get_access_at
r_anal_var_get_access_at.restype = POINTER_T(struct_r_anal_var_access_t)
r_anal_var_get_access_at.argtypes = [POINTER_T(struct_r_anal_var_t), ctypes.c_uint64]
r_anal_var_get_argnum = _r_anal.r_anal_var_get_argnum
r_anal_var_get_argnum.restype = ctypes.c_int32
r_anal_var_get_argnum.argtypes = [POINTER_T(struct_r_anal_var_t)]
r_anal_extract_vars = _r_anal.r_anal_extract_vars
r_anal_extract_vars.restype = None
r_anal_extract_vars.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_op_t)]
r_anal_extract_rarg = _r_anal.r_anal_extract_rarg
r_anal_extract_rarg.restype = None
r_anal_extract_rarg.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_int32), POINTER_T(ctypes.c_int32)]
r_anal_var_get_dst_var = _r_anal.r_anal_var_get_dst_var
r_anal_var_get_dst_var.restype = POINTER_T(struct_r_anal_var_t)
r_anal_var_get_dst_var.argtypes = [POINTER_T(struct_r_anal_var_t)]
class struct_r_anal_fcn_vars_cache(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bvars', POINTER_T(struct_r_list_t)),
    ('rvars', POINTER_T(struct_r_list_t)),
    ('svars', POINTER_T(struct_r_list_t)),
     ]

RAnalFcnVarsCache = struct_r_anal_fcn_vars_cache
r_anal_fcn_vars_cache_init = _r_anal.r_anal_fcn_vars_cache_init
r_anal_fcn_vars_cache_init.restype = None
r_anal_fcn_vars_cache_init.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_fcn_vars_cache), POINTER_T(struct_r_anal_function_t)]
r_anal_fcn_vars_cache_fini = _r_anal.r_anal_fcn_vars_cache_fini
r_anal_fcn_vars_cache_fini.restype = None
r_anal_fcn_vars_cache_fini.argtypes = [POINTER_T(struct_r_anal_fcn_vars_cache)]
r_anal_fcn_format_sig = _r_anal.r_anal_fcn_format_sig
r_anal_fcn_format_sig.restype = POINTER_T(ctypes.c_char)
r_anal_fcn_format_sig.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_fcn_vars_cache), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_xrefs_init = _r_anal.r_anal_xrefs_init
r_anal_xrefs_init.restype = ctypes.c_bool
r_anal_xrefs_init.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_diff_new = _r_anal.r_anal_diff_new
r_anal_diff_new.restype = POINTER_T(struct_r_anal_diff_t)
r_anal_diff_new.argtypes = []
r_anal_diff_setup = _r_anal.r_anal_diff_setup
r_anal_diff_setup.restype = None
r_anal_diff_setup.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_double, ctypes.c_double]
r_anal_diff_setup_i = _r_anal.r_anal_diff_setup_i
r_anal_diff_setup_i.restype = None
r_anal_diff_setup_i.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_anal_diff_free = _r_anal.r_anal_diff_free
r_anal_diff_free.restype = POINTER_T(None)
r_anal_diff_free.argtypes = [POINTER_T(struct_r_anal_diff_t)]
r_anal_diff_fingerprint_bb = _r_anal.r_anal_diff_fingerprint_bb
r_anal_diff_fingerprint_bb.restype = ctypes.c_int32
r_anal_diff_fingerprint_bb.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_bb_t)]
r_anal_diff_fingerprint_fcn = _r_anal.r_anal_diff_fingerprint_fcn
r_anal_diff_fingerprint_fcn.restype = size_t
r_anal_diff_fingerprint_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_diff_bb = _r_anal.r_anal_diff_bb
r_anal_diff_bb.restype = ctypes.c_bool
r_anal_diff_bb.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_function_t)]
r_anal_diff_fcn = _r_anal.r_anal_diff_fcn
r_anal_diff_fcn.restype = ctypes.c_int32
r_anal_diff_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_list_t), POINTER_T(struct_r_list_t)]
r_anal_diff_eval = _r_anal.r_anal_diff_eval
r_anal_diff_eval.restype = ctypes.c_int32
r_anal_diff_eval.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_value_new = _r_anal.r_anal_value_new
r_anal_value_new.restype = POINTER_T(struct_r_anal_value_t)
r_anal_value_new.argtypes = []
r_anal_value_copy = _r_anal.r_anal_value_copy
r_anal_value_copy.restype = POINTER_T(struct_r_anal_value_t)
r_anal_value_copy.argtypes = [POINTER_T(struct_r_anal_value_t)]
r_anal_value_new_from_string = _r_anal.r_anal_value_new_from_string
r_anal_value_new_from_string.restype = POINTER_T(struct_r_anal_value_t)
r_anal_value_new_from_string.argtypes = [POINTER_T(ctypes.c_char)]
r_anal_value_to_string = _r_anal.r_anal_value_to_string
r_anal_value_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_value_to_string.argtypes = [POINTER_T(struct_r_anal_value_t)]
r_anal_value_to_ut64 = _r_anal.r_anal_value_to_ut64
r_anal_value_to_ut64.restype = ctypes.c_uint64
r_anal_value_to_ut64.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_value_t)]
r_anal_value_set_ut64 = _r_anal.r_anal_value_set_ut64
r_anal_value_set_ut64.restype = ctypes.c_int32
r_anal_value_set_ut64.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_value_t), ctypes.c_uint64]
r_anal_value_free = _r_anal.r_anal_value_free
r_anal_value_free.restype = None
r_anal_value_free.argtypes = [POINTER_T(struct_r_anal_value_t)]
r_anal_cond_new = _r_anal.r_anal_cond_new
r_anal_cond_new.restype = POINTER_T(struct_r_anal_cond_t)
r_anal_cond_new.argtypes = []
r_anal_cond_new_from_op = _r_anal.r_anal_cond_new_from_op
r_anal_cond_new_from_op.restype = POINTER_T(struct_r_anal_cond_t)
r_anal_cond_new_from_op.argtypes = [POINTER_T(struct_r_anal_op_t)]
r_anal_cond_fini = _r_anal.r_anal_cond_fini
r_anal_cond_fini.restype = None
r_anal_cond_fini.argtypes = [POINTER_T(struct_r_anal_cond_t)]
r_anal_cond_free = _r_anal.r_anal_cond_free
r_anal_cond_free.restype = None
r_anal_cond_free.argtypes = [POINTER_T(struct_r_anal_cond_t)]
r_anal_cond_to_string = _r_anal.r_anal_cond_to_string
r_anal_cond_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_cond_to_string.argtypes = [POINTER_T(struct_r_anal_cond_t)]
r_anal_cond_eval = _r_anal.r_anal_cond_eval
r_anal_cond_eval.restype = ctypes.c_int32
r_anal_cond_eval.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_cond_t)]
r_anal_cond_new_from_string = _r_anal.r_anal_cond_new_from_string
r_anal_cond_new_from_string.restype = POINTER_T(struct_r_anal_cond_t)
r_anal_cond_new_from_string.argtypes = [POINTER_T(ctypes.c_char)]
r_anal_cond_tostring = _r_anal.r_anal_cond_tostring
r_anal_cond_tostring.restype = POINTER_T(ctypes.c_char)
r_anal_cond_tostring.argtypes = [ctypes.c_int32]
r_anal_jmptbl = _r_anal.r_anal_jmptbl
r_anal_jmptbl.restype = ctypes.c_bool
r_anal_jmptbl.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
try_get_delta_jmptbl_info = _r_anal.try_get_delta_jmptbl_info
try_get_delta_jmptbl_info.restype = ctypes.c_bool
try_get_delta_jmptbl_info.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, ctypes.c_uint64, POINTER_T(ctypes.c_uint64), POINTER_T(ctypes.c_uint64)]
try_walkthrough_jmptbl = _r_anal.try_walkthrough_jmptbl
try_walkthrough_jmptbl.restype = ctypes.c_bool
try_walkthrough_jmptbl.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_bool]
try_walkthrough_casetbl = _r_anal.try_walkthrough_casetbl
try_walkthrough_casetbl.restype = ctypes.c_bool
try_walkthrough_casetbl.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_bool]
try_get_jmptbl_info = _r_anal.try_get_jmptbl_info
try_get_jmptbl_info.restype = ctypes.c_bool
try_get_jmptbl_info.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_uint64, POINTER_T(struct_r_anal_bb_t), POINTER_T(ctypes.c_uint64), POINTER_T(ctypes.c_uint64)]
walkthrough_arm_jmptbl_style = _r_anal.walkthrough_arm_jmptbl_style
walkthrough_arm_jmptbl_style.restype = ctypes.c_int32
walkthrough_arm_jmptbl_style.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_anal_reflines_get = _r_anal.r_anal_reflines_get
r_anal_reflines_get.restype = POINTER_T(struct_r_list_t)
r_anal_reflines_get.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_anal_reflines_middle = _r_anal.r_anal_reflines_middle
r_anal_reflines_middle.restype = ctypes.c_int32
r_anal_reflines_middle.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_list_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_reflines_str = _r_anal.r_anal_reflines_str
r_anal_reflines_str.restype = POINTER_T(struct_r_anal_ref_char)
r_anal_reflines_str.argtypes = [POINTER_T(None), ctypes.c_uint64, ctypes.c_int32]
r_anal_reflines_str_free = _r_anal.r_anal_reflines_str_free
r_anal_reflines_str_free.restype = None
r_anal_reflines_str_free.argtypes = [POINTER_T(struct_r_anal_ref_char)]
r_anal_var_list_show = _r_anal.r_anal_var_list_show
r_anal_var_list_show.restype = None
r_anal_var_list_show.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_pj_t)]
r_anal_var_list = _r_anal.r_anal_var_list
r_anal_var_list.restype = POINTER_T(struct_r_list_t)
r_anal_var_list.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t), ctypes.c_int32]
r_anal_var_all_list = _r_anal.r_anal_var_all_list
r_anal_var_all_list.restype = POINTER_T(struct_r_list_t)
r_anal_var_all_list.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_function_get_var_fields = _r_anal.r_anal_function_get_var_fields
r_anal_function_get_var_fields.restype = POINTER_T(struct_r_list_t)
r_anal_function_get_var_fields.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_int32]
r_anal_cc_exist = _r_anal.r_anal_cc_exist
r_anal_cc_exist.restype = ctypes.c_bool
r_anal_cc_exist.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_del = _r_anal.r_anal_cc_del
r_anal_cc_del.restype = None
r_anal_cc_del.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_set = _r_anal.r_anal_cc_set
r_anal_cc_set.restype = ctypes.c_bool
r_anal_cc_set.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_get = _r_anal.r_anal_cc_get
r_anal_cc_get.restype = POINTER_T(ctypes.c_char)
r_anal_cc_get.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_arg = _r_anal.r_anal_cc_arg
r_anal_cc_arg.restype = POINTER_T(ctypes.c_char)
r_anal_cc_arg.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_anal_cc_self = _r_anal.r_anal_cc_self
r_anal_cc_self.restype = POINTER_T(ctypes.c_char)
r_anal_cc_self.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_error = _r_anal.r_anal_cc_error
r_anal_cc_error.restype = POINTER_T(ctypes.c_char)
r_anal_cc_error.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_max_arg = _r_anal.r_anal_cc_max_arg
r_anal_cc_max_arg.restype = ctypes.c_int32
r_anal_cc_max_arg.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_ret = _r_anal.r_anal_cc_ret
r_anal_cc_ret.restype = POINTER_T(ctypes.c_char)
r_anal_cc_ret.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_cc_default = _r_anal.r_anal_cc_default
r_anal_cc_default.restype = POINTER_T(ctypes.c_char)
r_anal_cc_default.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_cc_func = _r_anal.r_anal_cc_func
r_anal_cc_func.restype = POINTER_T(ctypes.c_char)
r_anal_cc_func.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_noreturn_at = _r_anal.r_anal_noreturn_at
r_anal_noreturn_at.restype = ctypes.c_bool
r_anal_noreturn_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
class struct_r_anal_data_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('type', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ptr', ctypes.c_uint64),
    ('str', POINTER_T(ctypes.c_char)),
    ('len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('sbuf', ctypes.c_ubyte * 8),
     ]

RAnalData = struct_r_anal_data_t
r_anal_data = _r_anal.r_anal_data
r_anal_data.restype = POINTER_T(struct_r_anal_data_t)
r_anal_data.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32]
r_anal_data_kind = _r_anal.r_anal_data_kind
r_anal_data_kind.restype = POINTER_T(ctypes.c_char)
r_anal_data_kind.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_anal_data_new_string = _r_anal.r_anal_data_new_string
r_anal_data_new_string.restype = POINTER_T(struct_r_anal_data_t)
r_anal_data_new_string.argtypes = [ctypes.c_uint64, POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_anal_data_new = _r_anal.r_anal_data_new
r_anal_data_new.restype = POINTER_T(struct_r_anal_data_t)
r_anal_data_new.argtypes = [ctypes.c_uint64, ctypes.c_int32, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_anal_data_free = _r_anal.r_anal_data_free
r_anal_data_free.restype = None
r_anal_data_free.argtypes = [POINTER_T(struct_r_anal_data_t)]
r_anal_data_to_string = _r_anal.r_anal_data_to_string
r_anal_data_to_string.restype = POINTER_T(ctypes.c_char)
r_anal_data_to_string.argtypes = [POINTER_T(struct_r_anal_data_t), POINTER_T(struct_r_cons_printable_palette_t)]
r_meta_set = _r_anal.r_meta_set
r_meta_set.restype = ctypes.c_bool
r_meta_set.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType, ctypes.c_uint64, ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_meta_set_with_subtype = _r_anal.r_meta_set_with_subtype
r_meta_set_with_subtype.restype = ctypes.c_bool
r_meta_set_with_subtype.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType, ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_meta_del = _r_anal.r_meta_del
r_meta_del.restype = None
r_meta_del.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType, ctypes.c_uint64, ctypes.c_uint64]
r_meta_set_string = _r_anal.r_meta_set_string
r_meta_set_string.restype = ctypes.c_bool
r_meta_set_string.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType, ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_meta_get_string = _r_anal.r_meta_get_string
r_meta_get_string.restype = POINTER_T(ctypes.c_char)
r_meta_get_string.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType, ctypes.c_uint64]
r_meta_set_data_at = _r_anal.r_meta_set_data_at
r_meta_set_data_at.restype = None
r_meta_set_data_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_meta_get_at = _r_anal.r_meta_get_at
r_meta_get_at.restype = POINTER_T(struct_r_anal_meta_item_t)
r_meta_get_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, RAnalMetaType, POINTER_T(ctypes.c_uint64)]
r_meta_get_in = _r_anal.r_meta_get_in
r_meta_get_in.restype = POINTER_T(struct_r_interval_node_t)
r_meta_get_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, RAnalMetaType]
r_meta_get_all_at = _r_anal.r_meta_get_all_at
r_meta_get_all_at.restype = POINTER_T(struct_r_pvector_t)
r_meta_get_all_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_meta_get_all_in = _r_anal.r_meta_get_all_in
r_meta_get_all_in.restype = POINTER_T(struct_r_pvector_t)
r_meta_get_all_in.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, RAnalMetaType]
r_meta_get_all_intersect = _r_anal.r_meta_get_all_intersect
r_meta_get_all_intersect.restype = POINTER_T(struct_r_pvector_t)
r_meta_get_all_intersect.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64, RAnalMetaType]
r_meta_space_unset_for = _r_anal.r_meta_space_unset_for
r_meta_space_unset_for.restype = None
r_meta_space_unset_for.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_space_t)]
r_meta_space_count_for = _r_anal.r_meta_space_count_for
r_meta_space_count_for.restype = ctypes.c_int32
r_meta_space_count_for.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_space_t)]
r_meta_rebase = _r_anal.r_meta_rebase
r_meta_rebase.restype = None
r_meta_rebase.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_meta_get_size = _r_anal.r_meta_get_size
r_meta_get_size.restype = ctypes.c_uint64
r_meta_get_size.argtypes = [POINTER_T(struct_r_anal_t), RAnalMetaType]
r_meta_type_to_string = _r_anal.r_meta_type_to_string
r_meta_type_to_string.restype = POINTER_T(ctypes.c_char)
r_meta_type_to_string.argtypes = [ctypes.c_int32]
r_meta_print = _r_anal.r_meta_print
r_meta_print.restype = None
r_meta_print.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_meta_item_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, POINTER_T(struct_pj_t), ctypes.c_bool]
r_meta_print_list_all = _r_anal.r_meta_print_list_all
r_meta_print_list_all.restype = None
r_meta_print_list_all.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_int32]
r_meta_print_list_at = _r_anal.r_meta_print_list_at
r_meta_print_list_at.restype = None
r_meta_print_list_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_meta_print_list_in_function = _r_anal.r_meta_print_list_in_function
r_meta_print_list_in_function.restype = None
r_meta_print_list_in_function.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64]
r_anal_hint_del = _r_anal.r_anal_hint_del
r_anal_hint_del.restype = None
r_anal_hint_del.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_clear = _r_anal.r_anal_hint_clear
r_anal_hint_clear.restype = None
r_anal_hint_clear.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_hint_free = _r_anal.r_anal_hint_free
r_anal_hint_free.restype = None
r_anal_hint_free.argtypes = [POINTER_T(struct_r_anal_hint_t)]
r_anal_hint_set_syntax = _r_anal.r_anal_hint_set_syntax
r_anal_hint_set_syntax.restype = None
r_anal_hint_set_syntax.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_hint_set_type = _r_anal.r_anal_hint_set_type
r_anal_hint_set_type.restype = None
r_anal_hint_set_type.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_hint_set_jump = _r_anal.r_anal_hint_set_jump
r_anal_hint_set_jump.restype = None
r_anal_hint_set_jump.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_fail = _r_anal.r_anal_hint_set_fail
r_anal_hint_set_fail.restype = None
r_anal_hint_set_fail.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_newbits = _r_anal.r_anal_hint_set_newbits
r_anal_hint_set_newbits.restype = None
r_anal_hint_set_newbits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_hint_set_nword = _r_anal.r_anal_hint_set_nword
r_anal_hint_set_nword.restype = None
r_anal_hint_set_nword.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_hint_set_offset = _r_anal.r_anal_hint_set_offset
r_anal_hint_set_offset.restype = None
r_anal_hint_set_offset.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_hint_set_immbase = _r_anal.r_anal_hint_set_immbase
r_anal_hint_set_immbase.restype = None
r_anal_hint_set_immbase.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_hint_set_size = _r_anal.r_anal_hint_set_size
r_anal_hint_set_size.restype = None
r_anal_hint_set_size.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_opcode = _r_anal.r_anal_hint_set_opcode
r_anal_hint_set_opcode.restype = None
r_anal_hint_set_opcode.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_hint_set_esil = _r_anal.r_anal_hint_set_esil
r_anal_hint_set_esil.restype = None
r_anal_hint_set_esil.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_hint_set_pointer = _r_anal.r_anal_hint_set_pointer
r_anal_hint_set_pointer.restype = None
r_anal_hint_set_pointer.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_ret = _r_anal.r_anal_hint_set_ret
r_anal_hint_set_ret.restype = None
r_anal_hint_set_ret.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_high = _r_anal.r_anal_hint_set_high
r_anal_hint_set_high.restype = None
r_anal_hint_set_high.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_set_stackframe = _r_anal.r_anal_hint_set_stackframe
r_anal_hint_set_stackframe.restype = None
r_anal_hint_set_stackframe.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_val = _r_anal.r_anal_hint_set_val
r_anal_hint_set_val.restype = None
r_anal_hint_set_val.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_hint_set_arch = _r_anal.r_anal_hint_set_arch
r_anal_hint_set_arch.restype = None
r_anal_hint_set_arch.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_hint_set_bits = _r_anal.r_anal_hint_set_bits
r_anal_hint_set_bits.restype = None
r_anal_hint_set_bits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_hint_unset_val = _r_anal.r_anal_hint_unset_val
r_anal_hint_unset_val.restype = None
r_anal_hint_unset_val.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_high = _r_anal.r_anal_hint_unset_high
r_anal_hint_unset_high.restype = None
r_anal_hint_unset_high.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_immbase = _r_anal.r_anal_hint_unset_immbase
r_anal_hint_unset_immbase.restype = None
r_anal_hint_unset_immbase.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_nword = _r_anal.r_anal_hint_unset_nword
r_anal_hint_unset_nword.restype = None
r_anal_hint_unset_nword.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_size = _r_anal.r_anal_hint_unset_size
r_anal_hint_unset_size.restype = None
r_anal_hint_unset_size.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_type = _r_anal.r_anal_hint_unset_type
r_anal_hint_unset_type.restype = None
r_anal_hint_unset_type.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_esil = _r_anal.r_anal_hint_unset_esil
r_anal_hint_unset_esil.restype = None
r_anal_hint_unset_esil.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_opcode = _r_anal.r_anal_hint_unset_opcode
r_anal_hint_unset_opcode.restype = None
r_anal_hint_unset_opcode.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_syntax = _r_anal.r_anal_hint_unset_syntax
r_anal_hint_unset_syntax.restype = None
r_anal_hint_unset_syntax.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_pointer = _r_anal.r_anal_hint_unset_pointer
r_anal_hint_unset_pointer.restype = None
r_anal_hint_unset_pointer.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_ret = _r_anal.r_anal_hint_unset_ret
r_anal_hint_unset_ret.restype = None
r_anal_hint_unset_ret.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_offset = _r_anal.r_anal_hint_unset_offset
r_anal_hint_unset_offset.restype = None
r_anal_hint_unset_offset.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_jump = _r_anal.r_anal_hint_unset_jump
r_anal_hint_unset_jump.restype = None
r_anal_hint_unset_jump.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_fail = _r_anal.r_anal_hint_unset_fail
r_anal_hint_unset_fail.restype = None
r_anal_hint_unset_fail.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_newbits = _r_anal.r_anal_hint_unset_newbits
r_anal_hint_unset_newbits.restype = None
r_anal_hint_unset_newbits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_stackframe = _r_anal.r_anal_hint_unset_stackframe
r_anal_hint_unset_stackframe.restype = None
r_anal_hint_unset_stackframe.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_arch = _r_anal.r_anal_hint_unset_arch
r_anal_hint_unset_arch.restype = None
r_anal_hint_unset_arch.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_hint_unset_bits = _r_anal.r_anal_hint_unset_bits
r_anal_hint_unset_bits.restype = None
r_anal_hint_unset_bits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_addr_hints_at = _r_anal.r_anal_addr_hints_at
r_anal_addr_hints_at.restype = POINTER_T(struct_r_vector_t)
r_anal_addr_hints_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
RAnalAddrHintRecordsCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint64, POINTER_T(struct_r_vector_t), POINTER_T(None)))
r_anal_addr_hints_foreach = _r_anal.r_anal_addr_hints_foreach
r_anal_addr_hints_foreach.restype = None
r_anal_addr_hints_foreach.argtypes = [POINTER_T(struct_r_anal_t), RAnalAddrHintRecordsCb, POINTER_T(None)]
RAnalArchHintCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint64, POINTER_T(ctypes.c_char), POINTER_T(None)))
r_anal_arch_hints_foreach = _r_anal.r_anal_arch_hints_foreach
r_anal_arch_hints_foreach.restype = None
r_anal_arch_hints_foreach.argtypes = [POINTER_T(struct_r_anal_t), RAnalArchHintCb, POINTER_T(None)]
RAnalBitsHintCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint64, ctypes.c_int32, POINTER_T(None)))
r_anal_bits_hints_foreach = _r_anal.r_anal_bits_hints_foreach
r_anal_bits_hints_foreach.restype = None
r_anal_bits_hints_foreach.argtypes = [POINTER_T(struct_r_anal_t), RAnalBitsHintCb, POINTER_T(None)]
r_anal_hint_arch_at = _r_anal.r_anal_hint_arch_at
r_anal_hint_arch_at.restype = POINTER_T(ctypes.c_char)
r_anal_hint_arch_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_uint64)]
r_anal_hint_bits_at = _r_anal.r_anal_hint_bits_at
r_anal_hint_bits_at.restype = ctypes.c_int32
r_anal_hint_bits_at.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_uint64)]
r_anal_hint_get = _r_anal.r_anal_hint_get
r_anal_hint_get.restype = POINTER_T(struct_r_anal_hint_t)
r_anal_hint_get.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_anal_switch_op_new = _r_anal.r_anal_switch_op_new
r_anal_switch_op_new.restype = POINTER_T(struct_r_anal_switch_obj_t)
r_anal_switch_op_new.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_anal_switch_op_free = _r_anal.r_anal_switch_op_free
r_anal_switch_op_free.restype = None
r_anal_switch_op_free.argtypes = [POINTER_T(struct_r_anal_switch_obj_t)]
r_anal_switch_op_add_case = _r_anal.r_anal_switch_op_add_case
r_anal_switch_op_add_case.restype = POINTER_T(struct_r_anal_case_obj_t)
r_anal_switch_op_add_case.argtypes = [POINTER_T(struct_r_anal_switch_obj_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_anal_cycle_frame_new = _r_anal.r_anal_cycle_frame_new
r_anal_cycle_frame_new.restype = POINTER_T(struct_r_anal_cycle_frame_t)
r_anal_cycle_frame_new.argtypes = []
r_anal_cycle_frame_free = _r_anal.r_anal_cycle_frame_free
r_anal_cycle_frame_free.restype = None
r_anal_cycle_frame_free.argtypes = [POINTER_T(struct_r_anal_cycle_frame_t)]
r_anal_function_get_label = _r_anal.r_anal_function_get_label
r_anal_function_get_label.restype = ctypes.c_uint64
r_anal_function_get_label.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)]
r_anal_function_get_label_at = _r_anal.r_anal_function_get_label_at
r_anal_function_get_label_at.restype = POINTER_T(ctypes.c_char)
r_anal_function_get_label_at.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_function_set_label = _r_anal.r_anal_function_set_label
r_anal_function_set_label.restype = ctypes.c_bool
r_anal_function_set_label.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_anal_function_delete_label = _r_anal.r_anal_function_delete_label
r_anal_function_delete_label.restype = ctypes.c_bool
r_anal_function_delete_label.argtypes = [POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)]
r_anal_function_delete_label_at = _r_anal.r_anal_function_delete_label_at
r_anal_function_delete_label_at.restype = ctypes.c_bool
r_anal_function_delete_label_at.argtypes = [POINTER_T(struct_r_anal_function_t), ctypes.c_uint64]
r_anal_set_limits = _r_anal.r_anal_set_limits
r_anal_set_limits.restype = None
r_anal_set_limits.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint64]
r_anal_unset_limits = _r_anal.r_anal_unset_limits
r_anal_unset_limits.restype = None
r_anal_unset_limits.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_esil_to_reil_setup = _r_anal.r_anal_esil_to_reil_setup
r_anal_esil_to_reil_setup.restype = ctypes.c_int32
r_anal_esil_to_reil_setup.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(struct_r_anal_t), ctypes.c_int32, ctypes.c_int32]
r_anal_noreturn_list = _r_anal.r_anal_noreturn_list
r_anal_noreturn_list.restype = None
r_anal_noreturn_list.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_noreturn_add = _r_anal.r_anal_noreturn_add
r_anal_noreturn_add.restype = ctypes.c_bool
r_anal_noreturn_add.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_anal_noreturn_drop = _r_anal.r_anal_noreturn_drop
r_anal_noreturn_drop.restype = ctypes.c_bool
r_anal_noreturn_drop.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_noreturn_at_addr = _r_anal.r_anal_noreturn_at_addr
r_anal_noreturn_at_addr.restype = ctypes.c_bool
r_anal_noreturn_at_addr.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64]
r_sign_space_count_for = _r_anal.r_sign_space_count_for
r_sign_space_count_for.restype = ctypes.c_int32
r_sign_space_count_for.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_space_t)]
r_sign_space_unset_for = _r_anal.r_sign_space_unset_for
r_sign_space_unset_for.restype = None
r_sign_space_unset_for.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_space_t)]
r_sign_space_rename_for = _r_anal.r_sign_space_rename_for
r_sign_space_rename_for.restype = None
r_sign_space_rename_for.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_space_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
class struct_c__SA_RVTableContext(ctypes.Structure):
    pass

struct_c__SA_RVTableContext._pack_ = True # source:False
struct_c__SA_RVTableContext._fields_ = [
    ('anal', POINTER_T(struct_r_anal_t)),
    ('abi', RAnalCPPABI),
    ('word_size', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('read_addr', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_uint64)))),
]

RVTableContext = struct_c__SA_RVTableContext
class struct_vtable_info_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('saddr', ctypes.c_uint64),
    ('methods', struct_r_vector_t),
     ]

RVTableInfo = struct_vtable_info_t
class struct_vtable_method_info_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('vtable_offset', ctypes.c_uint64),
     ]

RVTableMethodInfo = struct_vtable_method_info_t
r_anal_vtable_info_free = _r_anal.r_anal_vtable_info_free
r_anal_vtable_info_free.restype = None
r_anal_vtable_info_free.argtypes = [POINTER_T(struct_vtable_info_t)]
r_anal_vtable_info_get_size = _r_anal.r_anal_vtable_info_get_size
r_anal_vtable_info_get_size.restype = ctypes.c_uint64
r_anal_vtable_info_get_size.argtypes = [POINTER_T(struct_c__SA_RVTableContext), POINTER_T(struct_vtable_info_t)]
r_anal_vtable_begin = _r_anal.r_anal_vtable_begin
r_anal_vtable_begin.restype = ctypes.c_bool
r_anal_vtable_begin.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_c__SA_RVTableContext)]
r_anal_vtable_parse_at = _r_anal.r_anal_vtable_parse_at
r_anal_vtable_parse_at.restype = POINTER_T(struct_vtable_info_t)
r_anal_vtable_parse_at.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64]
r_anal_vtable_search = _r_anal.r_anal_vtable_search
r_anal_vtable_search.restype = POINTER_T(struct_r_list_t)
r_anal_vtable_search.argtypes = [POINTER_T(struct_c__SA_RVTableContext)]
r_anal_list_vtables = _r_anal.r_anal_list_vtables
r_anal_list_vtables.restype = None
r_anal_list_vtables.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_rtti_msvc_demangle_class_name = _r_anal.r_anal_rtti_msvc_demangle_class_name
r_anal_rtti_msvc_demangle_class_name.restype = POINTER_T(ctypes.c_char)
r_anal_rtti_msvc_demangle_class_name.argtypes = [POINTER_T(struct_c__SA_RVTableContext), POINTER_T(ctypes.c_char)]
r_anal_rtti_msvc_print_complete_object_locator = _r_anal.r_anal_rtti_msvc_print_complete_object_locator
r_anal_rtti_msvc_print_complete_object_locator.restype = None
r_anal_rtti_msvc_print_complete_object_locator.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_msvc_print_type_descriptor = _r_anal.r_anal_rtti_msvc_print_type_descriptor
r_anal_rtti_msvc_print_type_descriptor.restype = None
r_anal_rtti_msvc_print_type_descriptor.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_msvc_print_class_hierarchy_descriptor = _r_anal.r_anal_rtti_msvc_print_class_hierarchy_descriptor
r_anal_rtti_msvc_print_class_hierarchy_descriptor.restype = None
r_anal_rtti_msvc_print_class_hierarchy_descriptor.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_msvc_print_base_class_descriptor = _r_anal.r_anal_rtti_msvc_print_base_class_descriptor
r_anal_rtti_msvc_print_base_class_descriptor.restype = None
r_anal_rtti_msvc_print_base_class_descriptor.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_msvc_print_at_vtable = _r_anal.r_anal_rtti_msvc_print_at_vtable
r_anal_rtti_msvc_print_at_vtable.restype = ctypes.c_bool
r_anal_rtti_msvc_print_at_vtable.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32, ctypes.c_bool]
r_anal_rtti_msvc_recover_all = _r_anal.r_anal_rtti_msvc_recover_all
r_anal_rtti_msvc_recover_all.restype = None
r_anal_rtti_msvc_recover_all.argtypes = [POINTER_T(struct_c__SA_RVTableContext), POINTER_T(struct_r_list_t)]
r_anal_rtti_itanium_demangle_class_name = _r_anal.r_anal_rtti_itanium_demangle_class_name
r_anal_rtti_itanium_demangle_class_name.restype = POINTER_T(ctypes.c_char)
r_anal_rtti_itanium_demangle_class_name.argtypes = [POINTER_T(struct_c__SA_RVTableContext), POINTER_T(ctypes.c_char)]
r_anal_rtti_itanium_print_at_vtable = _r_anal.r_anal_rtti_itanium_print_at_vtable
r_anal_rtti_itanium_print_at_vtable.restype = ctypes.c_bool
r_anal_rtti_itanium_print_at_vtable.argtypes = [POINTER_T(struct_c__SA_RVTableContext), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_itanium_recover_all = _r_anal.r_anal_rtti_itanium_recover_all
r_anal_rtti_itanium_recover_all.restype = None
r_anal_rtti_itanium_recover_all.argtypes = [POINTER_T(struct_c__SA_RVTableContext), POINTER_T(struct_r_list_t)]
r_anal_rtti_demangle_class_name = _r_anal.r_anal_rtti_demangle_class_name
r_anal_rtti_demangle_class_name.restype = POINTER_T(ctypes.c_char)
r_anal_rtti_demangle_class_name.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_rtti_print_at_vtable = _r_anal.r_anal_rtti_print_at_vtable
r_anal_rtti_print_at_vtable.restype = None
r_anal_rtti_print_at_vtable.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_anal_rtti_print_all = _r_anal.r_anal_rtti_print_all
r_anal_rtti_print_all.restype = None
r_anal_rtti_print_all.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_rtti_recover_all = _r_anal.r_anal_rtti_recover_all
r_anal_rtti_recover_all.restype = None
r_anal_rtti_recover_all.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_colorize_bb = _r_anal.r_anal_colorize_bb
r_anal_colorize_bb.restype = None
r_anal_colorize_bb.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_uint32]
r_anal_preludes = _r_anal.r_anal_preludes
r_anal_preludes.restype = POINTER_T(struct_r_list_t)
r_anal_preludes.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_is_prelude = _r_anal.r_anal_is_prelude
r_anal_is_prelude.restype = ctypes.c_bool
r_anal_is_prelude.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
class struct_r_anal_method_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('vtable_offset', ctypes.c_int64),
     ]

RAnalMethod = struct_r_anal_method_t
class struct_r_anal_base_class_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('id', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_uint64),
    ('class_name', POINTER_T(ctypes.c_char)),
     ]

RAnalBaseClass = struct_r_anal_base_class_t
class struct_r_anal_vtable_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('id', POINTER_T(ctypes.c_char)),
    ('offset', ctypes.c_uint64),
    ('addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
     ]

RAnalVTable = struct_r_anal_vtable_t

# values for enumeration 'c__EA_RAnalClassErr'
c__EA_RAnalClassErr__enumvalues = {
    0: 'R_ANAL_CLASS_ERR_SUCCESS',
    1: 'R_ANAL_CLASS_ERR_CLASH',
    2: 'R_ANAL_CLASS_ERR_NONEXISTENT_ATTR',
    3: 'R_ANAL_CLASS_ERR_NONEXISTENT_CLASS',
    4: 'R_ANAL_CLASS_ERR_OTHER',
}
R_ANAL_CLASS_ERR_SUCCESS = 0
R_ANAL_CLASS_ERR_CLASH = 1
R_ANAL_CLASS_ERR_NONEXISTENT_ATTR = 2
R_ANAL_CLASS_ERR_NONEXISTENT_CLASS = 3
R_ANAL_CLASS_ERR_OTHER = 4
c__EA_RAnalClassErr = ctypes.c_int # enum
RAnalClassErr = c__EA_RAnalClassErr
RAnalClassErr__enumvalues = c__EA_RAnalClassErr__enumvalues
r_anal_class_create = _r_anal.r_anal_class_create
r_anal_class_create.restype = None
r_anal_class_create.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_delete = _r_anal.r_anal_class_delete
r_anal_class_delete.restype = None
r_anal_class_delete.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_exists = _r_anal.r_anal_class_exists
r_anal_class_exists.restype = ctypes.c_bool
r_anal_class_exists.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_get_all = _r_anal.r_anal_class_get_all
r_anal_class_get_all.restype = POINTER_T(struct_ls_t)
r_anal_class_get_all.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_bool]
r_anal_class_foreach = _r_anal.r_anal_class_foreach
r_anal_class_foreach.restype = None
r_anal_class_foreach.argtypes = [POINTER_T(struct_r_anal_t), SdbForeachCallback, POINTER_T(None)]
r_anal_class_rename = _r_anal.r_anal_class_rename
r_anal_class_rename.restype = RAnalClassErr
r_anal_class_rename.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_class_method_fini = _r_anal.r_anal_class_method_fini
r_anal_class_method_fini.restype = None
r_anal_class_method_fini.argtypes = [POINTER_T(struct_r_anal_method_t)]
r_anal_class_method_get = _r_anal.r_anal_class_method_get
r_anal_class_method_get.restype = RAnalClassErr
r_anal_class_method_get.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_method_t)]
r_anal_class_method_get_all = _r_anal.r_anal_class_method_get_all
r_anal_class_method_get_all.restype = POINTER_T(struct_r_vector_t)
r_anal_class_method_get_all.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_method_set = _r_anal.r_anal_class_method_set
r_anal_class_method_set.restype = RAnalClassErr
r_anal_class_method_set.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_method_t)]
r_anal_class_method_rename = _r_anal.r_anal_class_method_rename
r_anal_class_method_rename.restype = RAnalClassErr
r_anal_class_method_rename.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_class_method_delete = _r_anal.r_anal_class_method_delete
r_anal_class_method_delete.restype = RAnalClassErr
r_anal_class_method_delete.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_class_base_fini = _r_anal.r_anal_class_base_fini
r_anal_class_base_fini.restype = None
r_anal_class_base_fini.argtypes = [POINTER_T(struct_r_anal_base_class_t)]
r_anal_class_base_get = _r_anal.r_anal_class_base_get
r_anal_class_base_get.restype = RAnalClassErr
r_anal_class_base_get.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_base_class_t)]
r_anal_class_base_get_all = _r_anal.r_anal_class_base_get_all
r_anal_class_base_get_all.restype = POINTER_T(struct_r_vector_t)
r_anal_class_base_get_all.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_base_set = _r_anal.r_anal_class_base_set
r_anal_class_base_set.restype = RAnalClassErr
r_anal_class_base_set.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_base_class_t)]
r_anal_class_base_delete = _r_anal.r_anal_class_base_delete
r_anal_class_base_delete.restype = RAnalClassErr
r_anal_class_base_delete.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_class_vtable_fini = _r_anal.r_anal_class_vtable_fini
r_anal_class_vtable_fini.restype = None
r_anal_class_vtable_fini.argtypes = [POINTER_T(struct_r_anal_vtable_t)]
r_anal_class_vtable_get = _r_anal.r_anal_class_vtable_get
r_anal_class_vtable_get.restype = RAnalClassErr
r_anal_class_vtable_get.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_vtable_t)]
r_anal_class_vtable_get_all = _r_anal.r_anal_class_vtable_get_all
r_anal_class_vtable_get_all.restype = POINTER_T(struct_r_vector_t)
r_anal_class_vtable_get_all.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_vtable_set = _r_anal.r_anal_class_vtable_set
r_anal_class_vtable_set.restype = RAnalClassErr
r_anal_class_vtable_set.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_anal_vtable_t)]
r_anal_class_vtable_delete = _r_anal.r_anal_class_vtable_delete
r_anal_class_vtable_delete.restype = RAnalClassErr
r_anal_class_vtable_delete.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_class_print = _r_anal.r_anal_class_print
r_anal_class_print.restype = None
r_anal_class_print.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_anal_class_json = _r_anal.r_anal_class_json
r_anal_class_json.restype = None
r_anal_class_json.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_pj_t), POINTER_T(ctypes.c_char)]
r_anal_class_list = _r_anal.r_anal_class_list
r_anal_class_list.restype = None
r_anal_class_list.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_anal_class_list_bases = _r_anal.r_anal_class_list_bases
r_anal_class_list_bases.restype = None
r_anal_class_list_bases.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_list_vtables = _r_anal.r_anal_class_list_vtables
r_anal_class_list_vtables.restype = None
r_anal_class_list_vtables.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_anal_class_list_vtable_offset_functions = _r_anal.r_anal_class_list_vtable_offset_functions
r_anal_class_list_vtable_offset_functions.restype = None
r_anal_class_list_vtable_offset_functions.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_anal_class_get_inheritance_graph = _r_anal.r_anal_class_get_inheritance_graph
r_anal_class_get_inheritance_graph.restype = POINTER_T(struct_r_graph_t)
r_anal_class_get_inheritance_graph.argtypes = [POINTER_T(struct_r_anal_t)]
r_anal_esil_cfg_expr = _r_anal.r_anal_esil_cfg_expr
r_anal_esil_cfg_expr.restype = POINTER_T(struct_r_anal_esil_cfg_t)
r_anal_esil_cfg_expr.argtypes = [POINTER_T(struct_r_anal_esil_cfg_t), POINTER_T(struct_r_anal_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)]
r_anal_esil_cfg_op = _r_anal.r_anal_esil_cfg_op
r_anal_esil_cfg_op.restype = POINTER_T(struct_r_anal_esil_cfg_t)
r_anal_esil_cfg_op.argtypes = [POINTER_T(struct_r_anal_esil_cfg_t), POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_op_t)]
r_anal_esil_cfg_merge_blocks = _r_anal.r_anal_esil_cfg_merge_blocks
r_anal_esil_cfg_merge_blocks.restype = None
r_anal_esil_cfg_merge_blocks.argtypes = [POINTER_T(struct_r_anal_esil_cfg_t)]
r_anal_esil_cfg_free = _r_anal.r_anal_esil_cfg_free
r_anal_esil_cfg_free.restype = None
r_anal_esil_cfg_free.argtypes = [POINTER_T(struct_r_anal_esil_cfg_t)]
r_anal_esil_dfg_node_new = _r_anal.r_anal_esil_dfg_node_new
r_anal_esil_dfg_node_new.restype = POINTER_T(struct_r_anal_esil_dfg_node_t)
r_anal_esil_dfg_node_new.argtypes = [POINTER_T(struct_r_anal_esil_dfg_t), POINTER_T(ctypes.c_char)]
r_anal_esil_dfg_new = _r_anal.r_anal_esil_dfg_new
r_anal_esil_dfg_new.restype = POINTER_T(struct_r_anal_esil_dfg_t)
r_anal_esil_dfg_new.argtypes = [POINTER_T(struct_r_reg_t)]
r_anal_esil_dfg_free = _r_anal.r_anal_esil_dfg_free
r_anal_esil_dfg_free.restype = None
r_anal_esil_dfg_free.argtypes = [POINTER_T(struct_r_anal_esil_dfg_t)]
r_anal_esil_dfg_expr = _r_anal.r_anal_esil_dfg_expr
r_anal_esil_dfg_expr.restype = POINTER_T(struct_r_anal_esil_dfg_t)
r_anal_esil_dfg_expr.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_esil_dfg_t), POINTER_T(ctypes.c_char)]
r_anal_esil_dfg_filter = _r_anal.r_anal_esil_dfg_filter
r_anal_esil_dfg_filter.restype = POINTER_T(struct_c__SA_RStrBuf)
r_anal_esil_dfg_filter.argtypes = [POINTER_T(struct_r_anal_esil_dfg_t), POINTER_T(ctypes.c_char)]
r_anal_esil_dfg_filter_expr = _r_anal.r_anal_esil_dfg_filter_expr
r_anal_esil_dfg_filter_expr.restype = POINTER_T(struct_c__SA_RStrBuf)
r_anal_esil_dfg_filter_expr.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_anal_types_from_fcn = _r_anal.r_anal_types_from_fcn
r_anal_types_from_fcn.restype = POINTER_T(struct_r_list_t)
r_anal_types_from_fcn.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_function_t)]
r_anal_get_base_type = _r_anal.r_anal_get_base_type
r_anal_get_base_type.restype = POINTER_T(struct_r_anal_base_type_t)
r_anal_get_base_type.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_parse_pdb_types = _r_anal.r_parse_pdb_types
r_parse_pdb_types.restype = None
r_parse_pdb_types.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_pdb_t)]
r_anal_save_base_type = _r_anal.r_anal_save_base_type
r_anal_save_base_type.restype = None
r_anal_save_base_type.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_base_type_t)]
r_anal_base_type_free = _r_anal.r_anal_base_type_free
r_anal_base_type_free.restype = None
r_anal_base_type_free.argtypes = [POINTER_T(struct_r_anal_base_type_t)]
r_anal_base_type_new = _r_anal.r_anal_base_type_new
r_anal_base_type_new.restype = POINTER_T(struct_r_anal_base_type_t)
r_anal_base_type_new.argtypes = [RAnalBaseTypeKind]
r_anal_dwarf_process_info = _r_anal.r_anal_dwarf_process_info
r_anal_dwarf_process_info.restype = None
r_anal_dwarf_process_info.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_anal_dwarf_context)]
r_anal_dwarf_integrate_functions = _r_anal.r_anal_dwarf_integrate_functions
r_anal_dwarf_integrate_functions.restype = None
r_anal_dwarf_integrate_functions.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(struct_r_flag_t), POINTER_T(struct_sdb_t)]
r_anal_plugin_null = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_6502 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_6502_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_8051 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_amd29k = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_arc = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_arm_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_arm_gnu = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_avr = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_bf = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_chip8 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_cr16 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_cris = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_dalvik = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_ebc = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_gb = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_h8300 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_hexagon = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_i4004 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_i8080 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_java = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_m68k_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_m680x_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_malbolge = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_mcore = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_mips_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_mips_gnu = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_msp430 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_nios2 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_or1k = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_pic = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_ppc_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_ppc_gnu = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_propeller = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_riscv = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_riscv_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_rsp = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_sh = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_snes = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_sparc_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_sparc_gnu = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_sysz = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_tms320 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_tms320c64x = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_tricore = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_v810 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_v850 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_vax = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_wasm = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_ws = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_x86 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_x86_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_x86_im = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_x86_simple = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_x86_udis = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_xap = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_xcore_cs = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_xtensa = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_z80 = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
r_anal_plugin_pyc = struct_r_anal_plugin_t # Variable struct_r_anal_plugin_t
__all__ = \
    ['ARG_CONST', 'ARG_ESIL_INTERNAL', 'ARG_NONE', 'ARG_REG',
    'ARG_TEMP', 'DW_AT_KIND_ADDRESS', 'DW_AT_KIND_BLOCK',
    'DW_AT_KIND_CONSTANT', 'DW_AT_KIND_EXPRLOC', 'DW_AT_KIND_FLAG',
    'DW_AT_KIND_LINEPTR', 'DW_AT_KIND_LOCLISTPTR',
    'DW_AT_KIND_MACPTR', 'DW_AT_KIND_RANGELISTPTR',
    'DW_AT_KIND_REFERENCE', 'DW_AT_KIND_STRING', 'PTRACE_ARCH_PRCTL',
    'PTRACE_ATTACH', 'PTRACE_CONT', 'PTRACE_DETACH',
    'PTRACE_GETEVENTMSG', 'PTRACE_GETFPREGS', 'PTRACE_GETFPXREGS',
    'PTRACE_GETREGS', 'PTRACE_GETREGSET', 'PTRACE_GETSIGINFO',
    'PTRACE_GETSIGMASK', 'PTRACE_GET_THREAD_AREA', 'PTRACE_INTERRUPT',
    'PTRACE_KILL', 'PTRACE_LISTEN', 'PTRACE_PEEKDATA',
    'PTRACE_PEEKSIGINFO', 'PTRACE_PEEKTEXT', 'PTRACE_PEEKUSER',
    'PTRACE_POKEDATA', 'PTRACE_POKETEXT', 'PTRACE_POKEUSER',
    'PTRACE_SECCOMP_GET_FILTER', 'PTRACE_SECCOMP_GET_METADATA',
    'PTRACE_SEIZE', 'PTRACE_SETFPREGS', 'PTRACE_SETFPXREGS',
    'PTRACE_SETOPTIONS', 'PTRACE_SETREGS', 'PTRACE_SETREGSET',
    'PTRACE_SETSIGINFO', 'PTRACE_SETSIGMASK',
    'PTRACE_SET_THREAD_AREA', 'PTRACE_SINGLEBLOCK',
    'PTRACE_SINGLESTEP', 'PTRACE_SYSCALL', 'PTRACE_SYSEMU',
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'RAnal',
    'RAnalAddrCb', 'RAnalAddrHintRecord', 'RAnalAddrHintRecordsCb',
    'RAnalAddrHintType', 'RAnalAddrHintType__enumvalues',
    'RAnalArchHintCb', 'RAnalAttr', 'RAnalBaseClass', 'RAnalBaseType',
    'RAnalBaseTypeEnum', 'RAnalBaseTypeKind',
    'RAnalBaseTypeKind__enumvalues', 'RAnalBaseTypeStruct',
    'RAnalBaseTypeUnion', 'RAnalBind', 'RAnalBitsHintCb',
    'RAnalBlock', 'RAnalBlockCb', 'RAnalCPPABI',
    'RAnalCPPABI__enumvalues', 'RAnalCallbacks', 'RAnalCaseOp',
    'RAnalClassErr', 'RAnalClassErr__enumvalues', 'RAnalCmdExt',
    'RAnalCond', 'RAnalCycleFrame', 'RAnalCycleHook', 'RAnalData',
    'RAnalDataType', 'RAnalDataType__enumvalues', 'RAnalDiff',
    'RAnalDiffBBCallback', 'RAnalDiffEvalCallback',
    'RAnalDiffFcnCallback', 'RAnalDwarfContext', 'RAnalEnumCase',
    'RAnalEsil', 'RAnalEsilBB', 'RAnalEsilBlockEnterType',
    'RAnalEsilBlockEnterType__enumvalues', 'RAnalEsilCB',
    'RAnalEsilCFG', 'RAnalEsilCallbacks', 'RAnalEsilDFG',
    'RAnalEsilDFGBlockType', 'RAnalEsilDFGBlockType__enumvalues',
    'RAnalEsilDFGNode', 'RAnalEsilEOffset', 'RAnalEsilHookRegWriteCB',
    'RAnalEsilInterrupt', 'RAnalEsilInterruptCB',
    'RAnalEsilInterruptHandler', 'RAnalEsilLoopCB',
    'RAnalEsilMemChange', 'RAnalEsilOp', 'RAnalEsilOpCb',
    'RAnalEsilRegChange', 'RAnalEsilSource', 'RAnalEsilTrace',
    'RAnalEsilTrapCB', 'RAnalEsilWord', 'RAnalFPBBCallback',
    'RAnalFPFcnCallback', 'RAnalFcnMeta', 'RAnalFcnVarsCache',
    'RAnalFuncArg', 'RAnalFunction', 'RAnalGetFcnIn', 'RAnalGetHint',
    'RAnalHint', 'RAnalLabelAt', 'RAnalMetaItem', 'RAnalMetaType',
    'RAnalMetaType__enumvalues', 'RAnalMetaUserItem', 'RAnalMethod',
    'RAnalOp', 'RAnalOpCallback', 'RAnalOpDirection',
    'RAnalOpDirection__enumvalues', 'RAnalOpFamily',
    'RAnalOpFamily__enumvalues', 'RAnalOpMask',
    'RAnalOpMask__enumvalues', 'RAnalOpPrefix',
    'RAnalOpPrefix__enumvalues', 'RAnalOptions', 'RAnalPlugin',
    'RAnalRange', 'RAnalRef', 'RAnalRefCmp', 'RAnalRefStr',
    'RAnalRefType', 'RAnalRefType__enumvalues', 'RAnalRefline',
    'RAnalRegProfCallback', 'RAnalRegProfGetCallback', 'RAnalReil',
    'RAnalReilArg', 'RAnalReilArgType',
    'RAnalReilArgType__enumvalues', 'RAnalReilInst',
    'RAnalReilOpcode', 'RAnalReilOpcode__enumvalues', 'RAnalStackOp',
    'RAnalStackOp__enumvalues', 'RAnalStructMember', 'RAnalSwitchOp',
    'RAnalType', 'RAnalTypeAlloca', 'RAnalTypeArray', 'RAnalTypePtr',
    'RAnalTypeStruct', 'RAnalTypeUnion', 'RAnalTypeVar',
    'RAnalUnionMember', 'RAnalVTable', 'RAnalValue',
    'RAnalValueAccess', 'RAnalValueAccess__enumvalues',
    'RAnalValueType', 'RAnalValueType__enumvalues', 'RAnalVar',
    'RAnalVarAccess', 'RAnalVarAccessType',
    'RAnalVarAccessType__enumvalues', 'RAnalVarConstraint',
    'RAnalVarField', 'RAnalVarKind', 'RAnalVarKind__enumvalues',
    'REIL_ADD', 'REIL_AND', 'REIL_DIV', 'REIL_EQ', 'REIL_JCC',
    'REIL_LDM', 'REIL_LT', 'REIL_MOD', 'REIL_MUL', 'REIL_NEG',
    'REIL_NOP', 'REIL_NOT', 'REIL_OR', 'REIL_SDIV', 'REIL_SHL',
    'REIL_SHR', 'REIL_SMOD', 'REIL_SMUL', 'REIL_STM', 'REIL_STR',
    'REIL_SUB', 'REIL_UNK', 'REIL_XOR', 'RHintCb', 'RNCAND',
    'RNCASSIGN', 'RNCDEC', 'RNCDIV', 'RNCEND', 'RNCINC', 'RNCLEFTP',
    'RNCMINUS', 'RNCMOD', 'RNCMUL', 'RNCNAME', 'RNCNEG', 'RNCNUMBER',
    'RNCORR', 'RNCPLUS', 'RNCPRINT', 'RNCRIGHTP', 'RNCROL', 'RNCROR',
    'RNCSHL', 'RNCSHR', 'RNCXOR', 'RVTableContext', 'RVTableInfo',
    'RVTableMethodInfo', 'R_ANAL_ACC_R', 'R_ANAL_ACC_UNKNOWN',
    'R_ANAL_ACC_W', 'R_ANAL_ADDR_HINT_TYPE_ESIL',
    'R_ANAL_ADDR_HINT_TYPE_FAIL', 'R_ANAL_ADDR_HINT_TYPE_HIGH',
    'R_ANAL_ADDR_HINT_TYPE_IMMBASE', 'R_ANAL_ADDR_HINT_TYPE_JUMP',
    'R_ANAL_ADDR_HINT_TYPE_NEW_BITS', 'R_ANAL_ADDR_HINT_TYPE_NWORD',
    'R_ANAL_ADDR_HINT_TYPE_OPCODE', 'R_ANAL_ADDR_HINT_TYPE_OPTYPE',
    'R_ANAL_ADDR_HINT_TYPE_PTR', 'R_ANAL_ADDR_HINT_TYPE_RET',
    'R_ANAL_ADDR_HINT_TYPE_SIZE', 'R_ANAL_ADDR_HINT_TYPE_STACKFRAME',
    'R_ANAL_ADDR_HINT_TYPE_SYNTAX',
    'R_ANAL_ADDR_HINT_TYPE_TYPE_OFFSET', 'R_ANAL_ADDR_HINT_TYPE_VAL',
    'R_ANAL_BASE_TYPE_KIND_ATOMIC', 'R_ANAL_BASE_TYPE_KIND_ENUM',
    'R_ANAL_BASE_TYPE_KIND_STRUCT', 'R_ANAL_BASE_TYPE_KIND_TYPEDEF',
    'R_ANAL_BASE_TYPE_KIND_UNION', 'R_ANAL_CLASS_ERR_CLASH',
    'R_ANAL_CLASS_ERR_NONEXISTENT_ATTR',
    'R_ANAL_CLASS_ERR_NONEXISTENT_CLASS', 'R_ANAL_CLASS_ERR_OTHER',
    'R_ANAL_CLASS_ERR_SUCCESS', 'R_ANAL_COND_AL', 'R_ANAL_COND_EQ',
    'R_ANAL_COND_GE', 'R_ANAL_COND_GT', 'R_ANAL_COND_HI',
    'R_ANAL_COND_HS', 'R_ANAL_COND_LE', 'R_ANAL_COND_LO',
    'R_ANAL_COND_LS', 'R_ANAL_COND_LT', 'R_ANAL_COND_MI',
    'R_ANAL_COND_NE', 'R_ANAL_COND_NV', 'R_ANAL_COND_PL',
    'R_ANAL_COND_VC', 'R_ANAL_COND_VS', 'R_ANAL_CPP_ABI_ITANIUM',
    'R_ANAL_CPP_ABI_MSVC', 'R_ANAL_DATATYPE_ARRAY',
    'R_ANAL_DATATYPE_BOOLEAN', 'R_ANAL_DATATYPE_CLASS',
    'R_ANAL_DATATYPE_FLOAT', 'R_ANAL_DATATYPE_INT16',
    'R_ANAL_DATATYPE_INT32', 'R_ANAL_DATATYPE_INT64',
    'R_ANAL_DATATYPE_NULL', 'R_ANAL_DATATYPE_OBJECT',
    'R_ANAL_DATATYPE_STRING', 'R_ANAL_DATA_TYPE_HEADER',
    'R_ANAL_DATA_TYPE_INVALID', 'R_ANAL_DATA_TYPE_NULL',
    'R_ANAL_DATA_TYPE_NUMBER', 'R_ANAL_DATA_TYPE_PATTERN',
    'R_ANAL_DATA_TYPE_POINTER', 'R_ANAL_DATA_TYPE_SEQUENCE',
    'R_ANAL_DATA_TYPE_STRING', 'R_ANAL_DATA_TYPE_UNKNOWN',
    'R_ANAL_DATA_TYPE_WIDE_STRING', 'R_ANAL_DIFF_TYPE_MATCH',
    'R_ANAL_DIFF_TYPE_NULL', 'R_ANAL_DIFF_TYPE_UNMATCH',
    'R_ANAL_ESIL_BLOCK_ENTER_FALSE', 'R_ANAL_ESIL_BLOCK_ENTER_GLUE',
    'R_ANAL_ESIL_BLOCK_ENTER_NORMAL', 'R_ANAL_ESIL_BLOCK_ENTER_TRUE',
    'R_ANAL_ESIL_DFG_BLOCK_CONST', 'R_ANAL_ESIL_DFG_BLOCK_GENERATIVE',
    'R_ANAL_ESIL_DFG_BLOCK_PTR', 'R_ANAL_ESIL_DFG_BLOCK_RESULT',
    'R_ANAL_ESIL_DFG_BLOCK_VAR', 'R_ANAL_ESIL_FLAG_CARRY',
    'R_ANAL_ESIL_FLAG_OVERFLOW', 'R_ANAL_ESIL_FLAG_PARITY',
    'R_ANAL_ESIL_FLAG_SIGN', 'R_ANAL_ESIL_FLAG_ZERO',
    'R_ANAL_ESIL_OP_TYPE_CONTROL_FLOW', 'R_ANAL_ESIL_OP_TYPE_CUSTOM',
    'R_ANAL_ESIL_OP_TYPE_MATH', 'R_ANAL_ESIL_OP_TYPE_MEM_READ',
    'R_ANAL_ESIL_OP_TYPE_MEM_WRITE', 'R_ANAL_ESIL_OP_TYPE_REG_WRITE',
    'R_ANAL_ESIL_OP_TYPE_UNKNOWN', 'R_ANAL_ESIL_PARM_INVALID',
    'R_ANAL_ESIL_PARM_NUM', 'R_ANAL_ESIL_PARM_REG',
    'R_ANAL_FCN_TYPE_ANY', 'R_ANAL_FCN_TYPE_FCN',
    'R_ANAL_FCN_TYPE_IMP', 'R_ANAL_FCN_TYPE_INT',
    'R_ANAL_FCN_TYPE_LOC', 'R_ANAL_FCN_TYPE_NULL',
    'R_ANAL_FCN_TYPE_ROOT', 'R_ANAL_FCN_TYPE_SYM',
    'R_ANAL_FQUALIFIER_INLINE', 'R_ANAL_FQUALIFIER_NAKED',
    'R_ANAL_FQUALIFIER_NONE', 'R_ANAL_FQUALIFIER_STATIC',
    'R_ANAL_FQUALIFIER_VIRTUAL', 'R_ANAL_FQUALIFIER_VOLATILE',
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
    'R_ANAL_OP_TYPE_ABS', 'R_ANAL_OP_TYPE_ACMP', 'R_ANAL_OP_TYPE_ADD',
    'R_ANAL_OP_TYPE_AND', 'R_ANAL_OP_TYPE_CALL',
    'R_ANAL_OP_TYPE_CASE', 'R_ANAL_OP_TYPE_CAST',
    'R_ANAL_OP_TYPE_CCALL', 'R_ANAL_OP_TYPE_CJMP',
    'R_ANAL_OP_TYPE_CMOV', 'R_ANAL_OP_TYPE_CMP',
    'R_ANAL_OP_TYPE_COND', 'R_ANAL_OP_TYPE_CPL',
    'R_ANAL_OP_TYPE_CRET', 'R_ANAL_OP_TYPE_CRYPTO',
    'R_ANAL_OP_TYPE_CSWI', 'R_ANAL_OP_TYPE_DIV',
    'R_ANAL_OP_TYPE_ICALL', 'R_ANAL_OP_TYPE_IJMP',
    'R_ANAL_OP_TYPE_ILL', 'R_ANAL_OP_TYPE_IND', 'R_ANAL_OP_TYPE_IO',
    'R_ANAL_OP_TYPE_IRCALL', 'R_ANAL_OP_TYPE_IRJMP',
    'R_ANAL_OP_TYPE_JMP', 'R_ANAL_OP_TYPE_LEA',
    'R_ANAL_OP_TYPE_LEAVE', 'R_ANAL_OP_TYPE_LENGTH',
    'R_ANAL_OP_TYPE_LOAD', 'R_ANAL_OP_TYPE_MCJMP',
    'R_ANAL_OP_TYPE_MEM', 'R_ANAL_OP_TYPE_MJMP', 'R_ANAL_OP_TYPE_MOD',
    'R_ANAL_OP_TYPE_MOV', 'R_ANAL_OP_TYPE_MUL', 'R_ANAL_OP_TYPE_NEW',
    'R_ANAL_OP_TYPE_NOP', 'R_ANAL_OP_TYPE_NOR', 'R_ANAL_OP_TYPE_NOT',
    'R_ANAL_OP_TYPE_NULL', 'R_ANAL_OP_TYPE_OR', 'R_ANAL_OP_TYPE_POP',
    'R_ANAL_OP_TYPE_PUSH', 'R_ANAL_OP_TYPE_RCALL',
    'R_ANAL_OP_TYPE_RCJMP', 'R_ANAL_OP_TYPE_REG',
    'R_ANAL_OP_TYPE_REP', 'R_ANAL_OP_TYPE_RET', 'R_ANAL_OP_TYPE_RJMP',
    'R_ANAL_OP_TYPE_ROL', 'R_ANAL_OP_TYPE_ROR',
    'R_ANAL_OP_TYPE_RPUSH', 'R_ANAL_OP_TYPE_SAL',
    'R_ANAL_OP_TYPE_SAR', 'R_ANAL_OP_TYPE_SHL', 'R_ANAL_OP_TYPE_SHR',
    'R_ANAL_OP_TYPE_STORE', 'R_ANAL_OP_TYPE_SUB',
    'R_ANAL_OP_TYPE_SWI', 'R_ANAL_OP_TYPE_SWITCH',
    'R_ANAL_OP_TYPE_SYNC', 'R_ANAL_OP_TYPE_TRAP',
    'R_ANAL_OP_TYPE_UCALL', 'R_ANAL_OP_TYPE_UCCALL',
    'R_ANAL_OP_TYPE_UCJMP', 'R_ANAL_OP_TYPE_UJMP',
    'R_ANAL_OP_TYPE_UNK', 'R_ANAL_OP_TYPE_UPUSH',
    'R_ANAL_OP_TYPE_XCHG', 'R_ANAL_OP_TYPE_XOR',
    'R_ANAL_REFLINE_TYPE_MIDDLE_AFTER',
    'R_ANAL_REFLINE_TYPE_MIDDLE_BEFORE', 'R_ANAL_REFLINE_TYPE_UTF8',
    'R_ANAL_REFLINE_TYPE_WIDE', 'R_ANAL_REF_TYPE_CALL',
    'R_ANAL_REF_TYPE_CODE', 'R_ANAL_REF_TYPE_DATA',
    'R_ANAL_REF_TYPE_NULL', 'R_ANAL_REF_TYPE_STRING',
    'R_ANAL_RET_DUP', 'R_ANAL_RET_END', 'R_ANAL_RET_ERROR',
    'R_ANAL_RET_NEW', 'R_ANAL_RET_NOP', 'R_ANAL_STACK_ALIGN',
    'R_ANAL_STACK_GET', 'R_ANAL_STACK_INC', 'R_ANAL_STACK_NOP',
    'R_ANAL_STACK_NULL', 'R_ANAL_STACK_RESET', 'R_ANAL_STACK_SET',
    'R_ANAL_TRAP_BREAKPOINT', 'R_ANAL_TRAP_DIVBYZERO',
    'R_ANAL_TRAP_EXEC_ERR', 'R_ANAL_TRAP_HALT', 'R_ANAL_TRAP_INVALID',
    'R_ANAL_TRAP_NONE', 'R_ANAL_TRAP_READ_ERR', 'R_ANAL_TRAP_TODO',
    'R_ANAL_TRAP_UNALIGNED', 'R_ANAL_TRAP_UNHANDLED',
    'R_ANAL_TRAP_WRITE_ERR', 'R_ANAL_VAL_IMM', 'R_ANAL_VAL_MEM',
    'R_ANAL_VAL_REG', 'R_ANAL_VAR_ACCESS_TYPE_READ',
    'R_ANAL_VAR_ACCESS_TYPE_WRITE', 'R_ANAL_VAR_KIND_BPV',
    'R_ANAL_VAR_KIND_REG', 'R_ANAL_VAR_KIND_SPV',
    'R_ANAL_VAR_SCOPE_LOCAL', 'R_META_TYPE_ANY', 'R_META_TYPE_CODE',
    'R_META_TYPE_COMMENT', 'R_META_TYPE_DATA', 'R_META_TYPE_FORMAT',
    'R_META_TYPE_HIDE', 'R_META_TYPE_HIGHLIGHT', 'R_META_TYPE_MAGIC',
    'R_META_TYPE_RUN', 'R_META_TYPE_STRING', 'R_META_TYPE_VARTYPE',
    'SdbForeachCallback', '_RAnalCond', '_RAnalCond__enumvalues',
    '_RAnalOpType', '_RAnalOpType__enumvalues', '_RAnalVarScope',
    '_RAnalVarScope__enumvalues', '__ptrace_request',
    'c__EA_RAnalBaseTypeKind', 'c__EA_RAnalCPPABI',
    'c__EA_RAnalClassErr', 'c__EA_RAnalEsilBlockEnterType',
    'c__EA_RAnalEsilDFGBlockType', 'c__EA_RAnalMetaType',
    'c__EA_RAnalOpDirection', 'c__EA_RAnalOpFamily',
    'c__EA_RAnalOpMask', 'c__EA_RAnalOpPrefix', 'c__EA_RAnalRefType',
    'c__EA_RAnalReilArgType', 'c__EA_RAnalReilOpcode',
    'c__EA_RAnalStackOp', 'c__EA_RAnalValueAccess',
    'c__EA_RAnalValueType', 'c__EA_RAnalVarAccessType',
    'c__EA_RAnalVarKind', 'c__EA_RBinDwarfAttrKind',
    'c__EA_RNumCalcToken', 'c__EA__RAnalCond', 'c__EA__RAnalOpType',
    'c__EA__RAnalVarScope', 'c__Ea_R_ANAL_DATA_TYPE_NULL',
    'c__Ea_R_ANAL_DIFF_TYPE_NULL', 'c__Ea_R_ANAL_ESIL_FLAG_ZERO',
    'c__Ea_R_ANAL_ESIL_OP_TYPE_UNKNOWN',
    'c__Ea_R_ANAL_ESIL_PARM_INVALID', 'c__Ea_R_ANAL_FCN_TYPE_NULL',
    'c__Ea_R_ANAL_FQUALIFIER_NONE', 'c__Ea_R_ANAL_REFLINE_TYPE_UTF8',
    'c__Ea_R_ANAL_RET_NOP', 'c__Ea_R_ANAL_TRAP_NONE', 'r_anal_add',
    'r_anal_add_function', 'r_anal_add_import',
    'r_anal_addr_hint_type_t', 'r_anal_addr_hints_at',
    'r_anal_addr_hints_foreach', 'r_anal_arch_hints_foreach',
    'r_anal_archinfo', 'r_anal_base_type_free',
    'r_anal_base_type_new', 'r_anal_bb_from_offset',
    'r_anal_bb_offset_inst', 'r_anal_bb_opaddr_at',
    'r_anal_bb_opaddr_i', 'r_anal_bb_set_offset', 'r_anal_bb_size_i',
    'r_anal_bind', 'r_anal_bits_hints_foreach',
    'r_anal_block_add_switch_case', 'r_anal_block_automerge',
    'r_anal_block_chop_noreturn', 'r_anal_block_merge',
    'r_anal_block_op_starts_at', 'r_anal_block_recurse',
    'r_anal_block_recurse_depth_first',
    'r_anal_block_recurse_followthrough', 'r_anal_block_recurse_list',
    'r_anal_block_ref', 'r_anal_block_relocate',
    'r_anal_block_set_size', 'r_anal_block_shortest_path',
    'r_anal_block_split', 'r_anal_block_successor_addrs_foreach',
    'r_anal_block_unref', 'r_anal_blocks_foreach_in',
    'r_anal_blocks_foreach_intersect', 'r_anal_cc_arg',
    'r_anal_cc_default', 'r_anal_cc_del', 'r_anal_cc_error',
    'r_anal_cc_exist', 'r_anal_cc_func', 'r_anal_cc_get',
    'r_anal_cc_max_arg', 'r_anal_cc_ret', 'r_anal_cc_self',
    'r_anal_cc_set', 'r_anal_check_fcn', 'r_anal_class_base_delete',
    'r_anal_class_base_fini', 'r_anal_class_base_get',
    'r_anal_class_base_get_all', 'r_anal_class_base_set',
    'r_anal_class_create', 'r_anal_class_delete',
    'r_anal_class_exists', 'r_anal_class_foreach',
    'r_anal_class_get_all', 'r_anal_class_get_inheritance_graph',
    'r_anal_class_json', 'r_anal_class_list',
    'r_anal_class_list_bases',
    'r_anal_class_list_vtable_offset_functions',
    'r_anal_class_list_vtables', 'r_anal_class_method_delete',
    'r_anal_class_method_fini', 'r_anal_class_method_get',
    'r_anal_class_method_get_all', 'r_anal_class_method_rename',
    'r_anal_class_method_set', 'r_anal_class_print',
    'r_anal_class_rename', 'r_anal_class_vtable_delete',
    'r_anal_class_vtable_fini', 'r_anal_class_vtable_get',
    'r_anal_class_vtable_get_all', 'r_anal_class_vtable_set',
    'r_anal_colorize_bb', 'r_anal_cond_eval', 'r_anal_cond_fini',
    'r_anal_cond_free', 'r_anal_cond_new', 'r_anal_cond_new_from_op',
    'r_anal_cond_new_from_string', 'r_anal_cond_to_string',
    'r_anal_cond_tostring', 'r_anal_create_block',
    'r_anal_create_function', 'r_anal_cycle_frame_free',
    'r_anal_cycle_frame_new', 'r_anal_data', 'r_anal_data_free',
    'r_anal_data_kind', 'r_anal_data_new', 'r_anal_data_new_string',
    'r_anal_data_to_string', 'r_anal_data_type_t',
    'r_anal_datatype_to_string', 'r_anal_del_jmprefs',
    'r_anal_delete_block', 'r_anal_diff_bb', 'r_anal_diff_eval',
    'r_anal_diff_fcn', 'r_anal_diff_fingerprint_bb',
    'r_anal_diff_fingerprint_fcn', 'r_anal_diff_free',
    'r_anal_diff_new', 'r_anal_diff_setup', 'r_anal_diff_setup_i',
    'r_anal_dwarf_integrate_functions', 'r_anal_dwarf_process_info',
    'r_anal_esil_cfg_expr', 'r_anal_esil_cfg_free',
    'r_anal_esil_cfg_merge_blocks', 'r_anal_esil_cfg_op',
    'r_anal_esil_claim_source', 'r_anal_esil_condition',
    'r_anal_esil_dfg_expr', 'r_anal_esil_dfg_filter',
    'r_anal_esil_dfg_filter_expr', 'r_anal_esil_dfg_free',
    'r_anal_esil_dfg_new', 'r_anal_esil_dfg_node_new',
    'r_anal_esil_dumpstack', 'r_anal_esil_fire_interrupt',
    'r_anal_esil_free', 'r_anal_esil_get_parm',
    'r_anal_esil_get_parm_type', 'r_anal_esil_get_source',
    'r_anal_esil_interrupt_free', 'r_anal_esil_interrupt_new',
    'r_anal_esil_interrupts_fini', 'r_anal_esil_interrupts_init',
    'r_anal_esil_load_interrupts',
    'r_anal_esil_load_interrupts_from_lib', 'r_anal_esil_load_source',
    'r_anal_esil_mem_read', 'r_anal_esil_mem_ro',
    'r_anal_esil_mem_write', 'r_anal_esil_new', 'r_anal_esil_parse',
    'r_anal_esil_pop', 'r_anal_esil_push', 'r_anal_esil_pushnum',
    'r_anal_esil_reg_read', 'r_anal_esil_reg_write',
    'r_anal_esil_release_source', 'r_anal_esil_runword',
    'r_anal_esil_set_interrupt', 'r_anal_esil_set_op',
    'r_anal_esil_set_pc', 'r_anal_esil_setup',
    'r_anal_esil_sources_fini', 'r_anal_esil_sources_init',
    'r_anal_esil_stack_free', 'r_anal_esil_stats',
    'r_anal_esil_to_reil_setup', 'r_anal_esil_trace_free',
    'r_anal_esil_trace_list', 'r_anal_esil_trace_new',
    'r_anal_esil_trace_op', 'r_anal_esil_trace_restore',
    'r_anal_esil_trace_show', 'r_anal_extract_rarg',
    'r_anal_extract_vars', 'r_anal_fcn', 'r_anal_fcn_add_bb',
    'r_anal_fcn_bb', 'r_anal_fcn_bbget_at', 'r_anal_fcn_bbget_in',
    'r_anal_fcn_count', 'r_anal_fcn_del', 'r_anal_fcn_del_locs',
    'r_anal_fcn_format_sig', 'r_anal_fcn_invalidate_read_ahead_cache',
    'r_anal_fcn_next', 'r_anal_fcn_vars_cache_fini',
    'r_anal_fcn_vars_cache_init', 'r_anal_fcntype_tostring',
    'r_anal_free', 'r_anal_function_add_block',
    'r_anal_function_autoname_var', 'r_anal_function_check_bp_use',
    'r_anal_function_complexity', 'r_anal_function_contains',
    'r_anal_function_cost', 'r_anal_function_count_edges',
    'r_anal_function_delete', 'r_anal_function_delete_all_vars',
    'r_anal_function_delete_label', 'r_anal_function_delete_label_at',
    'r_anal_function_delete_var',
    'r_anal_function_delete_vars_by_kind', 'r_anal_function_free',
    'r_anal_function_get_json', 'r_anal_function_get_label',
    'r_anal_function_get_label_at', 'r_anal_function_get_refs',
    'r_anal_function_get_signature', 'r_anal_function_get_var',
    'r_anal_function_get_var_byname',
    'r_anal_function_get_var_fields',
    'r_anal_function_get_var_reg_at',
    'r_anal_function_get_var_stackptr_at',
    'r_anal_function_get_vars_used_at', 'r_anal_function_get_xrefs',
    'r_anal_function_linear_size', 'r_anal_function_loops',
    'r_anal_function_max_addr', 'r_anal_function_min_addr',
    'r_anal_function_new', 'r_anal_function_purity',
    'r_anal_function_realsize', 'r_anal_function_rebase_vars',
    'r_anal_function_relocate', 'r_anal_function_remove_block',
    'r_anal_function_rename', 'r_anal_function_resize',
    'r_anal_function_set_label', 'r_anal_function_set_var',
    'r_anal_function_size_from_entry', 'r_anal_get_base_type',
    'r_anal_get_bbaddr', 'r_anal_get_block_at',
    'r_anal_get_blocks_in', 'r_anal_get_blocks_intersect',
    'r_anal_get_fcn_in', 'r_anal_get_fcn_in_bounds',
    'r_anal_get_fcns', 'r_anal_get_function_at',
    'r_anal_get_function_byname', 'r_anal_get_functions_in',
    'r_anal_get_reg_profile', 'r_anal_get_used_function_var',
    'r_anal_hint_arch_at', 'r_anal_hint_bits_at', 'r_anal_hint_clear',
    'r_anal_hint_del', 'r_anal_hint_free', 'r_anal_hint_get',
    'r_anal_hint_set_arch', 'r_anal_hint_set_bits',
    'r_anal_hint_set_esil', 'r_anal_hint_set_fail',
    'r_anal_hint_set_high', 'r_anal_hint_set_immbase',
    'r_anal_hint_set_jump', 'r_anal_hint_set_newbits',
    'r_anal_hint_set_nword', 'r_anal_hint_set_offset',
    'r_anal_hint_set_opcode', 'r_anal_hint_set_pointer',
    'r_anal_hint_set_ret', 'r_anal_hint_set_size',
    'r_anal_hint_set_stackframe', 'r_anal_hint_set_syntax',
    'r_anal_hint_set_type', 'r_anal_hint_set_val',
    'r_anal_hint_unset_arch', 'r_anal_hint_unset_bits',
    'r_anal_hint_unset_esil', 'r_anal_hint_unset_fail',
    'r_anal_hint_unset_high', 'r_anal_hint_unset_immbase',
    'r_anal_hint_unset_jump', 'r_anal_hint_unset_newbits',
    'r_anal_hint_unset_nword', 'r_anal_hint_unset_offset',
    'r_anal_hint_unset_opcode', 'r_anal_hint_unset_pointer',
    'r_anal_hint_unset_ret', 'r_anal_hint_unset_size',
    'r_anal_hint_unset_stackframe', 'r_anal_hint_unset_syntax',
    'r_anal_hint_unset_type', 'r_anal_hint_unset_val',
    'r_anal_is_prelude', 'r_anal_jmptbl', 'r_anal_list_vtables',
    'r_anal_mask', 'r_anal_new', 'r_anal_noreturn_add',
    'r_anal_noreturn_at', 'r_anal_noreturn_at_addr',
    'r_anal_noreturn_drop', 'r_anal_noreturn_list', 'r_anal_op',
    'r_anal_op_family_from_string', 'r_anal_op_family_to_string',
    'r_anal_op_fini', 'r_anal_op_free', 'r_anal_op_hexstr',
    'r_anal_op_hint', 'r_anal_op_init', 'r_anal_op_is_eob',
    'r_anal_op_ismemref', 'r_anal_op_list_new', 'r_anal_op_new',
    'r_anal_op_nonlinear', 'r_anal_op_reg_delta',
    'r_anal_op_to_string', 'r_anal_optype_from_string',
    'r_anal_optype_to_string', 'r_anal_pin', 'r_anal_pin_call',
    'r_anal_pin_fini', 'r_anal_pin_init', 'r_anal_pin_list',
    'r_anal_pin_unset', 'r_anal_plugin_6502', 'r_anal_plugin_6502_cs',
    'r_anal_plugin_8051', 'r_anal_plugin_amd29k', 'r_anal_plugin_arc',
    'r_anal_plugin_arm_cs', 'r_anal_plugin_arm_gnu',
    'r_anal_plugin_avr', 'r_anal_plugin_bf', 'r_anal_plugin_chip8',
    'r_anal_plugin_cr16', 'r_anal_plugin_cris',
    'r_anal_plugin_dalvik', 'r_anal_plugin_ebc', 'r_anal_plugin_free',
    'r_anal_plugin_gb', 'r_anal_plugin_h8300',
    'r_anal_plugin_hexagon', 'r_anal_plugin_i4004',
    'r_anal_plugin_i8080', 'r_anal_plugin_java',
    'r_anal_plugin_m680x_cs', 'r_anal_plugin_m68k_cs',
    'r_anal_plugin_malbolge', 'r_anal_plugin_mcore',
    'r_anal_plugin_mips_cs', 'r_anal_plugin_mips_gnu',
    'r_anal_plugin_msp430', 'r_anal_plugin_nios2',
    'r_anal_plugin_null', 'r_anal_plugin_or1k', 'r_anal_plugin_pic',
    'r_anal_plugin_ppc_cs', 'r_anal_plugin_ppc_gnu',
    'r_anal_plugin_propeller', 'r_anal_plugin_pyc',
    'r_anal_plugin_riscv', 'r_anal_plugin_riscv_cs',
    'r_anal_plugin_rsp', 'r_anal_plugin_sh', 'r_anal_plugin_snes',
    'r_anal_plugin_sparc_cs', 'r_anal_plugin_sparc_gnu',
    'r_anal_plugin_sysz', 'r_anal_plugin_tms320',
    'r_anal_plugin_tms320c64x', 'r_anal_plugin_tricore',
    'r_anal_plugin_v810', 'r_anal_plugin_v850', 'r_anal_plugin_vax',
    'r_anal_plugin_wasm', 'r_anal_plugin_ws', 'r_anal_plugin_x86',
    'r_anal_plugin_x86_cs', 'r_anal_plugin_x86_im',
    'r_anal_plugin_x86_simple', 'r_anal_plugin_x86_udis',
    'r_anal_plugin_xap', 'r_anal_plugin_xcore_cs',
    'r_anal_plugin_xtensa', 'r_anal_plugin_z80', 'r_anal_preludes',
    'r_anal_purge', 'r_anal_purge_imports', 'r_anal_ref_list_new',
    'r_anal_ref_type_tostring', 'r_anal_reflines_get',
    'r_anal_reflines_middle', 'r_anal_reflines_str',
    'r_anal_reflines_str_free', 'r_anal_refs_get',
    'r_anal_remove_import', 'r_anal_remove_parsed_type',
    'r_anal_rtti_demangle_class_name',
    'r_anal_rtti_itanium_demangle_class_name',
    'r_anal_rtti_itanium_print_at_vtable',
    'r_anal_rtti_itanium_recover_all',
    'r_anal_rtti_msvc_demangle_class_name',
    'r_anal_rtti_msvc_print_at_vtable',
    'r_anal_rtti_msvc_print_base_class_descriptor',
    'r_anal_rtti_msvc_print_class_hierarchy_descriptor',
    'r_anal_rtti_msvc_print_complete_object_locator',
    'r_anal_rtti_msvc_print_type_descriptor',
    'r_anal_rtti_msvc_recover_all', 'r_anal_rtti_print_all',
    'r_anal_rtti_print_at_vtable', 'r_anal_rtti_recover_all',
    'r_anal_save_base_type', 'r_anal_save_parsed_type',
    'r_anal_set_big_endian', 'r_anal_set_bits', 'r_anal_set_cpu',
    'r_anal_set_limits', 'r_anal_set_os', 'r_anal_set_reg_profile',
    'r_anal_set_triplet', 'r_anal_set_user_ptr',
    'r_anal_stackop_tostring', 'r_anal_str_to_fcn',
    'r_anal_switch_op_add_case', 'r_anal_switch_op_free',
    'r_anal_switch_op_new', 'r_anal_trace_bb', 'r_anal_trim_jmprefs',
    'r_anal_types_from_fcn', 'r_anal_unset_limits', 'r_anal_use',
    'r_anal_value_copy', 'r_anal_value_free', 'r_anal_value_new',
    'r_anal_value_new_from_string', 'r_anal_value_set_ut64',
    'r_anal_value_to_string', 'r_anal_value_to_ut64',
    'r_anal_var_add_constraint', 'r_anal_var_addr',
    'r_anal_var_all_list', 'r_anal_var_clear_accesses',
    'r_anal_var_count', 'r_anal_var_delete', 'r_anal_var_display',
    'r_anal_var_get_access_at', 'r_anal_var_get_argnum',
    'r_anal_var_get_constraints_readable', 'r_anal_var_get_dst_var',
    'r_anal_var_list', 'r_anal_var_list_show',
    'r_anal_var_remove_access_at', 'r_anal_var_rename',
    'r_anal_var_set_access', 'r_anal_var_set_type', 'r_anal_version',
    'r_anal_vtable_begin', 'r_anal_vtable_info_free',
    'r_anal_vtable_info_get_size', 'r_anal_vtable_parse_at',
    'r_anal_vtable_search', 'r_anal_xref_del', 'r_anal_xrefs_count',
    'r_anal_xrefs_deln', 'r_anal_xrefs_from', 'r_anal_xrefs_get',
    'r_anal_xrefs_get_from', 'r_anal_xrefs_init', 'r_anal_xrefs_list',
    'r_anal_xrefs_set', 'r_anal_xrefs_type',
    'r_anal_xrefs_type_tostring', 'r_meta_del', 'r_meta_get_all_at',
    'r_meta_get_all_in', 'r_meta_get_all_intersect', 'r_meta_get_at',
    'r_meta_get_in', 'r_meta_get_size', 'r_meta_get_string',
    'r_meta_print', 'r_meta_print_list_all', 'r_meta_print_list_at',
    'r_meta_print_list_in_function', 'r_meta_rebase', 'r_meta_set',
    'r_meta_set_data_at', 'r_meta_set_string',
    'r_meta_set_with_subtype', 'r_meta_space_count_for',
    'r_meta_space_unset_for', 'r_meta_type_to_string',
    'r_parse_pdb_types', 'r_sign_space_count_for',
    'r_sign_space_rename_for', 'r_sign_space_unset_for', 'size_t',
    'struct_R_PDB7_ROOT_STREAM', 'struct__IO_FILE',
    'struct__IO_codecvt', 'struct__IO_marker', 'struct__IO_wide_data',
    'struct_buffer', 'struct_c__SA_RAnalMetaUserItem',
    'struct_c__SA_RBinDwarfBlock', 'struct_c__SA_RBinDwarfCompUnit',
    'struct_c__SA_RBinDwarfCompUnitHdr',
    'struct_c__SA_RBinDwarfDebugInfo', 'struct_c__SA_RBinDwarfDie',
    'struct_c__SA_RNumCalcValue', 'struct_c__SA_RStrBuf',
    'struct_c__SA_RVTableContext', 'struct_c__SA_dict', 'struct_cdb',
    'struct_cdb_hp', 'struct_cdb_hplist', 'struct_cdb_make',
    'struct_dwarf_attr_kind', 'struct_dwarf_attr_kind_0_0',
    'struct_ht_pp_bucket_t', 'struct_ht_pp_kv',
    'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_pj_t', 'struct_ptrace_wrap_instance_t',
    'struct_r_anal_addr_hint_record_t', 'struct_r_anal_attr_t',
    'struct_r_anal_base_class_t', 'struct_r_anal_base_type_enum_t',
    'struct_r_anal_base_type_struct_t', 'struct_r_anal_base_type_t',
    'struct_r_anal_base_type_union_t', 'struct_r_anal_bb_t',
    'struct_r_anal_bind_t', 'struct_r_anal_callbacks_t',
    'struct_r_anal_case_obj_t', 'struct_r_anal_cond_t',
    'struct_r_anal_cycle_frame_t', 'struct_r_anal_cycle_hook_t',
    'struct_r_anal_data_t', 'struct_r_anal_diff_t',
    'struct_r_anal_dwarf_context', 'struct_r_anal_enum_case_t',
    'struct_r_anal_esil_basic_block_t',
    'struct_r_anal_esil_callbacks_t', 'struct_r_anal_esil_cfg_t',
    'struct_r_anal_esil_change_mem_t',
    'struct_r_anal_esil_change_reg_t',
    'struct_r_anal_esil_dfg_node_t', 'struct_r_anal_esil_dfg_t',
    'struct_r_anal_esil_expr_offset_t',
    'struct_r_anal_esil_interrupt_handler_t',
    'struct_r_anal_esil_interrupt_t',
    'struct_r_anal_esil_operation_t', 'struct_r_anal_esil_source_t',
    'struct_r_anal_esil_t', 'struct_r_anal_esil_trace_t',
    'struct_r_anal_esil_word_t', 'struct_r_anal_fcn_meta_t',
    'struct_r_anal_fcn_vars_cache', 'struct_r_anal_func_arg_t',
    'struct_r_anal_function_t', 'struct_r_anal_hint_cb_t',
    'struct_r_anal_hint_t', 'struct_r_anal_meta_item_t',
    'struct_r_anal_method_t', 'struct_r_anal_op_t',
    'struct_r_anal_options_t', 'struct_r_anal_plugin_t',
    'struct_r_anal_range_t', 'struct_r_anal_ref_char',
    'struct_r_anal_ref_t', 'struct_r_anal_refline_t',
    'struct_r_anal_reil', 'struct_r_anal_reil_arg',
    'struct_r_anal_reil_inst', 'struct_r_anal_struct_member_t',
    'struct_r_anal_switch_obj_t', 'struct_r_anal_t',
    'struct_r_anal_type_alloca_t', 'struct_r_anal_type_array_t',
    'struct_r_anal_type_ptr_t', 'struct_r_anal_type_struct_t',
    'struct_r_anal_type_t', 'struct_r_anal_type_union_t',
    'struct_r_anal_type_var_t', 'struct_r_anal_union_member_t',
    'struct_r_anal_value_t', 'struct_r_anal_var_access_t',
    'struct_r_anal_var_constraint_t', 'struct_r_anal_var_field_t',
    'struct_r_anal_var_t', 'struct_r_anal_vtable_t',
    'struct_r_bin_addr_t', 'struct_r_bin_arch_options_t',
    'struct_r_bin_bind_t', 'struct_r_bin_dbginfo_t',
    'struct_r_bin_file_t', 'struct_r_bin_hash_t',
    'struct_r_bin_info_t', 'struct_r_bin_object_t',
    'struct_r_bin_plugin_t', 'struct_r_bin_section_t',
    'struct_r_bin_t', 'struct_r_bin_write_t',
    'struct_r_bin_xtr_extract_t', 'struct_r_bin_xtr_metadata_t',
    'struct_r_bin_xtr_plugin_t', 'struct_r_buf_t',
    'struct_r_buffer_methods_t', 'struct_r_cache_t',
    'struct_r_cons_bind_t', 'struct_r_cons_printable_palette_t',
    'struct_r_containing_rb_node_t', 'struct_r_containing_rb_tree_t',
    'struct_r_core_bind_t', 'struct_r_event_t',
    'struct_r_flag_bind_t', 'struct_r_flag_item_t', 'struct_r_flag_t',
    'struct_r_graph_node_t', 'struct_r_graph_t', 'struct_r_id_pool_t',
    'struct_r_id_storage_t', 'struct_r_interval_node_t',
    'struct_r_interval_t', 'struct_r_interval_tree_t',
    'struct_r_io_bind_t', 'struct_r_io_desc_t', 'struct_r_io_map_t',
    'struct_r_io_plugin_t', 'struct_r_io_t', 'struct_r_io_undo_t',
    'struct_r_io_undos_t', 'struct_r_list_iter_t',
    'struct_r_list_range_t', 'struct_r_list_t', 'struct_r_num_calc_t',
    'struct_r_num_t', 'struct_r_pdb_t', 'struct_r_pvector_t',
    'struct_r_queue_t', 'struct_r_rb_node_t', 'struct_r_reg_arena_t',
    'struct_r_reg_item_t', 'struct_r_reg_set_t', 'struct_r_reg_t',
    'struct_r_skiplist_node_t', 'struct_r_skiplist_t',
    'struct_r_space_t', 'struct_r_spaces_t',
    'struct_r_str_constpool_t', 'struct_r_syscall_item_t',
    'struct_r_syscall_port_t', 'struct_r_syscall_t',
    'struct_r_vector_t', 'struct_sdb_kv', 'struct_sdb_t',
    'struct_vtable_info_t', 'struct_vtable_method_info_t',
    'try_get_delta_jmptbl_info', 'try_get_jmptbl_info',
    'try_walkthrough_casetbl', 'try_walkthrough_jmptbl',
    'union_dwarf_attr_kind_0', 'union_r_anal_addr_hint_record_t_0',
    'union_r_anal_base_type_t_0', 'union_r_anal_type_array_t_0',
    'union_r_anal_type_ptr_t_0', 'union_r_anal_type_var_t_0',
    'walkthrough_arm_jmptbl_style']

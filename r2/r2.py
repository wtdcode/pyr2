# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-I/home/mio/pyr2/radare2/installdir/usr/local/include/libr', '-I/home/mio/pyr2/radare2/installdir/usr/local/include/libr/sdb']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
import distutils.sysconfig
import pkg_resources
import sys
import os
from pathlib import Path

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

_libr_name_dict = { 'darwin': 'libr_core.dylib',
                    'win32': 'r_core.dll',
                    'linux': 'libr_core.so',
                    'linux2': 'libr_core.so' }
try:
    _libr_name = _libr_name_dict[sys.platform]
except KeyError:
    raise ImportError(f"Your platform {sys.platform} is not supported!")

_search_path = [Path(os.path.dirname(os.path.abspath(__file__))) / "libr",
                Path('') / "libr",
                Path("/usr/local/lib/") if sys.platform == 'darwin' else Path('/usr/lib64')]

# Workaround for dll dependencies.
# In Py3.8, we have a better way to do this.
def _load_libr_all(directory: Path):
    if (directory / _libr_name).exists():
        changed = True
        loaded = set()
        while changed:
            changed = False
            for p in directory.iterdir():
                if p in loaded:
                    continue
                if p.is_file() and p.name.endswith("dll"):
                    try:
                        dll = ctypes.cdll.LoadLibrary(str(p))
                        if p.name == _libr_name:
                            return dll
                        if p not in loaded:
                            changed = True
                            loaded.add(p)
                    except OSError:
                        pass
        return None
    else:
        return None

def _load_libr(directory: Path):
    libr_path = directory / _libr_name
    try:
        return ctypes.cdll.LoadLibrary(str(libr_path))
    except OSError:
        return None

for _path in _search_path:
    if sys.platform == "win32":
        _libr = _load_libr_all(_path)
    else:
        _libr = _load_libr(_path)
    if _libr is not None:
        break

if _libr is None:
    raise ImportError("Libr is not found on your system.")

_libraries = {}
_libraries['libr'] = _libr


class struct_r_ascii_node_t(ctypes.Structure):
    pass

class struct_r_graph_node_t(ctypes.Structure):
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

struct_r_ascii_node_t._pack_ = True # source:False
struct_r_ascii_node_t._fields_ = [
    ('gnode', POINTER_T(struct_r_graph_node_t)),
    ('title', POINTER_T(ctypes.c_char)),
    ('body', POINTER_T(ctypes.c_char)),
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
    ('layer', ctypes.c_int32),
    ('layer_height', ctypes.c_int32),
    ('layer_width', ctypes.c_int32),
    ('pos_in_layer', ctypes.c_int32),
    ('is_dummy', ctypes.c_int32),
    ('is_reversed', ctypes.c_int32),
    ('klass', ctypes.c_int32),
    ('difftype', ctypes.c_int32),
    ('is_mini', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

class struct_r_core_graph_hits_t(ctypes.Structure):
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

struct_r_core_graph_hits_t._pack_ = True # source:False
struct_r_core_graph_hits_t._fields_ = [
    ('old_word', POINTER_T(ctypes.c_char)),
    ('word_list', struct_r_vector_t),
    ('word_nth', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct_r_ascii_graph_t(ctypes.Structure):
    pass

class struct_r_cons_canvas_t(ctypes.Structure):
    pass

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

struct_r_cons_canvas_t._pack_ = True # source:False
struct_r_cons_canvas_t._fields_ = [
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
    ('b', POINTER_T(POINTER_T(ctypes.c_char))),
    ('blen', POINTER_T(ctypes.c_int32)),
    ('bsize', POINTER_T(ctypes.c_int32)),
    ('attr', POINTER_T(ctypes.c_char)),
    ('attrs', POINTER_T(struct_ht_up_t)),
    ('constpool', struct_r_str_constpool_t),
    ('sx', ctypes.c_int32),
    ('sy', ctypes.c_int32),
    ('color', ctypes.c_int32),
    ('linemode', ctypes.c_int32),
]

class struct_sdb_t(ctypes.Structure):
    pass

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

class struct_layer_t(ctypes.Structure):
    pass

class struct_r_graph_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('n_nodes', ctypes.c_uint32),
    ('n_edges', ctypes.c_uint32),
    ('last_index', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('nodes', POINTER_T(struct_r_list_t)),
     ]

struct_r_ascii_graph_t._pack_ = True # source:False
struct_r_ascii_graph_t._fields_ = [
    ('can', POINTER_T(struct_r_cons_canvas_t)),
    ('graph', POINTER_T(struct_r_graph_t)),
    ('curnode', POINTER_T(struct_r_graph_node_t)),
    ('title', POINTER_T(ctypes.c_char)),
    ('db', POINTER_T(struct_sdb_t)),
    ('nodes', POINTER_T(struct_sdb_t)),
    ('layout', ctypes.c_int32),
    ('is_instep', ctypes.c_int32),
    ('is_tiny', ctypes.c_bool),
    ('is_dis', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('edgemode', ctypes.c_int32),
    ('mode', ctypes.c_int32),
    ('is_callgraph', ctypes.c_bool),
    ('is_interactive', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('zoom', ctypes.c_int32),
    ('movspeed', ctypes.c_int32),
    ('hints', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 7),
    ('update_seek_on', POINTER_T(struct_r_ascii_node_t)),
    ('need_reload_nodes', ctypes.c_bool),
    ('need_set_layout', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 2),
    ('need_update_dim', ctypes.c_int32),
    ('force_update_seek', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('on_curnode_change', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_ascii_node_t), POINTER_T(None)))),
    ('on_curnode_change_data', POINTER_T(None)),
    ('dummy', ctypes.c_bool),
    ('show_node_titles', ctypes.c_bool),
    ('show_node_body', ctypes.c_bool),
    ('show_node_bubble', ctypes.c_bool),
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('back_edges', POINTER_T(struct_r_list_t)),
    ('long_edges', POINTER_T(struct_r_list_t)),
    ('layers', POINTER_T(struct_layer_t)),
    ('n_layers', ctypes.c_int32),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('dists', POINTER_T(struct_r_list_t)),
    ('edges', POINTER_T(struct_r_list_t)),
    ('ghits', struct_r_core_graph_hits_t),
]

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
class struct_r_anal_plugin_t(ctypes.Structure):
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
class struct_r_anal_esil_t(ctypes.Structure):
    pass

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

class struct_r_flag_bind_t(ctypes.Structure):
    pass

class struct_r_space_t(ctypes.Structure):
    pass

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

class struct_r_anal_hint_cb_t(ctypes.Structure):
    pass

struct_r_anal_hint_cb_t._pack_ = True # source:False
struct_r_anal_hint_cb_t._fields_ = [
    ('on_bits', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_bool))),
]

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

class struct_r_anal_callbacks_t(ctypes.Structure):
    pass

struct_r_anal_callbacks_t._pack_ = True # source:False
struct_r_anal_callbacks_t._fields_ = [
    ('on_fcn_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_delete', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t)))),
    ('on_fcn_rename', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(ctypes.c_char)))),
    ('on_fcn_bb_new', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_anal_t), POINTER_T(None), POINTER_T(struct_r_anal_function_t), POINTER_T(struct_r_anal_bb_t)))),
]

class struct_r_anal_esil_trace_t(ctypes.Structure):
    pass

class struct_r_reg_arena_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', POINTER_T(ctypes.c_ubyte)),
    ('size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

struct_r_anal_esil_trace_t._pack_ = True # source:False
struct_r_anal_esil_trace_t._fields_ = [
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

class struct_r_bin_bind_t(ctypes.Structure):
    pass

class struct_r_bin_t(ctypes.Structure):
    pass

class struct_r_bin_file_t(ctypes.Structure):
    pass

class struct_r_bin_section_t(ctypes.Structure):
    pass

class struct_r_bin_xtr_plugin_t(ctypes.Structure):
    pass

class struct_r_bin_xtr_extract_t(ctypes.Structure):
    pass

class struct_r_buf_t(ctypes.Structure):
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

class struct_r_bin_arch_options_t(ctypes.Structure):
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

class struct_r_io_bind_t(ctypes.Structure):
    pass

class struct_r_io_t(ctypes.Structure):
    pass

class struct_r_io_desc_t(ctypes.Structure):
    pass

class struct_r_cache_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('base', ctypes.c_uint64),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_uint64),
     ]

class struct_ptrace_wrap_instance_t(ctypes.Structure):
    pass

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

class struct_r_pvector_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('v', struct_r_vector_t),
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

class struct_r_io_map_t(ctypes.Structure):
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

class struct_r_reg_t(ctypes.Structure):
    pass

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

class struct_r_syscall_port_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('port', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
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

class struct__IO_FILE(ctypes.Structure):
    pass

class struct__IO_marker(ctypes.Structure):
    pass

class struct__IO_codecvt(ctypes.Structure):
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

class struct_r_bp_arch_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bits', ctypes.c_int32),
    ('length', ctypes.c_int32),
    ('endian', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('bytes', POINTER_T(ctypes.c_ubyte)),
     ]

class struct_r_bp_plugin_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arch', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_int32),
    ('nbps', ctypes.c_int32),
    ('bps', POINTER_T(struct_r_bp_arch_t)),
     ]

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

class struct_r_bp_t(ctypes.Structure):
    pass

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


# values for enumeration 'r_cmd_status_t'
r_cmd_status_t__enumvalues = {
    0: 'R_CMD_STATUS_OK',
    1: 'R_CMD_STATUS_WRONG_ARGS',
    2: 'R_CMD_STATUS_ERROR',
    3: 'R_CMD_STATUS_INVALID',
    4: 'R_CMD_STATUS_EXIT',
}
R_CMD_STATUS_OK = 0
R_CMD_STATUS_WRONG_ARGS = 1
R_CMD_STATUS_ERROR = 2
R_CMD_STATUS_INVALID = 3
R_CMD_STATUS_EXIT = 4
r_cmd_status_t = ctypes.c_int # enum
class struct_r_cmd_macro_label_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', ctypes.c_char * 80),
    ('ptr', POINTER_T(ctypes.c_char)),
     ]

class struct_r_cmd_macro_t(ctypes.Structure):
    pass

struct_r_cmd_macro_t._pack_ = True # source:False
struct_r_cmd_macro_t._fields_ = [
    ('counter', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('brk_value', POINTER_T(ctypes.c_uint64)),
    ('_brk_value', ctypes.c_uint64),
    ('brk', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('cmd', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('user', POINTER_T(None)),
    ('num', POINTER_T(struct_r_num_t)),
    ('labels_n', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('labels', struct_r_cmd_macro_label_t * 20),
    ('macros', POINTER_T(struct_r_list_t)),
]

class struct_r_cmd_item_t(ctypes.Structure):
    pass

struct_r_cmd_item_t._pack_ = True # source:False
struct_r_cmd_item_t._fields_ = [
    ('cmd', ctypes.c_char * 64),
    ('callback', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

class struct_r_cmd_alias_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('count', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('keys', POINTER_T(POINTER_T(ctypes.c_char))),
    ('values', POINTER_T(POINTER_T(ctypes.c_char))),
    ('remote', POINTER_T(ctypes.c_int32)),
     ]

class struct_r_cmd_desc_example_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('example', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
     ]

class struct_r_cmd_desc_help_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('summary', POINTER_T(ctypes.c_char)),
    ('description', POINTER_T(ctypes.c_char)),
    ('args_str', POINTER_T(ctypes.c_char)),
    ('usage', POINTER_T(ctypes.c_char)),
    ('options', POINTER_T(ctypes.c_char)),
    ('group_summary', POINTER_T(ctypes.c_char)),
    ('group_args_str', POINTER_T(ctypes.c_char)),
    ('examples', POINTER_T(struct_r_cmd_desc_example_t)),
     ]


# values for enumeration 'c__EA_RCmdDescType'
c__EA_RCmdDescType__enumvalues = {
    0: 'R_CMD_DESC_TYPE_OLDINPUT',
    1: 'R_CMD_DESC_TYPE_ARGV',
    2: 'R_CMD_DESC_TYPE_GROUP',
}
R_CMD_DESC_TYPE_OLDINPUT = 0
R_CMD_DESC_TYPE_ARGV = 1
R_CMD_DESC_TYPE_GROUP = 2
c__EA_RCmdDescType = ctypes.c_int # enum
class struct_r_cmd_desc_t(ctypes.Structure):
    pass

class union_r_cmd_desc_t_0(ctypes.Union):
    pass

class struct_r_cmd_desc_t_0_1(ctypes.Structure):
    pass

class struct_r_core_t(ctypes.Structure):
    pass

struct_r_cmd_desc_t_0_1._pack_ = True # source:False
struct_r_cmd_desc_t_0_1._fields_ = [
    ('cb', POINTER_T(ctypes.CFUNCTYPE(r_cmd_status_t, POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
]

class struct_r_cmd_desc_t_0_0(ctypes.Structure):
    pass

struct_r_cmd_desc_t_0_0._pack_ = True # source:False
struct_r_cmd_desc_t_0_0._fields_ = [
    ('cb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

union_r_cmd_desc_t_0._pack_ = True # source:False
union_r_cmd_desc_t_0._fields_ = [
    ('_0', struct_r_cmd_desc_t_0_0),
    ('_1', struct_r_cmd_desc_t_0_1),
]

struct_r_cmd_desc_t._pack_ = True # source:False
struct_r_cmd_desc_t._fields_ = [
    ('type', c__EA_RCmdDescType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
    ('parent', POINTER_T(struct_r_cmd_desc_t)),
    ('n_children', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('children', struct_r_pvector_t),
    ('help', POINTER_T(struct_r_cmd_desc_help_t)),
    ('_6', union_r_cmd_desc_t_0),
]

class struct_r_cmd_t(ctypes.Structure):
    pass

struct_r_cmd_t._pack_ = True # source:False
struct_r_cmd_t._fields_ = [
    ('data', POINTER_T(None)),
    ('nullcallback', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('cmds', POINTER_T(struct_r_cmd_item_t) * 255),
    ('macro', struct_r_cmd_macro_t),
    ('lcmds', POINTER_T(struct_r_list_t)),
    ('plist', POINTER_T(struct_r_list_t)),
    ('aliases', struct_r_cmd_alias_t),
    ('language', POINTER_T(None)),
    ('ts_symbols_ht', POINTER_T(struct_ht_up_t)),
    ('root_cmd_desc', POINTER_T(struct_r_cmd_desc_t)),
    ('ht_cmds', POINTER_T(struct_ht_pp_t)),
]

class struct_r_cmd_descriptor_t(ctypes.Structure):
    pass

struct_r_cmd_descriptor_t._pack_ = True # source:False
struct_r_cmd_descriptor_t._fields_ = [
    ('cmd', POINTER_T(ctypes.c_char)),
    ('help_msg', POINTER_T(POINTER_T(ctypes.c_char))),
    ('help_detail', POINTER_T(POINTER_T(ctypes.c_char))),
    ('help_detail2', POINTER_T(POINTER_T(ctypes.c_char))),
    ('sub', POINTER_T(struct_r_cmd_descriptor_t) * 127),
]

class struct_r_core_plugin_t(ctypes.Structure):
    pass

struct_r_core_plugin_t._pack_ = True # source:False
struct_r_core_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('call', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

class struct_r_config_t(ctypes.Structure):
    pass

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

class struct_r_cons_grep_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('strings', ctypes.c_char * 64 * 10),
    ('nstrings', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('str', POINTER_T(ctypes.c_char)),
    ('counter', ctypes.c_int32),
    ('charCounter', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('less', ctypes.c_int32),
    ('hud', ctypes.c_bool),
    ('human', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 2),
    ('json', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('json_path', POINTER_T(ctypes.c_char)),
    ('range_line', ctypes.c_int32),
    ('line', ctypes.c_int32),
    ('sort', ctypes.c_int32),
    ('sort_row', ctypes.c_int32),
    ('sort_invert', ctypes.c_bool),
    ('PADDING_4', ctypes.c_ubyte * 3),
    ('f_line', ctypes.c_int32),
    ('l_line', ctypes.c_int32),
    ('tokens', ctypes.c_int32 * 64),
    ('tokens_used', ctypes.c_int32),
    ('amp', ctypes.c_int32),
    ('zoom', ctypes.c_int32),
    ('zoomy', ctypes.c_int32),
    ('neg', ctypes.c_int32),
    ('begin', ctypes.c_int32),
    ('end', ctypes.c_int32),
    ('icase', ctypes.c_int32),
    ('PADDING_5', ctypes.c_ubyte * 4),
     ]

class struct_rcolor_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('attr', ctypes.c_ubyte),
    ('a', ctypes.c_ubyte),
    ('r', ctypes.c_ubyte),
    ('g', ctypes.c_ubyte),
    ('b', ctypes.c_ubyte),
    ('r2', ctypes.c_ubyte),
    ('g2', ctypes.c_ubyte),
    ('b2', ctypes.c_ubyte),
    ('id16', ctypes.c_byte),
     ]

class struct_r_cons_palette_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('b0x00', struct_rcolor_t),
    ('b0x7f', struct_rcolor_t),
    ('b0xff', struct_rcolor_t),
    ('args', struct_rcolor_t),
    ('bin', struct_rcolor_t),
    ('btext', struct_rcolor_t),
    ('call', struct_rcolor_t),
    ('cjmp', struct_rcolor_t),
    ('cmp', struct_rcolor_t),
    ('comment', struct_rcolor_t),
    ('usercomment', struct_rcolor_t),
    ('creg', struct_rcolor_t),
    ('flag', struct_rcolor_t),
    ('fline', struct_rcolor_t),
    ('floc', struct_rcolor_t),
    ('flow', struct_rcolor_t),
    ('flow2', struct_rcolor_t),
    ('fname', struct_rcolor_t),
    ('help', struct_rcolor_t),
    ('input', struct_rcolor_t),
    ('invalid', struct_rcolor_t),
    ('jmp', struct_rcolor_t),
    ('label', struct_rcolor_t),
    ('math', struct_rcolor_t),
    ('mov', struct_rcolor_t),
    ('nop', struct_rcolor_t),
    ('num', struct_rcolor_t),
    ('offset', struct_rcolor_t),
    ('other', struct_rcolor_t),
    ('pop', struct_rcolor_t),
    ('prompt', struct_rcolor_t),
    ('push', struct_rcolor_t),
    ('crypto', struct_rcolor_t),
    ('reg', struct_rcolor_t),
    ('reset', struct_rcolor_t),
    ('ret', struct_rcolor_t),
    ('swi', struct_rcolor_t),
    ('trap', struct_rcolor_t),
    ('ucall', struct_rcolor_t),
    ('ujmp', struct_rcolor_t),
    ('ai_read', struct_rcolor_t),
    ('ai_write', struct_rcolor_t),
    ('ai_exec', struct_rcolor_t),
    ('ai_seq', struct_rcolor_t),
    ('ai_ascii', struct_rcolor_t),
    ('gui_cflow', struct_rcolor_t),
    ('gui_dataoffset', struct_rcolor_t),
    ('gui_background', struct_rcolor_t),
    ('gui_alt_background', struct_rcolor_t),
    ('gui_border', struct_rcolor_t),
    ('wordhl', struct_rcolor_t),
    ('linehl', struct_rcolor_t),
    ('func_var', struct_rcolor_t),
    ('func_var_type', struct_rcolor_t),
    ('func_var_addr', struct_rcolor_t),
    ('widget_bg', struct_rcolor_t),
    ('widget_sel', struct_rcolor_t),
    ('graph_box', struct_rcolor_t),
    ('graph_box2', struct_rcolor_t),
    ('graph_box3', struct_rcolor_t),
    ('graph_box4', struct_rcolor_t),
    ('graph_true', struct_rcolor_t),
    ('graph_false', struct_rcolor_t),
    ('graph_trufae', struct_rcolor_t),
    ('graph_traced', struct_rcolor_t),
    ('graph_current', struct_rcolor_t),
    ('graph_diff_match', struct_rcolor_t),
    ('graph_diff_unmatch', struct_rcolor_t),
    ('graph_diff_unknown', struct_rcolor_t),
    ('graph_diff_new', struct_rcolor_t),
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

class struct_r_cons_context_t(ctypes.Structure):
    pass

class struct_r_stack_t(ctypes.Structure):
    pass

struct_r_stack_t._pack_ = True # source:False
struct_r_stack_t._fields_ = [
    ('elems', POINTER_T(POINTER_T(None))),
    ('n_elems', ctypes.c_uint32),
    ('top', ctypes.c_int32),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
]


# values for enumeration 'r_log_level'
r_log_level__enumvalues = {
    0: 'R_LOGLVL_SILLY',
    1: 'R_LOGLVL_DEBUG',
    2: 'R_LOGLVL_VERBOSE',
    3: 'R_LOGLVL_INFO',
    4: 'R_LOGLVL_WARN',
    5: 'R_LOGLVL_ERROR',
    6: 'R_LOGLVL_FATAL',
    255: 'R_LOGLVL_NONE',
}
R_LOGLVL_SILLY = 0
R_LOGLVL_DEBUG = 1
R_LOGLVL_VERBOSE = 2
R_LOGLVL_INFO = 3
R_LOGLVL_WARN = 4
R_LOGLVL_ERROR = 5
R_LOGLVL_FATAL = 6
R_LOGLVL_NONE = 255
r_log_level = ctypes.c_int # enum
struct_r_cons_context_t._pack_ = True # source:False
struct_r_cons_context_t._fields_ = [
    ('grep', struct_r_cons_grep_t),
    ('cons_stack', POINTER_T(struct_r_stack_t)),
    ('buffer', POINTER_T(ctypes.c_char)),
    ('buffer_len', ctypes.c_uint64),
    ('buffer_sz', ctypes.c_uint64),
    ('breaked', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('break_stack', POINTER_T(struct_r_stack_t)),
    ('event_interrupt', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('event_interrupt_data', POINTER_T(None)),
    ('cmd_depth', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('log_callback', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint32, r_log_level, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('lastOutput', POINTER_T(ctypes.c_char)),
    ('lastLength', ctypes.c_int32),
    ('lastMode', ctypes.c_bool),
    ('lastEnabled', ctypes.c_bool),
    ('is_interactive', ctypes.c_bool),
    ('pageable', ctypes.c_bool),
    ('color_mode', ctypes.c_int32),
    ('cpal', struct_r_cons_palette_t),
    ('PADDING_2', ctypes.c_ubyte * 6),
    ('pal', struct_r_cons_printable_palette_t),
]

class struct_r_cons_t(ctypes.Structure):
    pass

class struct_termios(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('c_iflag', ctypes.c_uint32),
    ('c_oflag', ctypes.c_uint32),
    ('c_cflag', ctypes.c_uint32),
    ('c_lflag', ctypes.c_uint32),
    ('c_line', ctypes.c_ubyte),
    ('c_cc', ctypes.c_ubyte * 32),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('c_ispeed', ctypes.c_uint32),
    ('c_ospeed', ctypes.c_uint32),
     ]

class struct_r_line_t(ctypes.Structure):
    pass

class struct_r_line_buffer_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('data', ctypes.c_char * 4096),
    ('index', ctypes.c_int32),
    ('length', ctypes.c_int32),
     ]

class struct_r_line_comp_t(ctypes.Structure):
    pass


# values for enumeration 'c__EA_RLinePromptType'
c__EA_RLinePromptType__enumvalues = {
    0: 'R_LINE_PROMPT_DEFAULT',
    1: 'R_LINE_PROMPT_OFFSET',
    2: 'R_LINE_PROMPT_FILE',
}
R_LINE_PROMPT_DEFAULT = 0
R_LINE_PROMPT_OFFSET = 1
R_LINE_PROMPT_FILE = 2
c__EA_RLinePromptType = ctypes.c_int # enum
struct_r_line_comp_t._pack_ = True # source:False
struct_r_line_comp_t._fields_ = [
    ('opt', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('args_limit', ctypes.c_uint64),
    ('quit', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('args', struct_r_pvector_t),
    ('run', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_comp_t), POINTER_T(struct_r_line_buffer_t), c__EA_RLinePromptType, POINTER_T(None)))),
    ('run_user', POINTER_T(None)),
]

class struct_r_hud_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('current_entry_n', ctypes.c_int32),
    ('top_entry_n', ctypes.c_int32),
    ('activate', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('vi', ctypes.c_int32),
     ]

class struct_r_selection_widget_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('options', POINTER_T(POINTER_T(ctypes.c_char))),
    ('options_len', ctypes.c_int32),
    ('selection', ctypes.c_int32),
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
    ('scroll', ctypes.c_int32),
    ('complete_common', ctypes.c_bool),
    ('direction', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

class struct_r_line_hist_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('data', POINTER_T(POINTER_T(ctypes.c_char))),
    ('size', ctypes.c_int32),
    ('index', ctypes.c_int32),
    ('top', ctypes.c_int32),
    ('autosave', ctypes.c_int32),
     ]

struct_r_line_t._pack_ = True # source:False
struct_r_line_t._fields_ = [
    ('completion', struct_r_line_comp_t),
    ('buffer', struct_r_line_buffer_t),
    ('history', struct_r_line_hist_t),
    ('sel_widget', POINTER_T(struct_r_selection_widget_t)),
    ('cb_history_up', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_t)))),
    ('cb_history_down', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_t)))),
    ('cb_editor', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cb_fkey', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_int32))),
    ('echo', ctypes.c_int32),
    ('has_echo', ctypes.c_int32),
    ('prompt', POINTER_T(ctypes.c_char)),
    ('kill_ring', POINTER_T(struct_r_list_t)),
    ('kill_ring_ptr', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('clipboard', POINTER_T(ctypes.c_char)),
    ('disable', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('user', POINTER_T(None)),
    ('hist_up', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('hist_down', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('contents', POINTER_T(ctypes.c_char)),
    ('zerosep', ctypes.c_bool),
    ('enable_vi_mode', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 2),
    ('vi_mode', ctypes.c_int32),
    ('prompt_mode', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 3),
    ('prompt_type', c__EA_RLinePromptType),
    ('offset_hist_index', ctypes.c_int32),
    ('file_hist_index', ctypes.c_int32),
    ('hud', POINTER_T(struct_r_hud_t)),
    ('sdbshell_hist', POINTER_T(struct_r_list_t)),
    ('sdbshell_hist_iter', POINTER_T(struct_r_list_iter_t)),
    ('vtmode', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
]

struct_r_cons_t._pack_ = True # source:False
struct_r_cons_t._fields_ = [
    ('context', POINTER_T(struct_r_cons_context_t)),
    ('lastline', POINTER_T(ctypes.c_char)),
    ('is_html', ctypes.c_bool),
    ('was_html', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('lines', ctypes.c_int32),
    ('rows', ctypes.c_int32),
    ('echo', ctypes.c_int32),
    ('fps', ctypes.c_int32),
    ('columns', ctypes.c_int32),
    ('force_rows', ctypes.c_int32),
    ('force_columns', ctypes.c_int32),
    ('fix_rows', ctypes.c_int32),
    ('fix_columns', ctypes.c_int32),
    ('break_lines', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('noflush', ctypes.c_int32),
    ('show_autocomplete_widget', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 7),
    ('fdin', POINTER_T(struct__IO_FILE)),
    ('fdout', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('teefile', POINTER_T(ctypes.c_char)),
    ('user_fgets', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('event_resize', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('event_data', POINTER_T(None)),
    ('mouse_event', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('cb_editor', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
    ('cb_break', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('cb_sleep_begin', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None)))),
    ('cb_sleep_end', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None)))),
    ('cb_click', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_int32, ctypes.c_int32))),
    ('cb_task_oneshot', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None), POINTER_T(None)))),
    ('cb_fkey', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_int32))),
    ('user', POINTER_T(None)),
    ('term_raw', struct_termios),
    ('term_buf', struct_termios),
    ('num', POINTER_T(struct_r_num_t)),
    ('pager', POINTER_T(ctypes.c_char)),
    ('blankline', ctypes.c_int32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('highlight', POINTER_T(ctypes.c_char)),
    ('enable_highlight', ctypes.c_bool),
    ('PADDING_6', ctypes.c_ubyte * 3),
    ('null', ctypes.c_int32),
    ('mouse', ctypes.c_int32),
    ('is_wine', ctypes.c_int32),
    ('line', POINTER_T(struct_r_line_t)),
    ('vline', POINTER_T(POINTER_T(ctypes.c_char))),
    ('refcnt', ctypes.c_int32),
    ('newline', ctypes.c_bool),
    ('PADDING_7', ctypes.c_ubyte * 3),
    ('vtmode', ctypes.c_int32),
    ('flush', ctypes.c_bool),
    ('use_utf8', ctypes.c_bool),
    ('use_utf8_curvy', ctypes.c_bool),
    ('dotted_lines', ctypes.c_bool),
    ('linesleep', ctypes.c_int32),
    ('pagesize', ctypes.c_int32),
    ('break_word', POINTER_T(ctypes.c_char)),
    ('break_word_len', ctypes.c_int32),
    ('PADDING_8', ctypes.c_ubyte * 4),
    ('timeout', ctypes.c_uint64),
    ('grep_color', ctypes.c_bool),
    ('grep_highlight', ctypes.c_bool),
    ('use_tts', ctypes.c_bool),
    ('filter', ctypes.c_bool),
    ('PADDING_9', ctypes.c_ubyte * 4),
    ('rgbstr', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64))),
    ('click_set', ctypes.c_bool),
    ('PADDING_10', ctypes.c_ubyte * 3),
    ('click_x', ctypes.c_int32),
    ('click_y', ctypes.c_int32),
    ('show_vals', ctypes.c_bool),
    ('PADDING_11', ctypes.c_ubyte * 3),
]

RLinePromptType = c__EA_RLinePromptType
RLinePromptType__enumvalues = c__EA_RLinePromptType__enumvalues
class struct_r_panels_menu_item(ctypes.Structure):
    pass

class struct_r_panel_t(ctypes.Structure):
    pass

class struct_r_panel_model_t(ctypes.Structure):
    pass


# values for enumeration 'c__EA_RPanelType'
c__EA_RPanelType__enumvalues = {
    0: 'PANEL_TYPE_DEFAULT',
    1: 'PANEL_TYPE_MENU',
}
PANEL_TYPE_DEFAULT = 0
PANEL_TYPE_MENU = 1
c__EA_RPanelType = ctypes.c_int # enum
struct_r_panel_model_t._pack_ = True # source:False
struct_r_panel_model_t._fields_ = [
    ('directionCb', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_int32))),
    ('rotateCb', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_bool))),
    ('print_cb', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None)))),
    ('type', c__EA_RPanelType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('cmd', POINTER_T(ctypes.c_char)),
    ('title', POINTER_T(ctypes.c_char)),
    ('baseAddr', ctypes.c_uint64),
    ('addr', ctypes.c_uint64),
    ('cache', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('cmdStrCache', POINTER_T(ctypes.c_char)),
    ('readOnly', POINTER_T(ctypes.c_char)),
    ('funcName', POINTER_T(ctypes.c_char)),
    ('filter', POINTER_T(POINTER_T(ctypes.c_char))),
    ('n_filter', ctypes.c_int32),
    ('rotate', ctypes.c_int32),
]

class struct_r_panel_view_t(ctypes.Structure):
    pass

class struct_r_panel_pos_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
     ]

struct_r_panel_view_t._pack_ = True # source:False
struct_r_panel_view_t._fields_ = [
    ('pos', struct_r_panel_pos_t),
    ('prevPos', struct_r_panel_pos_t),
    ('sx', ctypes.c_int32),
    ('sy', ctypes.c_int32),
    ('curpos', ctypes.c_int32),
    ('refresh', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('edge', ctypes.c_int32),
]

struct_r_panel_t._pack_ = True # source:False
struct_r_panel_t._fields_ = [
    ('model', POINTER_T(struct_r_panel_model_t)),
    ('view', POINTER_T(struct_r_panel_view_t)),
]

struct_r_panels_menu_item._pack_ = True # source:False
struct_r_panels_menu_item._fields_ = [
    ('n_sub', ctypes.c_int32),
    ('selectedIndex', ctypes.c_int32),
    ('name', POINTER_T(ctypes.c_char)),
    ('sub', POINTER_T(POINTER_T(struct_r_panels_menu_item))),
    ('cb', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))),
    ('p', POINTER_T(struct_r_panel_t)),
]

class struct_r_panels_menu_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('root', POINTER_T(struct_r_panels_menu_item)),
    ('history', POINTER_T(POINTER_T(struct_r_panels_menu_item))),
    ('depth', ctypes.c_int32),
    ('n_refresh', ctypes.c_int32),
    ('refreshPanels', POINTER_T(POINTER_T(struct_r_panel_t))),
     ]


# values for enumeration 'c__EA_RPanelsMode'
c__EA_RPanelsMode__enumvalues = {
    0: 'PANEL_MODE_DEFAULT',
    1: 'PANEL_MODE_MENU',
    2: 'PANEL_MODE_ZOOM',
    3: 'PANEL_MODE_WINDOW',
    4: 'PANEL_MODE_HELP',
}
PANEL_MODE_DEFAULT = 0
PANEL_MODE_MENU = 1
PANEL_MODE_ZOOM = 2
PANEL_MODE_WINDOW = 3
PANEL_MODE_HELP = 4
c__EA_RPanelsMode = ctypes.c_int # enum

# values for enumeration 'c__EA_RPanelsFun'
c__EA_RPanelsFun__enumvalues = {
    0: 'PANEL_FUN_SNOW',
    1: 'PANEL_FUN_SAKURA',
    2: 'PANEL_FUN_NOFUN',
}
PANEL_FUN_SNOW = 0
PANEL_FUN_SAKURA = 1
PANEL_FUN_NOFUN = 2
c__EA_RPanelsFun = ctypes.c_int # enum

# values for enumeration 'c__EA_RPanelsLayout'
c__EA_RPanelsLayout__enumvalues = {
    0: 'PANEL_LAYOUT_DEFAULT_STATIC',
    1: 'PANEL_LAYOUT_DEFAULT_DYNAMIC',
}
PANEL_LAYOUT_DEFAULT_STATIC = 0
PANEL_LAYOUT_DEFAULT_DYNAMIC = 1
c__EA_RPanelsLayout = ctypes.c_int # enum
class struct_r_panels_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('can', POINTER_T(struct_r_cons_canvas_t)),
    ('panel', POINTER_T(POINTER_T(struct_r_panel_t))),
    ('n_panels', ctypes.c_int32),
    ('columnWidth', ctypes.c_int32),
    ('curnode', ctypes.c_int32),
    ('mouse_orig_x', ctypes.c_int32),
    ('mouse_orig_y', ctypes.c_int32),
    ('autoUpdate', ctypes.c_bool),
    ('mouse_on_edge_x', ctypes.c_bool),
    ('mouse_on_edge_y', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte),
    ('panels_menu', POINTER_T(struct_r_panels_menu_t)),
    ('db', POINTER_T(struct_sdb_t)),
    ('rotate_db', POINTER_T(struct_sdb_t)),
    ('almighty_db', POINTER_T(struct_sdb_t)),
    ('mht', POINTER_T(struct_ht_pp_t)),
    ('mode', c__EA_RPanelsMode),
    ('fun', c__EA_RPanelsFun),
    ('prevMode', c__EA_RPanelsMode),
    ('layout', c__EA_RPanelsLayout),
    ('snows', POINTER_T(struct_r_list_t)),
    ('name', POINTER_T(ctypes.c_char)),
     ]


# values for enumeration 'c__EA_RPanelsRootState'
c__EA_RPanelsRootState__enumvalues = {
    0: 'DEFAULT',
    1: 'ROTATE',
    2: 'DEL',
    3: 'QUIT',
}
DEFAULT = 0
ROTATE = 1
DEL = 2
QUIT = 3
c__EA_RPanelsRootState = ctypes.c_int # enum
class struct_r_panels_root_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('n_panels', ctypes.c_int32),
    ('cur_panels', ctypes.c_int32),
    ('pdc_caches', POINTER_T(struct_sdb_t)),
    ('cur_pdc_cache', POINTER_T(struct_sdb_t)),
    ('panels', POINTER_T(POINTER_T(struct_r_panels_t))),
    ('root_state', c__EA_RPanelsRootState),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]


# values for enumeration 'c__EA_RDebugRecoilMode'
c__EA_RDebugRecoilMode__enumvalues = {
    0: 'R_DBG_RECOIL_NONE',
    1: 'R_DBG_RECOIL_STEP',
    2: 'R_DBG_RECOIL_CONTINUE',
}
R_DBG_RECOIL_NONE = 0
R_DBG_RECOIL_STEP = 1
R_DBG_RECOIL_CONTINUE = 2
c__EA_RDebugRecoilMode = ctypes.c_int # enum
class struct_r_debug_reason_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_int32),
    ('tid', ctypes.c_int32),
    ('signum', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('bp_addr', ctypes.c_uint64),
    ('timestamp', ctypes.c_uint64),
    ('addr', ctypes.c_uint64),
    ('ptr', ctypes.c_uint64),
     ]

class struct_r_debug_map_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('addr_end', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('file', POINTER_T(ctypes.c_char)),
    ('perm', ctypes.c_int32),
    ('user', ctypes.c_int32),
    ('shared', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
     ]

class struct_r_debug_checkpoint_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cnum', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arena', POINTER_T(struct_r_reg_arena_t) * 8),
    ('snaps', POINTER_T(struct_r_list_t)),
     ]

class struct_r_debug_session_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('cnum', ctypes.c_uint32),
    ('maxcnum', ctypes.c_uint32),
    ('cur_chkpt', POINTER_T(struct_r_debug_checkpoint_t)),
    ('checkpoints', POINTER_T(struct_r_vector_t)),
    ('memory', POINTER_T(struct_ht_up_t)),
    ('registers', POINTER_T(struct_ht_up_t)),
    ('reasontype', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('bp', POINTER_T(struct_r_bp_item_t)),
     ]

class struct_r_debug_trace_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('traces', POINTER_T(struct_r_list_t)),
    ('count', ctypes.c_int32),
    ('enabled', ctypes.c_int32),
    ('tag', ctypes.c_int32),
    ('dup', ctypes.c_int32),
    ('addresses', POINTER_T(ctypes.c_char)),
    ('ht', POINTER_T(struct_ht_pp_t)),
     ]

class struct_r_debug_t(ctypes.Structure):
    pass

class struct_r_tree_t(ctypes.Structure):
    pass

class struct_r_tree_node_t(ctypes.Structure):
    pass

struct_r_tree_node_t._pack_ = True # source:False
struct_r_tree_node_t._fields_ = [
    ('parent', POINTER_T(struct_r_tree_node_t)),
    ('tree', POINTER_T(struct_r_tree_t)),
    ('children', POINTER_T(struct_r_list_t)),
    ('n_children', ctypes.c_uint32),
    ('depth', ctypes.c_int32),
    ('free', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))),
    ('data', POINTER_T(None)),
]

struct_r_tree_t._pack_ = True # source:False
struct_r_tree_t._fields_ = [
    ('root', POINTER_T(struct_r_tree_node_t)),
]

class struct_r_egg_t(ctypes.Structure):
    pass

class struct_r_egg_lang_t(ctypes.Structure):
    pass

class struct_r_egg_lang_t_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('body', POINTER_T(ctypes.c_char)),
     ]

class struct_r_egg_lang_t_2(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('content', POINTER_T(ctypes.c_char)),
     ]

class struct_r_egg_lang_t_1(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('arg', POINTER_T(ctypes.c_char)),
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
    ('lang', struct_r_egg_lang_t),
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

class struct_r_debug_plugin_t(ctypes.Structure):
    pass

class struct_r_debug_desc_plugin_t(ctypes.Structure):
    pass

struct_r_debug_desc_plugin_t._pack_ = True # source:False
struct_r_debug_desc_plugin_t._fields_ = [
    ('open', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('close', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32))),
    ('read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32))),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32))),
    ('seek', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_uint64))),
    ('dup', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32))),
    ('list', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), ctypes.c_int32))),
]

class struct_r_debug_info_t(ctypes.Structure):
    pass

struct_r_debug_plugin_t._pack_ = True # source:False
struct_r_debug_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('author', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arch', POINTER_T(ctypes.c_char)),
    ('canstep', ctypes.c_int32),
    ('keepio', ctypes.c_int32),
    ('info', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_debug_info_t), POINTER_T(struct_r_debug_t), POINTER_T(ctypes.c_char)))),
    ('startv', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('attach', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('detach', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('select', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, ctypes.c_int32))),
    ('threads', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('pids', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('tids', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('backtrace', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(POINTER_T(None)), POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('stop', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t)))),
    ('step', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t)))),
    ('step_over', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t)))),
    ('cont', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32))),
    ('wait', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32))),
    ('gcore', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_debug_t), POINTER_T(struct_r_buf_t)))),
    ('kill', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_debug_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32))),
    ('kill_list', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t)))),
    ('contsc', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, ctypes.c_int32))),
    ('frames', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t), ctypes.c_uint64))),
    ('breakpoint', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_bp_t), POINTER_T(struct_r_bp_item_t), ctypes.c_bool))),
    ('reg_read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('reg_write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('reg_profile', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(struct_r_debug_t)))),
    ('set_reg_profile', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('map_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t)))),
    ('modules_get', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_list_t), POINTER_T(struct_r_debug_t)))),
    ('map_alloc', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_debug_map_t), POINTER_T(struct_r_debug_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_bool))),
    ('map_dealloc', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_uint64, ctypes.c_int32))),
    ('map_protect', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32))),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t)))),
    ('drx', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_debug_t), ctypes.c_int32, ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32))),
    ('desc', struct_r_debug_desc_plugin_t),
]

struct_r_debug_t._pack_ = True # source:False
struct_r_debug_t._fields_ = [
    ('arch', POINTER_T(ctypes.c_char)),
    ('bits', ctypes.c_int32),
    ('hitinfo', ctypes.c_int32),
    ('main_pid', ctypes.c_int32),
    ('pid', ctypes.c_int32),
    ('tid', ctypes.c_int32),
    ('forked_pid', ctypes.c_int32),
    ('n_threads', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('threads', POINTER_T(struct_r_list_t)),
    ('malloc', POINTER_T(ctypes.c_char)),
    ('bpsize', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('btalgo', POINTER_T(ctypes.c_char)),
    ('btdepth', ctypes.c_int32),
    ('regcols', ctypes.c_int32),
    ('swstep', ctypes.c_int32),
    ('stop_all_threads', ctypes.c_int32),
    ('trace_forks', ctypes.c_int32),
    ('trace_execs', ctypes.c_int32),
    ('trace_aftersyscall', ctypes.c_int32),
    ('trace_clone', ctypes.c_int32),
    ('follow_child', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('glob_libs', POINTER_T(ctypes.c_char)),
    ('glob_unlibs', POINTER_T(ctypes.c_char)),
    ('consbreak', ctypes.c_bool),
    ('continue_all_threads', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 2),
    ('steps', ctypes.c_int32),
    ('reason', struct_r_debug_reason_t),
    ('recoil_mode', c__EA_RDebugRecoilMode),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('stopaddr', ctypes.c_uint64),
    ('trace', POINTER_T(struct_r_debug_trace_t)),
    ('tracenodes', POINTER_T(struct_sdb_t)),
    ('tree', POINTER_T(struct_r_tree_t)),
    ('call_frames', POINTER_T(struct_r_list_t)),
    ('reg', POINTER_T(struct_r_reg_t)),
    ('q_regs', POINTER_T(struct_r_list_t)),
    ('creg', POINTER_T(ctypes.c_char)),
    ('bp', POINTER_T(struct_r_bp_t)),
    ('user', POINTER_T(None)),
    ('snap_path', POINTER_T(ctypes.c_char)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('iob', struct_r_io_bind_t),
    ('h', POINTER_T(struct_r_debug_plugin_t)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('pc_at_bp', ctypes.c_bool),
    ('pc_at_bp_set', ctypes.c_bool),
    ('PADDING_5', ctypes.c_ubyte * 6),
    ('ev', POINTER_T(struct_r_event_t)),
    ('anal', POINTER_T(struct_r_anal_t)),
    ('maps', POINTER_T(struct_r_list_t)),
    ('maps_user', POINTER_T(struct_r_list_t)),
    ('trace_continue', ctypes.c_bool),
    ('PADDING_6', ctypes.c_ubyte * 7),
    ('cur_op', POINTER_T(struct_r_anal_op_t)),
    ('session', POINTER_T(struct_r_debug_session_t)),
    ('sgnls', POINTER_T(struct_sdb_t)),
    ('corebind', struct_r_core_bind_t),
    ('_mode', ctypes.c_int32),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('num', POINTER_T(struct_r_num_t)),
    ('egg', POINTER_T(struct_r_egg_t)),
    ('verbose', ctypes.c_bool),
    ('main_arena_resolved', ctypes.c_bool),
    ('PADDING_8', ctypes.c_ubyte * 2),
    ('glibc_version', ctypes.c_int32),
]

struct_r_debug_info_t._pack_ = True # source:False
struct_r_debug_info_t._fields_ = [
    ('pid', ctypes.c_int32),
    ('tid', ctypes.c_int32),
    ('uid', ctypes.c_int32),
    ('gid', ctypes.c_int32),
    ('usr', POINTER_T(ctypes.c_char)),
    ('exe', POINTER_T(ctypes.c_char)),
    ('cmdline', POINTER_T(ctypes.c_char)),
    ('libname', POINTER_T(ctypes.c_char)),
    ('cwd', POINTER_T(ctypes.c_char)),
    ('status', ctypes.c_int32),
    ('signum', ctypes.c_int32),
    ('lib', POINTER_T(None)),
    ('thread', POINTER_T(None)),
    ('kernel_stack', POINTER_T(ctypes.c_char)),
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

class struct_r_fs_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iob', struct_r_io_bind_t),
    ('cob', struct_r_core_bind_t),
    ('csb', struct_r_cons_bind_t),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('roots', POINTER_T(struct_r_list_t)),
    ('view', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ptr', POINTER_T(None)),
     ]

class struct_r_fs_shell_t(ctypes.Structure):
    pass

struct_r_fs_shell_t._pack_ = True # source:False
struct_r_fs_shell_t._fields_ = [
    ('cwd', POINTER_T(POINTER_T(ctypes.c_char))),
    ('set_prompt', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char)))),
    ('readline', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char)))),
    ('hist_add', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
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

class struct_r_lang_t(ctypes.Structure):
    pass

class struct_r_lang_plugin_t(ctypes.Structure):
    pass

struct_r_lang_plugin_t._pack_ = True # source:False
struct_r_lang_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('alias', POINTER_T(ctypes.c_char)),
    ('desc', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('help', POINTER_T(POINTER_T(ctypes.c_char))),
    ('ext', POINTER_T(ctypes.c_char)),
    ('init', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('setup', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_lang_t)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('prompt', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t)))),
    ('run', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('run_file', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), POINTER_T(ctypes.c_char)))),
    ('set_argv', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_lang_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
]

struct_r_lang_t._pack_ = True # source:False
struct_r_lang_t._fields_ = [
    ('cur', POINTER_T(struct_r_lang_plugin_t)),
    ('user', POINTER_T(None)),
    ('defs', POINTER_T(struct_r_list_t)),
    ('langs', POINTER_T(struct_r_list_t)),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('cmd_str', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmdf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

class struct_r_lib_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('symname', POINTER_T(ctypes.c_char)),
    ('symnamefunc', POINTER_T(ctypes.c_char)),
    ('plugins', POINTER_T(struct_r_list_t)),
    ('handlers', POINTER_T(struct_r_list_t)),
     ]

class struct_r_search_keyword_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bin_keyword', POINTER_T(ctypes.c_ubyte)),
    ('bin_binmask', POINTER_T(ctypes.c_ubyte)),
    ('keyword_length', ctypes.c_uint32),
    ('binmask_length', ctypes.c_uint32),
    ('data', POINTER_T(None)),
    ('count', ctypes.c_int32),
    ('kwidx', ctypes.c_int32),
    ('icase', ctypes.c_int32),
    ('type', ctypes.c_int32),
    ('last', ctypes.c_uint64),
     ]

class struct_r_search_t(ctypes.Structure):
    pass

struct_r_search_t._pack_ = True # source:False
struct_r_search_t._fields_ = [
    ('n_kws', ctypes.c_int32),
    ('mode', ctypes.c_int32),
    ('pattern_size', ctypes.c_uint32),
    ('string_min', ctypes.c_uint32),
    ('string_max', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('data', POINTER_T(None)),
    ('user', POINTER_T(None)),
    ('callback', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_search_keyword_t), POINTER_T(None), ctypes.c_uint64))),
    ('nhits', ctypes.c_uint64),
    ('maxhits', ctypes.c_uint64),
    ('hits', POINTER_T(struct_r_list_t)),
    ('distance', ctypes.c_int32),
    ('inverse', ctypes.c_int32),
    ('overlap', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('contiguous', ctypes.c_int32),
    ('align', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('update', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_search_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('kws', POINTER_T(struct_r_list_t)),
    ('iob', struct_r_io_bind_t),
    ('bckwrds', ctypes.c_char),
    ('PADDING_3', ctypes.c_ubyte * 7),
]

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


# values for enumeration 'c__EA_RThreadFunctionRet'
c__EA_RThreadFunctionRet__enumvalues = {
    -1: 'R_TH_FREED',
    0: 'R_TH_STOP',
    1: 'R_TH_REPEAT',
}
R_TH_FREED = -1
R_TH_STOP = 0
R_TH_REPEAT = 1
c__EA_RThreadFunctionRet = ctypes.c_int # enum
class struct_r_th_sem_t(ctypes.Structure):
    pass

class union_c__UA_sem_t(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('__size', ctypes.c_char * 32),
    ('__align', ctypes.c_int64),
    ('PADDING_0', ctypes.c_ubyte * 24),
     ]

struct_r_th_sem_t._pack_ = True # source:False
struct_r_th_sem_t._fields_ = [
    ('sem', POINTER_T(union_c__UA_sem_t)),
]

class struct_r_th_lock_t(ctypes.Structure):
    pass

class union_c__UA_pthread_mutex_t(ctypes.Union):
    pass

class struct___pthread_mutex_s(ctypes.Structure):
    pass

class struct___pthread_internal_list(ctypes.Structure):
    pass

struct___pthread_internal_list._pack_ = True # source:False
struct___pthread_internal_list._fields_ = [
    ('__prev', POINTER_T(struct___pthread_internal_list)),
    ('__next', POINTER_T(struct___pthread_internal_list)),
]

struct___pthread_mutex_s._pack_ = True # source:False
struct___pthread_mutex_s._fields_ = [
    ('__lock', ctypes.c_int32),
    ('__count', ctypes.c_uint32),
    ('__owner', ctypes.c_int32),
    ('__nusers', ctypes.c_uint32),
    ('__kind', ctypes.c_int32),
    ('__spins', ctypes.c_int16),
    ('__elision', ctypes.c_int16),
    ('__list', struct___pthread_internal_list),
]

union_c__UA_pthread_mutex_t._pack_ = True # source:False
union_c__UA_pthread_mutex_t._fields_ = [
    ('__data', struct___pthread_mutex_s),
    ('__size', ctypes.c_char * 40),
    ('__align', ctypes.c_int64),
    ('PADDING_0', ctypes.c_ubyte * 32),
]

struct_r_th_lock_t._pack_ = True # source:False
struct_r_th_lock_t._fields_ = [
    ('lock', union_c__UA_pthread_mutex_t),
]

class struct_r_th_cond_t(ctypes.Structure):
    pass

class union_c__UA_pthread_cond_t(ctypes.Union):
    pass

class struct___pthread_cond_s(ctypes.Structure):
    pass

class union___pthread_cond_s_1(ctypes.Union):
    pass

class struct___pthread_cond_s_1_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('__low', ctypes.c_uint32),
    ('__high', ctypes.c_uint32),
     ]

union___pthread_cond_s_1._pack_ = True # source:False
union___pthread_cond_s_1._fields_ = [
    ('__g1_start', ctypes.c_uint64),
    ('_1', struct___pthread_cond_s_1_0),
]

class union___pthread_cond_s_0(ctypes.Union):
    pass

class struct___pthread_cond_s_0_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('__low', ctypes.c_uint32),
    ('__high', ctypes.c_uint32),
     ]

union___pthread_cond_s_0._pack_ = True # source:False
union___pthread_cond_s_0._fields_ = [
    ('__wseq', ctypes.c_uint64),
    ('_1', struct___pthread_cond_s_0_0),
]

struct___pthread_cond_s._pack_ = True # source:False
struct___pthread_cond_s._fields_ = [
    ('_0', union___pthread_cond_s_0),
    ('_1', union___pthread_cond_s_1),
    ('__g_refs', ctypes.c_uint32 * 2),
    ('__g_size', ctypes.c_uint32 * 2),
    ('__g1_orig_size', ctypes.c_uint32),
    ('__wrefs', ctypes.c_uint32),
    ('__g_signals', ctypes.c_uint32 * 2),
]

union_c__UA_pthread_cond_t._pack_ = True # source:False
union_c__UA_pthread_cond_t._fields_ = [
    ('__data', struct___pthread_cond_s),
    ('__size', ctypes.c_char * 48),
    ('__align', ctypes.c_int64),
    ('PADDING_0', ctypes.c_ubyte * 40),
]

struct_r_th_cond_t._pack_ = True # source:False
struct_r_th_cond_t._fields_ = [
    ('cond', union_c__UA_pthread_cond_t),
]

class struct_r_th_t(ctypes.Structure):
    pass

struct_r_th_t._pack_ = True # source:False
struct_r_th_t._fields_ = [
    ('tid', ctypes.c_uint64),
    ('lock', POINTER_T(struct_r_th_lock_t)),
    ('fun', POINTER_T(ctypes.CFUNCTYPE(c__EA_RThreadFunctionRet, POINTER_T(struct_r_th_t)))),
    ('user', POINTER_T(None)),
    ('running', ctypes.c_int32),
    ('breaked', ctypes.c_int32),
    ('delay', ctypes.c_int32),
    ('ready', ctypes.c_int32),
]

class struct_pj_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sb', struct_c__SA_RStrBuf),
    ('is_first', ctypes.c_bool),
    ('is_key', ctypes.c_bool),
    ('braces', ctypes.c_char * 128),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('level', ctypes.c_int32),
     ]

class struct_r_annotated_code_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('code', POINTER_T(ctypes.c_char)),
    ('annotations', struct_r_vector_t),
     ]

RInterval = struct_r_interval_t
class struct_r_print_zoom_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('from', ctypes.c_uint64),
    ('to', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('mode', ctypes.c_int32),
     ]

class struct_r_print_t(ctypes.Structure):
    pass

struct_r_print_t._pack_ = True # source:False
struct_r_print_t._fields_ = [
    ('user', POINTER_T(None)),
    ('iob', struct_r_io_bind_t),
    ('pava', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('coreb', struct_r_core_bind_t),
    ('cfmt', POINTER_T(ctypes.c_char)),
    ('datefmt', ctypes.c_char * 32),
    ('datezone', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('cb_printf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('cb_eprintf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('cb_color', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, ctypes.c_bool))),
    ('scr_prompt', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 7),
    ('disasm', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_uint64))),
    ('oprintf', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_char)))),
    ('big_endian', ctypes.c_int32),
    ('width', ctypes.c_int32),
    ('limit', ctypes.c_int32),
    ('bits', ctypes.c_int32),
    ('histblock', ctypes.c_bool),
    ('cur_enabled', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 2),
    ('cur', ctypes.c_int32),
    ('ocur', ctypes.c_int32),
    ('cols', ctypes.c_int32),
    ('flags', ctypes.c_int32),
    ('seggrn', ctypes.c_int32),
    ('use_comments', ctypes.c_bool),
    ('PADDING_4', ctypes.c_ubyte * 3),
    ('addrmod', ctypes.c_int32),
    ('col', ctypes.c_int32),
    ('stride', ctypes.c_int32),
    ('bytespace', ctypes.c_int32),
    ('pairs', ctypes.c_int32),
    ('resetbg', ctypes.c_bool),
    ('PADDING_5', ctypes.c_ubyte * 7),
    ('zoom', POINTER_T(struct_r_print_zoom_t)),
    ('offname', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('offsize', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_uint64))),
    ('colorfor', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64, ctypes.c_bool))),
    ('hasrefs', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64, ctypes.c_bool))),
    ('get_comments', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('get_section_name', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), ctypes.c_uint64))),
    ('formats', POINTER_T(struct_sdb_t)),
    ('sdb_types', POINTER_T(struct_sdb_t)),
    ('cons', POINTER_T(struct_r_cons_t)),
    ('consbind', struct_r_cons_bind_t),
    ('num', POINTER_T(struct_r_num_t)),
    ('reg', POINTER_T(struct_r_reg_t)),
    ('get_register', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(struct_r_reg_item_t), POINTER_T(struct_r_reg_t), POINTER_T(ctypes.c_char), ctypes.c_int32))),
    ('get_register_value', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint64, POINTER_T(struct_r_reg_t), POINTER_T(struct_r_reg_item_t)))),
    ('exists_var', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_print_t), ctypes.c_uint64, POINTER_T(ctypes.c_char)))),
    ('lines_cache', POINTER_T(ctypes.c_uint64)),
    ('lines_cache_sz', ctypes.c_int32),
    ('lines_abs', ctypes.c_int32),
    ('esc_bslash', ctypes.c_bool),
    ('wide_offsets', ctypes.c_bool),
    ('PADDING_6', ctypes.c_ubyte * 6),
    ('strconv_mode', POINTER_T(ctypes.c_char)),
    ('vars', POINTER_T(struct_r_list_t)),
    ('io_unalloc_ch', ctypes.c_char),
    ('show_offset', ctypes.c_bool),
    ('calc_row_offsets', ctypes.c_bool),
    ('PADDING_7', ctypes.c_ubyte * 5),
    ('row_offsets', POINTER_T(ctypes.c_uint32)),
    ('row_offsets_sz', ctypes.c_int32),
    ('vflush', ctypes.c_bool),
    ('PADDING_8', ctypes.c_ubyte * 3),
    ('screen_bounds', ctypes.c_uint64),
]

class struct_c__SA_RStrpool(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('str', POINTER_T(ctypes.c_char)),
    ('len', ctypes.c_int32),
    ('size', ctypes.c_int32),
     ]

class struct_c__SA_RListInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('pitv', struct_r_interval_t),
    ('vitv', struct_r_interval_t),
    ('perm', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('extra', POINTER_T(ctypes.c_char)),
     ]

class struct_c__SA_RTable(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('rows', POINTER_T(struct_r_list_t)),
    ('cols', POINTER_T(struct_r_list_t)),
    ('totalCols', ctypes.c_int32),
    ('showHeader', ctypes.c_bool),
    ('showFancy', ctypes.c_bool),
    ('showJSON', ctypes.c_bool),
    ('showCSV', ctypes.c_bool),
    ('showSum', ctypes.c_bool),
    ('adjustedCols', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('cons', POINTER_T(None)),
     ]

size_t = ctypes.c_uint64
r_core_version = _libraries['libr'].r_core_version
r_core_version.restype = POINTER_T(ctypes.c_char)
r_core_version.argtypes = []

# values for enumeration 'c__EA_RCoreVisualMode'
c__EA_RCoreVisualMode__enumvalues = {
    0: 'R_CORE_VISUAL_MODE_PX',
    1: 'R_CORE_VISUAL_MODE_PD',
    2: 'R_CORE_VISUAL_MODE_DB',
    3: 'R_CORE_VISUAL_MODE_OV',
    4: 'R_CORE_VISUAL_MODE_CD',
}
R_CORE_VISUAL_MODE_PX = 0
R_CORE_VISUAL_MODE_PD = 1
R_CORE_VISUAL_MODE_DB = 2
R_CORE_VISUAL_MODE_OV = 3
R_CORE_VISUAL_MODE_CD = 4
c__EA_RCoreVisualMode = ctypes.c_int # enum
RCoreVisualMode = c__EA_RCoreVisualMode
RCoreVisualMode__enumvalues = c__EA_RCoreVisualMode__enumvalues
class struct_r_core_rtr_host_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('proto', ctypes.c_int32),
    ('host', ctypes.c_char * 512),
    ('port', ctypes.c_int32),
    ('file', ctypes.c_char * 1024),
    ('fd', POINTER_T(struct_r_socket_t)),
     ]

RCoreRtrHost = struct_r_core_rtr_host_t
class struct_r_core_undo_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('action', POINTER_T(ctypes.c_char)),
    ('revert', POINTER_T(ctypes.c_char)),
    ('tstamp', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
     ]

RCoreUndo = struct_r_core_undo_t

# values for enumeration 'c__EA_RAutocompleteType'
c__EA_RAutocompleteType__enumvalues = {
    0: 'AUTOCOMPLETE_DEFAULT',
    1: 'AUTOCOMPLETE_MS',
}
AUTOCOMPLETE_DEFAULT = 0
AUTOCOMPLETE_MS = 1
c__EA_RAutocompleteType = ctypes.c_int # enum
RAutocompleteType = c__EA_RAutocompleteType
RAutocompleteType__enumvalues = c__EA_RAutocompleteType__enumvalues
class struct_c__SA_RCoreUndoCondition(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('glob', POINTER_T(ctypes.c_char)),
    ('minstamp', ctypes.c_uint64),
     ]

RCoreUndoCondition = struct_c__SA_RCoreUndoCondition
class struct_r_core_log_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('first', ctypes.c_int32),
    ('last', ctypes.c_int32),
    ('sp', POINTER_T(struct_c__SA_RStrpool)),
     ]

RCoreLog = struct_r_core_log_t
class struct_r_core_file_t(ctypes.Structure):
    pass

class struct_r_core_autocomplete_t(ctypes.Structure):
    pass

struct_r_core_autocomplete_t._pack_ = True # source:False
struct_r_core_autocomplete_t._fields_ = [
    ('cmd', POINTER_T(ctypes.c_char)),
    ('length', ctypes.c_int32),
    ('n_subcmds', ctypes.c_int32),
    ('locked', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('type', ctypes.c_int32),
    ('subcmds', POINTER_T(POINTER_T(struct_r_core_autocomplete_t))),
]

class struct_r_core_times_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('loadlibs_init_time', ctypes.c_uint64),
    ('loadlibs_time', ctypes.c_uint64),
    ('file_open_time', ctypes.c_uint64),
     ]

class struct_r_core_tasks_t(ctypes.Structure):
    pass

class struct_r_core_task_t(ctypes.Structure):
    pass


# values for enumeration 'c__EA_RTaskState'
c__EA_RTaskState__enumvalues = {
    0: 'R_CORE_TASK_STATE_BEFORE_START',
    1: 'R_CORE_TASK_STATE_RUNNING',
    2: 'R_CORE_TASK_STATE_SLEEPING',
    3: 'R_CORE_TASK_STATE_DONE',
}
R_CORE_TASK_STATE_BEFORE_START = 0
R_CORE_TASK_STATE_RUNNING = 1
R_CORE_TASK_STATE_SLEEPING = 2
R_CORE_TASK_STATE_DONE = 3
c__EA_RTaskState = ctypes.c_int # enum
struct_r_core_task_t._pack_ = True # source:False
struct_r_core_task_t._fields_ = [
    ('id', ctypes.c_int32),
    ('state', c__EA_RTaskState),
    ('transient', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('refcount', ctypes.c_int32),
    ('running_sem', POINTER_T(struct_r_th_sem_t)),
    ('user', POINTER_T(None)),
    ('core', POINTER_T(struct_r_core_t)),
    ('dispatched', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('dispatch_cond', POINTER_T(struct_r_th_cond_t)),
    ('dispatch_lock', POINTER_T(struct_r_th_lock_t)),
    ('thread', POINTER_T(struct_r_th_t)),
    ('cmd', POINTER_T(ctypes.c_char)),
    ('res', POINTER_T(ctypes.c_char)),
    ('cmd_log', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 7),
    ('cons_context', POINTER_T(struct_r_cons_context_t)),
    ('cb', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(ctypes.c_char)))),
]

struct_r_core_tasks_t._pack_ = True # source:False
struct_r_core_tasks_t._fields_ = [
    ('task_id_next', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('tasks', POINTER_T(struct_r_list_t)),
    ('tasks_queue', POINTER_T(struct_r_list_t)),
    ('oneshot_queue', POINTER_T(struct_r_list_t)),
    ('oneshots_enqueued', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('current_task', POINTER_T(struct_r_core_task_t)),
    ('main_task', POINTER_T(struct_r_core_task_t)),
    ('lock', POINTER_T(struct_r_th_lock_t)),
    ('tasks_running', ctypes.c_int32),
    ('oneshot_running', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 3),
]

class struct_r_core_visual_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tabs', POINTER_T(struct_r_list_t)),
    ('tab', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

struct_r_core_t._pack_ = True # source:False
struct_r_core_t._fields_ = [
    ('bin', POINTER_T(struct_r_bin_t)),
    ('config', POINTER_T(struct_r_config_t)),
    ('offset', ctypes.c_uint64),
    ('prompt_offset', ctypes.c_uint64),
    ('blocksize', ctypes.c_uint32),
    ('blocksize_max', ctypes.c_uint32),
    ('block', POINTER_T(ctypes.c_ubyte)),
    ('yank_buf', POINTER_T(struct_r_buf_t)),
    ('yank_addr', ctypes.c_uint64),
    ('tmpseek', ctypes.c_bool),
    ('vmode', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('interrupted', ctypes.c_int32),
    ('cons', POINTER_T(struct_r_cons_t)),
    ('io', POINTER_T(struct_r_io_t)),
    ('file', POINTER_T(struct_r_core_file_t)),
    ('files', POINTER_T(struct_r_list_t)),
    ('num', POINTER_T(struct_r_num_t)),
    ('rc', ctypes.c_uint64),
    ('lib', POINTER_T(struct_r_lib_t)),
    ('rcmd', POINTER_T(struct_r_cmd_t)),
    ('root_cmd_descriptor', struct_r_cmd_descriptor_t),
    ('cmd_descriptors', POINTER_T(struct_r_list_t)),
    ('anal', POINTER_T(struct_r_anal_t)),
    ('rasm', POINTER_T(struct_r_asm_t)),
    ('times', POINTER_T(struct_r_core_times_t)),
    ('parser', POINTER_T(struct_r_parse_t)),
    ('print', POINTER_T(struct_r_print_t)),
    ('lang', POINTER_T(struct_r_lang_t)),
    ('dbg', POINTER_T(struct_r_debug_t)),
    ('flags', POINTER_T(struct_r_flag_t)),
    ('search', POINTER_T(struct_r_search_t)),
    ('fs', POINTER_T(struct_r_fs_t)),
    ('rfs', POINTER_T(struct_r_fs_shell_t)),
    ('egg', POINTER_T(struct_r_egg_t)),
    ('log', POINTER_T(struct_r_core_log_t)),
    ('graph', POINTER_T(struct_r_ascii_graph_t)),
    ('panels_root', POINTER_T(struct_r_panels_root_t)),
    ('panels', POINTER_T(struct_r_panels_t)),
    ('cmdqueue', POINTER_T(ctypes.c_char)),
    ('lastcmd', POINTER_T(ctypes.c_char)),
    ('cmdlog', POINTER_T(ctypes.c_char)),
    ('cfglog', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('cmdrepeat', ctypes.c_int32),
    ('cmdtimes', POINTER_T(ctypes.c_char)),
    ('cmd_in_backticks', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 3),
    ('rtr_n', ctypes.c_int32),
    ('rtr_host', struct_r_core_rtr_host_t * 255),
    ('asmqjmps', POINTER_T(ctypes.c_uint64)),
    ('asmqjmps_count', ctypes.c_int32),
    ('asmqjmps_size', ctypes.c_int32),
    ('is_asmqjmps_letter', ctypes.c_bool),
    ('keep_asmqjmps', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 6),
    ('visual', struct_r_core_visual_t),
    ('http_up', ctypes.c_int32),
    ('gdbserver_up', ctypes.c_int32),
    ('printidx', RCoreVisualMode),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('stkcmd', POINTER_T(ctypes.c_char)),
    ('in_search', ctypes.c_bool),
    ('PADDING_5', ctypes.c_ubyte * 7),
    ('watchers', POINTER_T(struct_r_list_t)),
    ('scriptstack', POINTER_T(struct_r_list_t)),
    ('tasks', struct_r_core_tasks_t),
    ('max_cmd_depth', ctypes.c_int32),
    ('switch_file_view', ctypes.c_ubyte),
    ('PADDING_6', ctypes.c_ubyte * 3),
    ('sdb', POINTER_T(struct_sdb_t)),
    ('incomment', ctypes.c_int32),
    ('curtab', ctypes.c_int32),
    ('seltab', ctypes.c_int32),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('cmdremote', POINTER_T(ctypes.c_char)),
    ('lastsearch', POINTER_T(ctypes.c_char)),
    ('cmdfilter', POINTER_T(ctypes.c_char)),
    ('break_loop', ctypes.c_bool),
    ('PADDING_8', ctypes.c_ubyte * 7),
    ('undos', POINTER_T(struct_r_list_t)),
    ('binat', ctypes.c_bool),
    ('fixedbits', ctypes.c_bool),
    ('fixedarch', ctypes.c_bool),
    ('fixedblock', ctypes.c_bool),
    ('PADDING_9', ctypes.c_ubyte * 4),
    ('table_query', POINTER_T(ctypes.c_char)),
    ('sync_index', ctypes.c_int32),
    ('PADDING_10', ctypes.c_ubyte * 4),
    ('c2', POINTER_T(struct_r_core_t)),
    ('autocomplete', POINTER_T(struct_r_core_autocomplete_t)),
    ('autocomplete_type', ctypes.c_int32),
    ('maxtab', ctypes.c_int32),
    ('ev', POINTER_T(struct_r_event_t)),
    ('gadgets', POINTER_T(struct_r_list_t)),
    ('scr_gadgets', ctypes.c_bool),
    ('log_events', ctypes.c_bool),
    ('PADDING_11', ctypes.c_ubyte * 6),
    ('ropchain', POINTER_T(struct_r_list_t)),
    ('use_tree_sitter_r2cmd', ctypes.c_bool),
    ('marks_init', ctypes.c_bool),
    ('PADDING_12', ctypes.c_ubyte * 6),
    ('marks', ctypes.c_uint64 * 256),
    ('r_main_radare2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_rafind2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_radiff2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_rabin2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_rarun2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_ragg2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_rasm2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
    ('r_main_rax2', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))))),
]

struct_r_core_file_t._pack_ = True # source:False
struct_r_core_file_t._fields_ = [
    ('dbg', ctypes.c_int32),
    ('fd', ctypes.c_int32),
    ('binb', struct_r_bin_bind_t),
    ('core', POINTER_T(struct_r_core_t)),
    ('alive', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

RCoreFile = struct_r_core_file_t
RCoreTimes = struct_r_core_times_t

# values for enumeration 'r_core_autocomplete_types_t'
r_core_autocomplete_types_t__enumvalues = {
    0: 'R_CORE_AUTOCMPLT_DFLT',
    1: 'R_CORE_AUTOCMPLT_FLAG',
    2: 'R_CORE_AUTOCMPLT_FLSP',
    3: 'R_CORE_AUTOCMPLT_SEEK',
    4: 'R_CORE_AUTOCMPLT_FCN',
    5: 'R_CORE_AUTOCMPLT_ZIGN',
    6: 'R_CORE_AUTOCMPLT_EVAL',
    7: 'R_CORE_AUTOCMPLT_PRJT',
    8: 'R_CORE_AUTOCMPLT_MINS',
    9: 'R_CORE_AUTOCMPLT_BRKP',
    10: 'R_CORE_AUTOCMPLT_MACR',
    11: 'R_CORE_AUTOCMPLT_FILE',
    12: 'R_CORE_AUTOCMPLT_THME',
    13: 'R_CORE_AUTOCMPLT_OPTN',
    14: 'R_CORE_AUTOCMPLT_MS',
    15: 'R_CORE_AUTOCMPLT_SDB',
    16: 'R_CORE_AUTOCMPLT_END',
}
R_CORE_AUTOCMPLT_DFLT = 0
R_CORE_AUTOCMPLT_FLAG = 1
R_CORE_AUTOCMPLT_FLSP = 2
R_CORE_AUTOCMPLT_SEEK = 3
R_CORE_AUTOCMPLT_FCN = 4
R_CORE_AUTOCMPLT_ZIGN = 5
R_CORE_AUTOCMPLT_EVAL = 6
R_CORE_AUTOCMPLT_PRJT = 7
R_CORE_AUTOCMPLT_MINS = 8
R_CORE_AUTOCMPLT_BRKP = 9
R_CORE_AUTOCMPLT_MACR = 10
R_CORE_AUTOCMPLT_FILE = 11
R_CORE_AUTOCMPLT_THME = 12
R_CORE_AUTOCMPLT_OPTN = 13
R_CORE_AUTOCMPLT_MS = 14
R_CORE_AUTOCMPLT_SDB = 15
R_CORE_AUTOCMPLT_END = 16
r_core_autocomplete_types_t = ctypes.c_int # enum
RCoreAutocompleteType = r_core_autocomplete_types_t
RCoreAutocompleteType__enumvalues = r_core_autocomplete_types_t__enumvalues
RCoreAutocomplete = struct_r_core_autocomplete_t
class struct_r_core_visual_tab_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('printidx', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('offset', ctypes.c_uint64),
    ('cur_enabled', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('cur', ctypes.c_int32),
    ('ocur', ctypes.c_int32),
    ('cols', ctypes.c_int32),
    ('disMode', ctypes.c_int32),
    ('hexMode', ctypes.c_int32),
    ('asm_offset', ctypes.c_int32),
    ('asm_instr', ctypes.c_int32),
    ('asm_indent', ctypes.c_int32),
    ('asm_bytes', ctypes.c_int32),
    ('asm_cmt_col', ctypes.c_int32),
    ('printMode', ctypes.c_int32),
    ('current3format', ctypes.c_int32),
    ('current4format', ctypes.c_int32),
    ('current5format', ctypes.c_int32),
    ('dumpCols', ctypes.c_int32),
    ('name', ctypes.c_char * 32),
     ]

RCoreVisualTab = struct_r_core_visual_tab_t
RCoreVisual = struct_r_core_visual_t
class struct_c__SA_RCoreGadget(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
    ('w', ctypes.c_int32),
    ('h', ctypes.c_int32),
    ('cmd', POINTER_T(ctypes.c_char)),
     ]

RCoreGadget = struct_c__SA_RCoreGadget
r_core_gadget_free = _libraries['libr'].r_core_gadget_free
r_core_gadget_free.restype = None
r_core_gadget_free.argtypes = [POINTER_T(struct_c__SA_RCoreGadget)]
RCoreTaskScheduler = struct_r_core_tasks_t
class struct_r_core_item_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', POINTER_T(ctypes.c_char)),
    ('addr', ctypes.c_uint64),
    ('next', ctypes.c_uint64),
    ('prev', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('perm', ctypes.c_int32),
    ('data', POINTER_T(ctypes.c_char)),
    ('comment', POINTER_T(ctypes.c_char)),
    ('sectname', POINTER_T(ctypes.c_char)),
    ('fcnname', POINTER_T(ctypes.c_char)),
     ]

RCoreItem = struct_r_core_item_t
r_core_item_at = _libraries['libr'].r_core_item_at
r_core_item_at.restype = POINTER_T(struct_r_core_item_t)
r_core_item_at.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_item_free = _libraries['libr'].r_core_item_free
r_core_item_free.restype = None
r_core_item_free.argtypes = [POINTER_T(struct_r_core_item_t)]
r_core_bind = _libraries['libr'].r_core_bind
r_core_bind.restype = ctypes.c_int32
r_core_bind.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_bind_t)]
class struct_r_core_cmpwatch_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('addr', ctypes.c_uint64),
    ('size', ctypes.c_int32),
    ('cmd', ctypes.c_char * 32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('odata', POINTER_T(ctypes.c_ubyte)),
    ('ndata', POINTER_T(ctypes.c_ubyte)),
     ]

RCoreCmpWatcher = struct_r_core_cmpwatch_t
RCoreSearchCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
r_core_list_themes = _libraries['libr'].r_core_list_themes
r_core_list_themes.restype = POINTER_T(struct_r_list_t)
r_core_list_themes.argtypes = [POINTER_T(struct_r_core_t)]
r_core_get_theme = _libraries['libr'].r_core_get_theme
r_core_get_theme.restype = POINTER_T(ctypes.c_char)
r_core_get_theme.argtypes = []
r_core_get_section_name = _libraries['libr'].r_core_get_section_name
r_core_get_section_name.restype = POINTER_T(ctypes.c_char)
r_core_get_section_name.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_get_cons = _libraries['libr'].r_core_get_cons
r_core_get_cons.restype = POINTER_T(struct_r_cons_t)
r_core_get_cons.argtypes = [POINTER_T(struct_r_core_t)]
r_core_get_bin = _libraries['libr'].r_core_get_bin
r_core_get_bin.restype = POINTER_T(struct_r_bin_t)
r_core_get_bin.argtypes = [POINTER_T(struct_r_core_t)]
r_core_get_config = _libraries['libr'].r_core_get_config
r_core_get_config.restype = POINTER_T(struct_r_config_t)
r_core_get_config.argtypes = [POINTER_T(struct_r_core_t)]
r_core_init = _libraries['libr'].r_core_init
r_core_init.restype = ctypes.c_bool
r_core_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_bind_cons = _libraries['libr'].r_core_bind_cons
r_core_bind_cons.restype = None
r_core_bind_cons.argtypes = [POINTER_T(struct_r_core_t)]
r_core_new = _libraries['libr'].r_core_new
r_core_new.restype = POINTER_T(struct_r_core_t)
r_core_new.argtypes = []
r_core_free = _libraries['libr'].r_core_free
r_core_free.restype = None
r_core_free.argtypes = [POINTER_T(struct_r_core_t)]
r_core_fini = _libraries['libr'].r_core_fini
r_core_fini.restype = None
r_core_fini.argtypes = [POINTER_T(struct_r_core_t)]
r_core_wait = _libraries['libr'].r_core_wait
r_core_wait.restype = None
r_core_wait.argtypes = [POINTER_T(struct_r_core_t)]
r_core_ncast = _libraries['libr'].r_core_ncast
r_core_ncast.restype = POINTER_T(struct_r_core_t)
r_core_ncast.argtypes = [ctypes.c_uint64]
r_core_cast = _libraries['libr'].r_core_cast
r_core_cast.restype = POINTER_T(struct_r_core_t)
r_core_cast.argtypes = [POINTER_T(None)]
r_core_bin_load_structs = _libraries['libr'].r_core_bin_load_structs
r_core_bin_load_structs.restype = ctypes.c_bool
r_core_bin_load_structs.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_config_init = _libraries['libr'].r_core_config_init
r_core_config_init.restype = ctypes.c_int32
r_core_config_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_config_update = _libraries['libr'].r_core_config_update
r_core_config_update.restype = None
r_core_config_update.argtypes = [POINTER_T(struct_r_core_t)]
r_core_parse_radare2rc = _libraries['libr'].r_core_parse_radare2rc
r_core_parse_radare2rc.restype = None
r_core_parse_radare2rc.argtypes = [POINTER_T(struct_r_core_t)]
r_core_prompt = _libraries['libr'].r_core_prompt
r_core_prompt.restype = ctypes.c_int32
r_core_prompt.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_prompt_exec = _libraries['libr'].r_core_prompt_exec
r_core_prompt_exec.restype = ctypes.c_int32
r_core_prompt_exec.argtypes = [POINTER_T(struct_r_core_t)]
r_core_lines_initcache = _libraries['libr'].r_core_lines_initcache
r_core_lines_initcache.restype = ctypes.c_int32
r_core_lines_initcache.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64]
r_core_lines_currline = _libraries['libr'].r_core_lines_currline
r_core_lines_currline.restype = ctypes.c_int32
r_core_lines_currline.argtypes = [POINTER_T(struct_r_core_t)]
r_core_prompt_loop = _libraries['libr'].r_core_prompt_loop
r_core_prompt_loop.restype = None
r_core_prompt_loop.argtypes = [POINTER_T(struct_r_core_t)]
r_core_pava = _libraries['libr'].r_core_pava
r_core_pava.restype = ctypes.c_uint64
r_core_pava.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_cmd = _libraries['libr'].r_core_cmd
r_core_cmd.restype = ctypes.c_int32
r_core_cmd.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_cmd_task_sync = _libraries['libr'].r_core_cmd_task_sync
r_core_cmd_task_sync.restype = ctypes.c_int32
r_core_cmd_task_sync.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_core_editor = _libraries['libr'].r_core_editor
r_core_editor.restype = POINTER_T(ctypes.c_char)
r_core_editor.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_fgets = _libraries['libr'].r_core_fgets
r_core_fgets.restype = ctypes.c_int32
r_core_fgets.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_flag_get_by_spaces = _libraries['libr'].r_core_flag_get_by_spaces
r_core_flag_get_by_spaces.restype = POINTER_T(struct_r_flag_item_t)
r_core_flag_get_by_spaces.argtypes = [POINTER_T(struct_r_flag_t), ctypes.c_uint64]
r_core_cmdf = _libraries['libr'].r_core_cmdf
r_core_cmdf.restype = ctypes.c_int32
r_core_cmdf.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_flush = _libraries['libr'].r_core_flush
r_core_flush.restype = ctypes.c_int32
r_core_flush.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd0 = _libraries['libr'].r_core_cmd0
r_core_cmd0.restype = ctypes.c_int32
r_core_cmd0.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_init = _libraries['libr'].r_core_cmd_init
r_core_cmd_init.restype = None
r_core_cmd_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_cmd_pipe = _libraries['libr'].r_core_cmd_pipe
r_core_cmd_pipe.restype = ctypes.c_int32
r_core_cmd_pipe.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_cmd_str = _libraries['libr'].r_core_cmd_str
r_core_cmd_str.restype = POINTER_T(ctypes.c_char)
r_core_cmd_str.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_strf = _libraries['libr'].r_core_cmd_strf
r_core_cmd_strf.restype = POINTER_T(ctypes.c_char)
r_core_cmd_strf.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_str_pipe = _libraries['libr'].r_core_cmd_str_pipe
r_core_cmd_str_pipe.restype = POINTER_T(ctypes.c_char)
r_core_cmd_str_pipe.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_file = _libraries['libr'].r_core_cmd_file
r_core_cmd_file.restype = ctypes.c_int32
r_core_cmd_file.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_lines = _libraries['libr'].r_core_cmd_lines
r_core_cmd_lines.restype = ctypes.c_int32
r_core_cmd_lines.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_command = _libraries['libr'].r_core_cmd_command
r_core_cmd_command.restype = ctypes.c_int32
r_core_cmd_command.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_run_script = _libraries['libr'].r_core_run_script
r_core_run_script.restype = ctypes.c_bool
r_core_run_script.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_seek = _libraries['libr'].r_core_seek
r_core_seek.restype = ctypes.c_bool
r_core_seek.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_bool]
r_core_visual_bit_editor = _libraries['libr'].r_core_visual_bit_editor
r_core_visual_bit_editor.restype = ctypes.c_bool
r_core_visual_bit_editor.argtypes = [POINTER_T(struct_r_core_t)]
r_core_seek_base = _libraries['libr'].r_core_seek_base
r_core_seek_base.restype = ctypes.c_int32
r_core_seek_base.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_seek_previous = _libraries['libr'].r_core_seek_previous
r_core_seek_previous.restype = None
r_core_seek_previous.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_seek_next = _libraries['libr'].r_core_seek_next
r_core_seek_next.restype = None
r_core_seek_next.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_seek_align = _libraries['libr'].r_core_seek_align
r_core_seek_align.restype = ctypes.c_int32
r_core_seek_align.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_arch_bits_at = _libraries['libr'].r_core_arch_bits_at
r_core_arch_bits_at.restype = None
r_core_arch_bits_at.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_int32), POINTER_T(POINTER_T(ctypes.c_char))]
r_core_seek_arch_bits = _libraries['libr'].r_core_seek_arch_bits
r_core_seek_arch_bits.restype = None
r_core_seek_arch_bits.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_block_read = _libraries['libr'].r_core_block_read
r_core_block_read.restype = ctypes.c_int32
r_core_block_read.argtypes = [POINTER_T(struct_r_core_t)]
r_core_block_size = _libraries['libr'].r_core_block_size
r_core_block_size.restype = ctypes.c_int32
r_core_block_size.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_seek_size = _libraries['libr'].r_core_seek_size
r_core_seek_size.restype = ctypes.c_int32
r_core_seek_size.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_is_valid_offset = _libraries['libr'].r_core_is_valid_offset
r_core_is_valid_offset.restype = ctypes.c_int32
r_core_is_valid_offset.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_shift_block = _libraries['libr'].r_core_shift_block
r_core_shift_block.restype = ctypes.c_int32
r_core_shift_block.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int64]
r_core_autocomplete = _libraries['libr'].r_core_autocomplete
r_core_autocomplete.restype = None
r_core_autocomplete.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_line_comp_t), POINTER_T(struct_r_line_buffer_t), RLinePromptType]
r_core_print_scrollbar = _libraries['libr'].r_core_print_scrollbar
r_core_print_scrollbar.restype = None
r_core_print_scrollbar.argtypes = [POINTER_T(struct_r_core_t)]
r_core_print_scrollbar_bottom = _libraries['libr'].r_core_print_scrollbar_bottom
r_core_print_scrollbar_bottom.restype = None
r_core_print_scrollbar_bottom.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_prompt_input = _libraries['libr'].r_core_visual_prompt_input
r_core_visual_prompt_input.restype = None
r_core_visual_prompt_input.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_toggle_decompiler_disasm = _libraries['libr'].r_core_visual_toggle_decompiler_disasm
r_core_visual_toggle_decompiler_disasm.restype = None
r_core_visual_toggle_decompiler_disasm.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_bool, ctypes.c_bool]
r_core_visual_applyDisMode = _libraries['libr'].r_core_visual_applyDisMode
r_core_visual_applyDisMode.restype = None
r_core_visual_applyDisMode.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_visual_applyHexMode = _libraries['libr'].r_core_visual_applyHexMode
r_core_visual_applyHexMode.restype = None
r_core_visual_applyHexMode.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_visual_refs = _libraries['libr'].r_core_visual_refs
r_core_visual_refs.restype = ctypes.c_int32
r_core_visual_refs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_bool, ctypes.c_bool]
r_core_visual_append_help = _libraries['libr'].r_core_visual_append_help
r_core_visual_append_help.restype = None
r_core_visual_append_help.argtypes = [POINTER_T(struct_c__SA_RStrBuf), POINTER_T(ctypes.c_char), POINTER_T(POINTER_T(ctypes.c_char))]
r_core_prevop_addr = _libraries['libr'].r_core_prevop_addr
r_core_prevop_addr.restype = ctypes.c_bool
r_core_prevop_addr.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, POINTER_T(ctypes.c_uint64)]
r_core_prevop_addr_force = _libraries['libr'].r_core_prevop_addr_force
r_core_prevop_addr_force.restype = ctypes.c_uint64
r_core_prevop_addr_force.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_visual_hudstuff = _libraries['libr'].r_core_visual_hudstuff
r_core_visual_hudstuff.restype = ctypes.c_bool
r_core_visual_hudstuff.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_classes = _libraries['libr'].r_core_visual_classes
r_core_visual_classes.restype = ctypes.c_int32
r_core_visual_classes.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_anal_classes = _libraries['libr'].r_core_visual_anal_classes
r_core_visual_anal_classes.restype = ctypes.c_int32
r_core_visual_anal_classes.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_types = _libraries['libr'].r_core_visual_types
r_core_visual_types.restype = ctypes.c_int32
r_core_visual_types.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual = _libraries['libr'].r_core_visual
r_core_visual.restype = ctypes.c_int32
r_core_visual.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_visual_graph = _libraries['libr'].r_core_visual_graph
r_core_visual_graph.restype = ctypes.c_int32
r_core_visual_graph.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_ascii_graph_t), POINTER_T(struct_r_anal_function_t), ctypes.c_int32]
r_core_visual_panels_root = _libraries['libr'].r_core_visual_panels_root
r_core_visual_panels_root.restype = ctypes.c_bool
r_core_visual_panels_root.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_panels_root_t)]
r_core_visual_browse = _libraries['libr'].r_core_visual_browse
r_core_visual_browse.restype = None
r_core_visual_browse.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_visual_cmd = _libraries['libr'].r_core_visual_cmd
r_core_visual_cmd.restype = ctypes.c_int32
r_core_visual_cmd.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_visual_seek_animation = _libraries['libr'].r_core_visual_seek_animation
r_core_visual_seek_animation.restype = None
r_core_visual_seek_animation.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_visual_asm = _libraries['libr'].r_core_visual_asm
r_core_visual_asm.restype = None
r_core_visual_asm.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_visual_colors = _libraries['libr'].r_core_visual_colors
r_core_visual_colors.restype = None
r_core_visual_colors.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_showcursor = _libraries['libr'].r_core_visual_showcursor
r_core_visual_showcursor.restype = None
r_core_visual_showcursor.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_visual_offset = _libraries['libr'].r_core_visual_offset
r_core_visual_offset.restype = None
r_core_visual_offset.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_hud = _libraries['libr'].r_core_visual_hud
r_core_visual_hud.restype = ctypes.c_int32
r_core_visual_hud.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_jump = _libraries['libr'].r_core_visual_jump
r_core_visual_jump.restype = None
r_core_visual_jump.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_ubyte]
r_core_visual_disasm_up = _libraries['libr'].r_core_visual_disasm_up
r_core_visual_disasm_up.restype = None
r_core_visual_disasm_up.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_int32)]
r_core_visual_disasm_down = _libraries['libr'].r_core_visual_disasm_down
r_core_visual_disasm_down.restype = None
r_core_visual_disasm_down.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_asm_op_t), POINTER_T(ctypes.c_int32)]
r_core_getreloc = _libraries['libr'].r_core_getreloc
r_core_getreloc.restype = POINTER_T(struct_r_bin_reloc_t)
r_core_getreloc.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_get_asmqjmps = _libraries['libr'].r_core_get_asmqjmps
r_core_get_asmqjmps.restype = ctypes.c_uint64
r_core_get_asmqjmps.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_set_asmqjmps = _libraries['libr'].r_core_set_asmqjmps
r_core_set_asmqjmps.restype = None
r_core_set_asmqjmps.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), size_t, ctypes.c_int32]
r_core_add_asmqjmp = _libraries['libr'].r_core_add_asmqjmp
r_core_add_asmqjmp.restype = POINTER_T(ctypes.c_char)
r_core_add_asmqjmp.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_type_init = _libraries['libr'].r_core_anal_type_init
r_core_anal_type_init.restype = None
r_core_anal_type_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_link_stroff = _libraries['libr'].r_core_link_stroff
r_core_link_stroff.restype = None
r_core_link_stroff.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
r_core_anal_inflags = _libraries['libr'].r_core_anal_inflags
r_core_anal_inflags.restype = None
r_core_anal_inflags.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
cmd_anal_objc = _libraries['libr'].cmd_anal_objc
cmd_anal_objc.restype = ctypes.c_bool
cmd_anal_objc.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_core_anal_cc_init = _libraries['libr'].r_core_anal_cc_init
r_core_anal_cc_init.restype = None
r_core_anal_cc_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_paths = _libraries['libr'].r_core_anal_paths
r_core_anal_paths.restype = None
r_core_anal_paths.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_bool, ctypes.c_int32, ctypes.c_bool]
r_core_anal_esil_graph = _libraries['libr'].r_core_anal_esil_graph
r_core_anal_esil_graph.restype = None
r_core_anal_esil_graph.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_listinfo_new = _libraries['libr'].r_listinfo_new
r_listinfo_new.restype = POINTER_T(struct_c__SA_RListInfo)
r_listinfo_new.argtypes = [POINTER_T(ctypes.c_char), RInterval, RInterval, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_listinfo_free = _libraries['libr'].r_listinfo_free
r_listinfo_free.restype = None
r_listinfo_free.argtypes = [POINTER_T(struct_c__SA_RListInfo)]
r_core_visual_mark_seek = _libraries['libr'].r_core_visual_mark_seek
r_core_visual_mark_seek.restype = None
r_core_visual_mark_seek.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_ubyte]
r_core_visual_mark = _libraries['libr'].r_core_visual_mark
r_core_visual_mark.restype = None
r_core_visual_mark.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_ubyte]
r_core_visual_mark_set = _libraries['libr'].r_core_visual_mark_set
r_core_visual_mark_set.restype = None
r_core_visual_mark_set.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_ubyte, ctypes.c_uint64]
r_core_visual_mark_del = _libraries['libr'].r_core_visual_mark_del
r_core_visual_mark_del.restype = None
r_core_visual_mark_del.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_ubyte]
r_core_visual_mark_dump = _libraries['libr'].r_core_visual_mark_dump
r_core_visual_mark_dump.restype = ctypes.c_bool
r_core_visual_mark_dump.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_mark_reset = _libraries['libr'].r_core_visual_mark_reset
r_core_visual_mark_reset.restype = None
r_core_visual_mark_reset.argtypes = [POINTER_T(struct_r_core_t)]
r_core_search_cb = _libraries['libr'].r_core_search_cb
r_core_search_cb.restype = ctypes.c_int32
r_core_search_cb.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, RCoreSearchCallback]
r_core_serve = _libraries['libr'].r_core_serve
r_core_serve.restype = ctypes.c_bool
r_core_serve.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_io_desc_t)]
r_core_file_reopen = _libraries['libr'].r_core_file_reopen
r_core_file_reopen.restype = ctypes.c_int32
r_core_file_reopen.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_core_file_reopen_debug = _libraries['libr'].r_core_file_reopen_debug
r_core_file_reopen_debug.restype = None
r_core_file_reopen_debug.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_file_reopen_remote_debug = _libraries['libr'].r_core_file_reopen_remote_debug
r_core_file_reopen_remote_debug.restype = None
r_core_file_reopen_remote_debug.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_core_file_find_by_fd = _libraries['libr'].r_core_file_find_by_fd
r_core_file_find_by_fd.restype = POINTER_T(struct_r_core_file_t)
r_core_file_find_by_fd.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_file_find_by_name = _libraries['libr'].r_core_file_find_by_name
r_core_file_find_by_name.restype = POINTER_T(struct_r_core_file_t)
r_core_file_find_by_name.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_file_cur = _libraries['libr'].r_core_file_cur
r_core_file_cur.restype = POINTER_T(struct_r_core_file_t)
r_core_file_cur.argtypes = [POINTER_T(struct_r_core_t)]
r_core_file_set_by_fd = _libraries['libr'].r_core_file_set_by_fd
r_core_file_set_by_fd.restype = ctypes.c_int32
r_core_file_set_by_fd.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_file_set_by_name = _libraries['libr'].r_core_file_set_by_name
r_core_file_set_by_name.restype = ctypes.c_int32
r_core_file_set_by_name.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_file_set_by_file = _libraries['libr'].r_core_file_set_by_file
r_core_file_set_by_file.restype = ctypes.c_int32
r_core_file_set_by_file.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_file_t)]
r_core_setup_debugger = _libraries['libr'].r_core_setup_debugger
r_core_setup_debugger.restype = ctypes.c_int32
r_core_setup_debugger.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_core_file_free = _libraries['libr'].r_core_file_free
r_core_file_free.restype = None
r_core_file_free.argtypes = [POINTER_T(struct_r_core_file_t)]
r_core_file_open = _libraries['libr'].r_core_file_open
r_core_file_open.restype = POINTER_T(struct_r_core_file_t)
r_core_file_open.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_uint64]
r_core_file_open_many = _libraries['libr'].r_core_file_open_many
r_core_file_open_many.restype = POINTER_T(struct_r_core_file_t)
r_core_file_open_many.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_uint64]
r_core_file_get_by_fd = _libraries['libr'].r_core_file_get_by_fd
r_core_file_get_by_fd.restype = POINTER_T(struct_r_core_file_t)
r_core_file_get_by_fd.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_file_close = _libraries['libr'].r_core_file_close
r_core_file_close.restype = ctypes.c_int32
r_core_file_close.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_file_t)]
r_core_file_close_fd = _libraries['libr'].r_core_file_close_fd
r_core_file_close_fd.restype = ctypes.c_bool
r_core_file_close_fd.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_file_close_all_but = _libraries['libr'].r_core_file_close_all_but
r_core_file_close_all_but.restype = ctypes.c_bool
r_core_file_close_all_but.argtypes = [POINTER_T(struct_r_core_t)]
r_core_file_list = _libraries['libr'].r_core_file_list
r_core_file_list.restype = ctypes.c_int32
r_core_file_list.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_file_binlist = _libraries['libr'].r_core_file_binlist
r_core_file_binlist.restype = ctypes.c_int32
r_core_file_binlist.argtypes = [POINTER_T(struct_r_core_t)]
r_core_file_bin_raise = _libraries['libr'].r_core_file_bin_raise
r_core_file_bin_raise.restype = ctypes.c_bool
r_core_file_bin_raise.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint32]
r_core_seek_delta = _libraries['libr'].r_core_seek_delta
r_core_seek_delta.restype = ctypes.c_int32
r_core_seek_delta.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int64]
r_core_extend_at = _libraries['libr'].r_core_extend_at
r_core_extend_at.restype = ctypes.c_bool
r_core_extend_at.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_write_at = _libraries['libr'].r_core_write_at
r_core_write_at.restype = ctypes.c_bool
r_core_write_at.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_core_write_op = _libraries['libr'].r_core_write_op
r_core_write_op.restype = ctypes.c_int32
r_core_write_op.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_char]
r_core_transform_op = _libraries['libr'].r_core_transform_op
r_core_transform_op.restype = POINTER_T(ctypes.c_ubyte)
r_core_transform_op.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_char]
r_core_file_cur_fd = _libraries['libr'].r_core_file_cur_fd
r_core_file_cur_fd.restype = ctypes.c_uint32
r_core_file_cur_fd.argtypes = [POINTER_T(struct_r_core_t)]
r_core_debug_rr = _libraries['libr'].r_core_debug_rr
r_core_debug_rr.restype = None
r_core_debug_rr.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_reg_t), ctypes.c_int32]
r_core_fortune_list_types = _libraries['libr'].r_core_fortune_list_types
r_core_fortune_list_types.restype = None
r_core_fortune_list_types.argtypes = []
r_core_fortune_list = _libraries['libr'].r_core_fortune_list
r_core_fortune_list.restype = None
r_core_fortune_list.argtypes = [POINTER_T(struct_r_core_t)]
r_core_fortune_print_random = _libraries['libr'].r_core_fortune_print_random
r_core_fortune_print_random.restype = None
r_core_fortune_print_random.argtypes = [POINTER_T(struct_r_core_t)]
r_core_project_load = _libraries['libr'].r_core_project_load
r_core_project_load.restype = ctypes.c_bool
r_core_project_load.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_project_load_bg = _libraries['libr'].r_core_project_load_bg
r_core_project_load_bg.restype = POINTER_T(struct_r_th_t)
r_core_project_load_bg.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_project_execute_cmds = _libraries['libr'].r_core_project_execute_cmds
r_core_project_execute_cmds.restype = None
r_core_project_execute_cmds.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_yank = _libraries['libr'].r_core_yank
r_core_yank.restype = ctypes.c_int32
r_core_yank.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_yank_string = _libraries['libr'].r_core_yank_string
r_core_yank_string.restype = ctypes.c_int32
r_core_yank_string.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_yank_hexpair = _libraries['libr'].r_core_yank_hexpair
r_core_yank_hexpair.restype = ctypes.c_bool
r_core_yank_hexpair.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_yank_paste = _libraries['libr'].r_core_yank_paste
r_core_yank_paste.restype = ctypes.c_int32
r_core_yank_paste.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_yank_set = _libraries['libr'].r_core_yank_set
r_core_yank_set.restype = ctypes.c_int32
r_core_yank_set.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_uint32]
r_core_yank_set_str = _libraries['libr'].r_core_yank_set_str
r_core_yank_set_str.restype = ctypes.c_int32
r_core_yank_set_str.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_char), ctypes.c_uint32]
r_core_yank_to = _libraries['libr'].r_core_yank_to
r_core_yank_to.restype = ctypes.c_int32
r_core_yank_to.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_yank_dump = _libraries['libr'].r_core_yank_dump
r_core_yank_dump.restype = ctypes.c_bool
r_core_yank_dump.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_yank_hexdump = _libraries['libr'].r_core_yank_hexdump
r_core_yank_hexdump.restype = ctypes.c_int32
r_core_yank_hexdump.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_yank_cat = _libraries['libr'].r_core_yank_cat
r_core_yank_cat.restype = ctypes.c_int32
r_core_yank_cat.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_yank_cat_string = _libraries['libr'].r_core_yank_cat_string
r_core_yank_cat_string.restype = ctypes.c_int32
r_core_yank_cat_string.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_yank_hud_file = _libraries['libr'].r_core_yank_hud_file
r_core_yank_hud_file.restype = ctypes.c_int32
r_core_yank_hud_file.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_yank_hud_path = _libraries['libr'].r_core_yank_hud_path
r_core_yank_hud_path.restype = ctypes.c_int32
r_core_yank_hud_path.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_yank_file_ex = _libraries['libr'].r_core_yank_file_ex
r_core_yank_file_ex.restype = ctypes.c_bool
r_core_yank_file_ex.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_yank_file_all = _libraries['libr'].r_core_yank_file_all
r_core_yank_file_all.restype = ctypes.c_int32
r_core_yank_file_all.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_loadlibs_init = _libraries['libr'].r_core_loadlibs_init
r_core_loadlibs_init.restype = None
r_core_loadlibs_init.argtypes = [POINTER_T(struct_r_core_t)]
r_core_loadlibs = _libraries['libr'].r_core_loadlibs
r_core_loadlibs.restype = ctypes.c_int32
r_core_loadlibs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_cmd_buffer = _libraries['libr'].r_core_cmd_buffer
r_core_cmd_buffer.restype = ctypes.c_int32
r_core_cmd_buffer.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmd_foreach = _libraries['libr'].r_core_cmd_foreach
r_core_cmd_foreach.restype = ctypes.c_int32
r_core_cmd_foreach.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_cmd_foreach3 = _libraries['libr'].r_core_cmd_foreach3
r_core_cmd_foreach3.restype = ctypes.c_int32
r_core_cmd_foreach3.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_op_str = _libraries['libr'].r_core_op_str
r_core_op_str.restype = POINTER_T(ctypes.c_char)
r_core_op_str.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_op_anal = _libraries['libr'].r_core_op_anal
r_core_op_anal.restype = POINTER_T(struct_r_anal_op_t)
r_core_op_anal.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, RAnalOpMask]
r_core_disassemble_instr = _libraries['libr'].r_core_disassemble_instr
r_core_disassemble_instr.restype = POINTER_T(ctypes.c_char)
r_core_disassemble_instr.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_disassemble_bytes = _libraries['libr'].r_core_disassemble_bytes
r_core_disassemble_bytes.restype = POINTER_T(ctypes.c_char)
r_core_disassemble_bytes.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_get_func_args = _libraries['libr'].r_core_get_func_args
r_core_get_func_args.restype = POINTER_T(struct_r_list_t)
r_core_get_func_args.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_print_func_args = _libraries['libr'].r_core_print_func_args
r_core_print_func_args.restype = None
r_core_print_func_args.argtypes = [POINTER_T(struct_r_core_t)]
resolve_fcn_name = _libraries['libr'].resolve_fcn_name
resolve_fcn_name.restype = POINTER_T(ctypes.c_char)
resolve_fcn_name.argtypes = [POINTER_T(struct_r_anal_t), POINTER_T(ctypes.c_char)]
r_core_get_stacksz = _libraries['libr'].r_core_get_stacksz
r_core_get_stacksz.restype = ctypes.c_int32
r_core_get_stacksz.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64]
r_core_anal_op = _libraries['libr'].r_core_anal_op
r_core_anal_op.restype = POINTER_T(struct_r_anal_op_t)
r_core_anal_op.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_anal_esil = _libraries['libr'].r_core_anal_esil
r_core_anal_esil.restype = None
r_core_anal_esil.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_anal_fcn_merge = _libraries['libr'].r_core_anal_fcn_merge
r_core_anal_fcn_merge.restype = None
r_core_anal_fcn_merge.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64]
r_core_anal_optype_colorfor = _libraries['libr'].r_core_anal_optype_colorfor
r_core_anal_optype_colorfor.restype = POINTER_T(ctypes.c_char)
r_core_anal_optype_colorfor.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_bool]
r_core_anal_address = _libraries['libr'].r_core_anal_address
r_core_anal_address.restype = ctypes.c_uint64
r_core_anal_address.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_undefine = _libraries['libr'].r_core_anal_undefine
r_core_anal_undefine.restype = None
r_core_anal_undefine.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_hint_print = _libraries['libr'].r_core_anal_hint_print
r_core_anal_hint_print.restype = None
r_core_anal_hint_print.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_uint64, ctypes.c_int32]
r_core_anal_hint_list = _libraries['libr'].r_core_anal_hint_list
r_core_anal_hint_list.restype = None
r_core_anal_hint_list.argtypes = [POINTER_T(struct_r_anal_t), ctypes.c_int32]
r_core_anal_search = _libraries['libr'].r_core_anal_search
r_core_anal_search.restype = ctypes.c_int32
r_core_anal_search.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_core_anal_search_xrefs = _libraries['libr'].r_core_anal_search_xrefs
r_core_anal_search_xrefs.restype = ctypes.c_int32
r_core_anal_search_xrefs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_core_anal_data = _libraries['libr'].r_core_anal_data
r_core_anal_data.restype = ctypes.c_int32
r_core_anal_data.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_core_anal_datarefs = _libraries['libr'].r_core_anal_datarefs
r_core_anal_datarefs.restype = None
r_core_anal_datarefs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_coderefs = _libraries['libr'].r_core_anal_coderefs
r_core_anal_coderefs.restype = None
r_core_anal_coderefs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_codexrefs = _libraries['libr'].r_core_anal_codexrefs
r_core_anal_codexrefs.restype = None
r_core_anal_codexrefs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_importxrefs = _libraries['libr'].r_core_anal_importxrefs
r_core_anal_importxrefs.restype = None
r_core_anal_importxrefs.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_callgraph = _libraries['libr'].r_core_anal_callgraph
r_core_anal_callgraph.restype = None
r_core_anal_callgraph.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_anal_refs = _libraries['libr'].r_core_anal_refs
r_core_anal_refs.restype = ctypes.c_int32
r_core_anal_refs.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_agraph_print = _libraries['libr'].r_core_agraph_print
r_core_agraph_print.restype = None
r_core_agraph_print.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_esil_cmd = _libraries['libr'].r_core_esil_cmd
r_core_esil_cmd.restype = ctypes.c_bool
r_core_esil_cmd.argtypes = [POINTER_T(struct_r_anal_esil_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64]
r_core_esil_step = _libraries['libr'].r_core_esil_step
r_core_esil_step.restype = ctypes.c_int32
r_core_esil_step.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_uint64), ctypes.c_bool]
r_core_esil_step_back = _libraries['libr'].r_core_esil_step_back
r_core_esil_step_back.restype = ctypes.c_int32
r_core_esil_step_back.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_bb_seek = _libraries['libr'].r_core_anal_bb_seek
r_core_anal_bb_seek.restype = ctypes.c_bool
r_core_anal_bb_seek.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_fcn = _libraries['libr'].r_core_anal_fcn
r_core_anal_fcn.restype = ctypes.c_int32
r_core_anal_fcn.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_core_anal_fcn_autoname = _libraries['libr'].r_core_anal_fcn_autoname
r_core_anal_fcn_autoname.restype = POINTER_T(ctypes.c_char)
r_core_anal_fcn_autoname.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_core_anal_autoname_all_fcns = _libraries['libr'].r_core_anal_autoname_all_fcns
r_core_anal_autoname_all_fcns.restype = None
r_core_anal_autoname_all_fcns.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_autoname_all_golang_fcns = _libraries['libr'].r_core_anal_autoname_all_golang_fcns
r_core_anal_autoname_all_golang_fcns.restype = None
r_core_anal_autoname_all_golang_fcns.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_fcn_list = _libraries['libr'].r_core_anal_fcn_list
r_core_anal_fcn_list.restype = ctypes.c_int32
r_core_anal_fcn_list.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_anal_fcn_name = _libraries['libr'].r_core_anal_fcn_name
r_core_anal_fcn_name.restype = POINTER_T(ctypes.c_char)
r_core_anal_fcn_name.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
r_core_anal_fcn_list_size = _libraries['libr'].r_core_anal_fcn_list_size
r_core_anal_fcn_list_size.restype = ctypes.c_uint64
r_core_anal_fcn_list_size.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_fcn_clean = _libraries['libr'].r_core_anal_fcn_clean
r_core_anal_fcn_clean.restype = ctypes.c_int32
r_core_anal_fcn_clean.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_print_bb_custom = _libraries['libr'].r_core_print_bb_custom
r_core_print_bb_custom.restype = ctypes.c_int32
r_core_print_bb_custom.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
r_core_print_bb_gml = _libraries['libr'].r_core_print_bb_gml
r_core_print_bb_gml.restype = ctypes.c_int32
r_core_print_bb_gml.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
r_core_anal_graph = _libraries['libr'].r_core_anal_graph
r_core_anal_graph.restype = ctypes.c_int32
r_core_anal_graph.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_anal_graph_to = _libraries['libr'].r_core_anal_graph_to
r_core_anal_graph_to.restype = POINTER_T(struct_r_list_t)
r_core_anal_graph_to.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_anal_all = _libraries['libr'].r_core_anal_all
r_core_anal_all.restype = ctypes.c_int32
r_core_anal_all.argtypes = [POINTER_T(struct_r_core_t)]
r_core_anal_cycles = _libraries['libr'].r_core_anal_cycles
r_core_anal_cycles.restype = POINTER_T(struct_r_list_t)
r_core_anal_cycles.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_anal_fcn_get_calls = _libraries['libr'].r_core_anal_fcn_get_calls
r_core_anal_fcn_get_calls.restype = POINTER_T(struct_r_list_t)
r_core_anal_fcn_get_calls.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
r_core_anal_type_match = _libraries['libr'].r_core_anal_type_match
r_core_anal_type_match.restype = None
r_core_anal_type_match.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t)]
class struct_r_core_asm_hit(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('code', POINTER_T(ctypes.c_char)),
    ('len', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('addr', ctypes.c_uint64),
    ('valid', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 7),
     ]

RCoreAsmHit = struct_r_core_asm_hit
r_core_syscall = _libraries['libr'].r_core_syscall
r_core_syscall.restype = POINTER_T(struct_r_buf_t)
r_core_syscall.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_syscallf = _libraries['libr'].r_core_syscallf
r_core_syscallf.restype = POINTER_T(struct_r_buf_t)
r_core_syscallf.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_asm_hit_new = _libraries['libr'].r_core_asm_hit_new
r_core_asm_hit_new.restype = POINTER_T(struct_r_core_asm_hit)
r_core_asm_hit_new.argtypes = []
r_core_asm_hit_list_new = _libraries['libr'].r_core_asm_hit_list_new
r_core_asm_hit_list_new.restype = POINTER_T(struct_r_list_t)
r_core_asm_hit_list_new.argtypes = []
r_core_asm_hit_free = _libraries['libr'].r_core_asm_hit_free
r_core_asm_hit_free.restype = None
r_core_asm_hit_free.argtypes = [POINTER_T(None)]
r_core_set_asm_configs = _libraries['libr'].r_core_set_asm_configs
r_core_set_asm_configs.restype = None
r_core_set_asm_configs.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_uint32, ctypes.c_int32]
r_core_asm_search = _libraries['libr'].r_core_asm_search
r_core_asm_search.restype = POINTER_T(ctypes.c_char)
r_core_asm_search.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_asm_strsearch = _libraries['libr'].r_core_asm_strsearch
r_core_asm_strsearch.restype = POINTER_T(struct_r_list_t)
r_core_asm_strsearch.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_core_asm_bwdisassemble = _libraries['libr'].r_core_asm_bwdisassemble
r_core_asm_bwdisassemble.restype = POINTER_T(struct_r_list_t)
r_core_asm_bwdisassemble.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32]
r_core_asm_back_disassemble_instr = _libraries['libr'].r_core_asm_back_disassemble_instr
r_core_asm_back_disassemble_instr.restype = POINTER_T(struct_r_list_t)
r_core_asm_back_disassemble_instr.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_uint32, ctypes.c_uint32]
r_core_asm_back_disassemble_byte = _libraries['libr'].r_core_asm_back_disassemble_byte
r_core_asm_back_disassemble_byte.restype = POINTER_T(struct_r_list_t)
r_core_asm_back_disassemble_byte.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_uint32, ctypes.c_uint32]
r_core_asm_bwdis_len = _libraries['libr'].r_core_asm_bwdis_len
r_core_asm_bwdis_len.restype = ctypes.c_uint32
r_core_asm_bwdis_len.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_int32), POINTER_T(ctypes.c_uint64), ctypes.c_uint32]
r_core_print_disasm = _libraries['libr'].r_core_print_disasm
r_core_print_disasm.restype = ctypes.c_int32
r_core_print_disasm.argtypes = [POINTER_T(struct_r_print_t), POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_bool, POINTER_T(struct_pj_t), POINTER_T(struct_r_anal_function_t)]
r_core_print_disasm_json = _libraries['libr'].r_core_print_disasm_json
r_core_print_disasm_json.restype = ctypes.c_int32
r_core_print_disasm_json.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_pj_t)]
r_core_print_disasm_instructions_with_buf = _libraries['libr'].r_core_print_disasm_instructions_with_buf
r_core_print_disasm_instructions_with_buf.restype = ctypes.c_int32
r_core_print_disasm_instructions_with_buf.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32]
r_core_print_disasm_instructions = _libraries['libr'].r_core_print_disasm_instructions
r_core_print_disasm_instructions.restype = ctypes.c_int32
r_core_print_disasm_instructions.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32]
r_core_print_disasm_all = _libraries['libr'].r_core_print_disasm_all
r_core_print_disasm_all.restype = ctypes.c_int32
r_core_print_disasm_all.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_core_disasm_pdi_with_buf = _libraries['libr'].r_core_disasm_pdi_with_buf
r_core_disasm_pdi_with_buf.restype = ctypes.c_int32
r_core_disasm_pdi_with_buf.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32]
r_core_disasm_pdi = _libraries['libr'].r_core_disasm_pdi
r_core_disasm_pdi.restype = ctypes.c_int32
r_core_disasm_pdi.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_core_disasm_pde = _libraries['libr'].r_core_disasm_pde
r_core_disasm_pde.restype = ctypes.c_int32
r_core_disasm_pde.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32]
r_core_flag_in_middle = _libraries['libr'].r_core_flag_in_middle
r_core_flag_in_middle.restype = ctypes.c_int32
r_core_flag_in_middle.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, POINTER_T(ctypes.c_int32)]
r_core_bb_starts_in_middle = _libraries['libr'].r_core_bb_starts_in_middle
r_core_bb_starts_in_middle.restype = ctypes.c_int32
r_core_bb_starts_in_middle.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_bin_raise = _libraries['libr'].r_core_bin_raise
r_core_bin_raise.restype = ctypes.c_bool
r_core_bin_raise.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint32]
r_core_bin_set_env = _libraries['libr'].r_core_bin_set_env
r_core_bin_set_env.restype = ctypes.c_int32
r_core_bin_set_env.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_bin_file_t)]
r_core_bin_set_by_fd = _libraries['libr'].r_core_bin_set_by_fd
r_core_bin_set_by_fd.restype = ctypes.c_int32
r_core_bin_set_by_fd.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_bin_set_by_name = _libraries['libr'].r_core_bin_set_by_name
r_core_bin_set_by_name.restype = ctypes.c_int32
r_core_bin_set_by_name.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_bin_load = _libraries['libr'].r_core_bin_load
r_core_bin_load.restype = ctypes.c_bool
r_core_bin_load.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_uint64]
r_core_bin_rebase = _libraries['libr'].r_core_bin_rebase
r_core_bin_rebase.restype = ctypes.c_int32
r_core_bin_rebase.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_bin_export_info = _libraries['libr'].r_core_bin_export_info
r_core_bin_export_info.restype = None
r_core_bin_export_info.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_bin_list = _libraries['libr'].r_core_bin_list
r_core_bin_list.restype = ctypes.c_int32
r_core_bin_list.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_bin_delete = _libraries['libr'].r_core_bin_delete
r_core_bin_delete.restype = ctypes.c_bool
r_core_bin_delete.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint32]
r_core_bin_impaddr = _libraries['libr'].r_core_bin_impaddr
r_core_bin_impaddr.restype = ctypes.c_uint64
r_core_bin_impaddr.argtypes = [POINTER_T(struct_r_bin_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_pseudo_code = _libraries['libr'].r_core_pseudo_code
r_core_pseudo_code.restype = ctypes.c_int32
r_core_pseudo_code.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_zdiff = _libraries['libr'].r_core_zdiff
r_core_zdiff.restype = ctypes.c_int32
r_core_zdiff.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_t)]
r_core_gdiff = _libraries['libr'].r_core_gdiff
r_core_gdiff.restype = ctypes.c_int32
r_core_gdiff.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_t)]
r_core_gdiff_fcn = _libraries['libr'].r_core_gdiff_fcn
r_core_gdiff_fcn.restype = ctypes.c_int32
r_core_gdiff_fcn.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64]
r_core_project_open = _libraries['libr'].r_core_project_open
r_core_project_open.restype = ctypes.c_bool
r_core_project_open.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_core_project_cat = _libraries['libr'].r_core_project_cat
r_core_project_cat.restype = ctypes.c_int32
r_core_project_cat.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_project_delete = _libraries['libr'].r_core_project_delete
r_core_project_delete.restype = ctypes.c_int32
r_core_project_delete.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_project_list = _libraries['libr'].r_core_project_list
r_core_project_list.restype = ctypes.c_int32
r_core_project_list.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_project_save_script = _libraries['libr'].r_core_project_save_script
r_core_project_save_script.restype = ctypes.c_bool
r_core_project_save_script.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_project_save = _libraries['libr'].r_core_project_save
r_core_project_save.restype = ctypes.c_bool
r_core_project_save.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_project_info = _libraries['libr'].r_core_project_info
r_core_project_info.restype = POINTER_T(ctypes.c_char)
r_core_project_info.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_project_notes_file = _libraries['libr'].r_core_project_notes_file
r_core_project_notes_file.restype = POINTER_T(ctypes.c_char)
r_core_project_notes_file.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_sysenv_begin = _libraries['libr'].r_core_sysenv_begin
r_core_sysenv_begin.restype = POINTER_T(ctypes.c_char)
r_core_sysenv_begin.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_sysenv_end = _libraries['libr'].r_core_sysenv_end
r_core_sysenv_end.restype = None
r_core_sysenv_end.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_recover_vars = _libraries['libr'].r_core_recover_vars
r_core_recover_vars.restype = None
r_core_recover_vars.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_anal_function_t), ctypes.c_bool]
class struct_r_core_bin_filter_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('offset', ctypes.c_uint64),
    ('name', POINTER_T(ctypes.c_char)),
     ]

RCoreBinFilter = struct_r_core_bin_filter_t
r_core_bin_info = _libraries['libr'].r_core_bin_info
r_core_bin_info.restype = ctypes.c_int32
r_core_bin_info.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_core_bin_filter_t), POINTER_T(ctypes.c_char)]
r_core_bin_set_arch_bits = _libraries['libr'].r_core_bin_set_arch_bits
r_core_bin_set_arch_bits.restype = ctypes.c_int32
r_core_bin_set_arch_bits.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint16]
r_core_bin_update_arch_bits = _libraries['libr'].r_core_bin_update_arch_bits
r_core_bin_update_arch_bits.restype = ctypes.c_int32
r_core_bin_update_arch_bits.argtypes = [POINTER_T(struct_r_core_t)]
r_core_bin_method_flags_str = _libraries['libr'].r_core_bin_method_flags_str
r_core_bin_method_flags_str.restype = POINTER_T(ctypes.c_char)
r_core_bin_method_flags_str.argtypes = [ctypes.c_uint64, ctypes.c_int32]
r_core_pdb_info = _libraries['libr'].r_core_pdb_info
r_core_pdb_info.restype = ctypes.c_bool
r_core_pdb_info.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_rtr_cmds = _libraries['libr'].r_core_rtr_cmds
r_core_rtr_cmds.restype = ctypes.c_int32
r_core_rtr_cmds.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_cmds_query = _libraries['libr'].r_core_rtr_cmds_query
r_core_rtr_cmds_query.restype = POINTER_T(ctypes.c_char)
r_core_rtr_cmds_query.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_rtr_pushout = _libraries['libr'].r_core_rtr_pushout
r_core_rtr_pushout.restype = None
r_core_rtr_pushout.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_list = _libraries['libr'].r_core_rtr_list
r_core_rtr_list.restype = None
r_core_rtr_list.argtypes = [POINTER_T(struct_r_core_t)]
r_core_rtr_add = _libraries['libr'].r_core_rtr_add
r_core_rtr_add.restype = None
r_core_rtr_add.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_remove = _libraries['libr'].r_core_rtr_remove
r_core_rtr_remove.restype = None
r_core_rtr_remove.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_session = _libraries['libr'].r_core_rtr_session
r_core_rtr_session.restype = None
r_core_rtr_session.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_cmd = _libraries['libr'].r_core_rtr_cmd
r_core_rtr_cmd.restype = None
r_core_rtr_cmd.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_rtr_http = _libraries['libr'].r_core_rtr_http
r_core_rtr_http.restype = ctypes.c_int32
r_core_rtr_http.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_rtr_http_stop = _libraries['libr'].r_core_rtr_http_stop
r_core_rtr_http_stop.restype = ctypes.c_int32
r_core_rtr_http_stop.argtypes = [POINTER_T(struct_r_core_t)]
r_core_rtr_gdb = _libraries['libr'].r_core_rtr_gdb
r_core_rtr_gdb.restype = ctypes.c_int32
r_core_rtr_gdb.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_visual_prevopsz = _libraries['libr'].r_core_visual_prevopsz
r_core_visual_prevopsz.restype = ctypes.c_int32
r_core_visual_prevopsz.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_visual_config = _libraries['libr'].r_core_visual_config
r_core_visual_config.restype = None
r_core_visual_config.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_mounts = _libraries['libr'].r_core_visual_mounts
r_core_visual_mounts.restype = None
r_core_visual_mounts.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_anal = _libraries['libr'].r_core_visual_anal
r_core_visual_anal.restype = None
r_core_visual_anal.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_visual_debugtraces = _libraries['libr'].r_core_visual_debugtraces
r_core_visual_debugtraces.restype = None
r_core_visual_debugtraces.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_visual_define = _libraries['libr'].r_core_visual_define
r_core_visual_define.restype = None
r_core_visual_define.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_core_visual_trackflags = _libraries['libr'].r_core_visual_trackflags
r_core_visual_trackflags.restype = ctypes.c_int32
r_core_visual_trackflags.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_view_graph = _libraries['libr'].r_core_visual_view_graph
r_core_visual_view_graph.restype = ctypes.c_int32
r_core_visual_view_graph.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_view_zigns = _libraries['libr'].r_core_visual_view_zigns
r_core_visual_view_zigns.restype = ctypes.c_int32
r_core_visual_view_zigns.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_view_rop = _libraries['libr'].r_core_visual_view_rop
r_core_visual_view_rop.restype = ctypes.c_int32
r_core_visual_view_rop.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_comments = _libraries['libr'].r_core_visual_comments
r_core_visual_comments.restype = ctypes.c_int32
r_core_visual_comments.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_prompt = _libraries['libr'].r_core_visual_prompt
r_core_visual_prompt.restype = ctypes.c_int32
r_core_visual_prompt.argtypes = [POINTER_T(struct_r_core_t)]
r_core_visual_esil = _libraries['libr'].r_core_visual_esil
r_core_visual_esil.restype = ctypes.c_bool
r_core_visual_esil.argtypes = [POINTER_T(struct_r_core_t)]
r_core_search_preludes = _libraries['libr'].r_core_search_preludes
r_core_search_preludes.restype = ctypes.c_int32
r_core_search_preludes.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_bool]
r_core_search_prelude = _libraries['libr'].r_core_search_prelude
r_core_search_prelude.restype = ctypes.c_int32
r_core_search_prelude.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_core_get_boundaries_prot = _libraries['libr'].r_core_get_boundaries_prot
r_core_get_boundaries_prot.restype = POINTER_T(struct_r_list_t)
r_core_get_boundaries_prot.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_patch = _libraries['libr'].r_core_patch
r_core_patch.restype = ctypes.c_int32
r_core_patch.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_hack_help = _libraries['libr'].r_core_hack_help
r_core_hack_help.restype = None
r_core_hack_help.argtypes = [POINTER_T(struct_r_core_t)]
r_core_hack = _libraries['libr'].r_core_hack
r_core_hack.restype = ctypes.c_int32
r_core_hack.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_dump = _libraries['libr'].r_core_dump
r_core_dump.restype = ctypes.c_bool
r_core_dump.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32]
r_core_diff_show = _libraries['libr'].r_core_diff_show
r_core_diff_show.restype = None
r_core_diff_show.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_t)]
r_core_clippy = _libraries['libr'].r_core_clippy
r_core_clippy.restype = None
r_core_clippy.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_cmpwatch_free = _libraries['libr'].r_core_cmpwatch_free
r_core_cmpwatch_free.restype = None
r_core_cmpwatch_free.argtypes = [POINTER_T(struct_r_core_cmpwatch_t)]
r_core_cmpwatch_get = _libraries['libr'].r_core_cmpwatch_get
r_core_cmpwatch_get.restype = POINTER_T(struct_r_core_cmpwatch_t)
r_core_cmpwatch_get.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_cmpwatch_add = _libraries['libr'].r_core_cmpwatch_add
r_core_cmpwatch_add.restype = ctypes.c_int32
r_core_cmpwatch_add.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_core_cmpwatch_del = _libraries['libr'].r_core_cmpwatch_del
r_core_cmpwatch_del.restype = ctypes.c_int32
r_core_cmpwatch_del.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_cmpwatch_update = _libraries['libr'].r_core_cmpwatch_update
r_core_cmpwatch_update.restype = ctypes.c_int32
r_core_cmpwatch_update.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_cmpwatch_show = _libraries['libr'].r_core_cmpwatch_show
r_core_cmpwatch_show.restype = ctypes.c_int32
r_core_cmpwatch_show.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_int32]
r_core_cmpwatch_revert = _libraries['libr'].r_core_cmpwatch_revert
r_core_cmpwatch_revert.restype = ctypes.c_int32
r_core_cmpwatch_revert.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_undo_new = _libraries['libr'].r_core_undo_new
r_core_undo_new.restype = POINTER_T(struct_r_core_undo_t)
r_core_undo_new.argtypes = [ctypes.c_uint64, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_core_undo_print = _libraries['libr'].r_core_undo_print
r_core_undo_print.restype = None
r_core_undo_print.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(struct_c__SA_RCoreUndoCondition)]
r_core_undo_free = _libraries['libr'].r_core_undo_free
r_core_undo_free.restype = None
r_core_undo_free.argtypes = [POINTER_T(struct_r_core_undo_t)]
r_core_undo_push = _libraries['libr'].r_core_undo_push
r_core_undo_push.restype = None
r_core_undo_push.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_undo_t)]
r_core_undo_pop = _libraries['libr'].r_core_undo_pop
r_core_undo_pop.restype = None
r_core_undo_pop.argtypes = [POINTER_T(struct_r_core_t)]
RCoreLogCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_core_t), ctypes.c_int32, POINTER_T(ctypes.c_char)))
r_core_log_free = _libraries['libr'].r_core_log_free
r_core_log_free.restype = None
r_core_log_free.argtypes = [POINTER_T(struct_r_core_log_t)]
r_core_log_init = _libraries['libr'].r_core_log_init
r_core_log_init.restype = None
r_core_log_init.argtypes = [POINTER_T(struct_r_core_log_t)]
r_core_log_get = _libraries['libr'].r_core_log_get
r_core_log_get.restype = POINTER_T(ctypes.c_char)
r_core_log_get.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_log_new = _libraries['libr'].r_core_log_new
r_core_log_new.restype = POINTER_T(struct_r_core_log_t)
r_core_log_new.argtypes = []
r_core_log_run = _libraries['libr'].r_core_log_run
r_core_log_run.restype = ctypes.c_bool
r_core_log_run.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char), RCoreLogCallback]
r_core_log_list = _libraries['libr'].r_core_log_list
r_core_log_list.restype = ctypes.c_int32
r_core_log_list.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_char]
r_core_log_add = _libraries['libr'].r_core_log_add
r_core_log_add.restype = None
r_core_log_add.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_log_del = _libraries['libr'].r_core_log_del
r_core_log_del.restype = None
r_core_log_del.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
PrintItemCallback = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(None), ctypes.c_bool))
r_str_widget_list = _libraries['libr'].r_str_widget_list
r_str_widget_list.restype = POINTER_T(ctypes.c_char)
r_str_widget_list.argtypes = [POINTER_T(None), POINTER_T(struct_r_list_t), ctypes.c_int32, ctypes.c_int32, PrintItemCallback]
r_core_cmd_help = _libraries['libr'].r_core_cmd_help
r_core_cmd_help.restype = None
r_core_cmd_help.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char) * 0]
class struct_c__SA_RCoreAnalStatsItem(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('youarehere', ctypes.c_uint32),
    ('flags', ctypes.c_uint32),
    ('comments', ctypes.c_uint32),
    ('functions', ctypes.c_uint32),
    ('blocks', ctypes.c_uint32),
    ('in_functions', ctypes.c_uint32),
    ('symbols', ctypes.c_uint32),
    ('strings', ctypes.c_uint32),
    ('perm', ctypes.c_uint32),
     ]

RCoreAnalStatsItem = struct_c__SA_RCoreAnalStatsItem
class struct_c__SA_RCoreAnalStats(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('block', POINTER_T(struct_c__SA_RCoreAnalStatsItem)),
     ]

RCoreAnalStats = struct_c__SA_RCoreAnalStats
core_anal_bbs = _libraries['libr'].core_anal_bbs
core_anal_bbs.restype = ctypes.c_bool
core_anal_bbs.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
core_anal_bbs_range = _libraries['libr'].core_anal_bbs_range
core_anal_bbs_range.restype = ctypes.c_bool
core_anal_bbs_range.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_anal_hasrefs = _libraries['libr'].r_core_anal_hasrefs
r_core_anal_hasrefs.restype = POINTER_T(ctypes.c_char)
r_core_anal_hasrefs.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_bool]
r_core_anal_get_comments = _libraries['libr'].r_core_anal_get_comments
r_core_anal_get_comments.restype = POINTER_T(ctypes.c_char)
r_core_anal_get_comments.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_anal_get_stats = _libraries['libr'].r_core_anal_get_stats
r_core_anal_get_stats.restype = POINTER_T(struct_c__SA_RCoreAnalStats)
r_core_anal_get_stats.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
r_core_anal_stats_free = _libraries['libr'].r_core_anal_stats_free
r_core_anal_stats_free.restype = None
r_core_anal_stats_free.argtypes = [POINTER_T(struct_c__SA_RCoreAnalStats)]
r_line_hist_offset_up = _libraries['libr'].r_line_hist_offset_up
r_line_hist_offset_up.restype = ctypes.c_int32
r_line_hist_offset_up.argtypes = [POINTER_T(struct_r_line_t)]
r_line_hist_offset_down = _libraries['libr'].r_line_hist_offset_down
r_line_hist_offset_down.restype = ctypes.c_int32
r_line_hist_offset_down.argtypes = [POINTER_T(struct_r_line_t)]
cmd_syscall_dostr = _libraries['libr'].cmd_syscall_dostr
cmd_syscall_dostr.restype = POINTER_T(ctypes.c_char)
cmd_syscall_dostr.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int64, ctypes.c_uint64]
RCoreTaskCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(ctypes.c_char)))
RTaskState = c__EA_RTaskState
RTaskState__enumvalues = c__EA_RTaskState__enumvalues
RCoreTask = struct_r_core_task_t
RCoreTaskOneShot = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))
r_core_echo = _libraries['libr'].r_core_echo
r_core_echo.restype = None
r_core_echo.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(ctypes.c_char)]
r_core_table = _libraries['libr'].r_core_table
r_core_table.restype = POINTER_T(struct_c__SA_RTable)
r_core_table.argtypes = [POINTER_T(struct_r_core_t)]
r_core_task_scheduler_init = _libraries['libr'].r_core_task_scheduler_init
r_core_task_scheduler_init.restype = None
r_core_task_scheduler_init.argtypes = [POINTER_T(struct_r_core_tasks_t), POINTER_T(struct_r_core_t)]
r_core_task_scheduler_fini = _libraries['libr'].r_core_task_scheduler_fini
r_core_task_scheduler_fini.restype = None
r_core_task_scheduler_fini.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_get_incref = _libraries['libr'].r_core_task_get_incref
r_core_task_get_incref.restype = POINTER_T(struct_r_core_task_t)
r_core_task_get_incref.argtypes = [POINTER_T(struct_r_core_tasks_t), ctypes.c_int32]
r_core_task_print = _libraries['libr'].r_core_task_print
r_core_task_print.restype = None
r_core_task_print.argtypes = [POINTER_T(struct_r_core_t), POINTER_T(struct_r_core_task_t), ctypes.c_int32]
r_core_task_list = _libraries['libr'].r_core_task_list
r_core_task_list.restype = None
r_core_task_list.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_int32]
r_core_task_running_tasks_count = _libraries['libr'].r_core_task_running_tasks_count
r_core_task_running_tasks_count.restype = ctypes.c_int32
r_core_task_running_tasks_count.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_status = _libraries['libr'].r_core_task_status
r_core_task_status.restype = POINTER_T(ctypes.c_char)
r_core_task_status.argtypes = [POINTER_T(struct_r_core_task_t)]
r_core_task_new = _libraries['libr'].r_core_task_new
r_core_task_new.restype = POINTER_T(struct_r_core_task_t)
r_core_task_new.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_bool, POINTER_T(ctypes.c_char), RCoreTaskCallback, POINTER_T(None)]
r_core_task_incref = _libraries['libr'].r_core_task_incref
r_core_task_incref.restype = None
r_core_task_incref.argtypes = [POINTER_T(struct_r_core_task_t)]
r_core_task_decref = _libraries['libr'].r_core_task_decref
r_core_task_decref.restype = None
r_core_task_decref.argtypes = [POINTER_T(struct_r_core_task_t)]
r_core_task_enqueue = _libraries['libr'].r_core_task_enqueue
r_core_task_enqueue.restype = None
r_core_task_enqueue.argtypes = [POINTER_T(struct_r_core_tasks_t), POINTER_T(struct_r_core_task_t)]
r_core_task_enqueue_oneshot = _libraries['libr'].r_core_task_enqueue_oneshot
r_core_task_enqueue_oneshot.restype = None
r_core_task_enqueue_oneshot.argtypes = [POINTER_T(struct_r_core_tasks_t), RCoreTaskOneShot, POINTER_T(None)]
r_core_task_run_sync = _libraries['libr'].r_core_task_run_sync
r_core_task_run_sync.restype = ctypes.c_int32
r_core_task_run_sync.argtypes = [POINTER_T(struct_r_core_tasks_t), POINTER_T(struct_r_core_task_t)]
r_core_task_sync_begin = _libraries['libr'].r_core_task_sync_begin
r_core_task_sync_begin.restype = None
r_core_task_sync_begin.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_sync_end = _libraries['libr'].r_core_task_sync_end
r_core_task_sync_end.restype = None
r_core_task_sync_end.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_yield = _libraries['libr'].r_core_task_yield
r_core_task_yield.restype = None
r_core_task_yield.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_sleep_begin = _libraries['libr'].r_core_task_sleep_begin
r_core_task_sleep_begin.restype = None
r_core_task_sleep_begin.argtypes = [POINTER_T(struct_r_core_task_t)]
r_core_task_sleep_end = _libraries['libr'].r_core_task_sleep_end
r_core_task_sleep_end.restype = None
r_core_task_sleep_end.argtypes = [POINTER_T(struct_r_core_task_t)]
r_core_task_break = _libraries['libr'].r_core_task_break
r_core_task_break.restype = None
r_core_task_break.argtypes = [POINTER_T(struct_r_core_tasks_t), ctypes.c_int32]
r_core_task_break_all = _libraries['libr'].r_core_task_break_all
r_core_task_break_all.restype = None
r_core_task_break_all.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_del = _libraries['libr'].r_core_task_del
r_core_task_del.restype = ctypes.c_int32
r_core_task_del.argtypes = [POINTER_T(struct_r_core_tasks_t), ctypes.c_int32]
r_core_task_del_all_done = _libraries['libr'].r_core_task_del_all_done
r_core_task_del_all_done.restype = None
r_core_task_del_all_done.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_self = _libraries['libr'].r_core_task_self
r_core_task_self.restype = POINTER_T(struct_r_core_task_t)
r_core_task_self.argtypes = [POINTER_T(struct_r_core_tasks_t)]
r_core_task_join = _libraries['libr'].r_core_task_join
r_core_task_join.restype = None
r_core_task_join.argtypes = [POINTER_T(struct_r_core_tasks_t), POINTER_T(struct_r_core_task_t), ctypes.c_int32]
inRangeCb = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_r_core_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, POINTER_T(None)))
r_core_search_value_in_range = _libraries['libr'].r_core_search_value_in_range
r_core_search_value_in_range.restype = ctypes.c_int32
r_core_search_value_in_range.argtypes = [POINTER_T(struct_r_core_t), RInterval, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, inRangeCb, POINTER_T(None)]
r_core_autocomplete_add = _libraries['libr'].r_core_autocomplete_add
r_core_autocomplete_add.restype = POINTER_T(struct_r_core_autocomplete_t)
r_core_autocomplete_add.argtypes = [POINTER_T(struct_r_core_autocomplete_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_bool]
r_core_autocomplete_free = _libraries['libr'].r_core_autocomplete_free
r_core_autocomplete_free.restype = None
r_core_autocomplete_free.argtypes = [POINTER_T(struct_r_core_autocomplete_t)]
r_core_autocomplete_reload = _libraries['libr'].r_core_autocomplete_reload
r_core_autocomplete_reload.restype = None
r_core_autocomplete_reload.argtypes = [POINTER_T(struct_r_core_t)]
r_core_autocomplete_find = _libraries['libr'].r_core_autocomplete_find
r_core_autocomplete_find.restype = POINTER_T(struct_r_core_autocomplete_t)
r_core_autocomplete_find.argtypes = [POINTER_T(struct_r_core_autocomplete_t), POINTER_T(ctypes.c_char), ctypes.c_bool]
r_core_autocomplete_remove = _libraries['libr'].r_core_autocomplete_remove
r_core_autocomplete_remove.restype = ctypes.c_bool
r_core_autocomplete_remove.argtypes = [POINTER_T(struct_r_core_autocomplete_t), POINTER_T(ctypes.c_char)]
r_core_anal_propagate_noreturn = _libraries['libr'].r_core_anal_propagate_noreturn
r_core_anal_propagate_noreturn.restype = None
r_core_anal_propagate_noreturn.argtypes = [POINTER_T(struct_r_core_t), ctypes.c_uint64]
r_core_plugin_java = struct_r_core_plugin_t # Variable struct_r_core_plugin_t
r_core_plugin_a2f = struct_r_core_plugin_t # Variable struct_r_core_plugin_t
r_core_annotated_code_print_json = _libraries['libr'].r_core_annotated_code_print_json
r_core_annotated_code_print_json.restype = None
r_core_annotated_code_print_json.argtypes = [POINTER_T(struct_r_annotated_code_t)]
r_core_annotated_code_print = _libraries['libr'].r_core_annotated_code_print
r_core_annotated_code_print.restype = None
r_core_annotated_code_print.argtypes = [POINTER_T(struct_r_annotated_code_t), POINTER_T(struct_r_vector_t)]
r_core_annotated_code_print_comment_cmds = _libraries['libr'].r_core_annotated_code_print_comment_cmds
r_core_annotated_code_print_comment_cmds.restype = None
r_core_annotated_code_print_comment_cmds.argtypes = [POINTER_T(struct_r_annotated_code_t)]
__all__ = \
    ['AUTOCOMPLETE_DEFAULT', 'AUTOCOMPLETE_MS', 'DEFAULT', 'DEL',
    'PANEL_FUN_NOFUN', 'PANEL_FUN_SAKURA', 'PANEL_FUN_SNOW',
    'PANEL_LAYOUT_DEFAULT_DYNAMIC', 'PANEL_LAYOUT_DEFAULT_STATIC',
    'PANEL_MODE_DEFAULT', 'PANEL_MODE_HELP', 'PANEL_MODE_MENU',
    'PANEL_MODE_WINDOW', 'PANEL_MODE_ZOOM', 'PANEL_TYPE_DEFAULT',
    'PANEL_TYPE_MENU', 'PTRACE_ARCH_PRCTL', 'PTRACE_ATTACH',
    'PTRACE_CONT', 'PTRACE_DETACH', 'PTRACE_GETEVENTMSG',
    'PTRACE_GETFPREGS', 'PTRACE_GETFPXREGS', 'PTRACE_GETREGS',
    'PTRACE_GETREGSET', 'PTRACE_GETSIGINFO', 'PTRACE_GETSIGMASK',
    'PTRACE_GET_THREAD_AREA', 'PTRACE_INTERRUPT', 'PTRACE_KILL',
    'PTRACE_LISTEN', 'PTRACE_PEEKDATA', 'PTRACE_PEEKSIGINFO',
    'PTRACE_PEEKTEXT', 'PTRACE_PEEKUSER', 'PTRACE_POKEDATA',
    'PTRACE_POKETEXT', 'PTRACE_POKEUSER', 'PTRACE_SECCOMP_GET_FILTER',
    'PTRACE_SECCOMP_GET_METADATA', 'PTRACE_SEIZE', 'PTRACE_SETFPREGS',
    'PTRACE_SETFPXREGS', 'PTRACE_SETOPTIONS', 'PTRACE_SETREGS',
    'PTRACE_SETREGSET', 'PTRACE_SETSIGINFO', 'PTRACE_SETSIGMASK',
    'PTRACE_SET_THREAD_AREA', 'PTRACE_SINGLEBLOCK',
    'PTRACE_SINGLESTEP', 'PTRACE_SYSCALL', 'PTRACE_SYSEMU',
    'PTRACE_SYSEMU_SINGLESTEP', 'PTRACE_TRACEME', 'PrintItemCallback',
    'QUIT', 'RAnalOpMask', 'RAnalOpMask__enumvalues',
    'RAutocompleteType', 'RAutocompleteType__enumvalues',
    'RCoreAnalStats', 'RCoreAnalStatsItem', 'RCoreAsmHit',
    'RCoreAutocomplete', 'RCoreAutocompleteType',
    'RCoreAutocompleteType__enumvalues', 'RCoreBinFilter',
    'RCoreCmpWatcher', 'RCoreFile', 'RCoreGadget', 'RCoreItem',
    'RCoreLog', 'RCoreLogCallback', 'RCoreRtrHost',
    'RCoreSearchCallback', 'RCoreTask', 'RCoreTaskCallback',
    'RCoreTaskOneShot', 'RCoreTaskScheduler', 'RCoreTimes',
    'RCoreUndo', 'RCoreUndoCondition', 'RCoreVisual',
    'RCoreVisualMode', 'RCoreVisualMode__enumvalues',
    'RCoreVisualTab', 'RInterval', 'RLinePromptType',
    'RLinePromptType__enumvalues', 'RNCAND', 'RNCASSIGN', 'RNCDEC',
    'RNCDIV', 'RNCEND', 'RNCINC', 'RNCLEFTP', 'RNCMINUS', 'RNCMOD',
    'RNCMUL', 'RNCNAME', 'RNCNEG', 'RNCNUMBER', 'RNCORR', 'RNCPLUS',
    'RNCPRINT', 'RNCRIGHTP', 'RNCROL', 'RNCROR', 'RNCSHL', 'RNCSHR',
    'RNCXOR', 'ROTATE', 'RTaskState', 'RTaskState__enumvalues',
    'R_ANAL_ACC_R', 'R_ANAL_ACC_UNKNOWN', 'R_ANAL_ACC_W',
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
    'R_ANAL_VAL_REG', 'R_CMD_DESC_TYPE_ARGV', 'R_CMD_DESC_TYPE_GROUP',
    'R_CMD_DESC_TYPE_OLDINPUT', 'R_CMD_STATUS_ERROR',
    'R_CMD_STATUS_EXIT', 'R_CMD_STATUS_INVALID', 'R_CMD_STATUS_OK',
    'R_CMD_STATUS_WRONG_ARGS', 'R_CORE_AUTOCMPLT_BRKP',
    'R_CORE_AUTOCMPLT_DFLT', 'R_CORE_AUTOCMPLT_END',
    'R_CORE_AUTOCMPLT_EVAL', 'R_CORE_AUTOCMPLT_FCN',
    'R_CORE_AUTOCMPLT_FILE', 'R_CORE_AUTOCMPLT_FLAG',
    'R_CORE_AUTOCMPLT_FLSP', 'R_CORE_AUTOCMPLT_MACR',
    'R_CORE_AUTOCMPLT_MINS', 'R_CORE_AUTOCMPLT_MS',
    'R_CORE_AUTOCMPLT_OPTN', 'R_CORE_AUTOCMPLT_PRJT',
    'R_CORE_AUTOCMPLT_SDB', 'R_CORE_AUTOCMPLT_SEEK',
    'R_CORE_AUTOCMPLT_THME', 'R_CORE_AUTOCMPLT_ZIGN',
    'R_CORE_TASK_STATE_BEFORE_START', 'R_CORE_TASK_STATE_DONE',
    'R_CORE_TASK_STATE_RUNNING', 'R_CORE_TASK_STATE_SLEEPING',
    'R_CORE_VISUAL_MODE_CD', 'R_CORE_VISUAL_MODE_DB',
    'R_CORE_VISUAL_MODE_OV', 'R_CORE_VISUAL_MODE_PD',
    'R_CORE_VISUAL_MODE_PX', 'R_DBG_RECOIL_CONTINUE',
    'R_DBG_RECOIL_NONE', 'R_DBG_RECOIL_STEP', 'R_LINE_PROMPT_DEFAULT',
    'R_LINE_PROMPT_FILE', 'R_LINE_PROMPT_OFFSET', 'R_LOGLVL_DEBUG',
    'R_LOGLVL_ERROR', 'R_LOGLVL_FATAL', 'R_LOGLVL_INFO',
    'R_LOGLVL_NONE', 'R_LOGLVL_SILLY', 'R_LOGLVL_VERBOSE',
    'R_LOGLVL_WARN', 'R_TH_FREED', 'R_TH_REPEAT', 'R_TH_STOP',
    '__ptrace_request', 'c__EA_RAnalCPPABI', 'c__EA_RAnalOpDirection',
    'c__EA_RAnalOpFamily', 'c__EA_RAnalOpMask', 'c__EA_RAnalOpPrefix',
    'c__EA_RAnalStackOp', 'c__EA_RAnalValueAccess',
    'c__EA_RAnalValueType', 'c__EA_RAutocompleteType',
    'c__EA_RCmdDescType', 'c__EA_RCoreVisualMode',
    'c__EA_RDebugRecoilMode', 'c__EA_RLinePromptType',
    'c__EA_RNumCalcToken', 'c__EA_RPanelType', 'c__EA_RPanelsFun',
    'c__EA_RPanelsLayout', 'c__EA_RPanelsMode',
    'c__EA_RPanelsRootState', 'c__EA_RTaskState',
    'c__EA_RThreadFunctionRet', 'c__EA__RAnalCond', 'cmd_anal_objc',
    'cmd_syscall_dostr', 'core_anal_bbs', 'core_anal_bbs_range',
    'inRangeCb', 'r_anal_data_type_t', 'r_cmd_status_t',
    'r_core_add_asmqjmp', 'r_core_agraph_print',
    'r_core_anal_address', 'r_core_anal_all',
    'r_core_anal_autoname_all_fcns',
    'r_core_anal_autoname_all_golang_fcns', 'r_core_anal_bb_seek',
    'r_core_anal_callgraph', 'r_core_anal_cc_init',
    'r_core_anal_coderefs', 'r_core_anal_codexrefs',
    'r_core_anal_cycles', 'r_core_anal_data', 'r_core_anal_datarefs',
    'r_core_anal_esil', 'r_core_anal_esil_graph', 'r_core_anal_fcn',
    'r_core_anal_fcn_autoname', 'r_core_anal_fcn_clean',
    'r_core_anal_fcn_get_calls', 'r_core_anal_fcn_list',
    'r_core_anal_fcn_list_size', 'r_core_anal_fcn_merge',
    'r_core_anal_fcn_name', 'r_core_anal_get_comments',
    'r_core_anal_get_stats', 'r_core_anal_graph',
    'r_core_anal_graph_to', 'r_core_anal_hasrefs',
    'r_core_anal_hint_list', 'r_core_anal_hint_print',
    'r_core_anal_importxrefs', 'r_core_anal_inflags',
    'r_core_anal_op', 'r_core_anal_optype_colorfor',
    'r_core_anal_paths', 'r_core_anal_propagate_noreturn',
    'r_core_anal_refs', 'r_core_anal_search',
    'r_core_anal_search_xrefs', 'r_core_anal_stats_free',
    'r_core_anal_type_init', 'r_core_anal_type_match',
    'r_core_anal_undefine', 'r_core_annotated_code_print',
    'r_core_annotated_code_print_comment_cmds',
    'r_core_annotated_code_print_json', 'r_core_arch_bits_at',
    'r_core_asm_back_disassemble_byte',
    'r_core_asm_back_disassemble_instr', 'r_core_asm_bwdis_len',
    'r_core_asm_bwdisassemble', 'r_core_asm_hit_free',
    'r_core_asm_hit_list_new', 'r_core_asm_hit_new',
    'r_core_asm_search', 'r_core_asm_strsearch',
    'r_core_autocomplete', 'r_core_autocomplete_add',
    'r_core_autocomplete_find', 'r_core_autocomplete_free',
    'r_core_autocomplete_reload', 'r_core_autocomplete_remove',
    'r_core_autocomplete_types_t', 'r_core_bb_starts_in_middle',
    'r_core_bin_delete', 'r_core_bin_export_info',
    'r_core_bin_impaddr', 'r_core_bin_info', 'r_core_bin_list',
    'r_core_bin_load', 'r_core_bin_load_structs',
    'r_core_bin_method_flags_str', 'r_core_bin_raise',
    'r_core_bin_rebase', 'r_core_bin_set_arch_bits',
    'r_core_bin_set_by_fd', 'r_core_bin_set_by_name',
    'r_core_bin_set_env', 'r_core_bin_update_arch_bits',
    'r_core_bind', 'r_core_bind_cons', 'r_core_block_read',
    'r_core_block_size', 'r_core_cast', 'r_core_clippy', 'r_core_cmd',
    'r_core_cmd0', 'r_core_cmd_buffer', 'r_core_cmd_command',
    'r_core_cmd_file', 'r_core_cmd_foreach', 'r_core_cmd_foreach3',
    'r_core_cmd_help', 'r_core_cmd_init', 'r_core_cmd_lines',
    'r_core_cmd_pipe', 'r_core_cmd_str', 'r_core_cmd_str_pipe',
    'r_core_cmd_strf', 'r_core_cmd_task_sync', 'r_core_cmdf',
    'r_core_cmpwatch_add', 'r_core_cmpwatch_del',
    'r_core_cmpwatch_free', 'r_core_cmpwatch_get',
    'r_core_cmpwatch_revert', 'r_core_cmpwatch_show',
    'r_core_cmpwatch_update', 'r_core_config_init',
    'r_core_config_update', 'r_core_debug_rr', 'r_core_diff_show',
    'r_core_disasm_pde', 'r_core_disasm_pdi',
    'r_core_disasm_pdi_with_buf', 'r_core_disassemble_bytes',
    'r_core_disassemble_instr', 'r_core_dump', 'r_core_echo',
    'r_core_editor', 'r_core_esil_cmd', 'r_core_esil_step',
    'r_core_esil_step_back', 'r_core_extend_at', 'r_core_fgets',
    'r_core_file_bin_raise', 'r_core_file_binlist',
    'r_core_file_close', 'r_core_file_close_all_but',
    'r_core_file_close_fd', 'r_core_file_cur', 'r_core_file_cur_fd',
    'r_core_file_find_by_fd', 'r_core_file_find_by_name',
    'r_core_file_free', 'r_core_file_get_by_fd', 'r_core_file_list',
    'r_core_file_open', 'r_core_file_open_many', 'r_core_file_reopen',
    'r_core_file_reopen_debug', 'r_core_file_reopen_remote_debug',
    'r_core_file_set_by_fd', 'r_core_file_set_by_file',
    'r_core_file_set_by_name', 'r_core_fini',
    'r_core_flag_get_by_spaces', 'r_core_flag_in_middle',
    'r_core_flush', 'r_core_fortune_list',
    'r_core_fortune_list_types', 'r_core_fortune_print_random',
    'r_core_free', 'r_core_gadget_free', 'r_core_gdiff',
    'r_core_gdiff_fcn', 'r_core_get_asmqjmps', 'r_core_get_bin',
    'r_core_get_boundaries_prot', 'r_core_get_config',
    'r_core_get_cons', 'r_core_get_func_args',
    'r_core_get_section_name', 'r_core_get_stacksz',
    'r_core_get_theme', 'r_core_getreloc', 'r_core_hack',
    'r_core_hack_help', 'r_core_init', 'r_core_is_valid_offset',
    'r_core_item_at', 'r_core_item_free', 'r_core_lines_currline',
    'r_core_lines_initcache', 'r_core_link_stroff',
    'r_core_list_themes', 'r_core_loadlibs', 'r_core_loadlibs_init',
    'r_core_log_add', 'r_core_log_del', 'r_core_log_free',
    'r_core_log_get', 'r_core_log_init', 'r_core_log_list',
    'r_core_log_new', 'r_core_log_run', 'r_core_ncast', 'r_core_new',
    'r_core_op_anal', 'r_core_op_str', 'r_core_parse_radare2rc',
    'r_core_patch', 'r_core_pava', 'r_core_pdb_info',
    'r_core_plugin_a2f', 'r_core_plugin_java', 'r_core_prevop_addr',
    'r_core_prevop_addr_force', 'r_core_print_bb_custom',
    'r_core_print_bb_gml', 'r_core_print_disasm',
    'r_core_print_disasm_all', 'r_core_print_disasm_instructions',
    'r_core_print_disasm_instructions_with_buf',
    'r_core_print_disasm_json', 'r_core_print_func_args',
    'r_core_print_scrollbar', 'r_core_print_scrollbar_bottom',
    'r_core_project_cat', 'r_core_project_delete',
    'r_core_project_execute_cmds', 'r_core_project_info',
    'r_core_project_list', 'r_core_project_load',
    'r_core_project_load_bg', 'r_core_project_notes_file',
    'r_core_project_open', 'r_core_project_save',
    'r_core_project_save_script', 'r_core_prompt',
    'r_core_prompt_exec', 'r_core_prompt_loop', 'r_core_pseudo_code',
    'r_core_recover_vars', 'r_core_rtr_add', 'r_core_rtr_cmd',
    'r_core_rtr_cmds', 'r_core_rtr_cmds_query', 'r_core_rtr_gdb',
    'r_core_rtr_http', 'r_core_rtr_http_stop', 'r_core_rtr_list',
    'r_core_rtr_pushout', 'r_core_rtr_remove', 'r_core_rtr_session',
    'r_core_run_script', 'r_core_search_cb', 'r_core_search_prelude',
    'r_core_search_preludes', 'r_core_search_value_in_range',
    'r_core_seek', 'r_core_seek_align', 'r_core_seek_arch_bits',
    'r_core_seek_base', 'r_core_seek_delta', 'r_core_seek_next',
    'r_core_seek_previous', 'r_core_seek_size', 'r_core_serve',
    'r_core_set_asm_configs', 'r_core_set_asmqjmps',
    'r_core_setup_debugger', 'r_core_shift_block', 'r_core_syscall',
    'r_core_syscallf', 'r_core_sysenv_begin', 'r_core_sysenv_end',
    'r_core_table', 'r_core_task_break', 'r_core_task_break_all',
    'r_core_task_decref', 'r_core_task_del',
    'r_core_task_del_all_done', 'r_core_task_enqueue',
    'r_core_task_enqueue_oneshot', 'r_core_task_get_incref',
    'r_core_task_incref', 'r_core_task_join', 'r_core_task_list',
    'r_core_task_new', 'r_core_task_print', 'r_core_task_run_sync',
    'r_core_task_running_tasks_count', 'r_core_task_scheduler_fini',
    'r_core_task_scheduler_init', 'r_core_task_self',
    'r_core_task_sleep_begin', 'r_core_task_sleep_end',
    'r_core_task_status', 'r_core_task_sync_begin',
    'r_core_task_sync_end', 'r_core_task_yield',
    'r_core_transform_op', 'r_core_undo_free', 'r_core_undo_new',
    'r_core_undo_pop', 'r_core_undo_print', 'r_core_undo_push',
    'r_core_version', 'r_core_visual', 'r_core_visual_anal',
    'r_core_visual_anal_classes', 'r_core_visual_append_help',
    'r_core_visual_applyDisMode', 'r_core_visual_applyHexMode',
    'r_core_visual_asm', 'r_core_visual_bit_editor',
    'r_core_visual_browse', 'r_core_visual_classes',
    'r_core_visual_cmd', 'r_core_visual_colors',
    'r_core_visual_comments', 'r_core_visual_config',
    'r_core_visual_debugtraces', 'r_core_visual_define',
    'r_core_visual_disasm_down', 'r_core_visual_disasm_up',
    'r_core_visual_esil', 'r_core_visual_graph', 'r_core_visual_hud',
    'r_core_visual_hudstuff', 'r_core_visual_jump',
    'r_core_visual_mark', 'r_core_visual_mark_del',
    'r_core_visual_mark_dump', 'r_core_visual_mark_reset',
    'r_core_visual_mark_seek', 'r_core_visual_mark_set',
    'r_core_visual_mounts', 'r_core_visual_offset',
    'r_core_visual_panels_root', 'r_core_visual_prevopsz',
    'r_core_visual_prompt', 'r_core_visual_prompt_input',
    'r_core_visual_refs', 'r_core_visual_seek_animation',
    'r_core_visual_showcursor',
    'r_core_visual_toggle_decompiler_disasm',
    'r_core_visual_trackflags', 'r_core_visual_types',
    'r_core_visual_view_graph', 'r_core_visual_view_rop',
    'r_core_visual_view_zigns', 'r_core_wait', 'r_core_write_at',
    'r_core_write_op', 'r_core_yank', 'r_core_yank_cat',
    'r_core_yank_cat_string', 'r_core_yank_dump',
    'r_core_yank_file_all', 'r_core_yank_file_ex',
    'r_core_yank_hexdump', 'r_core_yank_hexpair',
    'r_core_yank_hud_file', 'r_core_yank_hud_path',
    'r_core_yank_paste', 'r_core_yank_set', 'r_core_yank_set_str',
    'r_core_yank_string', 'r_core_yank_to', 'r_core_zdiff',
    'r_line_hist_offset_down', 'r_line_hist_offset_up',
    'r_listinfo_free', 'r_listinfo_new', 'r_log_level',
    'r_str_widget_list', 'resolve_fcn_name', 'size_t',
    'struct__IO_FILE', 'struct__IO_codecvt', 'struct__IO_marker',
    'struct__IO_wide_data', 'struct___pthread_cond_s',
    'struct___pthread_cond_s_0_0', 'struct___pthread_cond_s_1_0',
    'struct___pthread_internal_list', 'struct___pthread_mutex_s',
    'struct_buffer', 'struct_c__SA_RCoreAnalStats',
    'struct_c__SA_RCoreAnalStatsItem', 'struct_c__SA_RCoreGadget',
    'struct_c__SA_RCoreUndoCondition', 'struct_c__SA_RListInfo',
    'struct_c__SA_RNumCalcValue', 'struct_c__SA_RStrBuf',
    'struct_c__SA_RStrpool', 'struct_c__SA_RTable',
    'struct_c__SA_dict', 'struct_cdb', 'struct_cdb_hp',
    'struct_cdb_hplist', 'struct_cdb_make', 'struct_ht_pp_bucket_t',
    'struct_ht_pp_kv', 'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_in_addr',
    'struct_layer_t', 'struct_ls_iter_t', 'struct_ls_t',
    'struct_pj_t', 'struct_ptrace_wrap_instance_t',
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
    'struct_r_anal_value_t', 'struct_r_annotated_code_t',
    'struct_r_ascii_graph_t', 'struct_r_ascii_node_t',
    'struct_r_asm_op_t', 'struct_r_asm_plugin_t', 'struct_r_asm_t',
    'struct_r_bin_addr_t', 'struct_r_bin_arch_options_t',
    'struct_r_bin_bind_t', 'struct_r_bin_dbginfo_t',
    'struct_r_bin_file_t', 'struct_r_bin_hash_t',
    'struct_r_bin_import_t', 'struct_r_bin_info_t',
    'struct_r_bin_object_t', 'struct_r_bin_plugin_t',
    'struct_r_bin_reloc_t', 'struct_r_bin_section_t',
    'struct_r_bin_symbol_t', 'struct_r_bin_t', 'struct_r_bin_write_t',
    'struct_r_bin_xtr_extract_t', 'struct_r_bin_xtr_metadata_t',
    'struct_r_bin_xtr_plugin_t', 'struct_r_bp_arch_t',
    'struct_r_bp_item_t', 'struct_r_bp_plugin_t', 'struct_r_bp_t',
    'struct_r_buf_t', 'struct_r_buffer_methods_t', 'struct_r_cache_t',
    'struct_r_cmd_alias_t', 'struct_r_cmd_desc_example_t',
    'struct_r_cmd_desc_help_t', 'struct_r_cmd_desc_t',
    'struct_r_cmd_desc_t_0_0', 'struct_r_cmd_desc_t_0_1',
    'struct_r_cmd_descriptor_t', 'struct_r_cmd_item_t',
    'struct_r_cmd_macro_label_t', 'struct_r_cmd_macro_t',
    'struct_r_cmd_t', 'struct_r_config_t', 'struct_r_cons_bind_t',
    'struct_r_cons_canvas_t', 'struct_r_cons_context_t',
    'struct_r_cons_grep_t', 'struct_r_cons_palette_t',
    'struct_r_cons_printable_palette_t', 'struct_r_cons_t',
    'struct_r_core_asm_hit', 'struct_r_core_autocomplete_t',
    'struct_r_core_bin_filter_t', 'struct_r_core_bind_t',
    'struct_r_core_cmpwatch_t', 'struct_r_core_file_t',
    'struct_r_core_graph_hits_t', 'struct_r_core_item_t',
    'struct_r_core_log_t', 'struct_r_core_plugin_t',
    'struct_r_core_rtr_host_t', 'struct_r_core_t',
    'struct_r_core_task_t', 'struct_r_core_tasks_t',
    'struct_r_core_times_t', 'struct_r_core_undo_t',
    'struct_r_core_visual_t', 'struct_r_core_visual_tab_t',
    'struct_r_debug_checkpoint_t', 'struct_r_debug_desc_plugin_t',
    'struct_r_debug_info_t', 'struct_r_debug_map_t',
    'struct_r_debug_plugin_t', 'struct_r_debug_reason_t',
    'struct_r_debug_session_t', 'struct_r_debug_t',
    'struct_r_debug_trace_t', 'struct_r_egg_emit_t',
    'struct_r_egg_lang_t', 'struct_r_egg_lang_t_0',
    'struct_r_egg_lang_t_1', 'struct_r_egg_lang_t_2',
    'struct_r_egg_t', 'struct_r_event_t', 'struct_r_flag_bind_t',
    'struct_r_flag_item_t', 'struct_r_flag_t', 'struct_r_fs_shell_t',
    'struct_r_fs_t', 'struct_r_graph_node_t', 'struct_r_graph_t',
    'struct_r_hud_t', 'struct_r_id_pool_t', 'struct_r_id_storage_t',
    'struct_r_interval_node_t', 'struct_r_interval_t',
    'struct_r_interval_tree_t', 'struct_r_io_bind_t',
    'struct_r_io_desc_t', 'struct_r_io_map_t', 'struct_r_io_plugin_t',
    'struct_r_io_t', 'struct_r_io_undo_t', 'struct_r_io_undos_t',
    'struct_r_lang_plugin_t', 'struct_r_lang_t', 'struct_r_lib_t',
    'struct_r_line_buffer_t', 'struct_r_line_comp_t',
    'struct_r_line_hist_t', 'struct_r_line_t', 'struct_r_list_iter_t',
    'struct_r_list_t', 'struct_r_num_calc_t', 'struct_r_num_t',
    'struct_r_panel_model_t', 'struct_r_panel_pos_t',
    'struct_r_panel_t', 'struct_r_panel_view_t',
    'struct_r_panels_menu_item', 'struct_r_panels_menu_t',
    'struct_r_panels_root_t', 'struct_r_panels_t',
    'struct_r_parse_plugin_t', 'struct_r_parse_t', 'struct_r_print_t',
    'struct_r_print_zoom_t', 'struct_r_pvector_t', 'struct_r_queue_t',
    'struct_r_rb_node_t', 'struct_r_reg_arena_t',
    'struct_r_reg_item_t', 'struct_r_reg_set_t', 'struct_r_reg_t',
    'struct_r_search_keyword_t', 'struct_r_search_t',
    'struct_r_selection_widget_t', 'struct_r_skiplist_node_t',
    'struct_r_skiplist_t', 'struct_r_socket_t', 'struct_r_space_t',
    'struct_r_spaces_t', 'struct_r_stack_t',
    'struct_r_str_constpool_t', 'struct_r_syscall_item_t',
    'struct_r_syscall_port_t', 'struct_r_syscall_t',
    'struct_r_th_cond_t', 'struct_r_th_lock_t', 'struct_r_th_sem_t',
    'struct_r_th_t', 'struct_r_tree_node_t', 'struct_r_tree_t',
    'struct_r_vector_t', 'struct_rcolor_t', 'struct_sdb_kv',
    'struct_sdb_t', 'struct_sockaddr_in', 'struct_termios',
    'union___pthread_cond_s_0', 'union___pthread_cond_s_1',
    'union_c__UA_pthread_cond_t', 'union_c__UA_pthread_mutex_t',
    'union_c__UA_sem_t', 'union_r_cmd_desc_t_0']

libr = _libraries['libr']

if __name__ == "__main__":
    r2c = libr.r_core_new()
    libr.r_core_init(r2c)
    fh = libr.r_core_file_open(r2c, ctypes.create_string_buffer(b"/bin/ls"), 0b101, 0)
    libr.r_core_bin_load(r2c, ctypes.create_string_buffer(b"/bin/ls"), (1<<64) - 1)
    libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"ieq"))
    libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"aaa"))
    print(ctypes.string_at(libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"pdj"))))
    libr.r_core_file_close(r2c, fh)
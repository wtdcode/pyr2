# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_cons as _libr_cons


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



r_cons_version = _libr_cons.r_cons_version
r_cons_version.restype = POINTER_T(ctypes.c_char)
r_cons_version.argtypes = []
RConsGetSize = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))
RConsGetCursor = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))
RConsIsBreaked = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool))
RConsFlush = POINTER_T(ctypes.CFUNCTYPE(None))
RConsGrepCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(ctypes.c_char)))
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

RConsBind = struct_r_cons_bind_t
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

RConsGrep = struct_r_cons_grep_t

# values for enumeration 'c__Ea_ALPHA_RESET'
c__Ea_ALPHA_RESET__enumvalues = {
    0: 'ALPHA_RESET',
    1: 'ALPHA_FG',
    2: 'ALPHA_BG',
    3: 'ALPHA_FGBG',
}
ALPHA_RESET = 0
ALPHA_FG = 1
ALPHA_BG = 2
ALPHA_FGBG = 3
c__Ea_ALPHA_RESET = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_CONS_ATTR_BOLD'
c__Ea_R_CONS_ATTR_BOLD__enumvalues = {
    2: 'R_CONS_ATTR_BOLD',
    4: 'R_CONS_ATTR_DIM',
    8: 'R_CONS_ATTR_ITALIC',
    16: 'R_CONS_ATTR_UNDERLINE',
    32: 'R_CONS_ATTR_BLINK',
}
R_CONS_ATTR_BOLD = 2
R_CONS_ATTR_DIM = 4
R_CONS_ATTR_ITALIC = 8
R_CONS_ATTR_UNDERLINE = 16
R_CONS_ATTR_BLINK = 32
c__Ea_R_CONS_ATTR_BOLD = ctypes.c_int # enum
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

RColor = struct_rcolor_t
class struct_r_cons_palette_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('b0x00', RColor),
    ('b0x7f', RColor),
    ('b0xff', RColor),
    ('args', RColor),
    ('bin', RColor),
    ('btext', RColor),
    ('call', RColor),
    ('cjmp', RColor),
    ('cmp', RColor),
    ('comment', RColor),
    ('usercomment', RColor),
    ('creg', RColor),
    ('flag', RColor),
    ('fline', RColor),
    ('floc', RColor),
    ('flow', RColor),
    ('flow2', RColor),
    ('fname', RColor),
    ('help', RColor),
    ('input', RColor),
    ('invalid', RColor),
    ('jmp', RColor),
    ('label', RColor),
    ('math', RColor),
    ('mov', RColor),
    ('nop', RColor),
    ('num', RColor),
    ('offset', RColor),
    ('other', RColor),
    ('pop', RColor),
    ('prompt', RColor),
    ('push', RColor),
    ('crypto', RColor),
    ('reg', RColor),
    ('reset', RColor),
    ('ret', RColor),
    ('swi', RColor),
    ('trap', RColor),
    ('ucall', RColor),
    ('ujmp', RColor),
    ('ai_read', RColor),
    ('ai_write', RColor),
    ('ai_exec', RColor),
    ('ai_seq', RColor),
    ('ai_ascii', RColor),
    ('gui_cflow', RColor),
    ('gui_dataoffset', RColor),
    ('gui_background', RColor),
    ('gui_alt_background', RColor),
    ('gui_border', RColor),
    ('wordhl', RColor),
    ('linehl', RColor),
    ('func_var', RColor),
    ('func_var_type', RColor),
    ('func_var_addr', RColor),
    ('widget_bg', RColor),
    ('widget_sel', RColor),
    ('graph_box', RColor),
    ('graph_box2', RColor),
    ('graph_box3', RColor),
    ('graph_box4', RColor),
    ('graph_true', RColor),
    ('graph_false', RColor),
    ('graph_trufae', RColor),
    ('graph_traced', RColor),
    ('graph_current', RColor),
    ('graph_diff_match', RColor),
    ('graph_diff_unmatch', RColor),
    ('graph_diff_unknown', RColor),
    ('graph_diff_new', RColor),
     ]

RConsPalette = struct_r_cons_palette_t
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

RConsPrintablePalette = struct_r_cons_printable_palette_t
RConsEvent = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))
class struct_r_cons_canvas_t(ctypes.Structure):
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

class struct_r_str_constpool_t(ctypes.Structure):
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

struct_r_str_constpool_t._pack_ = True # source:False
struct_r_str_constpool_t._fields_ = [
    ('ht', POINTER_T(struct_ht_pp_t)),
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

RConsCanvas = struct_r_cons_canvas_t
RConsEditorCallback = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))
RConsClickCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_int32, ctypes.c_int32))
RConsBreakCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))
RConsSleepBeginCallback = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(None), POINTER_T(None)))
RConsSleepEndCallback = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None)))
RConsQueueTaskOneshot = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), POINTER_T(None), POINTER_T(None)))
RConsFunctionKey = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None), ctypes.c_int32))

# values for enumeration 'c__EA_RConsColorMode'
c__EA_RConsColorMode__enumvalues = {
    0: 'COLOR_MODE_DISABLED',
    1: 'COLOR_MODE_16',
    2: 'COLOR_MODE_256',
    3: 'COLOR_MODE_16M',
}
COLOR_MODE_DISABLED = 0
COLOR_MODE_16 = 1
COLOR_MODE_256 = 2
COLOR_MODE_16M = 3
c__EA_RConsColorMode = ctypes.c_int # enum
RConsColorMode = c__EA_RConsColorMode
RConsColorMode__enumvalues = c__EA_RConsColorMode__enumvalues
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
    ('grep', RConsGrep),
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
    ('cpal', RConsPalette),
    ('PADDING_2', ctypes.c_ubyte * 6),
    ('pal', RConsPrintablePalette),
]

RConsContext = struct_r_cons_context_t
class struct_r_cons_t(ctypes.Structure):
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

class struct_r_line_t(ctypes.Structure):
    pass

class struct_r_line_buffer_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('data', ctypes.c_char * 4096),
    ('index', ctypes.c_int32),
    ('length', ctypes.c_int32),
     ]

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
class struct_r_line_comp_t(ctypes.Structure):
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

class struct_r_hud_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('current_entry_n', ctypes.c_int32),
    ('top_entry_n', ctypes.c_int32),
    ('activate', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('vi', ctypes.c_int32),
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

RCons = struct_r_cons_t

# values for enumeration 'c__Ea_PAL_PROMPT'
c__Ea_PAL_PROMPT__enumvalues = {
    0: 'PAL_PROMPT',
    1: 'PAL_ADDRESS',
    2: 'PAL_DEFAULT',
    3: 'PAL_CHANGED',
    4: 'PAL_JUMP',
    5: 'PAL_CALL',
    6: 'PAL_PUSH',
    7: 'PAL_TRAP',
    8: 'PAL_CMP',
    9: 'PAL_RET',
    10: 'PAL_NOP',
    11: 'PAL_METADATA',
    12: 'PAL_HEADER',
    13: 'PAL_PRINTABLE',
    14: 'PAL_LINES0',
    15: 'PAL_LINES1',
    16: 'PAL_LINES2',
    17: 'PAL_00',
    18: 'PAL_7F',
    19: 'PAL_FF',
}
PAL_PROMPT = 0
PAL_ADDRESS = 1
PAL_DEFAULT = 2
PAL_CHANGED = 3
PAL_JUMP = 4
PAL_CALL = 5
PAL_PUSH = 6
PAL_TRAP = 7
PAL_CMP = 8
PAL_RET = 9
PAL_NOP = 10
PAL_METADATA = 11
PAL_HEADER = 12
PAL_PRINTABLE = 13
PAL_LINES0 = 14
PAL_LINES1 = 15
PAL_LINES2 = 16
PAL_00 = 17
PAL_7F = 18
PAL_FF = 19
c__Ea_PAL_PROMPT = ctypes.c_int # enum

# values for enumeration 'c__Ea_LINE_NONE'
c__Ea_LINE_NONE__enumvalues = {
    0: 'LINE_NONE',
    1: 'LINE_TRUE',
    2: 'LINE_FALSE',
    3: 'LINE_UNCJMP',
    4: 'LINE_NOSYM_VERT',
    5: 'LINE_NOSYM_HORIZ',
}
LINE_NONE = 0
LINE_TRUE = 1
LINE_FALSE = 2
LINE_UNCJMP = 3
LINE_NOSYM_VERT = 4
LINE_NOSYM_HORIZ = 5
c__Ea_LINE_NONE = ctypes.c_int # enum

# values for enumeration 'c__EA_RViMode'
c__EA_RViMode__enumvalues = {
    105: 'INSERT_MODE',
    99: 'CONTROL_MODE',
}
INSERT_MODE = 105
CONTROL_MODE = 99
c__EA_RViMode = ctypes.c_int # enum
RViMode = c__EA_RViMode
RViMode__enumvalues = c__EA_RViMode__enumvalues
class struct_r_cons_canvas_line_style_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('color', ctypes.c_int32),
    ('symbol', ctypes.c_int32),
    ('dot_style', ctypes.c_int32),
     ]

RCanvasLineStyle = struct_r_cons_canvas_line_style_t
r_cons_image = _libr_cons.r_cons_image
r_cons_image.restype = None
r_cons_image.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_cons_canvas_new = _libr_cons.r_cons_canvas_new
r_cons_canvas_new.restype = POINTER_T(struct_r_cons_canvas_t)
r_cons_canvas_new.argtypes = [ctypes.c_int32, ctypes.c_int32]
r_cons_canvas_free = _libr_cons.r_cons_canvas_free
r_cons_canvas_free.restype = None
r_cons_canvas_free.argtypes = [POINTER_T(struct_r_cons_canvas_t)]
r_cons_canvas_clear = _libr_cons.r_cons_canvas_clear
r_cons_canvas_clear.restype = None
r_cons_canvas_clear.argtypes = [POINTER_T(struct_r_cons_canvas_t)]
r_cons_canvas_print = _libr_cons.r_cons_canvas_print
r_cons_canvas_print.restype = None
r_cons_canvas_print.argtypes = [POINTER_T(struct_r_cons_canvas_t)]
r_cons_canvas_print_region = _libr_cons.r_cons_canvas_print_region
r_cons_canvas_print_region.restype = None
r_cons_canvas_print_region.argtypes = [POINTER_T(struct_r_cons_canvas_t)]
r_cons_canvas_to_string = _libr_cons.r_cons_canvas_to_string
r_cons_canvas_to_string.restype = POINTER_T(ctypes.c_char)
r_cons_canvas_to_string.argtypes = [POINTER_T(struct_r_cons_canvas_t)]
r_cons_canvas_write = _libr_cons.r_cons_canvas_write
r_cons_canvas_write.restype = None
r_cons_canvas_write.argtypes = [POINTER_T(struct_r_cons_canvas_t), POINTER_T(ctypes.c_char)]
r_cons_canvas_gotoxy = _libr_cons.r_cons_canvas_gotoxy
r_cons_canvas_gotoxy.restype = ctypes.c_bool
r_cons_canvas_gotoxy.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32]
r_cons_canvas_box = _libr_cons.r_cons_canvas_box
r_cons_canvas_box.restype = None
r_cons_canvas_box.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_cons_canvas_circle = _libr_cons.r_cons_canvas_circle
r_cons_canvas_circle.restype = None
r_cons_canvas_circle.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_cons_canvas_line = _libr_cons.r_cons_canvas_line
r_cons_canvas_line.restype = None
r_cons_canvas_line.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_cons_canvas_line_style_t)]
r_cons_canvas_line_diagonal = _libr_cons.r_cons_canvas_line_diagonal
r_cons_canvas_line_diagonal.restype = None
r_cons_canvas_line_diagonal.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_cons_canvas_line_style_t)]
r_cons_canvas_line_square = _libr_cons.r_cons_canvas_line_square
r_cons_canvas_line_square.restype = None
r_cons_canvas_line_square.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_cons_canvas_line_style_t)]
r_cons_canvas_resize = _libr_cons.r_cons_canvas_resize
r_cons_canvas_resize.restype = ctypes.c_int32
r_cons_canvas_resize.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32]
r_cons_canvas_fill = _libr_cons.r_cons_canvas_fill
r_cons_canvas_fill.restype = None
r_cons_canvas_fill.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_char]
r_cons_canvas_line_square_defined = _libr_cons.r_cons_canvas_line_square_defined
r_cons_canvas_line_square_defined.restype = None
r_cons_canvas_line_square_defined.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_cons_canvas_line_style_t), ctypes.c_int32, ctypes.c_int32]
r_cons_canvas_line_back_edge = _libr_cons.r_cons_canvas_line_back_edge
r_cons_canvas_line_back_edge.restype = None
r_cons_canvas_line_back_edge.argtypes = [POINTER_T(struct_r_cons_canvas_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, POINTER_T(struct_r_cons_canvas_line_style_t), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_cons_new = _libr_cons.r_cons_new
r_cons_new.restype = POINTER_T(struct_r_cons_t)
r_cons_new.argtypes = []
r_cons_singleton = _libr_cons.r_cons_singleton
r_cons_singleton.restype = POINTER_T(struct_r_cons_t)
r_cons_singleton.argtypes = []
r_cons_free = _libr_cons.r_cons_free
r_cons_free.restype = POINTER_T(struct_r_cons_t)
r_cons_free.argtypes = []
r_cons_lastline = _libr_cons.r_cons_lastline
r_cons_lastline.restype = POINTER_T(ctypes.c_char)
r_cons_lastline.argtypes = [POINTER_T(ctypes.c_int32)]
r_cons_lastline_utf8_ansi_len = _libr_cons.r_cons_lastline_utf8_ansi_len
r_cons_lastline_utf8_ansi_len.restype = POINTER_T(ctypes.c_char)
r_cons_lastline_utf8_ansi_len.argtypes = [POINTER_T(ctypes.c_int32)]
r_cons_set_click = _libr_cons.r_cons_set_click
r_cons_set_click.restype = None
r_cons_set_click.argtypes = [ctypes.c_int32, ctypes.c_int32]
r_cons_get_click = _libr_cons.r_cons_get_click
r_cons_get_click.restype = ctypes.c_bool
r_cons_get_click.argtypes = [POINTER_T(ctypes.c_int32), POINTER_T(ctypes.c_int32)]
RConsBreak = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(None)))
r_cons_is_breaked = _libr_cons.r_cons_is_breaked
r_cons_is_breaked.restype = ctypes.c_bool
r_cons_is_breaked.argtypes = []
r_cons_is_interactive = _libr_cons.r_cons_is_interactive
r_cons_is_interactive.restype = ctypes.c_bool
r_cons_is_interactive.argtypes = []
r_cons_default_context_is_interactive = _libr_cons.r_cons_default_context_is_interactive
r_cons_default_context_is_interactive.restype = ctypes.c_bool
r_cons_default_context_is_interactive.argtypes = []
r_cons_sleep_begin = _libr_cons.r_cons_sleep_begin
r_cons_sleep_begin.restype = POINTER_T(None)
r_cons_sleep_begin.argtypes = []
r_cons_sleep_end = _libr_cons.r_cons_sleep_end
r_cons_sleep_end.restype = None
r_cons_sleep_end.argtypes = [POINTER_T(None)]
r_cons_break_push = _libr_cons.r_cons_break_push
r_cons_break_push.restype = None
r_cons_break_push.argtypes = [RConsBreak, POINTER_T(None)]
r_cons_break_pop = _libr_cons.r_cons_break_pop
r_cons_break_pop.restype = None
r_cons_break_pop.argtypes = []
r_cons_break_clear = _libr_cons.r_cons_break_clear
r_cons_break_clear.restype = None
r_cons_break_clear.argtypes = []
r_cons_breakword = _libr_cons.r_cons_breakword
r_cons_breakword.restype = None
r_cons_breakword.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_break_end = _libr_cons.r_cons_break_end
r_cons_break_end.restype = None
r_cons_break_end.argtypes = []
r_cons_break_timeout = _libr_cons.r_cons_break_timeout
r_cons_break_timeout.restype = None
r_cons_break_timeout.argtypes = [ctypes.c_int32]
r_cons_pipe_open = _libr_cons.r_cons_pipe_open
r_cons_pipe_open.restype = ctypes.c_int32
r_cons_pipe_open.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_cons_pipe_close = _libr_cons.r_cons_pipe_close
r_cons_pipe_close.restype = None
r_cons_pipe_close.argtypes = [ctypes.c_int32]
r_cons_push = _libr_cons.r_cons_push
r_cons_push.restype = None
r_cons_push.argtypes = []
r_cons_pop = _libr_cons.r_cons_pop
r_cons_pop.restype = None
r_cons_pop.argtypes = []
r_cons_context_new = _libr_cons.r_cons_context_new
r_cons_context_new.restype = POINTER_T(struct_r_cons_context_t)
r_cons_context_new.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_context_free = _libr_cons.r_cons_context_free
r_cons_context_free.restype = None
r_cons_context_free.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_context_load = _libr_cons.r_cons_context_load
r_cons_context_load.restype = None
r_cons_context_load.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_context_reset = _libr_cons.r_cons_context_reset
r_cons_context_reset.restype = None
r_cons_context_reset.argtypes = []
r_cons_context_is_main = _libr_cons.r_cons_context_is_main
r_cons_context_is_main.restype = ctypes.c_bool
r_cons_context_is_main.argtypes = []
r_cons_context_break = _libr_cons.r_cons_context_break
r_cons_context_break.restype = None
r_cons_context_break.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_context_break_push = _libr_cons.r_cons_context_break_push
r_cons_context_break_push.restype = None
r_cons_context_break_push.argtypes = [POINTER_T(struct_r_cons_context_t), RConsBreak, POINTER_T(None), ctypes.c_bool]
r_cons_context_break_pop = _libr_cons.r_cons_context_break_pop
r_cons_context_break_pop.restype = None
r_cons_context_break_pop.argtypes = [POINTER_T(struct_r_cons_context_t), ctypes.c_bool]
r_cons_editor = _libr_cons.r_cons_editor
r_cons_editor.restype = POINTER_T(ctypes.c_char)
r_cons_editor.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_cons_reset = _libr_cons.r_cons_reset
r_cons_reset.restype = None
r_cons_reset.argtypes = []
r_cons_reset_colors = _libr_cons.r_cons_reset_colors
r_cons_reset_colors.restype = None
r_cons_reset_colors.argtypes = []
r_cons_print_clear = _libr_cons.r_cons_print_clear
r_cons_print_clear.restype = None
r_cons_print_clear.argtypes = []
r_cons_echo = _libr_cons.r_cons_echo
r_cons_echo.restype = None
r_cons_echo.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_zero = _libr_cons.r_cons_zero
r_cons_zero.restype = None
r_cons_zero.argtypes = []
r_cons_highlight = _libr_cons.r_cons_highlight
r_cons_highlight.restype = None
r_cons_highlight.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_clear = _libr_cons.r_cons_clear
r_cons_clear.restype = None
r_cons_clear.argtypes = []
r_cons_clear_buffer = _libr_cons.r_cons_clear_buffer
r_cons_clear_buffer.restype = None
r_cons_clear_buffer.argtypes = []
r_cons_clear00 = _libr_cons.r_cons_clear00
r_cons_clear00.restype = None
r_cons_clear00.argtypes = []
r_cons_clear_line = _libr_cons.r_cons_clear_line
r_cons_clear_line.restype = None
r_cons_clear_line.argtypes = [ctypes.c_int32]
r_cons_fill_line = _libr_cons.r_cons_fill_line
r_cons_fill_line.restype = None
r_cons_fill_line.argtypes = []
r_cons_gotoxy = _libr_cons.r_cons_gotoxy
r_cons_gotoxy.restype = None
r_cons_gotoxy.argtypes = [ctypes.c_int32, ctypes.c_int32]
r_cons_get_cur_line = _libr_cons.r_cons_get_cur_line
r_cons_get_cur_line.restype = ctypes.c_int32
r_cons_get_cur_line.argtypes = []
r_cons_show_cursor = _libr_cons.r_cons_show_cursor
r_cons_show_cursor.restype = None
r_cons_show_cursor.argtypes = [ctypes.c_int32]
r_cons_swap_ground = _libr_cons.r_cons_swap_ground
r_cons_swap_ground.restype = POINTER_T(ctypes.c_char)
r_cons_swap_ground.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_drop = _libr_cons.r_cons_drop
r_cons_drop.restype = ctypes.c_bool
r_cons_drop.argtypes = [ctypes.c_int32]
r_cons_chop = _libr_cons.r_cons_chop
r_cons_chop.restype = None
r_cons_chop.argtypes = []
r_cons_set_raw = _libr_cons.r_cons_set_raw
r_cons_set_raw.restype = None
r_cons_set_raw.argtypes = [ctypes.c_bool]
r_cons_set_interactive = _libr_cons.r_cons_set_interactive
r_cons_set_interactive.restype = None
r_cons_set_interactive.argtypes = [ctypes.c_bool]
r_cons_set_last_interactive = _libr_cons.r_cons_set_last_interactive
r_cons_set_last_interactive.restype = None
r_cons_set_last_interactive.argtypes = []
r_cons_set_utf8 = _libr_cons.r_cons_set_utf8
r_cons_set_utf8.restype = None
r_cons_set_utf8.argtypes = [ctypes.c_bool]
r_cons_grep = _libr_cons.r_cons_grep
r_cons_grep.restype = None
r_cons_grep.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_printf = _libr_cons.r_cons_printf
r_cons_printf.restype = ctypes.c_int32
r_cons_printf.argtypes = [POINTER_T(ctypes.c_char)]
class struct___va_list_tag(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('gp_offset', ctypes.c_uint32),
    ('fp_offset', ctypes.c_uint32),
    ('overflow_arg_area', POINTER_T(None)),
    ('reg_save_area', POINTER_T(None)),
     ]

va_list = struct___va_list_tag * 1
r_cons_printf_list = _libr_cons.r_cons_printf_list
r_cons_printf_list.restype = None
r_cons_printf_list.argtypes = [POINTER_T(ctypes.c_char), va_list]
r_cons_strcat = _libr_cons.r_cons_strcat
r_cons_strcat.restype = None
r_cons_strcat.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_strcat_at = _libr_cons.r_cons_strcat_at
r_cons_strcat_at.restype = None
r_cons_strcat_at.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_char, ctypes.c_int32, ctypes.c_int32]
r_cons_println = _libr_cons.r_cons_println
r_cons_println.restype = None
r_cons_println.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_strcat_justify = _libr_cons.r_cons_strcat_justify
r_cons_strcat_justify.restype = None
r_cons_strcat_justify.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_char]
r_cons_memcat = _libr_cons.r_cons_memcat
r_cons_memcat.restype = ctypes.c_int32
r_cons_memcat.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_cons_newline = _libr_cons.r_cons_newline
r_cons_newline.restype = None
r_cons_newline.argtypes = []
r_cons_filter = _libr_cons.r_cons_filter
r_cons_filter.restype = None
r_cons_filter.argtypes = []
r_cons_flush = _libr_cons.r_cons_flush
r_cons_flush.restype = None
r_cons_flush.argtypes = []
r_cons_print_fps = _libr_cons.r_cons_print_fps
r_cons_print_fps.restype = None
r_cons_print_fps.argtypes = [ctypes.c_int32]
r_cons_last = _libr_cons.r_cons_last
r_cons_last.restype = None
r_cons_last.argtypes = []
r_cons_less_str = _libr_cons.r_cons_less_str
r_cons_less_str.restype = ctypes.c_int32
r_cons_less_str.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_cons_less = _libr_cons.r_cons_less
r_cons_less.restype = None
r_cons_less.argtypes = []
r_cons_2048 = _libr_cons.r_cons_2048
r_cons_2048.restype = None
r_cons_2048.argtypes = [ctypes.c_bool]
r_cons_memset = _libr_cons.r_cons_memset
r_cons_memset.restype = None
r_cons_memset.argtypes = [ctypes.c_char, ctypes.c_int32]
r_cons_visual_flush = _libr_cons.r_cons_visual_flush
r_cons_visual_flush.restype = None
r_cons_visual_flush.argtypes = []
r_cons_visual_write = _libr_cons.r_cons_visual_write
r_cons_visual_write.restype = None
r_cons_visual_write.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_is_utf8 = _libr_cons.r_cons_is_utf8
r_cons_is_utf8.restype = ctypes.c_bool
r_cons_is_utf8.argtypes = []
r_cons_cmd_help = _libr_cons.r_cons_cmd_help
r_cons_cmd_help.restype = None
r_cons_cmd_help.argtypes = [POINTER_T(ctypes.c_char) * 0, ctypes.c_bool]
r_cons_controlz = _libr_cons.r_cons_controlz
r_cons_controlz.restype = ctypes.c_int32
r_cons_controlz.argtypes = [ctypes.c_int32]
r_cons_readchar = _libr_cons.r_cons_readchar
r_cons_readchar.restype = ctypes.c_int32
r_cons_readchar.argtypes = []
r_cons_readpush = _libr_cons.r_cons_readpush
r_cons_readpush.restype = ctypes.c_bool
r_cons_readpush.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_cons_readflush = _libr_cons.r_cons_readflush
r_cons_readflush.restype = None
r_cons_readflush.argtypes = []
r_cons_switchbuf = _libr_cons.r_cons_switchbuf
r_cons_switchbuf.restype = None
r_cons_switchbuf.argtypes = [ctypes.c_bool]
r_cons_readchar_timeout = _libr_cons.r_cons_readchar_timeout
r_cons_readchar_timeout.restype = ctypes.c_int32
r_cons_readchar_timeout.argtypes = [ctypes.c_uint32]
r_cons_any_key = _libr_cons.r_cons_any_key
r_cons_any_key.restype = ctypes.c_int32
r_cons_any_key.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_eof = _libr_cons.r_cons_eof
r_cons_eof.restype = ctypes.c_int32
r_cons_eof.argtypes = []
r_cons_pal_set = _libr_cons.r_cons_pal_set
r_cons_pal_set.restype = ctypes.c_int32
r_cons_pal_set.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_cons_pal_update_event = _libr_cons.r_cons_pal_update_event
r_cons_pal_update_event.restype = None
r_cons_pal_update_event.argtypes = []
r_cons_pal_free = _libr_cons.r_cons_pal_free
r_cons_pal_free.restype = None
r_cons_pal_free.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_pal_init = _libr_cons.r_cons_pal_init
r_cons_pal_init.restype = None
r_cons_pal_init.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_pal_copy = _libr_cons.r_cons_pal_copy
r_cons_pal_copy.restype = None
r_cons_pal_copy.argtypes = [POINTER_T(struct_r_cons_context_t), POINTER_T(struct_r_cons_context_t)]
r_cons_pal_parse = _libr_cons.r_cons_pal_parse
r_cons_pal_parse.restype = POINTER_T(ctypes.c_char)
r_cons_pal_parse.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(struct_rcolor_t)]
r_cons_pal_random = _libr_cons.r_cons_pal_random
r_cons_pal_random.restype = None
r_cons_pal_random.argtypes = []
r_cons_pal_get = _libr_cons.r_cons_pal_get
r_cons_pal_get.restype = RColor
r_cons_pal_get.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_pal_get_i = _libr_cons.r_cons_pal_get_i
r_cons_pal_get_i.restype = RColor
r_cons_pal_get_i.argtypes = [ctypes.c_int32]
r_cons_pal_get_name = _libr_cons.r_cons_pal_get_name
r_cons_pal_get_name.restype = POINTER_T(ctypes.c_char)
r_cons_pal_get_name.argtypes = [ctypes.c_int32]
r_cons_pal_len = _libr_cons.r_cons_pal_len
r_cons_pal_len.restype = ctypes.c_int32
r_cons_pal_len.argtypes = []
r_cons_rgb_parse = _libr_cons.r_cons_rgb_parse
r_cons_rgb_parse.restype = ctypes.c_int32
r_cons_rgb_parse.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.c_ubyte)]
r_cons_rgb_tostring = _libr_cons.r_cons_rgb_tostring
r_cons_rgb_tostring.restype = POINTER_T(ctypes.c_char)
r_cons_rgb_tostring.argtypes = [ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte]
r_cons_pal_list = _libr_cons.r_cons_pal_list
r_cons_pal_list.restype = None
r_cons_pal_list.argtypes = [ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_cons_pal_show = _libr_cons.r_cons_pal_show
r_cons_pal_show.restype = None
r_cons_pal_show.argtypes = []
r_cons_get_size = _libr_cons.r_cons_get_size
r_cons_get_size.restype = ctypes.c_int32
r_cons_get_size.argtypes = [POINTER_T(ctypes.c_int32)]
r_cons_isatty = _libr_cons.r_cons_isatty
r_cons_isatty.restype = ctypes.c_bool
r_cons_isatty.argtypes = []
r_cons_get_cursor = _libr_cons.r_cons_get_cursor
r_cons_get_cursor.restype = ctypes.c_int32
r_cons_get_cursor.argtypes = [POINTER_T(ctypes.c_int32)]
r_cons_arrow_to_hjkl = _libr_cons.r_cons_arrow_to_hjkl
r_cons_arrow_to_hjkl.restype = ctypes.c_int32
r_cons_arrow_to_hjkl.argtypes = [ctypes.c_int32]
r_cons_html_filter = _libr_cons.r_cons_html_filter
r_cons_html_filter.restype = POINTER_T(ctypes.c_char)
r_cons_html_filter.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_int32)]
r_cons_rainbow_get = _libr_cons.r_cons_rainbow_get
r_cons_rainbow_get.restype = POINTER_T(ctypes.c_char)
r_cons_rainbow_get.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_bool]
r_cons_rainbow_free = _libr_cons.r_cons_rainbow_free
r_cons_rainbow_free.restype = None
r_cons_rainbow_free.argtypes = [POINTER_T(struct_r_cons_context_t)]
r_cons_rainbow_new = _libr_cons.r_cons_rainbow_new
r_cons_rainbow_new.restype = None
r_cons_rainbow_new.argtypes = [POINTER_T(struct_r_cons_context_t), ctypes.c_int32]
r_cons_fgets = _libr_cons.r_cons_fgets
r_cons_fgets.restype = ctypes.c_int32
r_cons_fgets.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_cons_hud = _libr_cons.r_cons_hud
r_cons_hud.restype = POINTER_T(ctypes.c_char)
r_cons_hud.argtypes = [POINTER_T(struct_r_list_t), POINTER_T(ctypes.c_char)]
r_cons_hud_path = _libr_cons.r_cons_hud_path
r_cons_hud_path.restype = POINTER_T(ctypes.c_char)
r_cons_hud_path.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_cons_hud_string = _libr_cons.r_cons_hud_string
r_cons_hud_string.restype = POINTER_T(ctypes.c_char)
r_cons_hud_string.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_hud_file = _libr_cons.r_cons_hud_file
r_cons_hud_file.restype = POINTER_T(ctypes.c_char)
r_cons_hud_file.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_get_buffer = _libr_cons.r_cons_get_buffer
r_cons_get_buffer.restype = POINTER_T(ctypes.c_char)
r_cons_get_buffer.argtypes = []
r_cons_get_buffer_len = _libr_cons.r_cons_get_buffer_len
r_cons_get_buffer_len.restype = ctypes.c_int32
r_cons_get_buffer_len.argtypes = []
r_cons_grep_help = _libr_cons.r_cons_grep_help
r_cons_grep_help.restype = None
r_cons_grep_help.argtypes = []
r_cons_grep_parsecmd = _libr_cons.r_cons_grep_parsecmd
r_cons_grep_parsecmd.restype = None
r_cons_grep_parsecmd.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_cons_grep_strip = _libr_cons.r_cons_grep_strip
r_cons_grep_strip.restype = POINTER_T(ctypes.c_char)
r_cons_grep_strip.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_cons_grep_process = _libr_cons.r_cons_grep_process
r_cons_grep_process.restype = None
r_cons_grep_process.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_grep_line = _libr_cons.r_cons_grep_line
r_cons_grep_line.restype = ctypes.c_int32
r_cons_grep_line.argtypes = [POINTER_T(ctypes.c_char), ctypes.c_int32]
r_cons_grepbuf = _libr_cons.r_cons_grepbuf
r_cons_grepbuf.restype = None
r_cons_grepbuf.argtypes = []
r_cons_rgb_init = _libr_cons.r_cons_rgb_init
r_cons_rgb_init.restype = None
r_cons_rgb_init.argtypes = []
size_t = ctypes.c_uint64
r_cons_rgb_str_mode = _libr_cons.r_cons_rgb_str_mode
r_cons_rgb_str_mode.restype = POINTER_T(ctypes.c_char)
r_cons_rgb_str_mode.argtypes = [RConsColorMode, POINTER_T(ctypes.c_char), size_t, POINTER_T(struct_rcolor_t)]
r_cons_rgb_str = _libr_cons.r_cons_rgb_str
r_cons_rgb_str.restype = POINTER_T(ctypes.c_char)
r_cons_rgb_str.argtypes = [POINTER_T(ctypes.c_char), size_t, POINTER_T(struct_rcolor_t)]
r_cons_rgb_str_off = _libr_cons.r_cons_rgb_str_off
r_cons_rgb_str_off.restype = POINTER_T(ctypes.c_char)
r_cons_rgb_str_off.argtypes = [POINTER_T(ctypes.c_char), size_t, ctypes.c_uint64]
r_cons_color = _libr_cons.r_cons_color
r_cons_color.restype = None
r_cons_color.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_cons_color_random = _libr_cons.r_cons_color_random
r_cons_color_random.restype = RColor
r_cons_color_random.argtypes = [ctypes.c_ubyte]
r_cons_invert = _libr_cons.r_cons_invert
r_cons_invert.restype = None
r_cons_invert.argtypes = [ctypes.c_int32, ctypes.c_int32]
r_cons_yesno = _libr_cons.r_cons_yesno
r_cons_yesno.restype = ctypes.c_bool
r_cons_yesno.argtypes = [ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_cons_input = _libr_cons.r_cons_input
r_cons_input.restype = POINTER_T(ctypes.c_char)
r_cons_input.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_password = _libr_cons.r_cons_password
r_cons_password.restype = POINTER_T(ctypes.c_char)
r_cons_password.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_set_cup = _libr_cons.r_cons_set_cup
r_cons_set_cup.restype = ctypes.c_bool
r_cons_set_cup.argtypes = [ctypes.c_bool]
r_cons_column = _libr_cons.r_cons_column
r_cons_column.restype = None
r_cons_column.argtypes = [ctypes.c_int32]
r_cons_get_column = _libr_cons.r_cons_get_column
r_cons_get_column.restype = ctypes.c_int32
r_cons_get_column.argtypes = []
r_cons_message = _libr_cons.r_cons_message
r_cons_message.restype = POINTER_T(ctypes.c_char)
r_cons_message.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_set_title = _libr_cons.r_cons_set_title
r_cons_set_title.restype = None
r_cons_set_title.argtypes = [POINTER_T(ctypes.c_char)]
r_cons_enable_mouse = _libr_cons.r_cons_enable_mouse
r_cons_enable_mouse.restype = ctypes.c_bool
r_cons_enable_mouse.argtypes = [ctypes.c_bool]
r_cons_enable_highlight = _libr_cons.r_cons_enable_highlight
r_cons_enable_highlight.restype = None
r_cons_enable_highlight.argtypes = [ctypes.c_bool]
r_cons_bind = _libr_cons.r_cons_bind
r_cons_bind.restype = None
r_cons_bind.argtypes = [POINTER_T(struct_r_cons_bind_t)]
r_cons_get_rune = _libr_cons.r_cons_get_rune
r_cons_get_rune.restype = POINTER_T(ctypes.c_char)
r_cons_get_rune.argtypes = [ctypes.c_ubyte]
RSelWidget = struct_r_selection_widget_t
RLineHistory = struct_r_line_hist_t
RLineBuffer = struct_r_line_buffer_t
RLineHud = struct_r_hud_t
RLine = struct_r_line_t
RLineCompletion = struct_r_line_comp_t
RLinePromptType = c__EA_RLinePromptType
RLinePromptType__enumvalues = c__EA_RLinePromptType__enumvalues
RLineCompletionCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_comp_t), POINTER_T(struct_r_line_buffer_t), c__EA_RLinePromptType, POINTER_T(None)))
RLineEditorCb = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))
RLineHistoryUpCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_t)))
RLineHistoryDownCb = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_line_t)))
r_line_new = _libr_cons.r_line_new
r_line_new.restype = POINTER_T(struct_r_line_t)
r_line_new.argtypes = []
r_line_singleton = _libr_cons.r_line_singleton
r_line_singleton.restype = POINTER_T(struct_r_line_t)
r_line_singleton.argtypes = []
r_line_free = _libr_cons.r_line_free
r_line_free.restype = None
r_line_free.argtypes = []
r_line_get_prompt = _libr_cons.r_line_get_prompt
r_line_get_prompt.restype = POINTER_T(ctypes.c_char)
r_line_get_prompt.argtypes = []
r_line_set_prompt = _libr_cons.r_line_set_prompt
r_line_set_prompt.restype = None
r_line_set_prompt.argtypes = [POINTER_T(ctypes.c_char)]
r_line_dietline_init = _libr_cons.r_line_dietline_init
r_line_dietline_init.restype = ctypes.c_int32
r_line_dietline_init.argtypes = []
r_line_clipboard_push = _libr_cons.r_line_clipboard_push
r_line_clipboard_push.restype = None
r_line_clipboard_push.argtypes = [POINTER_T(ctypes.c_char)]
r_line_hist_free = _libr_cons.r_line_hist_free
r_line_hist_free.restype = None
r_line_hist_free.argtypes = []
RLineReadCallback = ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char))
r_line_readline = _libr_cons.r_line_readline
r_line_readline.restype = POINTER_T(ctypes.c_char)
r_line_readline.argtypes = []
r_line_readline_cb = _libr_cons.r_line_readline_cb
r_line_readline_cb.restype = POINTER_T(ctypes.c_char)
r_line_readline_cb.argtypes = [RLineReadCallback, POINTER_T(None)]
r_line_hist_load = _libr_cons.r_line_hist_load
r_line_hist_load.restype = ctypes.c_int32
r_line_hist_load.argtypes = [POINTER_T(ctypes.c_char)]
r_line_hist_add = _libr_cons.r_line_hist_add
r_line_hist_add.restype = ctypes.c_int32
r_line_hist_add.argtypes = [POINTER_T(ctypes.c_char)]
r_line_hist_save = _libr_cons.r_line_hist_save
r_line_hist_save.restype = ctypes.c_int32
r_line_hist_save.argtypes = [POINTER_T(ctypes.c_char)]
r_line_hist_list = _libr_cons.r_line_hist_list
r_line_hist_list.restype = ctypes.c_int32
r_line_hist_list.argtypes = []
r_line_hist_get = _libr_cons.r_line_hist_get
r_line_hist_get.restype = POINTER_T(ctypes.c_char)
r_line_hist_get.argtypes = [ctypes.c_int32]
r_line_set_hist_callback = _libr_cons.r_line_set_hist_callback
r_line_set_hist_callback.restype = ctypes.c_int32
r_line_set_hist_callback.argtypes = [POINTER_T(struct_r_line_t), RLineHistoryUpCb, RLineHistoryDownCb]
r_line_hist_cmd_up = _libr_cons.r_line_hist_cmd_up
r_line_hist_cmd_up.restype = ctypes.c_int32
r_line_hist_cmd_up.argtypes = [POINTER_T(struct_r_line_t)]
r_line_hist_cmd_down = _libr_cons.r_line_hist_cmd_down
r_line_hist_cmd_down.restype = ctypes.c_int32
r_line_hist_cmd_down.argtypes = [POINTER_T(struct_r_line_t)]
r_line_completion_init = _libr_cons.r_line_completion_init
r_line_completion_init.restype = None
r_line_completion_init.argtypes = [POINTER_T(struct_r_line_comp_t), size_t]
r_line_completion_fini = _libr_cons.r_line_completion_fini
r_line_completion_fini.restype = None
r_line_completion_fini.argtypes = [POINTER_T(struct_r_line_comp_t)]
r_line_completion_push = _libr_cons.r_line_completion_push
r_line_completion_push.restype = None
r_line_completion_push.argtypes = [POINTER_T(struct_r_line_comp_t), POINTER_T(ctypes.c_char)]
r_line_completion_set = _libr_cons.r_line_completion_set
r_line_completion_set.restype = None
r_line_completion_set.argtypes = [POINTER_T(struct_r_line_comp_t), ctypes.c_int32, POINTER_T(POINTER_T(ctypes.c_char))]
r_line_completion_clear = _libr_cons.r_line_completion_clear
r_line_completion_clear.restype = None
r_line_completion_clear.argtypes = [POINTER_T(struct_r_line_comp_t)]
RPanelsMenuCallback = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None)))
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

RPanelsMenuItem = struct_r_panels_menu_item
class struct_r_panels_menu_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('root', POINTER_T(struct_r_panels_menu_item)),
    ('history', POINTER_T(POINTER_T(struct_r_panels_menu_item))),
    ('depth', ctypes.c_int32),
    ('n_refresh', ctypes.c_int32),
    ('refreshPanels', POINTER_T(POINTER_T(struct_r_panel_t))),
     ]

RPanelsMenu = struct_r_panels_menu_t

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
RPanelsMode = c__EA_RPanelsMode
RPanelsMode__enumvalues = c__EA_RPanelsMode__enumvalues

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
RPanelsFun = c__EA_RPanelsFun
RPanelsFun__enumvalues = c__EA_RPanelsFun__enumvalues

# values for enumeration 'c__EA_RPanelsLayout'
c__EA_RPanelsLayout__enumvalues = {
    0: 'PANEL_LAYOUT_DEFAULT_STATIC',
    1: 'PANEL_LAYOUT_DEFAULT_DYNAMIC',
}
PANEL_LAYOUT_DEFAULT_STATIC = 0
PANEL_LAYOUT_DEFAULT_DYNAMIC = 1
c__EA_RPanelsLayout = ctypes.c_int # enum
RPanelsLayout = c__EA_RPanelsLayout
RPanelsLayout__enumvalues = c__EA_RPanelsLayout__enumvalues
class struct_c__SA_RPanelsSnow(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('x', ctypes.c_int32),
    ('y', ctypes.c_int32),
     ]

RPanelsSnow = struct_c__SA_RPanelsSnow
class struct_c__SA_RModal(ctypes.Structure):
    pass

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

struct_c__SA_RModal._pack_ = True # source:False
struct_c__SA_RModal._fields_ = [
    ('data', POINTER_T(struct_c__SA_RStrBuf)),
    ('pos', struct_r_panel_pos_t),
    ('idx', ctypes.c_int32),
    ('offset', ctypes.c_int32),
]

RModal = struct_c__SA_RModal
class struct_r_panels_t(ctypes.Structure):
    pass

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

struct_r_panels_t._pack_ = True # source:False
struct_r_panels_t._fields_ = [
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
    ('mode', RPanelsMode),
    ('fun', RPanelsFun),
    ('prevMode', RPanelsMode),
    ('layout', RPanelsLayout),
    ('snows', POINTER_T(struct_r_list_t)),
    ('name', POINTER_T(ctypes.c_char)),
]

RPanels = struct_r_panels_t

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
RPanelsRootState = c__EA_RPanelsRootState
RPanelsRootState__enumvalues = c__EA_RPanelsRootState__enumvalues
class struct_r_panels_root_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('n_panels', ctypes.c_int32),
    ('cur_panels', ctypes.c_int32),
    ('pdc_caches', POINTER_T(struct_sdb_t)),
    ('cur_pdc_cache', POINTER_T(struct_sdb_t)),
    ('panels', POINTER_T(POINTER_T(struct_r_panels_t))),
    ('root_state', RPanelsRootState),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

RPanelsRoot = struct_r_panels_root_t
__all__ = \
    ['ALPHA_BG', 'ALPHA_FG', 'ALPHA_FGBG', 'ALPHA_RESET',
    'COLOR_MODE_16', 'COLOR_MODE_16M', 'COLOR_MODE_256',
    'COLOR_MODE_DISABLED', 'CONTROL_MODE', 'DEFAULT', 'DEL',
    'INSERT_MODE', 'LINE_FALSE', 'LINE_NONE', 'LINE_NOSYM_HORIZ',
    'LINE_NOSYM_VERT', 'LINE_TRUE', 'LINE_UNCJMP', 'PAL_00', 'PAL_7F',
    'PAL_ADDRESS', 'PAL_CALL', 'PAL_CHANGED', 'PAL_CMP',
    'PAL_DEFAULT', 'PAL_FF', 'PAL_HEADER', 'PAL_JUMP', 'PAL_LINES0',
    'PAL_LINES1', 'PAL_LINES2', 'PAL_METADATA', 'PAL_NOP',
    'PAL_PRINTABLE', 'PAL_PROMPT', 'PAL_PUSH', 'PAL_RET', 'PAL_TRAP',
    'PANEL_FUN_NOFUN', 'PANEL_FUN_SAKURA', 'PANEL_FUN_SNOW',
    'PANEL_LAYOUT_DEFAULT_DYNAMIC', 'PANEL_LAYOUT_DEFAULT_STATIC',
    'PANEL_MODE_DEFAULT', 'PANEL_MODE_HELP', 'PANEL_MODE_MENU',
    'PANEL_MODE_WINDOW', 'PANEL_MODE_ZOOM', 'PANEL_TYPE_DEFAULT',
    'PANEL_TYPE_MENU', 'QUIT', 'RCanvasLineStyle', 'RColor', 'RCons',
    'RConsBind', 'RConsBreak', 'RConsBreakCallback', 'RConsCanvas',
    'RConsClickCallback', 'RConsColorMode',
    'RConsColorMode__enumvalues', 'RConsContext',
    'RConsEditorCallback', 'RConsEvent', 'RConsFlush',
    'RConsFunctionKey', 'RConsGetCursor', 'RConsGetSize', 'RConsGrep',
    'RConsGrepCallback', 'RConsIsBreaked', 'RConsPalette',
    'RConsPrintablePalette', 'RConsQueueTaskOneshot',
    'RConsSleepBeginCallback', 'RConsSleepEndCallback', 'RLine',
    'RLineBuffer', 'RLineCompletion', 'RLineCompletionCb',
    'RLineEditorCb', 'RLineHistory', 'RLineHistoryDownCb',
    'RLineHistoryUpCb', 'RLineHud', 'RLinePromptType',
    'RLinePromptType__enumvalues', 'RLineReadCallback', 'RModal',
    'RNCAND', 'RNCASSIGN', 'RNCDEC', 'RNCDIV', 'RNCEND', 'RNCINC',
    'RNCLEFTP', 'RNCMINUS', 'RNCMOD', 'RNCMUL', 'RNCNAME', 'RNCNEG',
    'RNCNUMBER', 'RNCORR', 'RNCPLUS', 'RNCPRINT', 'RNCRIGHTP',
    'RNCROL', 'RNCROR', 'RNCSHL', 'RNCSHR', 'RNCXOR', 'ROTATE',
    'RPanels', 'RPanelsFun', 'RPanelsFun__enumvalues',
    'RPanelsLayout', 'RPanelsLayout__enumvalues', 'RPanelsMenu',
    'RPanelsMenuCallback', 'RPanelsMenuItem', 'RPanelsMode',
    'RPanelsMode__enumvalues', 'RPanelsRoot', 'RPanelsRootState',
    'RPanelsRootState__enumvalues', 'RPanelsSnow', 'RSelWidget',
    'RViMode', 'RViMode__enumvalues', 'R_CONS_ATTR_BLINK',
    'R_CONS_ATTR_BOLD', 'R_CONS_ATTR_DIM', 'R_CONS_ATTR_ITALIC',
    'R_CONS_ATTR_UNDERLINE', 'R_LINE_PROMPT_DEFAULT',
    'R_LINE_PROMPT_FILE', 'R_LINE_PROMPT_OFFSET', 'R_LOGLVL_DEBUG',
    'R_LOGLVL_ERROR', 'R_LOGLVL_FATAL', 'R_LOGLVL_INFO',
    'R_LOGLVL_NONE', 'R_LOGLVL_SILLY', 'R_LOGLVL_VERBOSE',
    'R_LOGLVL_WARN', 'c__EA_RConsColorMode', 'c__EA_RLinePromptType',
    'c__EA_RNumCalcToken', 'c__EA_RPanelType', 'c__EA_RPanelsFun',
    'c__EA_RPanelsLayout', 'c__EA_RPanelsMode',
    'c__EA_RPanelsRootState', 'c__EA_RViMode', 'c__Ea_ALPHA_RESET',
    'c__Ea_LINE_NONE', 'c__Ea_PAL_PROMPT', 'c__Ea_R_CONS_ATTR_BOLD',
    'r_cons_2048', 'r_cons_any_key', 'r_cons_arrow_to_hjkl',
    'r_cons_bind', 'r_cons_break_clear', 'r_cons_break_end',
    'r_cons_break_pop', 'r_cons_break_push', 'r_cons_break_timeout',
    'r_cons_breakword', 'r_cons_canvas_box', 'r_cons_canvas_circle',
    'r_cons_canvas_clear', 'r_cons_canvas_fill', 'r_cons_canvas_free',
    'r_cons_canvas_gotoxy', 'r_cons_canvas_line',
    'r_cons_canvas_line_back_edge', 'r_cons_canvas_line_diagonal',
    'r_cons_canvas_line_square', 'r_cons_canvas_line_square_defined',
    'r_cons_canvas_new', 'r_cons_canvas_print',
    'r_cons_canvas_print_region', 'r_cons_canvas_resize',
    'r_cons_canvas_to_string', 'r_cons_canvas_write', 'r_cons_chop',
    'r_cons_clear', 'r_cons_clear00', 'r_cons_clear_buffer',
    'r_cons_clear_line', 'r_cons_cmd_help', 'r_cons_color',
    'r_cons_color_random', 'r_cons_column', 'r_cons_context_break',
    'r_cons_context_break_pop', 'r_cons_context_break_push',
    'r_cons_context_free', 'r_cons_context_is_main',
    'r_cons_context_load', 'r_cons_context_new',
    'r_cons_context_reset', 'r_cons_controlz',
    'r_cons_default_context_is_interactive', 'r_cons_drop',
    'r_cons_echo', 'r_cons_editor', 'r_cons_enable_highlight',
    'r_cons_enable_mouse', 'r_cons_eof', 'r_cons_fgets',
    'r_cons_fill_line', 'r_cons_filter', 'r_cons_flush',
    'r_cons_free', 'r_cons_get_buffer', 'r_cons_get_buffer_len',
    'r_cons_get_click', 'r_cons_get_column', 'r_cons_get_cur_line',
    'r_cons_get_cursor', 'r_cons_get_rune', 'r_cons_get_size',
    'r_cons_gotoxy', 'r_cons_grep', 'r_cons_grep_help',
    'r_cons_grep_line', 'r_cons_grep_parsecmd', 'r_cons_grep_process',
    'r_cons_grep_strip', 'r_cons_grepbuf', 'r_cons_highlight',
    'r_cons_html_filter', 'r_cons_hud', 'r_cons_hud_file',
    'r_cons_hud_path', 'r_cons_hud_string', 'r_cons_image',
    'r_cons_input', 'r_cons_invert', 'r_cons_is_breaked',
    'r_cons_is_interactive', 'r_cons_is_utf8', 'r_cons_isatty',
    'r_cons_last', 'r_cons_lastline', 'r_cons_lastline_utf8_ansi_len',
    'r_cons_less', 'r_cons_less_str', 'r_cons_memcat',
    'r_cons_memset', 'r_cons_message', 'r_cons_new', 'r_cons_newline',
    'r_cons_pal_copy', 'r_cons_pal_free', 'r_cons_pal_get',
    'r_cons_pal_get_i', 'r_cons_pal_get_name', 'r_cons_pal_init',
    'r_cons_pal_len', 'r_cons_pal_list', 'r_cons_pal_parse',
    'r_cons_pal_random', 'r_cons_pal_set', 'r_cons_pal_show',
    'r_cons_pal_update_event', 'r_cons_password', 'r_cons_pipe_close',
    'r_cons_pipe_open', 'r_cons_pop', 'r_cons_print_clear',
    'r_cons_print_fps', 'r_cons_printf', 'r_cons_printf_list',
    'r_cons_println', 'r_cons_push', 'r_cons_rainbow_free',
    'r_cons_rainbow_get', 'r_cons_rainbow_new', 'r_cons_readchar',
    'r_cons_readchar_timeout', 'r_cons_readflush', 'r_cons_readpush',
    'r_cons_reset', 'r_cons_reset_colors', 'r_cons_rgb_init',
    'r_cons_rgb_parse', 'r_cons_rgb_str', 'r_cons_rgb_str_mode',
    'r_cons_rgb_str_off', 'r_cons_rgb_tostring', 'r_cons_set_click',
    'r_cons_set_cup', 'r_cons_set_interactive',
    'r_cons_set_last_interactive', 'r_cons_set_raw',
    'r_cons_set_title', 'r_cons_set_utf8', 'r_cons_show_cursor',
    'r_cons_singleton', 'r_cons_sleep_begin', 'r_cons_sleep_end',
    'r_cons_strcat', 'r_cons_strcat_at', 'r_cons_strcat_justify',
    'r_cons_swap_ground', 'r_cons_switchbuf', 'r_cons_version',
    'r_cons_visual_flush', 'r_cons_visual_write', 'r_cons_yesno',
    'r_cons_zero', 'r_line_clipboard_push', 'r_line_completion_clear',
    'r_line_completion_fini', 'r_line_completion_init',
    'r_line_completion_push', 'r_line_completion_set',
    'r_line_dietline_init', 'r_line_free', 'r_line_get_prompt',
    'r_line_hist_add', 'r_line_hist_cmd_down', 'r_line_hist_cmd_up',
    'r_line_hist_free', 'r_line_hist_get', 'r_line_hist_list',
    'r_line_hist_load', 'r_line_hist_save', 'r_line_new',
    'r_line_readline', 'r_line_readline_cb',
    'r_line_set_hist_callback', 'r_line_set_prompt',
    'r_line_singleton', 'r_log_level', 'size_t', 'struct__IO_FILE',
    'struct__IO_codecvt', 'struct__IO_marker', 'struct__IO_wide_data',
    'struct___va_list_tag', 'struct_buffer', 'struct_c__SA_RModal',
    'struct_c__SA_RNumCalcValue', 'struct_c__SA_RPanelsSnow',
    'struct_c__SA_RStrBuf', 'struct_c__SA_dict', 'struct_cdb',
    'struct_cdb_hp', 'struct_cdb_hplist', 'struct_cdb_make',
    'struct_ht_pp_bucket_t', 'struct_ht_pp_kv',
    'struct_ht_pp_options_t', 'struct_ht_pp_t',
    'struct_ht_up_bucket_t', 'struct_ht_up_kv',
    'struct_ht_up_options_t', 'struct_ht_up_t', 'struct_ls_iter_t',
    'struct_ls_t', 'struct_r_cons_bind_t',
    'struct_r_cons_canvas_line_style_t', 'struct_r_cons_canvas_t',
    'struct_r_cons_context_t', 'struct_r_cons_grep_t',
    'struct_r_cons_palette_t', 'struct_r_cons_printable_palette_t',
    'struct_r_cons_t', 'struct_r_hud_t', 'struct_r_line_buffer_t',
    'struct_r_line_comp_t', 'struct_r_line_hist_t', 'struct_r_line_t',
    'struct_r_list_iter_t', 'struct_r_list_t', 'struct_r_num_calc_t',
    'struct_r_num_t', 'struct_r_panel_model_t',
    'struct_r_panel_pos_t', 'struct_r_panel_t',
    'struct_r_panel_view_t', 'struct_r_panels_menu_item',
    'struct_r_panels_menu_t', 'struct_r_panels_root_t',
    'struct_r_panels_t', 'struct_r_pvector_t',
    'struct_r_selection_widget_t', 'struct_r_stack_t',
    'struct_r_str_constpool_t', 'struct_r_vector_t',
    'struct_rcolor_t', 'struct_sdb_kv', 'struct_sdb_t',
    'struct_termios', 'va_list']

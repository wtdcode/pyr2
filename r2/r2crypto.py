# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_crypto as _libr_crypto


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



r_crypto_version = _libr_crypto.r_crypto_version
r_crypto_version.restype = POINTER_T(ctypes.c_char)
r_crypto_version.argtypes = []

# values for enumeration 'c__Ea_R_CRYPTO_MODE_ECB'
c__Ea_R_CRYPTO_MODE_ECB__enumvalues = {
    0: 'R_CRYPTO_MODE_ECB',
    1: 'R_CRYPTO_MODE_CBC',
    2: 'R_CRYPTO_MODE_OFB',
    3: 'R_CRYPTO_MODE_CFB',
}
R_CRYPTO_MODE_ECB = 0
R_CRYPTO_MODE_CBC = 1
R_CRYPTO_MODE_OFB = 2
R_CRYPTO_MODE_CFB = 3
c__Ea_R_CRYPTO_MODE_ECB = ctypes.c_int # enum

# values for enumeration 'c__Ea_R_CRYPTO_DIR_CIPHER'
c__Ea_R_CRYPTO_DIR_CIPHER__enumvalues = {
    0: 'R_CRYPTO_DIR_CIPHER',
    1: 'R_CRYPTO_DIR_DECIPHER',
}
R_CRYPTO_DIR_CIPHER = 0
R_CRYPTO_DIR_DECIPHER = 1
c__Ea_R_CRYPTO_DIR_CIPHER = ctypes.c_int # enum
class struct_r_crypto_t(ctypes.Structure):
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

class struct_r_crypto_plugin_t(ctypes.Structure):
    pass

struct_r_crypto_plugin_t._pack_ = True # source:False
struct_r_crypto_plugin_t._fields_ = [
    ('name', POINTER_T(ctypes.c_char)),
    ('license', POINTER_T(ctypes.c_char)),
    ('get_key_size', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_crypto_t)))),
    ('set_iv', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('set_key', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32))),
    ('update', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('final', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('use', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_bool, POINTER_T(ctypes.c_char)))),
    ('fini', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_r_crypto_t)))),
]

struct_r_crypto_t._pack_ = True # source:False
struct_r_crypto_t._fields_ = [
    ('h', POINTER_T(struct_r_crypto_plugin_t)),
    ('key', POINTER_T(ctypes.c_ubyte)),
    ('iv', POINTER_T(ctypes.c_ubyte)),
    ('key_len', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('output', POINTER_T(ctypes.c_ubyte)),
    ('output_len', ctypes.c_int32),
    ('output_size', ctypes.c_int32),
    ('dir', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('user', POINTER_T(None)),
    ('plugins', POINTER_T(struct_r_list_t)),
]

RCrypto = struct_r_crypto_t
RCryptoPlugin = struct_r_crypto_plugin_t
RCryptoSelector = ctypes.c_uint64
r_crypto_init = _libr_crypto.r_crypto_init
r_crypto_init.restype = POINTER_T(struct_r_crypto_t)
r_crypto_init.argtypes = [POINTER_T(struct_r_crypto_t), ctypes.c_int32]
r_crypto_as_new = _libr_crypto.r_crypto_as_new
r_crypto_as_new.restype = POINTER_T(struct_r_crypto_t)
r_crypto_as_new.argtypes = [POINTER_T(struct_r_crypto_t)]
r_crypto_add = _libr_crypto.r_crypto_add
r_crypto_add.restype = ctypes.c_int32
r_crypto_add.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(struct_r_crypto_plugin_t)]
r_crypto_new = _libr_crypto.r_crypto_new
r_crypto_new.restype = POINTER_T(struct_r_crypto_t)
r_crypto_new.argtypes = []
r_crypto_free = _libr_crypto.r_crypto_free
r_crypto_free.restype = POINTER_T(struct_r_crypto_t)
r_crypto_free.argtypes = [POINTER_T(struct_r_crypto_t)]
r_crypto_use = _libr_crypto.r_crypto_use
r_crypto_use.restype = ctypes.c_bool
r_crypto_use.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_char)]
r_crypto_set_key = _libr_crypto.r_crypto_set_key
r_crypto_set_key.restype = ctypes.c_bool
r_crypto_set_key.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
r_crypto_set_iv = _libr_crypto.r_crypto_set_iv
r_crypto_set_iv.restype = ctypes.c_bool
r_crypto_set_iv.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_crypto_update = _libr_crypto.r_crypto_update
r_crypto_update.restype = ctypes.c_int32
r_crypto_update.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_crypto_final = _libr_crypto.r_crypto_final
r_crypto_final.restype = ctypes.c_int32
r_crypto_final.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_crypto_append = _libr_crypto.r_crypto_append
r_crypto_append.restype = ctypes.c_int32
r_crypto_append.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_crypto_get_output = _libr_crypto.r_crypto_get_output
r_crypto_get_output.restype = POINTER_T(ctypes.c_ubyte)
r_crypto_get_output.argtypes = [POINTER_T(struct_r_crypto_t), POINTER_T(ctypes.c_int32)]
r_crypto_name = _libr_crypto.r_crypto_name
r_crypto_name.restype = POINTER_T(ctypes.c_char)
r_crypto_name.argtypes = [RCryptoSelector]
r_crypto_codec_name = _libr_crypto.r_crypto_codec_name
r_crypto_codec_name.restype = POINTER_T(ctypes.c_char)
r_crypto_codec_name.argtypes = [RCryptoSelector]
r_crypto_plugin_aes = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_des = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_rc4 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_xor = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_blowfish = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_rc2 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_rot = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_rol = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_ror = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_base64 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_base91 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_aes_cbc = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_punycode = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_rc6 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_cps2 = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
r_crypto_plugin_serpent = struct_r_crypto_plugin_t # Variable struct_r_crypto_plugin_t
__all__ = \
    ['RCrypto', 'RCryptoPlugin', 'RCryptoSelector',
    'R_CRYPTO_DIR_CIPHER', 'R_CRYPTO_DIR_DECIPHER',
    'R_CRYPTO_MODE_CBC', 'R_CRYPTO_MODE_CFB', 'R_CRYPTO_MODE_ECB',
    'R_CRYPTO_MODE_OFB', 'c__Ea_R_CRYPTO_DIR_CIPHER',
    'c__Ea_R_CRYPTO_MODE_ECB', 'r_crypto_add', 'r_crypto_append',
    'r_crypto_as_new', 'r_crypto_codec_name', 'r_crypto_final',
    'r_crypto_free', 'r_crypto_get_output', 'r_crypto_init',
    'r_crypto_name', 'r_crypto_new', 'r_crypto_plugin_aes',
    'r_crypto_plugin_aes_cbc', 'r_crypto_plugin_base64',
    'r_crypto_plugin_base91', 'r_crypto_plugin_blowfish',
    'r_crypto_plugin_cps2', 'r_crypto_plugin_des',
    'r_crypto_plugin_punycode', 'r_crypto_plugin_rc2',
    'r_crypto_plugin_rc4', 'r_crypto_plugin_rc6',
    'r_crypto_plugin_rol', 'r_crypto_plugin_ror',
    'r_crypto_plugin_rot', 'r_crypto_plugin_serpent',
    'r_crypto_plugin_xor', 'r_crypto_set_iv', 'r_crypto_set_key',
    'r_crypto_update', 'r_crypto_use', 'r_crypto_version',
    'struct_r_crypto_plugin_t', 'struct_r_crypto_t',
    'struct_r_list_iter_t', 'struct_r_list_t']

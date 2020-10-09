# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_hash as _libr_hash


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



r_hash_version = _libr_hash.r_hash_version
r_hash_version.restype = POINTER_T(ctypes.c_char)
r_hash_version.argtypes = []
class struct_c__SA_R_MD5_CTX(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('state', ctypes.c_uint32 * 4),
    ('count', ctypes.c_uint32 * 2),
    ('buffer', ctypes.c_ubyte * 64),
     ]

R_MD5_CTX = struct_c__SA_R_MD5_CTX
class struct_c__SA_R_SHA_CTX(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('H', ctypes.c_uint32 * 5),
    ('W', ctypes.c_uint32 * 80),
    ('lenW', ctypes.c_int32),
    ('sizeHi', ctypes.c_uint32),
    ('sizeLo', ctypes.c_uint32),
     ]

R_SHA_CTX = struct_c__SA_R_SHA_CTX
class struct__SHA256_CTX(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('state', ctypes.c_uint32 * 8),
    ('bitcount', ctypes.c_uint64),
    ('buffer', ctypes.c_ubyte * 64),
     ]

R_SHA256_CTX = struct__SHA256_CTX
class struct__SHA512_CTX(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('state', ctypes.c_uint64 * 8),
    ('bitcount', ctypes.c_uint64 * 2),
    ('buffer', ctypes.c_ubyte * 128),
     ]

R_SHA512_CTX = struct__SHA512_CTX
R_SHA384_CTX = struct__SHA512_CTX
utcrc = ctypes.c_uint64
size_t = ctypes.c_uint64
r_hash_fletcher8 = _libr_hash.r_hash_fletcher8
r_hash_fletcher8.restype = ctypes.c_uint16
r_hash_fletcher8.argtypes = [POINTER_T(ctypes.c_ubyte), size_t]
r_hash_fletcher16 = _libr_hash.r_hash_fletcher16
r_hash_fletcher16.restype = ctypes.c_uint16
r_hash_fletcher16.argtypes = [POINTER_T(ctypes.c_ubyte), size_t]
r_hash_fletcher32 = _libr_hash.r_hash_fletcher32
r_hash_fletcher32.restype = ctypes.c_uint32
r_hash_fletcher32.argtypes = [POINTER_T(ctypes.c_ubyte), size_t]
r_hash_fletcher64 = _libr_hash.r_hash_fletcher64
r_hash_fletcher64.restype = ctypes.c_uint64
r_hash_fletcher64.argtypes = [POINTER_T(ctypes.c_ubyte), size_t]
class struct_c__SA_R_CRC_CTX(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('crc', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('reflect', ctypes.c_int32),
    ('poly', ctypes.c_uint64),
    ('xout', ctypes.c_uint64),
     ]

R_CRC_CTX = struct_c__SA_R_CRC_CTX

# values for enumeration 'CRC_PRESETS'
CRC_PRESETS__enumvalues = {
    0: 'CRC_PRESET_8_SMBUS',
    1: 'CRC_PRESET_15_CAN',
    2: 'CRC_PRESET_16',
    3: 'CRC_PRESET_16_CITT',
    4: 'CRC_PRESET_16_USB',
    5: 'CRC_PRESET_16_HDLC',
    6: 'CRC_PRESET_24',
    7: 'CRC_PRESET_32',
    8: 'CRC_PRESET_32_ECMA_267',
    9: 'CRC_PRESET_32C',
    10: 'CRC_PRESET_CRC32_BZIP2',
    11: 'CRC_PRESET_CRC32D',
    12: 'CRC_PRESET_CRC32_MPEG2',
    13: 'CRC_PRESET_CRC32_POSIX',
    14: 'CRC_PRESET_CRC32Q',
    15: 'CRC_PRESET_CRC32_JAMCRC',
    16: 'CRC_PRESET_CRC32_XFER',
    17: 'CRC_PRESET_CRC64',
    18: 'CRC_PRESET_CRC64_ECMA182',
    19: 'CRC_PRESET_CRC64_WE',
    20: 'CRC_PRESET_CRC64_XZ',
    21: 'CRC_PRESET_CRC64_ISO',
    22: 'CRC_PRESET_SIZE',
}
CRC_PRESET_8_SMBUS = 0
CRC_PRESET_15_CAN = 1
CRC_PRESET_16 = 2
CRC_PRESET_16_CITT = 3
CRC_PRESET_16_USB = 4
CRC_PRESET_16_HDLC = 5
CRC_PRESET_24 = 6
CRC_PRESET_32 = 7
CRC_PRESET_32_ECMA_267 = 8
CRC_PRESET_32C = 9
CRC_PRESET_CRC32_BZIP2 = 10
CRC_PRESET_CRC32D = 11
CRC_PRESET_CRC32_MPEG2 = 12
CRC_PRESET_CRC32_POSIX = 13
CRC_PRESET_CRC32Q = 14
CRC_PRESET_CRC32_JAMCRC = 15
CRC_PRESET_CRC32_XFER = 16
CRC_PRESET_CRC64 = 17
CRC_PRESET_CRC64_ECMA182 = 18
CRC_PRESET_CRC64_WE = 19
CRC_PRESET_CRC64_XZ = 20
CRC_PRESET_CRC64_ISO = 21
CRC_PRESET_SIZE = 22
CRC_PRESETS = ctypes.c_int # enum
class struct_r_hash_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('md5', R_MD5_CTX),
    ('sha1', R_SHA_CTX),
    ('sha256', R_SHA256_CTX),
    ('sha384', R_SHA384_CTX),
    ('sha512', R_SHA512_CTX),
    ('rst', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('entropy', ctypes.c_double),
    ('digest', ctypes.c_ubyte * 128),
     ]

class struct_r_hash_seed_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('prefix', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

RHashSeed = struct_r_hash_seed_t

# values for enumeration 'HASH_INDICES'
HASH_INDICES__enumvalues = {
    0: 'R_HASH_IDX_MD5',
    1: 'R_HASH_IDX_SHA1',
    2: 'R_HASH_IDX_SHA256',
    3: 'R_HASH_IDX_SHA384',
    4: 'R_HASH_IDX_SHA512',
    5: 'R_HASH_IDX_MD4',
    6: 'R_HASH_IDX_XOR',
    7: 'R_HASH_IDX_XORPAIR',
    8: 'R_HASH_IDX_PARITY',
    9: 'R_HASH_IDX_ENTROPY',
    10: 'R_HASH_IDX_HAMDIST',
    11: 'R_HASH_IDX_PCPRINT',
    12: 'R_HASH_IDX_MOD255',
    13: 'R_HASH_IDX_XXHASH',
    14: 'R_HASH_IDX_ADLER32',
    15: 'R_HASH_IDX_BASE64',
    16: 'R_HASH_IDX_BASE91',
    17: 'R_HASH_IDX_PUNYCODE',
    18: 'R_HASH_IDX_LUHN',
    19: 'R_HASH_IDX_CRC8_SMBUS',
    20: 'R_HASH_IDX_CRC15_CAN',
    21: 'R_HASH_IDX_CRC16',
    22: 'R_HASH_IDX_CRC16_HDLC',
    23: 'R_HASH_IDX_CRC16_USB',
    24: 'R_HASH_IDX_CRC16_CITT',
    25: 'R_HASH_IDX_CRC24',
    26: 'R_HASH_IDX_CRC32',
    27: 'R_HASH_IDX_CRC32C',
    28: 'R_HASH_IDX_CRC32_ECMA_267',
    29: 'R_HASH_IDX_CRC32_BZIP2',
    30: 'R_HASH_IDX_CRC32D',
    31: 'R_HASH_IDX_CRC32_MPEG2',
    32: 'R_HASH_IDX_CRC32_POSIX',
    33: 'R_HASH_IDX_CRC32Q',
    34: 'R_HASH_IDX_CRC32_JAMCRC',
    35: 'R_HASH_IDX_CRC32_XFER',
    36: 'R_HASH_IDX_CRC64',
    37: 'R_HASH_IDX_CRC64_ECMA182',
    38: 'R_HASH_IDX_CRC64_WE',
    39: 'R_HASH_IDX_CRC64_XZ',
    40: 'R_HASH_IDX_CRC64_ISO',
    41: 'R_HASH_IDX_FLETCHER8',
    42: 'R_HASH_IDX_FLETCHER16',
    43: 'R_HASH_IDX_FLETCHER32',
    44: 'R_HASH_IDX_FLETCHER64',
    45: 'R_HASH_NUM_INDICES',
}
R_HASH_IDX_MD5 = 0
R_HASH_IDX_SHA1 = 1
R_HASH_IDX_SHA256 = 2
R_HASH_IDX_SHA384 = 3
R_HASH_IDX_SHA512 = 4
R_HASH_IDX_MD4 = 5
R_HASH_IDX_XOR = 6
R_HASH_IDX_XORPAIR = 7
R_HASH_IDX_PARITY = 8
R_HASH_IDX_ENTROPY = 9
R_HASH_IDX_HAMDIST = 10
R_HASH_IDX_PCPRINT = 11
R_HASH_IDX_MOD255 = 12
R_HASH_IDX_XXHASH = 13
R_HASH_IDX_ADLER32 = 14
R_HASH_IDX_BASE64 = 15
R_HASH_IDX_BASE91 = 16
R_HASH_IDX_PUNYCODE = 17
R_HASH_IDX_LUHN = 18
R_HASH_IDX_CRC8_SMBUS = 19
R_HASH_IDX_CRC15_CAN = 20
R_HASH_IDX_CRC16 = 21
R_HASH_IDX_CRC16_HDLC = 22
R_HASH_IDX_CRC16_USB = 23
R_HASH_IDX_CRC16_CITT = 24
R_HASH_IDX_CRC24 = 25
R_HASH_IDX_CRC32 = 26
R_HASH_IDX_CRC32C = 27
R_HASH_IDX_CRC32_ECMA_267 = 28
R_HASH_IDX_CRC32_BZIP2 = 29
R_HASH_IDX_CRC32D = 30
R_HASH_IDX_CRC32_MPEG2 = 31
R_HASH_IDX_CRC32_POSIX = 32
R_HASH_IDX_CRC32Q = 33
R_HASH_IDX_CRC32_JAMCRC = 34
R_HASH_IDX_CRC32_XFER = 35
R_HASH_IDX_CRC64 = 36
R_HASH_IDX_CRC64_ECMA182 = 37
R_HASH_IDX_CRC64_WE = 38
R_HASH_IDX_CRC64_XZ = 39
R_HASH_IDX_CRC64_ISO = 40
R_HASH_IDX_FLETCHER8 = 41
R_HASH_IDX_FLETCHER16 = 42
R_HASH_IDX_FLETCHER32 = 43
R_HASH_IDX_FLETCHER64 = 44
R_HASH_NUM_INDICES = 45
HASH_INDICES = ctypes.c_int # enum
r_hash_new = _libr_hash.r_hash_new
r_hash_new.restype = POINTER_T(struct_r_hash_t)
r_hash_new.argtypes = [ctypes.c_bool, ctypes.c_uint64]
r_hash_free = _libr_hash.r_hash_free
r_hash_free.restype = None
r_hash_free.argtypes = [POINTER_T(struct_r_hash_t)]
r_hash_do_md4 = _libr_hash.r_hash_do_md4
r_hash_do_md4.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_md4.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_md5 = _libr_hash.r_hash_do_md5
r_hash_do_md5.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_md5.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_sha1 = _libr_hash.r_hash_do_sha1
r_hash_do_sha1.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_sha1.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_sha256 = _libr_hash.r_hash_do_sha256
r_hash_do_sha256.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_sha256.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_sha384 = _libr_hash.r_hash_do_sha384
r_hash_do_sha384.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_sha384.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_sha512 = _libr_hash.r_hash_do_sha512
r_hash_do_sha512.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_sha512.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_do_hmac_sha256 = _libr_hash.r_hash_do_hmac_sha256
r_hash_do_hmac_sha256.restype = POINTER_T(ctypes.c_ubyte)
r_hash_do_hmac_sha256.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_to_string = _libr_hash.r_hash_to_string
r_hash_to_string.restype = POINTER_T(ctypes.c_char)
r_hash_to_string.argtypes = [POINTER_T(struct_r_hash_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_name = _libr_hash.r_hash_name
r_hash_name.restype = POINTER_T(ctypes.c_char)
r_hash_name.argtypes = [ctypes.c_uint64]
r_hash_name_to_bits = _libr_hash.r_hash_name_to_bits
r_hash_name_to_bits.restype = ctypes.c_uint64
r_hash_name_to_bits.argtypes = [POINTER_T(ctypes.c_char)]
r_hash_size = _libr_hash.r_hash_size
r_hash_size.restype = ctypes.c_int32
r_hash_size.argtypes = [ctypes.c_uint64]
r_hash_calculate = _libr_hash.r_hash_calculate
r_hash_calculate.restype = ctypes.c_int32
r_hash_calculate.argtypes = [POINTER_T(struct_r_hash_t), ctypes.c_uint64, POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_deviation = _libr_hash.r_hash_deviation
r_hash_deviation.restype = ctypes.c_ubyte
r_hash_deviation.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_adler32 = _libr_hash.r_hash_adler32
r_hash_adler32.restype = ctypes.c_uint32
r_hash_adler32.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_xxhash = _libr_hash.r_hash_xxhash
r_hash_xxhash.restype = ctypes.c_uint32
r_hash_xxhash.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_xor = _libr_hash.r_hash_xor
r_hash_xor.restype = ctypes.c_ubyte
r_hash_xor.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_xorpair = _libr_hash.r_hash_xorpair
r_hash_xorpair.restype = ctypes.c_uint16
r_hash_xorpair.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_parity = _libr_hash.r_hash_parity
r_hash_parity.restype = ctypes.c_int32
r_hash_parity.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_mod255 = _libr_hash.r_hash_mod255
r_hash_mod255.restype = ctypes.c_ubyte
r_hash_mod255.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_luhn = _libr_hash.r_hash_luhn
r_hash_luhn.restype = ctypes.c_uint64
r_hash_luhn.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_crc_preset = _libr_hash.r_hash_crc_preset
r_hash_crc_preset.restype = utcrc
r_hash_crc_preset.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint32, CRC_PRESETS]
r_hash_hamdist = _libr_hash.r_hash_hamdist
r_hash_hamdist.restype = ctypes.c_ubyte
r_hash_hamdist.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_hash_entropy = _libr_hash.r_hash_entropy
r_hash_entropy.restype = ctypes.c_double
r_hash_entropy.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_entropy_fraction = _libr_hash.r_hash_entropy_fraction
r_hash_entropy_fraction.restype = ctypes.c_double
r_hash_entropy_fraction.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_pcprint = _libr_hash.r_hash_pcprint
r_hash_pcprint.restype = ctypes.c_int32
r_hash_pcprint.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_uint64]
r_hash_do_begin = _libr_hash.r_hash_do_begin
r_hash_do_begin.restype = None
r_hash_do_begin.argtypes = [POINTER_T(struct_r_hash_t), ctypes.c_uint64]
r_hash_do_end = _libr_hash.r_hash_do_end
r_hash_do_end.restype = None
r_hash_do_end.argtypes = [POINTER_T(struct_r_hash_t), ctypes.c_uint64]
r_hash_do_spice = _libr_hash.r_hash_do_spice
r_hash_do_spice.restype = None
r_hash_do_spice.argtypes = [POINTER_T(struct_r_hash_t), ctypes.c_uint64, ctypes.c_int32, POINTER_T(struct_r_hash_seed_t)]
__all__ = \
    ['CRC_PRESETS', 'CRC_PRESET_15_CAN', 'CRC_PRESET_16',
    'CRC_PRESET_16_CITT', 'CRC_PRESET_16_HDLC', 'CRC_PRESET_16_USB',
    'CRC_PRESET_24', 'CRC_PRESET_32', 'CRC_PRESET_32C',
    'CRC_PRESET_32_ECMA_267', 'CRC_PRESET_8_SMBUS',
    'CRC_PRESET_CRC32D', 'CRC_PRESET_CRC32Q',
    'CRC_PRESET_CRC32_BZIP2', 'CRC_PRESET_CRC32_JAMCRC',
    'CRC_PRESET_CRC32_MPEG2', 'CRC_PRESET_CRC32_POSIX',
    'CRC_PRESET_CRC32_XFER', 'CRC_PRESET_CRC64',
    'CRC_PRESET_CRC64_ECMA182', 'CRC_PRESET_CRC64_ISO',
    'CRC_PRESET_CRC64_WE', 'CRC_PRESET_CRC64_XZ', 'CRC_PRESET_SIZE',
    'HASH_INDICES', 'RHashSeed', 'R_CRC_CTX', 'R_HASH_IDX_ADLER32',
    'R_HASH_IDX_BASE64', 'R_HASH_IDX_BASE91', 'R_HASH_IDX_CRC15_CAN',
    'R_HASH_IDX_CRC16', 'R_HASH_IDX_CRC16_CITT',
    'R_HASH_IDX_CRC16_HDLC', 'R_HASH_IDX_CRC16_USB',
    'R_HASH_IDX_CRC24', 'R_HASH_IDX_CRC32', 'R_HASH_IDX_CRC32C',
    'R_HASH_IDX_CRC32D', 'R_HASH_IDX_CRC32Q',
    'R_HASH_IDX_CRC32_BZIP2', 'R_HASH_IDX_CRC32_ECMA_267',
    'R_HASH_IDX_CRC32_JAMCRC', 'R_HASH_IDX_CRC32_MPEG2',
    'R_HASH_IDX_CRC32_POSIX', 'R_HASH_IDX_CRC32_XFER',
    'R_HASH_IDX_CRC64', 'R_HASH_IDX_CRC64_ECMA182',
    'R_HASH_IDX_CRC64_ISO', 'R_HASH_IDX_CRC64_WE',
    'R_HASH_IDX_CRC64_XZ', 'R_HASH_IDX_CRC8_SMBUS',
    'R_HASH_IDX_ENTROPY', 'R_HASH_IDX_FLETCHER16',
    'R_HASH_IDX_FLETCHER32', 'R_HASH_IDX_FLETCHER64',
    'R_HASH_IDX_FLETCHER8', 'R_HASH_IDX_HAMDIST', 'R_HASH_IDX_LUHN',
    'R_HASH_IDX_MD4', 'R_HASH_IDX_MD5', 'R_HASH_IDX_MOD255',
    'R_HASH_IDX_PARITY', 'R_HASH_IDX_PCPRINT', 'R_HASH_IDX_PUNYCODE',
    'R_HASH_IDX_SHA1', 'R_HASH_IDX_SHA256', 'R_HASH_IDX_SHA384',
    'R_HASH_IDX_SHA512', 'R_HASH_IDX_XOR', 'R_HASH_IDX_XORPAIR',
    'R_HASH_IDX_XXHASH', 'R_HASH_NUM_INDICES', 'R_MD5_CTX',
    'R_SHA256_CTX', 'R_SHA384_CTX', 'R_SHA512_CTX', 'R_SHA_CTX',
    'r_hash_adler32', 'r_hash_calculate', 'r_hash_crc_preset',
    'r_hash_deviation', 'r_hash_do_begin', 'r_hash_do_end',
    'r_hash_do_hmac_sha256', 'r_hash_do_md4', 'r_hash_do_md5',
    'r_hash_do_sha1', 'r_hash_do_sha256', 'r_hash_do_sha384',
    'r_hash_do_sha512', 'r_hash_do_spice', 'r_hash_entropy',
    'r_hash_entropy_fraction', 'r_hash_fletcher16',
    'r_hash_fletcher32', 'r_hash_fletcher64', 'r_hash_fletcher8',
    'r_hash_free', 'r_hash_hamdist', 'r_hash_luhn', 'r_hash_mod255',
    'r_hash_name', 'r_hash_name_to_bits', 'r_hash_new',
    'r_hash_parity', 'r_hash_pcprint', 'r_hash_size',
    'r_hash_to_string', 'r_hash_version', 'r_hash_xor',
    'r_hash_xorpair', 'r_hash_xxhash', 'size_t', 'struct__SHA256_CTX',
    'struct__SHA512_CTX', 'struct_c__SA_R_CRC_CTX',
    'struct_c__SA_R_MD5_CTX', 'struct_c__SA_R_SHA_CTX',
    'struct_r_hash_seed_t', 'struct_r_hash_t', 'utcrc']

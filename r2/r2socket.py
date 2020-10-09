# -*- coding: utf-8 -*-
#
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
from .r2libs import r_socket as _libr_socket


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

r_socket_version = _libr_socket.r_socket_version
r_socket_version.restype = POINTER_T(ctypes.c_char)
r_socket_version.argtypes = []
class struct_c__SA_R2Pipe(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('child', ctypes.c_int32),
    ('input', ctypes.c_int32 * 2),
    ('output', ctypes.c_int32 * 2),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('coreb', struct_r_core_bind_t),
     ]

R2Pipe = struct_c__SA_R2Pipe
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

RSocket = struct_r_socket_t
class struct_r_socket_http_options(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('authtokens', POINTER_T(struct_r_list_t)),
    ('accept_timeout', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('timeout', ctypes.c_int32),
    ('httpauth', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
     ]

RSocketHTTPOptions = struct_r_socket_http_options
r_socket_new_from_fd = _libr_socket.r_socket_new_from_fd
r_socket_new_from_fd.restype = POINTER_T(struct_r_socket_t)
r_socket_new_from_fd.argtypes = [ctypes.c_int32]
r_socket_new = _libr_socket.r_socket_new
r_socket_new.restype = POINTER_T(struct_r_socket_t)
r_socket_new.argtypes = [ctypes.c_bool]
r_socket_spawn = _libr_socket.r_socket_spawn
r_socket_spawn.restype = ctypes.c_bool
r_socket_spawn.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), ctypes.c_uint32]
r_socket_connect = _libr_socket.r_socket_connect
r_socket_connect.restype = ctypes.c_bool
r_socket_connect.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_uint32]
r_socket_connect_serial = _libr_socket.r_socket_connect_serial
r_socket_connect_serial.restype = ctypes.c_int32
r_socket_connect_serial.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32]
r_socket_listen = _libr_socket.r_socket_listen
r_socket_listen.restype = ctypes.c_bool
r_socket_listen.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
r_socket_port_by_name = _libr_socket.r_socket_port_by_name
r_socket_port_by_name.restype = ctypes.c_int32
r_socket_port_by_name.argtypes = [POINTER_T(ctypes.c_char)]
r_socket_close_fd = _libr_socket.r_socket_close_fd
r_socket_close_fd.restype = ctypes.c_int32
r_socket_close_fd.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_close = _libr_socket.r_socket_close
r_socket_close.restype = ctypes.c_int32
r_socket_close.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_free = _libr_socket.r_socket_free
r_socket_free.restype = ctypes.c_int32
r_socket_free.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_accept = _libr_socket.r_socket_accept
r_socket_accept.restype = POINTER_T(struct_r_socket_t)
r_socket_accept.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_accept_timeout = _libr_socket.r_socket_accept_timeout
r_socket_accept_timeout.restype = POINTER_T(struct_r_socket_t)
r_socket_accept_timeout.argtypes = [POINTER_T(struct_r_socket_t), ctypes.c_uint32]
r_socket_block_time = _libr_socket.r_socket_block_time
r_socket_block_time.restype = ctypes.c_bool
r_socket_block_time.argtypes = [POINTER_T(struct_r_socket_t), ctypes.c_bool, ctypes.c_int32, ctypes.c_int32]
r_socket_flush = _libr_socket.r_socket_flush
r_socket_flush.restype = ctypes.c_int32
r_socket_flush.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_ready = _libr_socket.r_socket_ready
r_socket_ready.restype = ctypes.c_int32
r_socket_ready.argtypes = [POINTER_T(struct_r_socket_t), ctypes.c_int32, ctypes.c_int32]
r_socket_to_string = _libr_socket.r_socket_to_string
r_socket_to_string.restype = POINTER_T(ctypes.c_char)
r_socket_to_string.argtypes = [POINTER_T(struct_r_socket_t)]
r_socket_write = _libr_socket.r_socket_write
r_socket_write.restype = ctypes.c_int32
r_socket_write.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(None), ctypes.c_int32]
r_socket_puts = _libr_socket.r_socket_puts
r_socket_puts.restype = ctypes.c_int32
r_socket_puts.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char)]
r_socket_printf = _libr_socket.r_socket_printf
r_socket_printf.restype = None
r_socket_printf.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char)]
r_socket_read = _libr_socket.r_socket_read
r_socket_read.restype = ctypes.c_int32
r_socket_read.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_socket_read_block = _libr_socket.r_socket_read_block
r_socket_read_block.restype = ctypes.c_int32
r_socket_read_block.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_socket_gets = _libr_socket.r_socket_gets
r_socket_gets.restype = ctypes.c_int32
r_socket_gets.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_socket_slurp = _libr_socket.r_socket_slurp
r_socket_slurp.restype = POINTER_T(ctypes.c_ubyte)
r_socket_slurp.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_int32)]
r_socket_is_connected = _libr_socket.r_socket_is_connected
r_socket_is_connected.restype = ctypes.c_bool
r_socket_is_connected.argtypes = [POINTER_T(struct_r_socket_t)]
class struct_r_socket_proc_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('fd0', ctypes.c_int32 * 2),
    ('fd1', ctypes.c_int32 * 2),
    ('pid', ctypes.c_int32),
     ]

RSocketProc = struct_r_socket_proc_t
r_socket_proc_open = _libr_socket.r_socket_proc_open
r_socket_proc_open.restype = POINTER_T(struct_r_socket_proc_t)
r_socket_proc_open.argtypes = [POINTER_T(ctypes.c_char) * 0]
r_socket_proc_close = _libr_socket.r_socket_proc_close
r_socket_proc_close.restype = ctypes.c_int32
r_socket_proc_close.argtypes = [POINTER_T(struct_r_socket_proc_t)]
r_socket_proc_read = _libr_socket.r_socket_proc_read
r_socket_proc_read.restype = ctypes.c_int32
r_socket_proc_read.argtypes = [POINTER_T(struct_r_socket_proc_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_socket_proc_gets = _libr_socket.r_socket_proc_gets
r_socket_proc_gets.restype = ctypes.c_int32
r_socket_proc_gets.argtypes = [POINTER_T(struct_r_socket_proc_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_socket_proc_write = _libr_socket.r_socket_proc_write
r_socket_proc_write.restype = ctypes.c_int32
r_socket_proc_write.argtypes = [POINTER_T(struct_r_socket_proc_t), POINTER_T(None), ctypes.c_int32]
r_socket_proc_printf = _libr_socket.r_socket_proc_printf
r_socket_proc_printf.restype = None
r_socket_proc_printf.argtypes = [POINTER_T(struct_r_socket_proc_t), POINTER_T(ctypes.c_char)]
r_socket_proc_ready = _libr_socket.r_socket_proc_ready
r_socket_proc_ready.restype = ctypes.c_int32
r_socket_proc_ready.argtypes = [POINTER_T(struct_r_socket_proc_t), ctypes.c_int32, ctypes.c_int32]
r_socket_http_get = _libr_socket.r_socket_http_get
r_socket_http_get.restype = POINTER_T(ctypes.c_char)
r_socket_http_get.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_int32), POINTER_T(ctypes.c_int32)]
r_socket_http_post = _libr_socket.r_socket_http_post
r_socket_http_post.restype = POINTER_T(ctypes.c_char)
r_socket_http_post.argtypes = [POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_int32), POINTER_T(ctypes.c_int32)]
r_socket_http_server_set_breaked = _libr_socket.r_socket_http_server_set_breaked
r_socket_http_server_set_breaked.restype = None
r_socket_http_server_set_breaked.argtypes = [POINTER_T(ctypes.c_bool)]
class struct_r_socket_http_request(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('s', POINTER_T(struct_r_socket_t)),
    ('path', POINTER_T(ctypes.c_char)),
    ('host', POINTER_T(ctypes.c_char)),
    ('agent', POINTER_T(ctypes.c_char)),
    ('method', POINTER_T(ctypes.c_char)),
    ('referer', POINTER_T(ctypes.c_char)),
    ('data', POINTER_T(ctypes.c_ubyte)),
    ('data_length', ctypes.c_int32),
    ('auth', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

RSocketHTTPRequest = struct_r_socket_http_request
r_socket_http_accept = _libr_socket.r_socket_http_accept
r_socket_http_accept.restype = POINTER_T(struct_r_socket_http_request)
r_socket_http_accept.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(struct_r_socket_http_options)]
r_socket_http_response = _libr_socket.r_socket_http_response
r_socket_http_response.restype = None
r_socket_http_response.argtypes = [POINTER_T(struct_r_socket_http_request), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char)]
r_socket_http_close = _libr_socket.r_socket_http_close
r_socket_http_close.restype = None
r_socket_http_close.argtypes = [POINTER_T(struct_r_socket_http_request)]
r_socket_http_handle_upload = _libr_socket.r_socket_http_handle_upload
r_socket_http_handle_upload.restype = POINTER_T(ctypes.c_ubyte)
r_socket_http_handle_upload.argtypes = [POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(ctypes.c_int32)]
rap_server_open = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))
rap_server_seek = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_uint64, ctypes.c_int32))
rap_server_read = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
rap_server_write = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))
rap_server_cmd = POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))
rap_server_close = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_int32))

# values for enumeration 'c__Ea_RAP_PACKET_OPEN'
c__Ea_RAP_PACKET_OPEN__enumvalues = {
    1: 'RAP_PACKET_OPEN',
    2: 'RAP_PACKET_READ',
    3: 'RAP_PACKET_WRITE',
    4: 'RAP_PACKET_SEEK',
    5: 'RAP_PACKET_CLOSE',
    7: 'RAP_PACKET_CMD',
    128: 'RAP_PACKET_REPLY',
    4096: 'RAP_PACKET_MAX',
}
RAP_PACKET_OPEN = 1
RAP_PACKET_READ = 2
RAP_PACKET_WRITE = 3
RAP_PACKET_SEEK = 4
RAP_PACKET_CLOSE = 5
RAP_PACKET_CMD = 7
RAP_PACKET_REPLY = 128
RAP_PACKET_MAX = 4096
c__Ea_RAP_PACKET_OPEN = ctypes.c_int # enum
class struct_r_socket_rap_server_t(ctypes.Structure):
    pass

struct_r_socket_rap_server_t._pack_ = True # source:False
struct_r_socket_rap_server_t._fields_ = [
    ('fd', POINTER_T(struct_r_socket_t)),
    ('port', POINTER_T(ctypes.c_char)),
    ('buf', ctypes.c_ubyte * 4128),
    ('open', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_char), ctypes.c_int32, ctypes.c_int32))),
    ('seek', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_uint64, ctypes.c_int32))),
    ('read', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('write', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), POINTER_T(ctypes.c_ubyte), ctypes.c_int32))),
    ('system', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('cmd', POINTER_T(ctypes.CFUNCTYPE(POINTER_T(ctypes.c_char), POINTER_T(None), POINTER_T(ctypes.c_char)))),
    ('close', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(None), ctypes.c_int32))),
    ('user', POINTER_T(None)),
]

RSocketRapServer = struct_r_socket_rap_server_t
r_socket_rap_server_new = _libr_socket.r_socket_rap_server_new
r_socket_rap_server_new.restype = POINTER_T(struct_r_socket_rap_server_t)
r_socket_rap_server_new.argtypes = [ctypes.c_bool, POINTER_T(ctypes.c_char)]
r_socket_rap_server_create = _libr_socket.r_socket_rap_server_create
r_socket_rap_server_create.restype = POINTER_T(struct_r_socket_rap_server_t)
r_socket_rap_server_create.argtypes = [POINTER_T(ctypes.c_char)]
r_socket_rap_server_free = _libr_socket.r_socket_rap_server_free
r_socket_rap_server_free.restype = None
r_socket_rap_server_free.argtypes = [POINTER_T(struct_r_socket_rap_server_t)]
r_socket_rap_server_listen = _libr_socket.r_socket_rap_server_listen
r_socket_rap_server_listen.restype = ctypes.c_bool
r_socket_rap_server_listen.argtypes = [POINTER_T(struct_r_socket_rap_server_t), POINTER_T(ctypes.c_char)]
r_socket_rap_server_accept = _libr_socket.r_socket_rap_server_accept
r_socket_rap_server_accept.restype = POINTER_T(struct_r_socket_t)
r_socket_rap_server_accept.argtypes = [POINTER_T(struct_r_socket_rap_server_t)]
r_socket_rap_server_continue = _libr_socket.r_socket_rap_server_continue
r_socket_rap_server_continue.restype = ctypes.c_bool
r_socket_rap_server_continue.argtypes = [POINTER_T(struct_r_socket_rap_server_t)]
r_socket_rap_client_open = _libr_socket.r_socket_rap_client_open
r_socket_rap_client_open.restype = ctypes.c_int32
r_socket_rap_client_open.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), ctypes.c_int32]
r_socket_rap_client_command = _libr_socket.r_socket_rap_client_command
r_socket_rap_client_command.restype = POINTER_T(ctypes.c_char)
r_socket_rap_client_command.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_char), POINTER_T(struct_r_core_bind_t)]
r_socket_rap_client_write = _libr_socket.r_socket_rap_client_write
r_socket_rap_client_write.restype = ctypes.c_int32
r_socket_rap_client_write.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_socket_rap_client_read = _libr_socket.r_socket_rap_client_read
r_socket_rap_client_read.restype = ctypes.c_int32
r_socket_rap_client_read.argtypes = [POINTER_T(struct_r_socket_t), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
r_socket_rap_client_seek = _libr_socket.r_socket_rap_client_seek
r_socket_rap_client_seek.restype = ctypes.c_int32
r_socket_rap_client_seek.argtypes = [POINTER_T(struct_r_socket_t), ctypes.c_uint64, ctypes.c_int32]
class struct_r_run_profile_t(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('_args', POINTER_T(ctypes.c_char) * 512),
    ('_argc', ctypes.c_int32),
    ('_daemon', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('_system', POINTER_T(ctypes.c_char)),
    ('_program', POINTER_T(ctypes.c_char)),
    ('_runlib', POINTER_T(ctypes.c_char)),
    ('_runlib_fcn', POINTER_T(ctypes.c_char)),
    ('_stdio', POINTER_T(ctypes.c_char)),
    ('_stdin', POINTER_T(ctypes.c_char)),
    ('_stdout', POINTER_T(ctypes.c_char)),
    ('_stderr', POINTER_T(ctypes.c_char)),
    ('_chgdir', POINTER_T(ctypes.c_char)),
    ('_chroot', POINTER_T(ctypes.c_char)),
    ('_libpath', POINTER_T(ctypes.c_char)),
    ('_preload', POINTER_T(ctypes.c_char)),
    ('_bits', ctypes.c_int32),
    ('_pid', ctypes.c_int32),
    ('_pidfile', POINTER_T(ctypes.c_char)),
    ('_r2preload', ctypes.c_int32),
    ('_docore', ctypes.c_int32),
    ('_dofork', ctypes.c_int32),
    ('_dodebug', ctypes.c_int32),
    ('_aslr', ctypes.c_int32),
    ('_maxstack', ctypes.c_int32),
    ('_maxproc', ctypes.c_int32),
    ('_maxfd', ctypes.c_int32),
    ('_r2sleep', ctypes.c_int32),
    ('_execve', ctypes.c_int32),
    ('_setuid', POINTER_T(ctypes.c_char)),
    ('_seteuid', POINTER_T(ctypes.c_char)),
    ('_setgid', POINTER_T(ctypes.c_char)),
    ('_setegid', POINTER_T(ctypes.c_char)),
    ('_input', POINTER_T(ctypes.c_char)),
    ('_connect', POINTER_T(ctypes.c_char)),
    ('_listen', POINTER_T(ctypes.c_char)),
    ('_pty', ctypes.c_int32),
    ('_timeout', ctypes.c_int32),
    ('_timeout_sig', ctypes.c_int32),
    ('_nice', ctypes.c_int32),
     ]

RRunProfile = struct_r_run_profile_t
r_run_new = _libr_socket.r_run_new
r_run_new.restype = POINTER_T(struct_r_run_profile_t)
r_run_new.argtypes = [POINTER_T(ctypes.c_char)]
r_run_parse = _libr_socket.r_run_parse
r_run_parse.restype = ctypes.c_bool
r_run_parse.argtypes = [POINTER_T(struct_r_run_profile_t), POINTER_T(ctypes.c_char)]
r_run_free = _libr_socket.r_run_free
r_run_free.restype = None
r_run_free.argtypes = [POINTER_T(struct_r_run_profile_t)]
r_run_parseline = _libr_socket.r_run_parseline
r_run_parseline.restype = ctypes.c_bool
r_run_parseline.argtypes = [POINTER_T(struct_r_run_profile_t), POINTER_T(ctypes.c_char)]
r_run_help = _libr_socket.r_run_help
r_run_help.restype = POINTER_T(ctypes.c_char)
r_run_help.argtypes = []
r_run_config_env = _libr_socket.r_run_config_env
r_run_config_env.restype = ctypes.c_int32
r_run_config_env.argtypes = [POINTER_T(struct_r_run_profile_t)]
r_run_start = _libr_socket.r_run_start
r_run_start.restype = ctypes.c_int32
r_run_start.argtypes = [POINTER_T(struct_r_run_profile_t)]
r_run_reset = _libr_socket.r_run_reset
r_run_reset.restype = None
r_run_reset.argtypes = [POINTER_T(struct_r_run_profile_t)]
r_run_parsefile = _libr_socket.r_run_parsefile
r_run_parsefile.restype = ctypes.c_bool
r_run_parsefile.argtypes = [POINTER_T(struct_r_run_profile_t), POINTER_T(ctypes.c_char)]
r_run_get_environ_profile = _libr_socket.r_run_get_environ_profile
r_run_get_environ_profile.restype = POINTER_T(ctypes.c_char)
r_run_get_environ_profile.argtypes = [POINTER_T(POINTER_T(ctypes.c_char))]
r2pipe_write = _libr_socket.r2pipe_write
r2pipe_write.restype = ctypes.c_int32
r2pipe_write.argtypes = [POINTER_T(struct_c__SA_R2Pipe), POINTER_T(ctypes.c_char)]
r2pipe_read = _libr_socket.r2pipe_read
r2pipe_read.restype = POINTER_T(ctypes.c_char)
r2pipe_read.argtypes = [POINTER_T(struct_c__SA_R2Pipe)]
r2pipe_close = _libr_socket.r2pipe_close
r2pipe_close.restype = ctypes.c_int32
r2pipe_close.argtypes = [POINTER_T(struct_c__SA_R2Pipe)]
r2pipe_open_corebind = _libr_socket.r2pipe_open_corebind
r2pipe_open_corebind.restype = POINTER_T(struct_c__SA_R2Pipe)
r2pipe_open_corebind.argtypes = [POINTER_T(struct_r_core_bind_t)]
r2pipe_open = _libr_socket.r2pipe_open
r2pipe_open.restype = POINTER_T(struct_c__SA_R2Pipe)
r2pipe_open.argtypes = [POINTER_T(ctypes.c_char)]
r2pipe_open_dl = _libr_socket.r2pipe_open_dl
r2pipe_open_dl.restype = POINTER_T(struct_c__SA_R2Pipe)
r2pipe_open_dl.argtypes = [POINTER_T(ctypes.c_char)]
r2pipe_cmd = _libr_socket.r2pipe_cmd
r2pipe_cmd.restype = POINTER_T(ctypes.c_char)
r2pipe_cmd.argtypes = [POINTER_T(struct_c__SA_R2Pipe), POINTER_T(ctypes.c_char)]
r2pipe_cmdf = _libr_socket.r2pipe_cmdf
r2pipe_cmdf.restype = POINTER_T(ctypes.c_char)
r2pipe_cmdf.argtypes = [POINTER_T(struct_c__SA_R2Pipe), POINTER_T(ctypes.c_char)]
__all__ = \
    ['R2Pipe', 'RAP_PACKET_CLOSE', 'RAP_PACKET_CMD', 'RAP_PACKET_MAX',
    'RAP_PACKET_OPEN', 'RAP_PACKET_READ', 'RAP_PACKET_REPLY',
    'RAP_PACKET_SEEK', 'RAP_PACKET_WRITE', 'RRunProfile', 'RSocket',
    'RSocketHTTPOptions', 'RSocketHTTPRequest', 'RSocketProc',
    'RSocketRapServer', 'c__Ea_RAP_PACKET_OPEN', 'r2pipe_close',
    'r2pipe_cmd', 'r2pipe_cmdf', 'r2pipe_open',
    'r2pipe_open_corebind', 'r2pipe_open_dl', 'r2pipe_read',
    'r2pipe_write', 'r_run_config_env', 'r_run_free',
    'r_run_get_environ_profile', 'r_run_help', 'r_run_new',
    'r_run_parse', 'r_run_parsefile', 'r_run_parseline',
    'r_run_reset', 'r_run_start', 'r_socket_accept',
    'r_socket_accept_timeout', 'r_socket_block_time',
    'r_socket_close', 'r_socket_close_fd', 'r_socket_connect',
    'r_socket_connect_serial', 'r_socket_flush', 'r_socket_free',
    'r_socket_gets', 'r_socket_http_accept', 'r_socket_http_close',
    'r_socket_http_get', 'r_socket_http_handle_upload',
    'r_socket_http_post', 'r_socket_http_response',
    'r_socket_http_server_set_breaked', 'r_socket_is_connected',
    'r_socket_listen', 'r_socket_new', 'r_socket_new_from_fd',
    'r_socket_port_by_name', 'r_socket_printf', 'r_socket_proc_close',
    'r_socket_proc_gets', 'r_socket_proc_open',
    'r_socket_proc_printf', 'r_socket_proc_read',
    'r_socket_proc_ready', 'r_socket_proc_write', 'r_socket_puts',
    'r_socket_rap_client_command', 'r_socket_rap_client_open',
    'r_socket_rap_client_read', 'r_socket_rap_client_seek',
    'r_socket_rap_client_write', 'r_socket_rap_server_accept',
    'r_socket_rap_server_continue', 'r_socket_rap_server_create',
    'r_socket_rap_server_free', 'r_socket_rap_server_listen',
    'r_socket_rap_server_new', 'r_socket_read', 'r_socket_read_block',
    'r_socket_ready', 'r_socket_slurp', 'r_socket_spawn',
    'r_socket_to_string', 'r_socket_version', 'r_socket_write',
    'rap_server_close', 'rap_server_cmd', 'rap_server_open',
    'rap_server_read', 'rap_server_seek', 'rap_server_write',
    'struct_c__SA_R2Pipe', 'struct_in_addr', 'struct_r_core_bind_t',
    'struct_r_list_iter_t', 'struct_r_list_t',
    'struct_r_run_profile_t', 'struct_r_socket_http_options',
    'struct_r_socket_http_request', 'struct_r_socket_proc_t',
    'struct_r_socket_rap_server_t', 'struct_r_socket_t',
    'struct_sockaddr_in']

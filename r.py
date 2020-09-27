from ctypes import *

PRCORE = POINTER(c_int64)

libr = cdll.LoadLibrary("libr_main.so")
libr.r_core_new.restype = PRCORE

r_core = libr.r_core_new()

libr.r_core_init(r_core)
libr.r_core_project_list(r_core)
libr.r_core_parse_radare2rc(r_core)
fh = libr.r_core_file_open(r_core, create_string_buffer(b"/bin/ls"), 0b101, 0)
libr.r_core_bin_load(r_core, create_string_buffer(b"/bin/ls"), 0xFFFFFFFFFFFFFFFF)
libr.r_core_cmd0(r_core, create_string_buffer(b"=!"))
libr.r_core_cmd0(r_core, create_string_buffer(b"ieq"))
libr.r_core_cmd0(r_core, create_string_buffer(b"aaa"))
print(string_at(libr.r_core_cmd_str(r_core, create_string_buffer(b"pdj"))))
libr.r_core_free(r_core)
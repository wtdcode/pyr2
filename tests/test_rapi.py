import unittest
import ctypes
import r2
import json
import struct

class RAPITest(unittest.TestCase):
    
    def test_r_core(self):
        r2c = r2.r_core.r_core_new()
        fh = r2.r_core.r_core_file_open(r2c, ctypes.create_string_buffer(b"/bin/ls"), 0b101, 0)
        r2.r_core.r_core_bin_load(r2c, ctypes.create_string_buffer(b"/bin/ls"), (1<<64) - 1)
        r2.r_core.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"ieq"))
        r2.r_core.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"aaa"))
        print(f'Disasm 1 instruction:\n{ctypes.string_at(r2.r_core.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"pd 1"))).decode("utf-8")}')
        r2.r_core.r_core_free(r2c)

    def test_r_anal(self):
        r2c = r2.r_core.r_core_new()
        fh = r2.r_core.r_core_file_open(r2c, ctypes.create_string_buffer(b"/bin/ls"), 0b101, 0)
        r2.r_core.r_core_bin_load(r2c, ctypes.create_string_buffer(b"/bin/ls"), (1<<64) - 1)
        r2.r_core.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"ieq"))
        r2.r_core.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"aaa"))
        # Workaround for multiple declarations in sources.
        r2anal = ctypes.cast(ctypes.addressof(r2c.contents.anal.contents), ctypes.POINTER(r2.r_anal.struct_r_anal_t))
        print(f"We have {r2.r_anal.r_anal_xrefs_count(r2anal)} xrefs!")

    def test_r_asm(self):
        buffer = b"\x90\x90\x90"
        buffer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))
        r2c = r2.r_core.r_core_new()
        fh = r2.r_core.r_core_file_open(r2c, ctypes.create_string_buffer(b"/bin/ls"), 0b101, 0)
        r2.r_core.r_core_bin_load(r2c, ctypes.create_string_buffer(b"/bin/ls"), (1<<64) - 1)
        r2asm = ctypes.cast(r2c.contents.rasm, ctypes.POINTER(r2.r_asm.struct_r_asm_t))
        asmcode = r2.r_asm.r_asm_mdisassemble(r2asm, buffer, 3)
        disasm_output = ctypes.string_at(asmcode.contents.assembly).decode('utf-8')
        self.assertEqual(disasm_output, "nop\nnop\nnop\n")

    def test_r_util_json(self):
        json_str = b'{"key" : "value"}'
        rjson = r2.r_util.r_json_parse(json_str)
        rjson = r2.r_util.r_json_get(rjson, b"key")
        # Stalled by https://github.com/trolldbois/ctypeslib/issues/93
        value = ctypes.string_at(rjson.contents.r_json_t_0.str_value).decode("utf-8")
        self.assertEqual(value, "value")

    def test_r_util_utf8(self):
        u8 = '\u4e91'
        rune = ord(u8)
        buffer = ctypes.create_string_buffer(4)
        buffer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))
        l = r2.r_util.r_utf8_encode(buffer, ctypes.c_uint32(rune))
        self.assertEqual(ctypes.string_at(buffer, l), u8.encode("utf-8"))

if __name__ == "__main__":
    unittest.main()
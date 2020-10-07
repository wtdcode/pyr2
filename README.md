## pyr2

Yet another radare2 python bindings.

## Install

```bash
pip3 install pyr2
```

**No need to install radare2** since all dynamic libraries are bundled with the Python wheels.

## Example

```python
import ctypes
from r2 import libr

r2c = libr.r_core_new()
libr.r_core_init(r2c)
fh = libr.r_core_file_open(r2c, ctypes.create_string_buffer(b"/bin/ls"), 0b101, 0)
libr.r_core_bin_load(r2c, ctypes.create_string_buffer(b"/bin/ls"), (1<<64) - 1)
libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"ieq"))
libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"aaa"))
print(ctypes.string_at(libr.r_core_cmd_str(r2c, ctypes.create_string_buffer(b"pdj"))))
libr.r_core_file_close(r2c, fh)
```

`libr` is the core library of radare2 which implements all low-level APIs. Note that it's exported as a bare ctypes library, be cautious with c-style strings.

## Build Instructions

Clone the repository and submodules.

```bash
git clone https://github.com/wtdcode/pyr2
cd pyr2
git submodule update --init --recursive
```

Since radare2 chooses `meson` as their alternative building system, the first step is install `meson`.

```bash
pip3 install meson
```

Build the package.

```bash
python3 setup.py build
```

Install and use.

```bash
# Or pip3 install -e .
pip3 install .
```

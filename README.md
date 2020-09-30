## pyr2

Yet another r2 python bindings.

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

## Example

```python
from r2cmd import R2

r2 = R2()
fh = r2.r_core_open_file("/bin/ls", 0b101, 0)
r2.r_core_load_bin("/bin/ls")
r2.r_core_cmd_str("ieq")
r2.r_core_cmd_str("aaa")
print(r2.r_core_cmd_str("pdj"))
r2.r_core_file_close(fh)
```
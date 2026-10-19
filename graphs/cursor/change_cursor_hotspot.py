# 代码由ds网页版贡献

from pathlib import Path
import struct

src = Path(r"C:\Users\Lee\Desktop\Qt notes\src_code\1-5-change_mouse_style\graphs\static_graphs\2-mouse_ico.cur")
dst = src.with_name("2-mouse_ico_fixed.cur")

data = bytearray(src.read_bytes())

# 1. 类型: 1 (ico) -> 2 (cur)
struct.pack_into("<H", data, 2, 2)

# 2. 热点设到图片正中心 (16, 16)
#    32x32 的中心像素下标是 16
struct.pack_into("<H", data, 10, 16)   # hotspot X
struct.pack_into("<H", data, 12, 16)   # hotspot Y

dst.write_bytes(data)

print("done:", dst)
print("head:", data[:4].hex(" "))
print("hotspot:", struct.unpack_from("<HH", data, 10))
# 由ds贡献
"""把本目录下的 0-icon.gif 转为 0-icon.ico（多尺寸，保留透明通道）。"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "0-icon.gif"
DST = HERE / "0-icon.ico"

# ICO 内嵌的尺寸，不超过源图边长
SIZES = [16, 24, 32, 48, 64, 96]


def main() -> None:
    with Image.open(SRC) as im:
        im.seek(0)  # 动图只取第一帧
        icon = im.convert("RGBA")  # 调色板转 RGBA，保留透明背景

    side = min(icon.size)
    sizes = sorted({s for s in SIZES if s <= side} or {side})
    icon.save(DST, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"{SRC.name} -> {DST.name}  {sizes}")


if __name__ == "__main__":
    main()

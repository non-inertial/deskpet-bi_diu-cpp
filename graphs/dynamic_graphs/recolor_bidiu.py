# 由ds贡献
"""把 1-zhuzhunian-fighting.gif 里比丢的身体颜色，改成 3-ri'chang-bye.gif 里的同款橙色。

两个 GIF 的比丢都是「纯色身体 + 抗锯齿过渡带 + 深棕描边」的结构。只换身体主色的话，
身体和描边之间那圈过渡像素仍是黄色系，边缘会残留一圈黄光晕；所以这里把
「身体色 → 描边色」整条色带按相对位置平移到新色带，描边本身不动。
FIGHTING 文字、腮红、闪光等其他元素的颜色一律不变。
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "1-zhuzhunian-fighting.gif"  # 原地替换，首次运行留一份 .bak
BACKUP = HERE / "1-zhuzhunian-fighting.gif.bak"

# 取样自两个 GIF 实际调色板的颜色
BODY_SRC = np.array([0xFC, 0xCE, 0x62], dtype=float)  # 原身体色：浅黄
BODY_DST = np.array([0xFF, 0xB0, 0x40], dtype=float)  # 目标身体色：橙色（取自 3-ri'chang-bye.gif）
OUTLINE = np.array([0x50, 0x2C, 0x1D], dtype=float)   # 描边深棕，保持不变

RAMP_TOL = 32.0    # 颜色到「身体 → 描边」直线的距离阈值，小于它才算身体或过渡色
TRANSPARENT = 255  # 输出 GIF 的透明索引，原文件也是 255


def build_map(colors):
    """色带上的颜色映射到新色带的同一相对位置，带外的颜色不映射。"""
    axis = OUTLINE - BODY_SRC
    mapping = {}
    for color in colors:
        px = np.asarray(color, dtype=float)
        t = float(np.clip(np.dot(px - BODY_SRC, axis) / np.dot(axis, axis), 0.0, 1.0))
        if np.linalg.norm(px - (BODY_SRC + t * axis)) < RAMP_TOL:
            mapping[color] = tuple(int(v) for v in np.round(BODY_DST + t * (OUTLINE - BODY_DST)))
    return mapping


def recolor(frame, mapping):
    """替换一帧里命中映射表的颜色，透明像素不动。返回 (新帧, 替换像素数)。"""
    out = frame.copy()
    src = frame.reshape(-1, 4)
    dst = out.reshape(-1, 4)
    opaque = src[:, 3] >= 128  # GIF 只有全透明/全不透明

    colors, inverse = np.unique(src[opaque][:, :3], axis=0, return_inverse=True)
    new = np.array(
        [mapping.get(tuple(int(v) for v in c), tuple(int(v) for v in c)) for c in colors],
        dtype=np.uint8,
    )
    dst[opaque, :3] = new[inverse]
    return out, int((new != colors).any(axis=1)[inverse].sum())


def save_gif(frames, duration, loop, transparent_rgb):
    """写回 GIF：全局调色板 + 二值透明，保留帧时长和循环设置。"""
    palette_colors = sorted(
        {tuple(c) for f in frames for c in f[..., :3][f[..., 3] >= 128].reshape(-1, 3)}
    )
    if len(palette_colors) > TRANSPARENT:
        raise SystemExit(f"颜色数 {len(palette_colors)} 超过 GIF 调色板上限 {TRANSPARENT}")

    index_of = {c: i for i, c in enumerate(palette_colors)}
    palette = [0] * 768
    for color, i in index_of.items():
        palette[i * 3 : i * 3 + 3] = list(color)
    # 透明像素的调色板 RGB 是解码器不支持透明时的兜底底色，跟原文件一样用白色
    palette[TRANSPARENT * 3 : TRANSPARENT * 3 + 3] = list(transparent_rgb)

    images = []
    for frame in frames:
        indices = np.full(frame.shape[:2], TRANSPARENT, dtype=np.uint8)
        opaque = frame[..., 3] >= 128
        indices[opaque] = [index_of[tuple(c)] for c in frame[..., :3][opaque]]
        img = Image.fromarray(indices, mode="P")
        img.putpalette(palette)
        images.append(img)

    images[0].save(
        SRC,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop,
        transparency=TRANSPARENT,
        disposal=2,  # 每帧都是整幅图，画完即还原成透明背景
        optimize=False,
    )


def main() -> None:
    with Image.open(SRC) as im:
        duration = im.info.get("duration", 100)
        loop = im.info.get("loop", 0)
        index = im.info.get("transparency")
        palette = im.getpalette()
        transparent_rgb = (
            tuple(palette[index * 3 : index * 3 + 3])
            if index is not None and palette
            else (255, 255, 255)
        )
        frames = []
        for i in range(im.n_frames):
            im.seek(i)  # 按顺序 seek，Pillow 会把增量帧合成成完整帧
            frames.append(np.array(im.convert("RGBA")))

    colors = {tuple(c) for f in frames for c in f[..., :3][f[..., 3] >= 128].reshape(-1, 3)}
    mapping = build_map(colors)
    new_frames, changed_px = [], 0
    for frame in frames:
        new, n = recolor(frame, mapping)
        new_frames.append(new)
        changed_px += n

    if changed_px == 0:
        raise SystemExit(f"{SRC.name} 里没有找到要替换的身体色，可能已经改过了")
    if not BACKUP.exists():
        BACKUP.write_bytes(SRC.read_bytes())

    save_gif(new_frames, duration, loop, transparent_rgb)
    n_colors = sum(1 for c, m in mapping.items() if c != m)
    print(f"{SRC.name}  帧数 {len(frames)}  替换 {n_colors} 个颜色 / {changed_px} 像素")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""生成官网 OG 分享图（1200x630，indigo→cyan 渐变，ai-study-kit 同款视觉）。

用法：python3 site/scripts/gen-og.py
产物 og.png 提交入库（CI 不装 PIL，避免运行期依赖）；改视觉时本地重跑再提交。
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
INDIGO = (79, 70, 229)
CYAN = (6, 182, 212)

CJK_FONTS = [
    "/System/Library/Fonts/PingFang.ttc",  # macOS
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",  # Linux (noto-cjk)
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux fallback（无中文）
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for p in CJK_FONTS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "public" / "og.png"

    # 对角渐变：2x2 角色块 + 双线性放大（与站内 --ft-gradient 同一走向）
    grad = Image.new("RGB", (2, 2))
    grad.putpixel((0, 0), INDIGO)
    grad.putpixel((1, 0), (60, 100, 230))
    grad.putpixel((0, 1), (30, 130, 235))
    grad.putpixel((1, 1), CYAN)
    img = grad.resize((W, H), Image.BILINEAR)
    draw = ImageDraw.Draw(img)

    # 左上徽标：白色圆角框 + 波形 + 点（镜像 site/src/assets/logo.svg）
    bx, by, side = 64, 64, 118
    draw.rounded_rectangle((bx, by, bx + side, by + side), radius=28,
                           outline=(255, 255, 255), width=4)
    # 波形：logo 的 path M6 17c4-8 10 8 14 0（viewBox 26）按比例放大
    def scale(p):
        return (bx + 18 + p[0] / 26 * (side - 36), by + 16 + p[1] / 26 * (side - 36))
    wave = []
    for i in range(41):
        t = i / 40
        # 两段三次贝塞尔的粗略合成：直接用 sin 近似原曲线形状
        x = 6 + 14 * t
        y = 17 - 6.2 * ((2 * t - 1) ** 3 - (2 * t - 1))  # S 曲线
        wave.append(scale((x, y)))
    draw.line(wave, fill=(255, 255, 255), width=6, joint="curve")
    dx, dy = scale((9, 9))
    draw.ellipse((dx - 7, dy - 7, dx + 7, dy + 7), fill=(255, 255, 255))

    # 标题区
    draw.text((66, 268), "flowtest", font=load_font(96), fill=(255, 255, 255), anchor="lm")
    draw.text((68, 372), "描述用户旅程，让代理在真实浏览器里测试它",
              font=load_font(52), fill=(255, 255, 255), anchor="lm")
    draw.text((68, 456), "流程是 YAML · 每步带截图 · 失败记成笔记",
              font=load_font(34), fill=(230, 240, 255), anchor="lm")
    # 底部标签条
    draw.text((68, H - 64), "开源 MIT · GitHub Pages",
              font=load_font(28), fill=(210, 225, 255), anchor="lm")

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    print(f"og image -> {out} ({W}x{H})")


if __name__ == "__main__":
    main()

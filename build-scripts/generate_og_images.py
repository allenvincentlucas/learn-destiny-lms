import sys
sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFont
from site_data import MODULE_META

W, H = 1200, 630
PAPER = (250, 249, 246)
PAPER_WARM = (243, 240, 232)
INK = (25, 27, 31)
INK_SOFT = (58, 61, 66)
BLUE = (42, 75, 141)
STONE = (132, 128, 111)
STONE_LINE = (216, 211, 196)

FONT_DIR = '/home/claude/fonts'

def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    try:
        if weight:
            f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

def space_grotesk(size, weight=700):
    return font(f'{FONT_DIR}/SpaceGrotesk.ttf', size, weight)

def inter(size, weight=400):
    return font(f'{FONT_DIR}/Inter.ttf', size, weight)

def mono(size, weight=500):
    return font(f'{FONT_DIR}/JetBrainsMono.ttf', size, weight)

def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines = []
    cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        bbox = draw.textbbox((0, 0), test, font=f)
        if bbox[2] - bbox[0] <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def base_canvas():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # subtle top-warm gradient band
    for y in range(0, 220):
        t = y / 220
        r = int(PAPER_WARM[0] + (PAPER[0] - PAPER_WARM[0]) * t)
        g = int(PAPER_WARM[1] + (PAPER[1] - PAPER_WARM[1]) * t)
        b = int(PAPER_WARM[2] + (PAPER[2] - PAPER_WARM[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # bottom accent bar
    d.rectangle([0, H - 10, W, H], fill=BLUE)
    return img, d

def draw_brand(d, x, y):
    # small bordered square mark "FD"
    size = 44
    d.rectangle([x, y, x + size, y + size], outline=INK, width=2)
    f = mono(18, 700)
    bbox = d.textbbox((0, 0), 'FD', font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((x + size / 2 - tw / 2, y + size / 2 - th / 2 - bbox[1]), 'FD', font=f, fill=INK)
    f2 = space_grotesk(22, 700)
    d.text((x + size + 14, y + size / 2 - 13), 'Destiny Training Curriculum', font=f2, fill=INK)

def draw_eyebrow(d, x, y, text, color=BLUE):
    f = mono(20, 700)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 14, 8
    d.rectangle([x, y, x + tw + pad_x * 2, y + th + pad_y * 2 + 6], outline=color, width=2)
    d.text((x + pad_x, y + pad_y - bbox[1]), text, font=f, fill=color)
    return th + pad_y * 2 + 6

def generate_module_image(m, meta, out_path):
    img, d = base_canvas()
    draw_brand(d, 70, 56)

    eb_h = draw_eyebrow(d, 70, 150, f'MODULE 0{m}' if m < 10 else f'MODULE {m}')

    title_font = space_grotesk(58, 700)
    title_y = 150 + eb_h + 28
    lines = wrap_text(d, meta['title'], title_font, W - 140)[:3]
    ly = title_y
    for line in lines:
        d.text((70, ly), line, font=title_font, fill=INK)
        bbox = d.textbbox((0, 0), line, font=title_font)
        ly += (bbox[3] - bbox[1]) + 16

    desc_font = inter(24, 400)
    desc_lines = wrap_text(d, meta['desc'], desc_font, W - 140)[:2]
    dy = ly + 14
    for line in desc_lines:
        d.text((70, dy), line, font=desc_font, fill=INK_SOFT)
        bbox = d.textbbox((0, 0), line, font=desc_font)
        dy += (bbox[3] - bbox[1]) + 10

    call_font = mono(19, 500)
    d.text((70, H - 56), f"CALL NO. {meta['call']}", font=call_font, fill=STONE)

    img.save(out_path, 'PNG')

def generate_home_image(out_path):
    img, d = base_canvas()
    draw_brand(d, 70, 56)
    draw_eyebrow(d, 70, 150, 'FREE RESOURCE FOR SCHOOL LIBRARIANS')

    title_font = space_grotesk(58, 700)
    lines = ['Learn Follett Destiny,', 'one module at a time.']
    ly = 236
    colors = [INK, BLUE]
    for line, c in zip(lines, colors):
        d.text((70, ly), line, font=title_font, fill=c)
        bbox = d.textbbox((0, 0), line, font=title_font)
        ly += (bbox[3] - bbox[1]) + 16

    desc_font = inter(24, 400)
    desc = 'A free, independent 9-module training curriculum for Follett Destiny, updated for Destiny 24.0/23.5.'
    dy = ly + 14
    for line in wrap_text(d, desc, desc_font, W - 140)[:2]:
        d.text((70, dy), line, font=desc_font, fill=INK_SOFT)
        bbox = d.textbbox((0, 0), line, font=desc_font)
        dy += (bbox[3] - bbox[1]) + 10

    d.text((70, H - 56), '9 MODULES  ·  VIDEO WALKTHROUGHS  ·  KNOWLEDGE CHECKS', font=mono(19, 500), fill=STONE)

    img.save(out_path, 'PNG')

if __name__ == '__main__':
    generate_home_image('../assets/img/og/home.png')
    for m in range(1, 10):
        generate_module_image(m, MODULE_META[m], f'../assets/img/og/module-{m}.png')
    print('OG images generated.')

# 工具模組，可以透過單一字元取得對應的點陣圖位元資料

import os

f = None # 字型檔物件

utf16_tables = [
    (0x00A2, 0x2642),
    (0x3000, 0x33E0),
    (0x4E00, 0x9FA4),
    (0xFE10, 0xFFE3),
]

def set_font_path(path):
    global f
    f = open(path, 'rb')

def get_bitmap(ch):
    if not f:
        print("Font file not loaded.")
        return None
    code = ord(ch)
    if code <= 0x7E:
        f.seek((code - 0x20) * 12)
        return f.read(12)
    offset = (0x7f - 0x20) * 12
    for start, end in utf16_tables:
        if start <= code <= end:
            offset += (code - start) * 24
            f.seek(offset)
            return f.read(24)
            break
        offset += (end - start + 1) * 24
    return None

# MicroPython only

import sys

if 'MicroPython' in sys.version:

    from framebuf import FrameBuffer, MONO_HLSB, MONO_HMSB

    # 在 oled 指定位置繪製單一字元
    def draw_bitmap(oled, bitmap, x, y):
        width = 8 if len(bitmap) == 12 else 16 
        height = 12
        pic_array = bytearray(bitmap) # 轉換成位元組陣列
        frame = FrameBuffer(          # 建立影格
            pic_array,                         
            width,
            height,
            MONO_HLSB # 單色圖形、每個位元組代表水平排列的 8 個像素、最高位元是最左邊的點
        )
        oled.blit(frame, x, y) # 繪製圖形

    def draw_text(oled, text, x, y):
        for c in text:
            y = y % 64
            if c == '\n':
                y += 12
                x = 0
                continue
            if c == '\r':
                x = 0
                continue
            bitmap = get_bitmap(c)
            if bitmap is None:
                bitmap = get_bitmap('☒')
                print(f"'{c}' not found in font file.")
            x_next = x + (6 if len(bitmap) == 12 else 12)
            if x_next >= 128:
                y += 12
                x = 0
            draw_bitmap(oled, bitmap, x, y)
            x += (6 if len(bitmap) == 12 else 12)

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
    if code < 0x7E:
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
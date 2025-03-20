# 從 BDF 檔擷取點陣圖資料建立客製的字型檔
# 客製字型檔中就是把每個字的點陣圖資料依序存放
import bdfparser

# 取得 script 本身的路徑
import os
import sys
parent_dir = os.path.dirname(os.path.realpath(__file__))
print(parent_dir)
font = bdfparser.Font(f"{parent_dir}/../fonts/fusion-pixel-12px-monospaced-zh_hant.bdf")
sys.path.append(f'{parent_dir}/../lib')


# 客製字型檔開頭會放 ASCII 32~126 的英數字符號，以 8x12 像素表示
# 接著放置以下這些涵蓋 big5 字元範圍的 UTF16 字元，以 12x12 像素表示
#   (0x00A2, 0x2642),
#   (0x3000, 0x33D5),
#   (0x4E00, 0x9FA4),
#   (0xFA0C, 0xFFE3)
# 不過實際上 fusion 字型中有缺字，所以調整後的 UTF16 字元範圍如下表
# 這些範圍中還是有許多缺字，但不是連續大範圍，這裡採簡易作法，缺字就填 0
# utf16_tables = [
#     (0x00A2, 0x2642),
#     (0x3000, 0x33E0),
#     (0x4E00, 0x9FA4),
#     (0xFE10, 0xFFE3),
# ]
from bitmap_font_tool import utf16_tables

with open('../lib/fonts/fusion_bdf.12', 'wb') as f:
    # ASCII 32~126
    for code in range(32, 127):
        glyph = font.glyph(chr(code))
        bitmap = glyph.draw()
        # 寬度裁到 6 像素，高度維持 12 像素，寬度再補齊到 8 的倍數
        # 這樣可以讓半形字每橫列 1 個位元組，共 12 個位元組
        bitmap = bitmap.crop(6, 12).bytepad(8)
        for b in bitmap.bindata:
            code = int(b, 2) # 轉換成整數
            f.write(code.to_bytes(1)) # 寫入 1 個位元組

    # UTF16 字元
    for start, end in utf16_tables:
        for code in range(start, end + 1):
            glyph = font.glyph(chr(code))
            if glyph is None:
                # fusion 字型檔中缺字就填 0
                # 之後顯示看到奇怪的空白就知道缺字
                # 因為有補齊位元到 8 的倍數，所以一個字是 16x12 位元 = 24 個位元組
                f.write(b'\x00' * 24)
                continue
            bitmap = glyph.draw()
            bitmap = bitmap.bytepad(8)
            for b in bitmap.bindata:
                code = int(b, 2)
                # 注意，to_bytes 預設是 big-endian 順序
                # 讀回來的時候也要使用相同的順序
                f.write(code.to_bytes(2))    
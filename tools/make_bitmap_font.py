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

# 匯入要製作的字型檔 UTF6 範圍表格
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
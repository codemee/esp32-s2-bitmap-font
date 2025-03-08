# 測試依據字元讀取 BDF 字型檔中的資訊

import bdfparser

def main():
    # 本例使用字型檔為全形 12x12, 半形 6x12 的像素字型
    font = bdfparser.Font("./fonts/fusion-pixel-12px-monospaced-zh_hant.bdf")

    while True:
        text = input("輸入要測試的文字：")
        if text == "":
            break
        for ch in text:
            print("-" * 20)
            glyph = font.glyph(ch)
            bitmap = glyph.draw()        # 取得點陣圖位元資料
            print(bitmap)                # 顯示點陣圖位元資料
            bitmap = bitmap.bytepad(8)   # 將點陣圖位元資料補齊到 8 的倍數
            print(bitmap.bindata)        # 顯示點陣圖位元資料（每列一個字串）
            for b in bitmap.bindata:     
                print(f'0x{int(b, 2):04X}:{b}') # 以 16 進位數字表示每一列

if __name__ == "__main__":
    main()

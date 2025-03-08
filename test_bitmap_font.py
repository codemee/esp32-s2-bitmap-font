# 用來測試 bitmap_font_tool.py 的程式
# 同時也確認 make_bitmap_font.py 客製的字型檔正確
from lib.bitmap_font_tool import set_font_path, get_bitmap

# 用 O 表示 bit 1 顯示字形
def print_byte(b):
    out = bin(b)[2:].zfill(8).replace('0', ' ').replace('1', 'O')
    print(out, end='')


set_font_path("lib/fonts/fusion_bdf.12")

while True:
    text = input("輸入測試文字：")
    if text == "":
        break
    
    for c in text:
        bitmap = get_bitmap(c)
        print('-' * 40)
        print(f"UTF16：{ord(c):04X}，字元：{c}")
        if bitmap is None:
            print("找不到字元：", c)
            continue
        if len(bitmap) == 12:
            # 半形字是 12 個位元組
            for i in range(12):
                # print(f"{bitmap[i]:08b}")
                print_byte(bitmap[i])
                print()
        if len(bitmap) == 24:
            # 全形字是 24 個位元組
            for i in range(12):
                print_byte(bitmap[i * 2])
                print_byte(bitmap[i * 2 + 1])
                print()
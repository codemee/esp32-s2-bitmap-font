# 用來檢查 big5 編碼對應的 utf16 編碼範圍內是否有連續範圍的缺字
# 以便剔除缺字範圍達到盡量縮減客製的字型檔所佔的空間

big5_tables = [
    (0x00A2, 0x2642),
    (0x3000, 0x33D5),
    (0x4E00, 0x9FA4),
    (0xFA0C, 0xFFE3)
]

with open('../fonts/fusion-pixel-12px-monospaced-zh_hant.bdf') as f:
    item = 0
    in_block = False
    prev_code = -1
    hole = 0
    for line in f:
        if line.startswith('ENCODING '):
            code = int(line.split()[1])
            if in_block and code != prev_code + 1:
                # print('Missing code:', hex(prev_code + 1))
                hole += 1
            prev_code = code
            if code == big5_tables[item][0]:
                print('Found start:', hex(code))
                in_block = True
            elif code == big5_tables[item][1]:
                print('Found end:', hex(code))
                in_block = False
                item += 1
            elif not in_block and code > big5_tables[item][0]:
                print('Missing start:', hex(code))
                in_block = True
                # item += 1
            elif in_block and code > big5_tables[item][1]:
                print('Missing end:', hex(code))
                item += 1
        if item >= len(big5_tables):
            print('Last code:', hex(code))
            print('Total holes:', hole)
            break
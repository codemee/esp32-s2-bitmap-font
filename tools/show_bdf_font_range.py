import bdfparser

font = bdfparser.Font("../fonts/fusion-pixel-12px-monospaced-zh_hant.bdf")

start = None
end = None
total = 0
prev_end = None

for codepoint in range(0xA1, 0xFFFF):
    glyph = font.glyph(chr(codepoint))
    if glyph is not None:
        if start is None: # 開始新的範圍
            start = codepoint
            if prev_end is not None: # 如果不是第一個範圍，顯示空缺數
                gap = start - prev_end - 1
                # 顯示空缺量，並且標記特別大的空缺
                print(f'GAP:{gap} characters{'<--' if 300 < gap < 500 else ''}')
                prev_end = None
        end = codepoint # 更新結束範圍
        continue
    if end is not None: # 結束範圍，顯示此範圍區間
        total += end - start + 1
        print(f"0x{start:04X}:0x{end:04X}[{end - start + 1}]")
        prev_end = end
        start = None
        end = None
print(f"Total: {total} characters")
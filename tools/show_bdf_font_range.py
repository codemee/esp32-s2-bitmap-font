import bdfparser

font = bdfparser.Font("../fonts/fusion-pixel-12px-monospaced-zh_hant.bdf")

start = None
end = None
total = 0

for codepoint in range(0xA1, 0xFFFF):
    glyph = font.glyph(chr(codepoint))
    if glyph is not None:
        if start is None:
            start = codepoint
        end = codepoint
        continue
    if end is not None:
        total += end - start + 1
        print(f"0x{start:04X}:0x{end:04X}[{end - start + 1}]")
        start = None
        end = None
print(f"Total: {total} characters")
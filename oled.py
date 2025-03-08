# 安裝模組
# 開發版要先連上網路
# import mip
# mip.install('ssd1306')

from ssd1306 import SSD1306_I2C
from machine import SoftI2C, Pin
from framebuf import FrameBuffer, MONO_HLSB, MONO_HMSB
from bitmap_font_tool import set_font_path, get_bitmap

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

# 在 oled 指定位置繪製單一字元
def draw_ch(oled, bitmap, x, y):
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


set_font_path('./lib/fonts/fusion_bdf.12')

x = 0
y = 16
text = '旗標科技超厲害★'
for c in text:
    if c == '\n':
        y += 12
        x = 0
        continue
    bitmap = get_bitmap(c)
    
    draw_ch(oled, bitmap, x, y)
    x += 6 if len(bitmap) == 12 else 12
oled.show()
# 安裝模組
# 開發版要先連上網路
# import mip
# mip.install('ssd1306')

from ssd1306 import SSD1306_I2C
from machine import SoftI2C, Pin
from bitmap_font_tool import (
    set_font_path,
    draw_text
)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

set_font_path('./fonts/fusion_bdf.12')

draw_text(oled, '┌─╭太帥了！╮─┐', 0, 16)
draw_text(oled, '╘═ㄊ►°℉℃θ═╛', 0, 28)
draw_text(oled, '到地府走一趟才發現\n連閻羅王都會 Python！', 0, 40)
draw_text(oled, '你看不見\r可以用\\r和\\n', 0, 0)
oled.show()
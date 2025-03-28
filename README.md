# 搭配 ESP32-S2 使用的中文字型檔

為了使用 ESP32-S2 在 OLED 上顯示中文字，原本的想法是使用古時候倚天的中文字型檔，雖然可行，但因為字型需要額外授權，所以做罷（國喬中文似乎可以免費使用，但現在也找不到字型檔）。不過剛好在趙英傑老師的《[超圖解 Arduino 互動設計入門 第五版](https://www.flag.com.tw/books/product/F5799)》看到[Fusion Pixel Font](https://fusion-pixel-font.takwolf.com/) 提供了開源的字體，雖然最大只有 12x12，美觀程度上比不上倚天字型，不過在小小的 OLED 上顯示也是剛好，因此就採用此字型檔處理過後讓 ESP32-S2 使用。

由於我的主要目的是顯示繁體中文，因此就以該字型中的 `fusion-pixel-12px-monospaced-zh_hant.bdf` 為主，不過它採用 [BDF](https://font.tomchen.org/bdf_spec/) 格式，耗費空間，因此我仿照倚天中文字形的方式，將原本的 BDF 處理之後，轉成點陣圖的位元資料依照 UTF16 編碼放置，並且參考倚天中文的 [big5](https://www.ifreesite.com/big5.htm) 編碼範圍，只放置我需要的字元後客製成單一字型檔，這個字型檔的結構如下：

|字元範圍|字型大小|位元組數|說明|
|---|---|---|---|
|0x32~0x7E|6x12|12|半形英數字符號，每列補白成 8 個像素|
|0x00A1~0x266F|12x12|24|全形字，每列補白成 16 個像素|
|0x3000~0x33E0|12x12|24|全形字，每列補白成 16 個像素|
|0x4E00~0x9FA4|12x12|24|全形字，每列補白成 16 個像素|
|0xFE10~0xFFE3|12x12|24|全形字，每列補白成 16 個像素|

個別字元的點陣圖就依據 UTF16 編碼順序放置，中間包含有許多原本 BDF 字型檔就缺字的部分，會以空白替代，雖然浪費空間，不過可以簡化字型檔的結構。實際使用時只要依據要顯示字元的 UTF16 編碼，計算出該字元字型點陣圖資料在檔案中的相對位置，就可以取得點陣圖資料了。最後產生的字型檔有 769020 位元組，雖然大了點，不過 ESP32-S2 有 4MB 的 flash，應該很夠用。

## 檔案說明

以下是個別檔案的功用:

|檔名|說明|
|---|---|
|fonts\fusion-pixel-12px-monospaced-zh_hant.bdf|原始的 BDF 字型檔|
|lib\fonts\fusion_bdf.12|從 BDF 字型檔客製後的字型檔|
|lib\bitmap_font_tool.py|搭配客製字型檔使用的模組，可取得指定字元的點陣圖|
|test_bdf_font.py|測試原始的 BDF 字型檔，可以顯示個別字元的樣子|
|test_bitmap_font.py|`bitmap_font_tool.py` 以及客製字型檔的測試程式|
|tools\make_bitmap_font.py|用來製作客製字型檔的工具程式|
|tools\checkrange.py|製作客製字型檔的輔助工具，用來檢查涵蓋 BIG5 編碼需要對應的 UTF16 範圍，減少客製字型檔的大小|
|tools\show_bdf_font_range.py|用來檢查 bdf 檔裡面涵蓋的 UTF16 範圍，並統計字數|
|tools\ranges.txt|上個工具的結果，供調整 make_bitmao_font.py 所需涵蓋的 UTF16 範圍|
|oled.py|MicroPython 範例|

## MicroPython 使用方法

請先把 `lib` 資料夾的內容上傳到 ESP32-S2 開發板上，即可匯入 `bitmap_font_tool` 模組，它提供以下的通用函式：

|函式|說明|
|---|---|
|set_font_path(path)|設定字型檔的路徑，字型檔在 lib\fonts 下|
|get_bitmap(ch)|取得指定字元的點陣圖位元組資料|

上述函式的基本用法可參考範例檔 `test_bitmap_font.py`。以下則是專為 MicroPython 設計的函式：

|函式|說明|
|---|---|
|draw_bitmap(oled, bitmap, x, y)|在 oled 控制的螢幕上 (x,y) 位置繪製點陣圖 bitmap|
|draw_text(oled, text, x, y)|在 oled 控制的螢幕上 (x,y) 位置繪製，它會自動折行，也可以使用 `\n` 強迫換行，或是用 `\r` 回到同一行左邊的行開頭

範例可參考 `oled.py`：

```python
# 安裝模組
# 開發版要先連上網路
# import mip
# mip.install('ssd1306')

from ssd1306 import SSD1306_I2C
from machine import SoftI2C, Pin
from bitmap_font_tool import (
    set_font_path,
    get_bitmap,
    draw_ch,
    draw_text
)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

set_font_path('./lib/fonts/fusion_bdf.12')

draw_text(oled, '┌─╭太帥了！╮─┐', 0, 16)
draw_text(oled, '╘═ㄊ►°℉℃θ═╛', 0, 28)
draw_text(oled, '到地府走一趟才發現\n連閻羅王都會 Python！', 0, 40)
draw_text(oled, '你看不見\r可以用\\r和\\n', 0, 0)
oled.show()
```

理論上只要你的開發板 flash 夠大，擺得進去客製的字型檔，應該就可以用，不過我是專門為了 ESP32-S2 設計，並沒有測試其他開發板。


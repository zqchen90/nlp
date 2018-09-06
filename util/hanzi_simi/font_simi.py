#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:43:40
# @Author  : zhaoqun.czq
# Calculate similarity based on character shape

import binascii

RECT_HEIGHT = 16
RECT_WIDTH = 16
BYTE_COUNT_PER_ROW = RECT_WIDTH / 8
BYTE_COUNT_PER_FONT = BYTE_COUNT_PER_ROW * RECT_HEIGHT

KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

class FontSimi(object):
    def __init__(self, font_file,
                 rect_height=RECT_HEIGHT, 
                 rect_width=RECT_WIDTH, 
                 byte_count_per_row=BYTE_COUNT_PER_ROW):
        self.font_file = font_file
        self.rect_height = rect_height
        self.rect_width = rect_width
        self.byte_count_per_row = byte_count_per_row

    def init_rect_list(self):
        rect_list = [] * RECT_HEIGHT

        for i in range(RECT_HEIGHT):
            rect_list.append([] * RECT_WIDTH)
        return rect_list

    def get_font_area_index(self, txt, encoding='utf-8'):
        if not isinstance(txt, unicode):
            txt = txt.decode(encoding)

        gb2312 = txt.encode('gb2312')
        hex_str = binascii.b2a_hex(gb2312)

        area = eval('0x' + hex_str[:2]) - 0xA0
        index = eval('0x' + hex_str[2:]) - 0xA0

        return area, index

    def get_font_rect(self, area, index):
        offset = (94 * (area-1) + (index-1)) * BYTE_COUNT_PER_FONT
        btxt = None

        with open(self.font_file, "rb") as f:
            f.seek(offset)
            btxt = f.read(BYTE_COUNT_PER_FONT)

        return btxt

    def convert_font_rect(self, font_rect, rect_list, ft=1, ff=0):
        for k in range(len(font_rect) / self.byte_count_per_row):
            row_list = rect_list[k]
            for j in range(self.byte_count_per_row):
                for i in range(8):
                    asc = binascii.b2a_hex(font_rect[k * self.byte_count_per_row + j])
                    asc = eval('0x' + asc)
                    flag = asc & KEYS[i]
                    row_list.append(flag and ft or ff)
        return rect_list

    def render_font_rect(self, rect_list=None):
        if not rect_list:
            rect_list = self.rect_list

        for row in rect_list:
            for i in row:
                if i:
                    print '■',
                else:
                    print '.',
            print ''
        print ''

    def rect_list_simi(self, rect_list1, rect_list2):
        common_cnt = 0
        for r in range(RECT_WIDTH):
            for c in range(RECT_HEIGHT):
                if rect_list1[r][c] == rect_list2[r][c]:
                    common_cnt = common_cnt + 1
        return common_cnt * 1.0 / RECT_HEIGHT / RECT_WIDTH

    def convert(self, text, ft=None, ff=None, encoding='utf-8'):
        if not isinstance(text, unicode):
            text = text.decode(encoding)
        area, index = self.get_font_area_index(text)
        font_rect = self.get_font_rect(area, index)
        rect_list = self.init_rect_list()
        rect_list = self.convert_font_rect(font_rect, rect_list, ft=ft, ff=ff)
        return rect_list

    def simi(self, char1, char2, renderFlag=False):
        rect_list1 = self.convert(char1, ft=1, ff=0)
        rect_list2 = self.convert(char2, ft=1, ff=0)
        if renderFlag:
            self.render_font_rect(rect_list1)
            self.render_font_rect(rect_list2)
        return self.rect_list_simi(rect_list1, rect_list2)

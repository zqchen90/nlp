#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:43:40
# @Author  : zhaoqun.czq
# Calculate similarity based on character shape

import binascii
from math import exp
from rectangle_min_distance import RecMinDistance

RECT_HEIGHT = 16
RECT_WIDTH = 16
BYTE_COUNT_PER_ROW = RECT_WIDTH / 8
BYTE_COUNT_PER_FONT = BYTE_COUNT_PER_ROW * RECT_HEIGHT

KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

class FontSimi(object):
    def __init__(self, font_file='./data/hzk16h',
                 rect_height=RECT_HEIGHT, 
                 rect_width=RECT_WIDTH, 
                 byte_count_per_row=BYTE_COUNT_PER_ROW):
        self.font_file = font_file
        self.rect_height = rect_height
        self.rect_width = rect_width
        self.byte_count_per_row = byte_count_per_row
        self.recMinDistance = RecMinDistance()

    def initRectList(self):
        rect_list = [] * RECT_HEIGHT

        for i in range(RECT_HEIGHT):
            rect_list.append([] * RECT_WIDTH)
        return rect_list

    def getFontAreaIndex(self, txt, encoding='utf-8'):
        if not isinstance(txt, unicode):
            txt = txt.decode(encoding)

        gb2312 = txt.encode('gb2312')
        hex_str = binascii.b2a_hex(gb2312)

        area = eval('0x' + hex_str[:2]) - 0xA0
        index = eval('0x' + hex_str[2:]) - 0xA0

        return area, index

    def getFontRect(self, area, index):
        offset = (94 * (area-1) + (index-1)) * BYTE_COUNT_PER_FONT
        btxt = None

        with open(self.font_file, "rb") as f:
            f.seek(offset)
            btxt = f.read(BYTE_COUNT_PER_FONT)

        return btxt

    def convertFontRect(self, font_rect, rect_list, ft=1, ff=0):
        for k in range(len(font_rect) / self.byte_count_per_row):
            row_list = rect_list[k]
            for j in range(self.byte_count_per_row):
                for i in range(8):
                    asc = binascii.b2a_hex(font_rect[k * self.byte_count_per_row + j])
                    asc = eval('0x' + asc)
                    flag = asc & KEYS[i]
                    row_list.append(flag and ft or ff)
        return rect_list

    def renderFontRect(self, rect_list=None):
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

    def rectListSimi(self, rect_list1, rect_list2, simi_type):
      common_cnt = 0
      common_one_cnt = 0
      total_one_cnt = 0
      simi = 0.0
      
      for r in range(RECT_WIDTH):
        for c in range(RECT_HEIGHT):
          if 1 == rect_list1[r][c] or 1 == rect_list2[r][c]:
            total_one_cnt = total_one_cnt + 1
          if 1 == rect_list1[r][c] and 1 == rect_list2[r][c]:
            common_one_cnt = common_one_cnt + 1
          if rect_list1[r][c] == rect_list2[r][c]:
              common_cnt = common_cnt + 1

      if 'jaccard' == simi_type:
        simi = common_one_cnt * 1.0 / total_one_cnt
      elif 'mindistance' == simi_type:
        distance12 = self.recMinDistance.distance(rect_list1, rect_list2, RECT_WIDTH, RECT_HEIGHT)
        distance21 = self.recMinDistance.distance(rect_list2, rect_list1, RECT_WIDTH, RECT_HEIGHT)
        simi = exp(-1 * max(distance12, distance21))
      else:
        simi = common_cnt * 1.0 / RECT_HEIGHT / RECT_WIDTH
      return simi

    def convert(self, text, ft=None, ff=None, encoding='utf-8'):
        if not isinstance(text, unicode):
            text = text.decode(encoding)
        area, index = self.getFontAreaIndex(text)
        font_rect = self.getFontRect(area, index)
        rect_list = self.initRectList()
        rect_list = self.convertFontRect(font_rect, rect_list, ft=ft, ff=ff)
        return rect_list

    def simi(self, char1, char2, simi_type = 'default', renderFlag=False):
        rect_list1 = self.convert(char1, ft=1, ff=0)
        rect_list2 = self.convert(char2, ft=1, ff=0)
        if renderFlag:
            self.renderFontRect(rect_list1)
            self.renderFontRect(rect_list2)
        return self.rectListSimi(rect_list1, rect_list2, simi_type)

if __name__ == '__main__':
    fs = FontSimi()
    print fs.simi(u'入', u'八', 'jaccard', True)
    print fs.simi(u'入', u'八', 'default', False)
    print fs.simi(u'入', u'八', 'mindistance', False)
    
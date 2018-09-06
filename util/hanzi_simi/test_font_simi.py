#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:51:47
# @Author  : zhaoqun.czq

from font_simi import FontSimi

def test():
  fs = FontSimi('./data/hzk16h')
  simiThreshold = 0.7

  testCases = [[u'杨', u'扬', True],[u'洒', u'酒', True],[u'大', u'太', True],[u'无', u'尤', True],[u'手', u'乎', True]
    ,[u'征', u'证', True], [u'光', u'先', True], [u'贵', u'费', True], [u'辩', u'辨', True]]
  for [char1, char2, simiFlag] in testCases:
    simi = fs.simi(char1, char2)
    assert(simiFlag == (simi >= simiThreshold))

if __name__ == '__main__':
  test()

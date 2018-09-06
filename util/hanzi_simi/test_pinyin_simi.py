#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 17:02:09
# @Author  : zhaoqun.czq

from pinyin_simi import PinyinSimi

def test():
  ps = PinyinSimi()

  simiThreshold = 0.9

  testCases = [
    [u'杨', u'扬', True], [u'杨', u'验', True], [u'转', u'钻', True], 
    [u'劈', u'辟', True], [u'装', u'钻', False], [u'装', u'呀', False]
  ]
  for [char1, char2, simiFlag] in testCases:
    simi = ps.simi(char1, char2)
    print '%s %s %2.2f' %(char1, char2, simi)
    assert(simiFlag == (simi >= simiThreshold))

if __name__ == '__main__':
  test()

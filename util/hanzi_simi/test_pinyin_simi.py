#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 17:02:09
# @Author  : zhaoqun.czq

from pinyin_simi import PinyinSimi

def test():
  ps = PinyinSimi()

  testCases = [
    [u'杨', u'扬', 1], [u'杨', u'验', 0.75], [u'转', u'钻', 0.8], 
    [u'劈', u'辟', 1], [u'装', u'呀', 0.17], [u'装', u'钻', 0.67]
  ]
  for [char1, char2, targetSimi] in testCases:
    simi = ps.simi(char1, char2)
    print '%s(%s) %s(%s) %2.2f' %(char1, ps.getPinyin(char1), char2, ps.getPinyin(char2), simi)
    assert(0.01 >= abs(targetSimi - simi))

if __name__ == '__main__':
  test()

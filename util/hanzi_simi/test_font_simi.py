#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:51:47
# @Author  : zhaoqun.czq

from font_simi import FontSimi

def testFontSimi():
  fs = FontSimi()
  simiThreshold = 0.7

  testCases = [
    [u'杨', u'扬', True],[u'洒', u'酒', True],[u'大', u'太', True],
    [u'征', u'证', True], [u'光', u'先', True], [u'辩', u'辨', True],
    [u'嬴', u'羸', True], [u'征', u'羸', False],
  ]
  passCnt = 0

  print 'char1 char2 simi default_simi jaccard_simi'
  for [char1, char2, simiFlag] in testCases:
    defaultsimi = fs.simi(char1, char2)
    jaccardSimi = fs.simi(char1, char2, 'jaccard')
    simi = (defaultsimi+jaccardSimi)/2
    print '%s %s %2.2f %2.2f %2.2f' %(char1, char2, simi, defaultsimi, jaccardSimi)
    if simiFlag == (simi >= simiThreshold):
      passCnt = passCnt + 1

  print '\nResult:\n  test case: %d\n  pass rate: %2.3f' %(len(testCases), 1.0 * passCnt / len(testCases))

if __name__ == '__main__':
  test()

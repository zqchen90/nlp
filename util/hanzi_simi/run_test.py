#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:51:47
# @Author  : zhaoqun.czq

from font_simi import FontSimi
from pinyin_simi import PinyinSimi
from hanzi_simi import HanziSimi

def testPinyin():
  print 'Now begin to test Pinyin Simi'
  ps = PinyinSimi()

  testCases = [
    [u'杨', u'扬', 1], [u'杨', u'验', 0.75], [u'转', u'钻', 0.8], 
    [u'劈', u'辟', 1], [u'装', u'呀', 0.17], [u'装', u'钻', 0.67]
  ]
  for [char1, char2, targetSimi] in testCases:
    simi = ps.simi(char1, char2)
    print '%s(%s) %s(%s) %2.2f' %(char1, ps.getPinyin(char1), char2, ps.getPinyin(char2), simi)
    assert(0.01 >= abs(targetSimi - simi))

def testFontSimi():
  fs = FontSimi()
  simiThreshold = 0.9

  testCases = [
    [u'杨', u'扬', True],[u'洒', u'酒', True],[u'大', u'太', True],
    [u'征', u'证', True], [u'光', u'先', True], [u'辩', u'辨', True],
    [u'嬴', u'羸', True], [u'征', u'羸', False],[u'大', u'辨', True]
  ]
  for [char1, char2, simiFlag] in testCases:
    defaultsimi = fs.simi(char1, char2)
    jaccardSimi = fs.simi(char1, char2, 'jaccard')
    simi = (defaultsimi+jaccardSimi)/2
    print '%s %s %2.2f %2.2f %2.2f' %(char1, char2, simi, defaultsimi, jaccardSimi)
    assert(simiFlag == (simi >= simiThreshold))

def evaluate():
  print 'Now begin to evaluate'
  
  cases = []

  with open('./data/gaokao_char_uniq_filter.txt', 'r') as fin:
    for line in fin.readlines():
      [flag, char1, char2] = line.strip().decode('utf8').split(',')
      cases.append([char1, char2, flag == '1'])

  print 'Load %s cases' %(len(cases))

  hanziSimi = HanziSimi()

  simiResult = []
  positiveCnt = 0
  negativeCnt = 0
  for case in cases:
    char1 = case[0]
    char2 = case[1]
    flag = case[2]
    simiResult.append([char1, char2, flag, hanziSimi.simi(char1, char2)])
    if flag:
      positiveCnt = positiveCnt + 1
    else:
      negativeCnt = negativeCnt + 1

  print 'Simi calculation done'

  simiStart = 0.4
  simiEnd = 1.0
  simiStep = 0.05
  simiThreshold = simiStart

  result = ['simi recall precision f1']
  badcases = {'FN': [], 'FP': []}
  print 'Search for best threshold'

  while simiThreshold <= simiEnd:
    print '  simi threshold=%2.2f' %simiThreshold
    TPCnt = 0
    FPCnt = 0
    TNCnt = 0
    FNCnt = 0
    for case in simiResult:
      simi = case[3]
      flag = case[2]
      if flag:
        if simi >= simiThreshold:
          TPCnt = TPCnt + 1
        else:
          FNCnt = FNCnt + 1
      else:
        if simi >= simiThreshold:
          FPCnt = FPCnt + 1
        else:
          TNCnt = TNCnt + 1
    
    if 0 == TPCnt + FNCnt or 0 == TPCnt + FPCnt:
      break
    recall = 1.0 * TPCnt / (TPCnt + FNCnt)
    precision = 1.0 * TPCnt / (TPCnt + FPCnt)
    f1 = 2.0 * recall * precision / (recall + precision)
    if f1 > 0.7:
      result.append('%2.2f %2.3f %2.3f %2.3f' %(simiThreshold, recall, precision, f1))
    simiThreshold = simiThreshold + simiStep

  print '\nResult:\n%s' %('\n'.join(result))

if __name__ == '__main__':
  evaluate()

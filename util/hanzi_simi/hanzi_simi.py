#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-07 16:45:15
# @Author  : zhaoqun.czq

from pinyin_simi import PinyinSimi
from font_simi import FontSimi

class HanziSimi(object):
  def __init__(self):
    self.pinyinSimi = PinyinSimi()
    self.fontSimi = FontSimi()

  def getFontSimi(self, char1, char2):
    simiList =[]
    simiList.append(self.fontSimi.simi(char1, char2))
    simiList.append(self.fontSimi.simi(char1, char2, 'jaccard'))
    #simiList.append(self.fontSimi.simi(char1, char2, 'mindistance'))
    if max(simiList) >= 0.9:
      return max(simiList)
    else:
      return sum(simiList) / len(simiList)

  def getPinyinSimi(self, char1, char2):
    return self.pinyinSimi.simi(char1, char2)

  def simi(self, char1, char2):
    return max([
        self.getFontSimi(char1, char2), 
        self.getPinyinSimi(char1, char2)
    ])
    
if __name__ == '__main__':
  hanziSimi = HanziSimi()
  print hanziSimi.simi(u'入', u'八')
  print hanziSimi.simi(u'洒', u'酒')
  print hanziSimi.simi(u'啦', u'酒')
  print hanziSimi.simi(u'就', u'酒')
  
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 16:44:06
# @Author  : zhaoqun.czq
# Calculate similarity based on character pinyin

from xpinyin import Pinyin
from difflib import SequenceMatcher

class PinyinSimi(object):
  def __init__(self):
    self.pinyin = Pinyin()

  def getPinyin(self, char):
    return self.pinyin.get_pinyin(char)

  def getLevenDistance(self, str1, str2):
   leven_cost = 0
   s = SequenceMatcher(None, str1, str2)
   for tag, i1, i2, j1, j2 in s.get_opcodes():
       if tag == 'replace':
           leven_cost += max(i2-i1, j2-j1)
       elif tag == 'insert':
           leven_cost += (j2-j1)
       elif tag == 'delete':
           leven_cost += (i2-i1)
   return leven_cost

  def simi(self, char1, char2):
    pinyin1 = self.getPinyin(char1)
    pinyin2 = self.getPinyin(char2)
    levenDistance = self.getLevenDistance(pinyin1, pinyin2)
    if levenDistance <= 1:
      return 1.0
    else:
      return 0.0 

    # simi = 1 - 1.0 * levenDistance / max(len(pinyin1), len(pinyin2))

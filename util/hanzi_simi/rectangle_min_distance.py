#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-10 16:59:58
# @Author  : zhaoqun.czq

DEBUG = False

class RecMinDistance(object):
  def findElementNearBy(self, rec, row, col, target):
    curRow = row
    curCol = col
    maxRow = len(rec)
    maxCol = len(rec[0])
    if DEBUG:
      print 'findElementNearBy row: %d, col: %d, maxRow: %d, maxCol: %d' %(row, col, maxRow, maxCol)
    minDistance = maxRow + maxCol - 2
    for step in range(max(maxRow, maxCol)):
      for curRow in range(max(0, row - step), min(maxRow, row + step + 1)):
        for curCol in range(max(0, col - step), min(maxCol, col + step + 1)):
          if DEBUG:
            print 'step: %d, curRow: %d, curCol: %d, row: %d, col: %d' %(step, curRow, curCol, row, col)
          if rec[curRow][curCol] == target:
            if DEBUG:
              print 'find target at row: %d, col: %d' %(curRow, curCol)
            dist = abs(curRow - row) + abs(curCol - col)
            if dist < minDistance:
              minDistance = dist
    if DEBUG:
      print 'min distance: %d' %(minDistance)
    return minDistance

  def distance(self, rec1, rec2, width, height):
    # print 'recMinDistance width: %d, height: %d' %(width, height)
    MAX_DISTANCE = width + height - 2
    distanceList = []
    for r in range(width):
      for c in range(height):
        if 1 == rec1[r][c]:
          dist = self.findElementNearBy(rec2, r, c, 1)
          if DEBUG:
            print 'recMinDistance find 1 in rec1 r: %d, c: %d, min distance in rec2 %d' %(r, c, dist)
          distanceList.append(dist)
    return sum(distanceList) * 1.0 / len(distanceList)

def testRecMinDistance(rec1, rec2, minDistance):
  recMinDistance = RecMinDistance()
  print '\nTest recMinDistance: '
  print rec1
  print rec2
  assert(len(rec1) == len(rec2))
  assert(len(rec1[0]) == len(rec2[0]))
  ret = recMinDistance.distance(rec1, rec2, len(rec1[0]), len(rec1))
  print 'actual: %2.1f expect: %2.1f' %(ret, minDistance)
  assert(abs(minDistance - ret) < 0.01)

def main():
  testRecMinDistance([[1,0],[0,0]], [[1,0],[0,0]], 0)
  testRecMinDistance([[1,0],[0,0]], [[0,0],[0,1]], 2)
  testRecMinDistance([[1,0,0],[1,0,0],[1,0,0]], [[0,1,0],[0,1,0],[0,1,0]], 1)
  testRecMinDistance([[1,0,0],[1,0,0],[1,0,0]], [[0,0,0],[1,1,1],[0,0,0]], 2.0/3.0)

if __name__ == '__main__':
  main()
  
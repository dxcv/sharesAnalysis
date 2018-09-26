# -*- coding:utf-8 -*-
import sys,os
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf
from sharesAnalysis.clcore import Stokes,k2strokes

'''
线段处理逻辑:
	把笔按以下方式进行处理
	0. 起始线段处理，如果不成立即遇到笔破坏,并且其后形成的线段与起笔是相悖的，则起笔不成立
	1. 按至少三笔成线段原则处理
	2. 按奇数笔成线段原则处理
	3. 按两种情况处理
	4. 第一种情况，1,2特征元素之间不存在缺口
	5. 第二种情况，1,2特征元素之间存在缺口
'''
def isLine(dirction,begin,end):
	print(dirction,'\n',begin,end)
	b = begin['最高价'] if dirction == '向下' else begin['最低价']
	e = begin['最低价'] if dirction == '向下' else begin['最高价']
	r = True if (dirction == '向下' and b>=e) or (dirction == '向上' and b<=e) else False
	return r


def drawLine():
	pass

def s_standry():
	pass
def s_inclusion():
	pass

def deal_line(strokesList):
	idx = 0
	# 1. 确定起笔
	#   如果三笔现成的一段，方向与第一笔是相悖的，说明起笔不对
	ret = isLine( strokesList[0].direction,strokesList[0].begin,strokesList[2].end )
	print(ret)


	# 2.特征序列标准化（包含处理）后连线

	# 3. 处理待确认的线段

	pass

def test_01():
	import pickle
	output = open('F:\\data\\log\\600000\\strokesList.pk', 'rb')
	strokesList = pickle.load(output)
	#Stokes()
	print(strokesList[0])
	deal_line(strokesList)

if __name__ == '__main__':
	import os
	import sys
	test_01()

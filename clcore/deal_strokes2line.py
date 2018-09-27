# -*- coding:utf-8 -*-
import sys,os
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf
from sharesAnalysis.clcore import Stokes,k2strokes
from sharesAnalysis.clcore import Line

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

def isLine(dirction,begin,end, dirctionType='顶底分型'):
	'''
	功能: 判断是否成线段
	:param dirction:
	:param begin:
	:param end:
	:param dirctionType: 默认是顶分型-底分型（底分型-顶分型）、同向分型
	:return:
	'''
	print(dirction,'\n',begin,end)
	if dirctionType == '顶底分型':
		b = begin['最高价'] if dirction == '向下' else begin['最低价']
	else:
		b = begin['最低价'] if dirction == '向下' else begin['最高价']

	e = end['最低价'] if dirction == '向下' else end['最高价']
	r = True if (dirction == '向下' and b>=e) or (dirction == '向上' and b<=e) else False
	return r

def isLineBySameType(dirction,begin,end):
	print(dirction,'\n',begin,end)
	b = begin['最低价'] if dirction == '向下' else begin['最高价']
	e = end['最低价'] if dirction == '向下' else end['最高价']
	r = True if (dirction == '向下' and b>=e) or (dirction == '向上' and b<=e) else False
	return r


def drawLine():
	pass

def s_standry():
	pass
def s_inclusion():
	pass

def dealStrokes2Line(strokesList):
	lineList=[]
	idx = 0
	# 1. 确定起笔
	#   如果三笔现成的一段，方向与第一笔是相悖的，说明起笔不对
	#ret1 = isLine( strokesList[0].direction,strokesList[0].begin,strokesList[2].end )
	#ret2 = isLine( strokesList[0].direction,strokesList[0].end,strokesList[2].end, dirctionType='同向' )
	#print(ret2)

	# 如果第一线段规则不成立，则认为第一笔为线段看待
	#if not(ret1 and ret2):
		#l = Line(strokesList[0].begin, strokesList[0].end,strokesList[0].direction)
		#lineList.append(l)

	#1. 预设第一笔为线段，线段类型为笔
	l = Line(strokesList[0].begin, strokesList[0].end,strokesList[0].direction)
	lineList.append(l)

	print(lineList[0])
	# 2.特征序列标准化（包含处理）后连线
	cnt = len(strokesList)-1
	while idx < cnt:
		# 取出3笔
		s3 = strokesList[idx:idx+3]
		# 判断是否构成线段、包含关系是否成立

		# 成立包含关系

		# 线段延续

		# 新线段成立

		idx += 1

	# 3. 处理待确认的线段

def test_01():
	import pickle
	output = open('F:\\data\\log\\600000\\strokesList.pk', 'rb')
	strokesList = pickle.load(output)
	print(strokesList[0])
	dealStrokes2Line(strokesList)

if __name__ == '__main__':
	import sys
	test_01()

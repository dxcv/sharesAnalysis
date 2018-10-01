# -*- coding:utf-8 -*-
import sys,os
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf
from sharesAnalysis.clcore import Strokes,k2strokes
from sharesAnalysis.clcore import Line,LINE_TYPE,LINE_JUDGE
from dweunit.unit import log_error, log_warning, log_debug, log_info
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
# 成线段
def isLine1(s3):
	# 1. 明显不成为一段的（存在缺口情况）
	pass

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

# 缺口判断
def s_gap( strokes_now:Strokes, line_befor:Line==None ):
	'''
	按三种情况对笔缺口进行判断
	:param strokes_now:
	:param line_befor:
	:return: True 存在缺口,False 不存在缺口
	'''
	#1. 如果当前判断点之前没有笔
	# 按存在缺口处理
	if line_befor is None:
		pass

	#2. 如果当前判断点之前为只有一笔
	# 当前一笔不能够包住前一笔，则认为是存在缺口
	elif LINE_TYPE[line_befor.lineType] == LINE_TYPE['笔']:
		pass

	#3. 如果当前判断带你之前为线段
	# 按标准缺口判断处理
	elif LINE_TYPE[line_befor.lineType] == LINE_TYPE['线段']:
		pass
	else:
		log_error( '线段类型设置有问题 line.type:%s' % str(line_befor.lineType) )
		raise('线段类型设置有问题')

# 分型、包含关系
def s_judge(ld,rd):
	pass

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
	ret1 = isLine( strokesList[0].direction,strokesList[0].begin,strokesList[2].end )
	ret2 = isLine( strokesList[0].direction,strokesList[0].end,strokesList[2].end, dirctionType='同向' )
	#print(ret2)

	# 如果第一线段规则不成立，则认为第一笔为线段看待
	if not(ret1 and ret2):
		l = Line(strokesList[0].begin, strokesList[0].end,strokesList[0].direction, '笔')
		idx = 1
	else:
		l = Line(strokesList[0].begin, strokesList[2].end,strokesList[0].direction,'线段')
		idx = 2
	lineList.append(l)

	#1. 预设第一笔为线段，线段类型为笔
	l = Line(strokesList[0].begin, strokesList[0].end,strokesList[0].direction)
	lineList.append(l)

	print(lineList[0])
	# 2.特征序列标准化（包含处理）后连线
	# 判断是否构成线段、包含关系是否成立
	# 成立包含关系
	# 线段延续
	# 新线段成立
	cnt 			= len(strokesList)-idx
	curJudge		= LINE_JUDGE['启动']
	nextStrokesList	=[]
	while idx < cnt:
		# 取出3笔
		s3 = strokesList[idx:idx+3]
		idx +=1

		# 缺口判断 属于下一个线段的初始入口位置
		if LINE_JUDGE[curJudge] == LINE_JUDGE['启动'] or LINE_JUDGE[curJudge] == LINE_JUDGE['判断缺口']:
			line_b 	= None if len(lineList) ==0 else lineList[-1]
			gap 	= s_gap(s3[0], line_b)
			curJudge= '第一种情况' if gap else '第二种情况'

			#重置下一线段的笔list
			nextStrokesList=[s3[0]]

			continue

		# 优先判断是否存在包含关系
		else:
			#isIn= s_judge()
			#if isIn:
			#	continue
			pass

		# 如果当前一笔与前一线段方向相同，判断是否延续，否则判断反方向分型是否成立
		if LINE_JUDGE[curJudge] == LINE_JUDGE['第一种情况']:
			print('第一种情况')
			pass

		elif LINE_JUDGE[curJudge] == LINE_JUDGE['第二种情况']:
			print('第二种情况')

		#idx += 1

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

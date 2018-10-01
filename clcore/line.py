# -*- coding:utf-8 -*-
'''
class LineType:
	def __init__(self):
		self.tp1 ={
			'笔':'笔',
			'线段':'线段',
			0:'笔',
			1:'线段',
		}
	def __getitem__(self, k):
		return self.tp1[k]
'''

LINE_JUDGE={
	'启动' : '启动',
	'判断缺口' : '判断缺口',
	'第一种情况' : '第一种情况',
	'第二种情况' : '第二种情况',
	'线段延续' : '线段延续',
}

LINE_TYPE= {
	0:'笔',
	1:'线段',

	'笔':'笔',
	'线段':'线段',
}
class Line:
	def __init__(self, begin, end, direction,lineType='线段'):
		self.begin 	= begin
		self.end 	= end
		self.status	= '待确认' # 待确认、确认
		self.lineType = lineType# 笔、线段     #、准线段
		self.direction = direction
		self.strokesList = []

	def __str__(self):
		return ('%s ~~ %s,%s, 线段类型:%s' % ( self.begin['日期'], self.end['日期'],
			self.direction, self.lineType))

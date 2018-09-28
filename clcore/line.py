# -*- coding:utf-8 -*-

class Line:
	def __init__(self, begin, end, direction,lineType='线段'):
		self.begin 	= begin
		self.end 	= end
		self.status	= '待确认' # 待确认、确认
		self.lineType= lineType# 笔、线段     #、准线段
		self.direction = direction

	def __str__(self):
		return ('%s ~~ %s,%s, 线段类型:%s' % ( self.begin['日期'], self.end['日期'],
			self.direction, self.lineType))

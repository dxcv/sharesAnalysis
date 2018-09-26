# -*- coding:utf-8 -*-

class Line:
	def __init__(self, begin, end, direction):
		self.begin 	= begin
		self.end 	= end
		self.status	= '待确认'
		self.direction = direction

	def __str__(self):
		return ('%s-%s,%s' % ( self.begin['日期'], self.end['日期'],
			self.direction))

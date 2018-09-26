# -*- coding:utf-8 -*-

class Stokes:
	def __init__(self, begin, end, status='正常一笔', isContinue='未延笔', reDeal='未重处理'):
		self.begin = begin
		self.end = end
		self.status = status
		self.isContinue = isContinue  # 是否被下一笔破坏而确定
		self.reDeal = reDeal
		self.direction = '向下' if self.begin['关系'] =='顶分型' else '向上'

	def __str__(self):
		return ('%s-%s, %s, %s 笔方向:%s' % ( self.begin['日期'], self.end['日期'],
			self.status, self.isContinue, self.direction))
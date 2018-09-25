# -*- coding:utf-8 -*-
import configparser

class Config:
	confdict = {}

	def __init__(self,confPath="D:\\分析系统\\sharesAnalysis\\conf\\config.ini",encoding='utf-8'):
		self.conf = configparser.ConfigParser()
		self.conf.read(confPath,encoding=encoding)


		self.setconfig('基础', '项目目录')

	def setconfig(self,m,s):
		if m not in self.confdict:
			self.confdict[m] = {}
		self.confdict[m][s] = self.conf.get('基础', '项目目录')

	def __getitem__(self,m):
		return self.confdict[m]

conf = Config()

if __name__ == '__main__':
	c = Config()
	print( c['基础']['项目目录'] )

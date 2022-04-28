#coding=utf-8
import os
import rumps
from MCLib_DB import DataBase
from MCLib_BarAPP import MenuBarApp

if __name__ == '__main__':
	PATH = rumps.application_support('MyCaseLib')
	DB_NAME = 'DB_MyCaseLib.db'
	DB_PATH = os.path.join(PATH, DB_NAME)
	DB = DataBase(PATH, DB_NAME, DB_PATH)

	bar_app = MenuBarApp(DB, DB_PATH)
	bar_app.run()


#coding=utf-8
import os
import sys

from MCLib_DB import DataBase
from MCLib_Main_Window import ui_main
from PyQt6.QtWidgets import QApplication

if os.name == 'posix':
	from AppKit import NSSearchPathForDirectoriesInDomains

if __name__ == '__main__':
	if os.name == 'posix':
		PATH = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, 1).objectAtIndex_(0), 'MyCaseLib')
	else:
		PATH = os.path.join(os.path.abspath('.'), 'MCLib')
	if not os.path.isdir(PATH):
		os.mkdir(PATH)
		
	DB_NAME = 'DB_MyCaseLib.db'
	DB_PATH = os.path.join(PATH, DB_NAME)
	DB = DataBase(PATH, DB_NAME, DB_PATH)
	SETTING_PATH = os.path.join(PATH, 'SETTING_MyCaseLib')
	VERSION = 'v 1.0'
	
	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(False)
	window_main = ui_main(DB = DB, DB_PATH = DB_PATH, VERSION = VERSION, SETTING_PATH = SETTING_PATH)

	window_main.show()
	sys.exit(app.exec())


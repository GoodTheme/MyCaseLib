#coding=utf-8
import os
import sys
from MCLib_Main import ui_main
from MCLib_DB import DataBase
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
	PATH = os.path.join(os.path.abspath('.'), 'MCLib')
	if not os.path.exists(PATH):
		os.makedirs(PATH)
	DB_NAME = 'DB_MyCaseLib'
	DB_PATH = os.path.join(PATH, DB_NAME)
	DB = DataBase(PATH, DB_NAME, DB_PATH)

	app = QApplication(sys.argv)
	window_main = ui_main(DB, DB_PATH)
	window_main.show()
	sys.exit(app.exec_())
	

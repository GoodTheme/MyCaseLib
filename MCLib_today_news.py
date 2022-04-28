# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MCLib_widgets_UI import Ui_today_news_window

class ui_today_news(QDialog, Ui_today_news_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, parent = None):
		super(ui_today_news, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.message_view.setStyleSheet('background-color: rgb(255,255,255,150);')
		self.message_view.setHtml(self.DB.generate_report_html())

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()


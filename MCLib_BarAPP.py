#coding=utf-8
import rumps
import subprocess
import sys
import time
from datetime import datetime, timedelta
from MCLib_Main_Window import ui_main
from functools import partial
from PyQt5.QtWidgets import QApplication
from AppKit import NSApp, NSApplicationActivationPolicyRegular

class MenuBarApp(rumps.App):
	def __init__(self, DB, DB_PATH):
		self.NAME = 'MyCaseLib'
		self.TITLE = 'C'
		self.QUIT = '关闭'
		self.DB = DB
		self.DB_PATH = DB_PATH
		super(MenuBarApp, self).__init__(name = self.NAME, quit_button = None, 
			icon = 'MCLib_Bar_icon.png', template = True)
		self.app = rumps.App(name = self.NAME)
		self.at_start()

	def at_start(self):
		self.start_event = rumps.Timer(callback = self.start_main, interval = 1)
		self.start_event.start()

	def start_main(self, _):
		self.start_event.stop()
		self.app = QApplication(sys.argv)
		self.window_main = ui_main(DB = self.DB, DB_PATH = self.DB_PATH)
		self.window_main.show()
		self.create_menu()
		NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
		sys.exit(self.app.exec_())

	def show_main_window(self, _):
		NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
		self.window_main.show()
		self.window_main.raise_()
		sys.exit(self.app.exec_())

	def show_today_news(self, _):
		self.window_main.show_today_news()
		sys.exit(self.app.exec_())

	def do_init(self, _):
		self.window_main.do_init()

	def back_up(self, _):
		self.window_main.back_up()

	def restore(self, _):
		self.window_main.restore()

	def change_default_path(self, _):
		self.window_main.change_default_path()

	def change_color(self, flag, _):
		self.window_main.change_color(flag)

	def show_about(self, _):
		self.window_main.show_about()

	def menu_refresh(self, _):
		self.create_menu()

	def quit(self, _):
		self.window_main.close()
		rumps.quit_application()

	def create_menu(self):
		self.menu.clear()
		new_menu = [rumps.MenuItem("主界面", callback = self.show_main_window)]
		new_menu.append(rumps.MenuItem("今日简报", callback = self.show_today_news))
		new_menu.append(None)
		
		order_dict = {'添加时间（正序）': 'id asc', 
		'添加时间（倒序）': 'id desc',  
		'标签（时间-正）': 'label, id asc', '标签（时间-倒）': 'label, id desc'}
		by_order = order_dict[self.DB.select('profile', 'value')[0]['value']]
		project_list = self.DB.select_by_order('project_list', 'project_name, label', by_order)

		menu = [rumps.MenuItem("项目文件夹")]
		sub_menu = [rumps.MenuItem("更新列表..", callback = self.menu_refresh)]
		sub_menu.append(None)

		for project in project_list:
			if project['label'] in '01':
				sub_menu.append(rumps.MenuItem(project['project_name'], 
					callback = partial(self.open_file, project['project_name'])))
		menu.append(sub_menu)
		new_menu.append(menu)
		new_menu.append(None)

		menu = [rumps.MenuItem("配置")]
		sub_menu = [rumps.MenuItem("默认项目文件夹", callback = self.change_default_path)]
		sub_menu.append(None)
		sub_menu.append(rumps.MenuItem("配色-今日简报", callback = partial(self.change_color, 2)))
		sub_menu.append(rumps.MenuItem("配色-项目信息", callback = partial(self.change_color, 0)))
		sub_menu.append(rumps.MenuItem("配色-案件信息", callback = partial(self.change_color, 1)))
		sub_menu.append(None)
		sub_menu.append(rumps.MenuItem("初始化", callback = self.do_init))
		sub_menu.append(rumps.MenuItem("备份", callback = self.back_up))
		sub_menu.append(rumps.MenuItem("还原", callback = self.restore))
		menu.append(sub_menu)
		new_menu.append(menu)

		new_menu.append(rumps.MenuItem(self.QUIT, callback = self.quit))
		self.menu.update(new_menu)

	def open_file(self, project_name, _):
		if self.DB.select('project_list', 'file_path', 'project_name', project_name):
			project_path = self.DB.select('project_list', 'file_path', 'project_name', 
				project_name)[0]['file_path']
			if project_path:
				subprocess.call(["open",project_path])



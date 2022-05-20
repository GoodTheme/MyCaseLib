#coding=utf-8
import os
import sys
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial, reduce
from datetime import datetime
from shutil import copyfile

from MCLib_UI import Ui_MainWindow
from MCLib_widgets import *

class ui_main(QMainWindow, Ui_MainWindow):
	def __init__(self, DB, DB_PATH, parent = None):
		super(ui_main, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle('MyCaseLib 案件管理')
		self.DB = DB
		self.DB_PATH = DB_PATH
		self.setWindowIcon(QtGui.QIcon('MCLib_icon.png'))
		self.version = 'v 0.1b'
		try:
			self.init()
		except:
			reply = QMessageBox.critical(self, "错误", "是否删除全部数据并初始化？", 
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.init()
				self.init()

	# 主界面初始
	def init(self):
		self.read_profile()
		self.label_init()
		self.p_c_tree_init()
		self.case_things_init()
		self.main_menu_init()

	def closeEvent(self, event):
		pass

	def read_profile(self):
		self.p_c_order, self.default_filepath = [x['value'] for x in self.DB.select('profile', 'value')][0:2]
		
	def p_c_tree_init(self):
		self.search_box.addItems(['全部', '信息', '待办', '记录', '记事'])
		self.search_bar.textChanged.connect(self.search_result)
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)
		self.p_c_treeview.customContextMenuRequested.connect(self.p_c_showmenu)
		self.p_c_treeview.itemDoubleClicked.connect(self.open_file)
		self.p_c_treeview.setExpandsOnDoubleClick(False)
		self.p_c_tree_refresh()

	def main_menu_init(self):
		self.menu_today_news.triggered.connect(self.show_today_news)
		self.menu_about.triggered.connect(self.show_about)
		self.menu_default_filepath.triggered.connect(self.change_default_path)
		self.menu_color_today.triggered.connect(partial(self.change_color, 2))
		self.menu_color_project.triggered.connect(partial(self.change_color, 0))
		self.menu_color_case.triggered.connect(partial(self.change_color, 1))
		self.menu_backup.triggered.connect(self.back_up)
		self.menu_restore.triggered.connect(self.restore)
		self.menu_init.triggered.connect(self.do_init)
		self.menu_close.triggered.connect(self.close)
		self.menu_manage_type_item.triggered.connect(self.show_manage_type)
		self.menu_manage_party_class.triggered.connect(partial(self.show_manage_party_contact, 'party'))
		self.menu_manage_contact_class.triggered.connect(partial(self.show_manage_party_contact, 'contact'))
		self.menu_parties.triggered.connect(partial(self.show_persons, 'party'))
		self.menu_contacts.triggered.connect(partial(self.show_persons, 'contact'))
		self.menu_new_project.triggered.connect(self.show_new_project)
		self.menu_new_case.triggered.connect(self.new_case)
		self.menu_delete_project.triggered.connect(self.delete_project)
		self.menu_delete_case.triggered.connect(self.delete_case)

	def case_things_init(self):
		self.todo_add_btn.clicked.connect(self.add_todo)
		self.event_add_btn.clicked.connect(self.add_event)
		self.todo_delete_btn.clicked.connect(self.delete_todo)
		self.event_delete_btn.clicked.connect(self.delete_event)
		self.to_event_btn.clicked.connect(self.to_event)
		self.things_menu()
		self.info_view.customContextMenuRequested.connect(self.case_info_showmenu)
		self.todo_view.customContextMenuRequested.connect(partial(self.things_showmenu, self.todo_menu))
		self.event_view.customContextMenuRequested.connect(partial(self.things_showmenu, self.event_menu))	

		self.todo_view.setHorizontalHeaderLabels(['日期', '事项', 'id'])
		self.todo_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.todo_view.setColumnHidden(2, True)
		self.todo_view.cellChanged.connect(self.edit_todo)
		self.todo_view.setSelectionBehavior(QTableWidget.SelectRows)

		self.event_view.setHorizontalHeaderLabels(['日期', '事项', 'id'])
		self.event_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.event_view.setColumnHidden(2, True)
		self.event_view.cellChanged.connect(self.edit_event)
		self.event_view.setSelectionBehavior(QTableWidget.SelectRows)

		self.notepad.textChanged.connect(self.notepad_input)

		for i in range(4):
			self.case_info_tab.setTabEnabled(i, False)
		self.case_info_tab.setCurrentIndex(0)

	def p_c_tree_menu(self, mark):
		self.p_c_menu = QMenu(self.p_c_treeview)

		if mark == 0:
			newAction = QAction('新的项目', self)
			newAction.triggered.connect(self.show_new_project)
			self.p_c_menu.addAction(newAction)

			self.p_c_menu.addSeparator()
			sub_menu = self.p_c_menu.addMenu('库..')
			sub_menu.setMinimumWidth(100)
			newAction = QAction('当事人', self)
			newAction.triggered.connect(partial(self.show_persons, 'party'))
			sub_menu.addAction(newAction)
			newAction = QAction('联系人', self)
			newAction.triggered.connect(partial(self.show_persons, 'contact'))
			sub_menu.addAction(newAction)

			sub_menu = self.p_c_menu.addMenu('模板..')
			sub_menu.setMinimumWidth(100)
			newAction = QAction('案件类型', self)
			newAction.triggered.connect(self.show_manage_type)
			sub_menu.addAction(newAction)
			sub_menu.addSeparator()
			newAction = QAction('当事人', self)
			newAction.triggered.connect(partial(self.show_manage_party_contact, 'party'))
			sub_menu.addAction(newAction)
			newAction = QAction('联系人', self)
			newAction.triggered.connect(partial(self.show_manage_party_contact, 'contact'))
			sub_menu.addAction(newAction)

			self.p_c_menu.addSeparator()
			sub_menu = self.p_c_menu.addMenu('排列顺序')
			sub_menu.setMinimumWidth(100)
			for s in ('添加时间（正序）', '添加时间（倒序）', '标签（时间-正）', '标签（时间-倒）'):
				newAction = QAction(s, self)
				newAction.triggered.connect(partial(self.change_by_order, s))
				sub_menu.addAction(newAction)


		elif mark == 1:
			newAction = QAction('从项目新建案件', self)
			newAction.triggered.connect(self.new_case)
			self.p_c_menu.addAction(newAction)
			self.p_c_menu.addSeparator()

			sub_menu = self.p_c_menu.addMenu('编辑项目')
			sub_menu.setMinimumWidth(100)
			newAction = QAction('变更项目名', self)
			newAction.triggered.connect(self.edit_project_name)
			sub_menu.addAction(newAction)
			newAction = QAction('变更项目号', self)
			newAction.triggered.connect(self.edit_project_num)
			sub_menu.addAction(newAction)
			newAction = QAction('变更项目文件夹', self)
			newAction.triggered.connect(self.edit_project_path)
			sub_menu.addAction(newAction)

			sub_menu = self.p_c_menu.addMenu('设置标签')
			sub_menu.setMinimumWidth(100)
			for i in range(5):
				current_project = self.p_c_treeview.currentIndex().data()
				current_label = self.DB.select('project_list', 'label', 'project_name', current_project)[0]['label']
				newAction = QAction(self.labels[i], self, checkable = True)
				if str(i) == current_label:
					newAction.setChecked(True)
				else:
					newAction.setChecked(False)
				newAction.triggered.connect(partial(self.set_label, i))
				sub_menu.addAction(newAction)
			sub_menu = self.p_c_menu.addMenu('排列顺序')
			sub_menu.setMinimumWidth(100)
			for s in ('添加时间（正序）', '添加时间（倒序）', '标签（时间-正）', '标签（时间-倒）'):
				newAction = QAction(s, self)
				newAction.triggered.connect(partial(self.change_by_order, s))
				sub_menu.addAction(newAction)
			self.p_c_menu.addSeparator()
			
			newAction = QAction('删除项目', self)
			newAction.triggered.connect(self.delete_project)
			self.p_c_menu.addAction(newAction)
			self.p_c_menu.addSeparator()

		elif mark == 2:
			sub_menu = self.p_c_menu.addMenu('编辑内容')
			sub_menu.setMinimumWidth(100)
			case = self.p_c_treeview.currentIndex().data()
			case_type = self.DB.select('case_list', 'case_type', 'case_name', case)[0]['case_type']
			items = self.DB.select('case_type', 'item, item_form', 'type_name', case_type)
			newAction = QAction("案件名", self)
			newAction.triggered.connect(partial(self.edit_case_name, case))
			sub_menu.addAction(newAction)
			for s in items:
				newAction = QAction(s['item'], self)
				newAction.triggered.connect(partial(self.edit_case_value, case, s['item'], s['item_form']))
				sub_menu.addAction(newAction)

			newAction = QAction('变更至项目', self)
			newAction.triggered.connect(self.change_project)
			self.p_c_menu.addAction(newAction)

			self.p_c_menu.addSeparator()
			newAction = QAction('删除案件', self)
			newAction.triggered.connect(self.delete_case)
			self.p_c_menu.addAction(newAction)

	# 第二窗口
	def close_widgets(self):
		self.p_c_tree_refresh()
		self.case_info_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def show_new_project(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		self.window_second = ui_new_project(DB = self.DB)
		self.window_second.show()
		self.window_second.close_signal.connect(self.close_widgets)

	def show_manage_type(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		self.window_second = ui_type_item_template(DB = self.DB)
		self.window_second.show()
		self.window_second.close_signal.connect(self.close_widgets)

	def show_manage_party_contact(self, which_type):
		self.window_second = ui_party_contact_template(DB = self.DB, which_type = which_type)
		self.window_second.show()
		self.window_second.close_signal.connect(self.case_info_refresh)

	def show_execute(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		self.window_second = ui_execute(DB = self.DB)
		self.window_second.show()
		self.window_second.close_signal.connect(self.close_widgets)

	def show_persons(self, which_type):
		self.window_second = ui_persons(DB = self.DB, which_type = which_type, flag = 0)
		self.window_second.show()
		self.window_second.close_signal.connect(self.case_info_refresh)

	def show_today_news(self):
		self.window_second = ui_today_news(DB = self.DB)
		self.window_second.show()
#		self.window_second.raise_()
#		self.window_second.activateWindow()

	def show_person_info(self, which_type, which_class, pid):
		self.window_second = ui_person_info(DB = self.DB, which_type = which_type, which_class = which_class, pid = pid, )
		self.window_second.show()

	def show_about(self):
		QMessageBox.about(self, 'MyCaseLib', f"MyCaseLib\n\n版本：{self.version}")

	# 案件列表
	def trans(self, s):
		if not s:
			return ''
		trans = ''
		for t in str(s):
			trans = trans + t if t != "'" else trans + "''"
		return trans

	def search_result(self):
		self.search_bar.textChanged.disconnect()
		keywords = self.search_bar.text()
		key_type = self.search_box.currentText()
		if keywords == 'showexecute':
			self.show_execute()
		elif keywords:
			self.p_c_tree_refresh(keywords, key_type)
		else:
			self.p_c_tree_refresh()
		self.search_bar.textChanged.connect(self.search_result)

	def p_c_tree_refresh(self, keywords = None, key_type = None):
		order_dict = {'添加时间（正序）': 'id asc', 
		'添加时间（倒序）': 'id desc',  
		'标签（时间-正）': 'label, id asc', '标签（时间-倒）': 'label, id desc'}
		by_order = order_dict[self.p_c_order]

		self.p_c_treeview.clear()
		self.p_c_treeview.setColumnCount(1)
		project_list = self.DB.select_by_order('project_list', 'project_name', by_order)
		for project in project_list:
			if keywords:
				case_selected = []
				if key_type == '全部' or key_type == '信息':
					case_list = self.DB.select('case_list', 'case_name', 'project_name', project['project_name'])
					for case in case_list:
						case_infos = self.DB.select_all('case_info', 'case_name', case['case_name'])
						flag = False
						if isinstance(case['case_name'], str) and case['case_name'].find(keywords) != -1:
							flag = True
						else:
							for t in case_infos:
								value_form = t['value_form']
								if value_form == 'text' and isinstance(t['value'], str) and t['value'].find(keywords) != -1:
									flag = True
								elif value_form == 'party' or value_form == 'contact':
									name = self.DB.select(f"{value_form}_info", 'value', 
											f"{value_form}_id" ,t['value2'])[0]['value']
									if isinstance(name, str) and name.find(keywords) != -1:
										flag = True								
						if flag and case not in case_selected:
							case_selected.append(case)

				if key_type == '全部' or key_type == '待办':
					todos = self.DB.select('todo_list', 'case_name, date, things', 
						'project_name', project['project_name'])
					for todo in todos:
						if (isinstance(todo['date'], str) and todo['date'].find(keywords) != -1) or (isinstance(todo['things'], str) and todo['things'].find(keywords) != -1):
							if {'case_name': todo['case_name']} not in case_selected:
								case_selected.append({'case_name': todo['case_name']})

				if key_type == '全部' or key_type == '记录':
					events = self.DB.select('event_list', 'case_name, date, things', 
						'project_name', project['project_name'])
					for event in events:
						if (isinstance(event['date'], str) and event['date'].find(keywords) != -1) or (isinstance(event['things'], str) and event['things'].find(keywords) != -1):
							if {'case_name': event['case_name']} not in case_selected:
								case_selected.append({'case_name': event['case_name']})

				if key_type == '全部' or key_type == '记事':
					notes = self.DB.select('case_list', 'case_name, notepad_text', 
						'project_name', project['project_name'])
					for note in notes:
						if isinstance(note['notepad_text'], str) and note['notepad_text'].find(keywords) != -1:
							if {'case_name': note['case_name']} not in case_selected:
								case_selected.append({'case_name': note['case_name']})

				if case_selected:
					root = QTreeWidgetItem(self.p_c_treeview)
					root.setText(0, project['project_name'])
					for case in case_selected:
						child = QTreeWidgetItem(root)
						child.setText(0, case['case_name'])

			else:
				root = QTreeWidgetItem(self.p_c_treeview)
				root.setText(0, project['project_name'])
				case_list = self.DB.select('case_list', 'case_name', 'project_name', project['project_name'])
				for case in case_list:
					child = QTreeWidgetItem(root)
					child.setText(0, case['case_name'])

		self.p_c_treeview.expandAll()
		self.p_c_treeview.setStyle(QStyleFactory.create('windows'))
	
	def change_by_order(self, by_order):
		self.p_c_order = by_order
		self.DB.update('profile', 'id', '1', 'value', by_order)
		self.p_c_tree_refresh()

	def label_init(self):
		self.labels = ('特殊', '进行中', '搁置', '已结', '其他')

	def set_label(self, label):
		current_project = self.p_c_treeview.currentIndex().data()
		self.DB.update('project_list', 'project_name', current_project, 'label', str(label))
		self.p_c_tree_refresh()

	def open_file(self, item):
		project_path = ''
		if self.p_c_treeview.currentIndex().data() and not self.p_c_treeview.currentIndex().parent().data():
			current_project = self.p_c_treeview.currentIndex().data()
			project_path = self.DB.select('project_list', 'file_path', 'project_name', 
				current_project)[0]['file_path']
		elif self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			current_project = self.p_c_treeview.currentIndex().parent().data()
			project_path = self.DB.select('project_list', 'file_path', 'project_name', 
				current_project)[0]['file_path']
		if project_path:
			subprocess.call(["open",project_path])

	def p_c_showmenu(self):
		localpos = self.p_c_treeview.mapFromGlobal(QCursor().pos())
		current = self.p_c_treeview.currentIndex()

		if self.p_c_treeview.itemAt(localpos) and current.parent().data():
			self.p_c_tree_menu(2)
		elif self.p_c_treeview.itemAt(localpos):
			self.p_c_tree_menu(1)
		else:
			self.p_c_tree_menu(0)
		
		self.p_c_menu.move(QCursor().pos())
		self.p_c_menu.show()

	# 修改项目
	def edit_project_name(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		new_project_name, flag = QInputDialog.getText(self, "项目名", "请输入新的项目名：")
		if flag and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			try:
				self.DB.rename_project(current_project, new_project_name)
			except:
				QMessageBox.warning(self, "错误", "该项目已存在。")
			finally:
				self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def edit_project_num(self):
		new_project_num, flag = QInputDialog.getText(self, "项目号", "请输入新的项目号：")
		if flag and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			self.DB.update('project_list', 'project_name', current_project, 'project_num', new_project_num)
			self.case_info_refresh()

	def edit_project_path(self):
		new_project_path = QFileDialog.getExistingDirectory(self, "选择项目文件夹", self.default_filepath)
		if new_project_path and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			self.DB.update('project_list', 'project_name', current_project, 'file_path', new_project_path)

	def delete_project(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data():
			current_project = self.p_c_treeview.currentIndex().data()
			reply = QMessageBox.warning(self, "删除项目", f"是否删除“{current_project}”？\n"\
				f"将会删除对应的案件。", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.delete_project(current_project)
				self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	# 修改案件
	def new_case(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		project_name = None
		if self.p_c_treeview.currentIndex().data() and not self.p_c_treeview.currentIndex().parent().data():
			project_name = self.p_c_treeview.currentIndex().data()
		else:
			projects = [x['project_name'] for x in self.DB.select('project_list', 'project_name')]
			project_name, flag = QInputDialog.getItem(self, "新的案件", 
				"从该项目中新建：", projects, 0, False)

		if project_name:
			case_name, flag2 = QInputDialog.getText(self, "新的案件", "请输入案件名：")
			if flag2 and case_name:
				cases = [x['case_name'] for x in self.DB.select('case_list', 'case_name')]
				if case_name in cases:
					QMessageBox.warning(self, "错误", "该案件已存在。")
				else:
					types = [x['type_name'] for x in self.DB.select('type_list', 'type_name')]
					case_type, flag3 = QInputDialog.getItem(self, "新的案件", 
						"选择新案件的类型：", types, 0, False)
					if flag3:
						self.DB.new_case(project_name, case_name, case_type)
						reply = QMessageBox.question(self, "新的案件", "是否开始输入案件信息？\n"\
							"（任意时刻退出将中止输入）", 
							QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
							
						if reply != 65536:
							items_forms = [[x['item'], x['item_form']] for x in self.DB.select('case_type', 
								'item, item_form', 'type_name', case_type)]

							for t in items_forms:
								item, item_form = t
								if item_form == 'text':
									new_data, go_on = QInputDialog.getText(self, case_name, f"请输入{item}：")
									if go_on:
										self.DB.insert_value(case_name, item, item_form, new_data)
									else:
										break
								elif item_form == 'party' or item_form == 'contact':
									self.window_second = ui_edit_case_persons(DB = self.DB, 
										which_type = item_form, case = case_name, item = item)
									self.window_second.exec()
								

		self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def delete_case(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			current_case = self.p_c_treeview.currentIndex().data()
			reply = QMessageBox.warning(self, "删除案件", f"是否删除“{current_case}”？", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.delete_case(current_case)
				self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)
		
	def change_project(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			current_case = self.p_c_treeview.currentIndex().data()
			current_project = self.p_c_treeview.currentIndex().parent().data()
			project_list = self.DB.select('project_list', 'project_name', 'project_name', 
				current_project, '!=')
			projects = [p['project_name'] for p in project_list]
			if projects:
				new_project, flag = QInputDialog.getItem(self, current_case, 
					"更换至项目：", projects, 0, False)
				if flag:
					self.DB.change_project(current_case, current_project, new_project)
		self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def edit_case_name(self, n_name):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			project_name = self.p_c_treeview.currentIndex().data()
			case_name, flag = QInputDialog.getText(self, "案件名", "请输入新案件名：")
			if flag and case_name:
				cases = [x['case_name'] for x in self.DB.select('case_list', 'case_name')]
				if case_name in cases:
					QMessageBox.warning(self, "错误", "该案件已存在。")
				else:
					self.DB.rename_case(project_name, n_name, case_name)

		self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def edit_case_value(self, case, item, item_form):
		if item_form == 'text':
			new_data, flag = QInputDialog.getText(self, item, f"请输入新的{item}：")
			if flag and self.p_c_treeview.currentIndex():
				case = self.p_c_treeview.currentIndex().data()
				current = self.DB.select_multi_condition('case_info', 'value', 
					f"case_name = '{self.trans(case)}' and item = '{self.trans(item)}'")
				if current:
					self.DB.update_multi_condition('case_info', f"case_name = '{self.trans(case)}' and "\
						f"item = '{self.trans(item)}'", 'value', new_data)
				else:
					self.DB.insert_value(case, item, item_form, new_data)
				self.case_info_refresh()

		elif item_form == 'party' or item_form == 'contact':
			self.window_second = ui_edit_case_persons(DB = self.DB, 
				which_type = item_form, case = case, item = item)
			self.window_second.show()
			self.window_second.close_signal.connect(self.case_info_refresh)
	
	# 案件信息显示
	def case_things_refresh(self):
		self.case_info_refresh()
		self.things_refresh()
		self.notepad_refresh()
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			for i in range(4):
				self.case_info_tab.setTabEnabled(i, True)
		else:
			self.case_info_tab.setCurrentIndex(0)
			self.case_info_tab.setTabEnabled(0, True)
			for i in range(1, 4):
				self.case_info_tab.setTabEnabled(i, False)

	def copy_mail_address(self, pid):
		QApplication.clipboard().setText(self.DB.generate_mail_address(pid))

	def copy_party_info_all(self, case):
		s = ''
		values = self.DB.select_multi_condition('case_info', 'value, value2', f"case_name = '{self.trans(case)}' "\
			f"and value_form = 'party'")
		values_uni = [[x['value'], x['value2']] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
		for party, pid in values_uni:
			s = s + f"{party}：{self.DB.generate_party_info(pid)}\n"
		QApplication.clipboard().setText(s)

	def copy_party_info(self, status, pid):
		QApplication.clipboard().setText(f"{status}：{self.DB.generate_party_info(pid)}")

	def show_party_info(self, pid):
		msgbox = QMessageBox()
		msgbox.setText(self.DB.get_party_info(pid))
		msgbox.exec()

	def copy_case_info(self, case, abbr):
		QApplication.clipboard().setText(self.DB.generate_case_info(case, abbr))

	def case_info_showmenu(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()

			self.case_info_menu = QMenu(self.info_view)
			newAction = QAction("----复制----".center(15), self)
			self.case_info_menu.addAction(newAction)

			sub_menu = self.case_info_menu.addMenu('案件信息..')
			sub_menu.setMinimumWidth(100)
			newAction = QAction("（不含简称）", self)
			newAction.triggered.connect(partial(self.copy_case_info, case, False))
			sub_menu.addAction(newAction)
			newAction = QAction("（含简称）", self)
			newAction.triggered.connect(partial(self.copy_case_info, case, True))
			sub_menu.addAction(newAction)

			sub_menu = self.case_info_menu.addMenu('当事人..')
			sub_menu.setMinimumWidth(100)
			newAction = QAction("全部", self)
			newAction.triggered.connect(partial(self.copy_party_info_all, case))
			sub_menu.addAction(newAction)
			sub_menu.addSeparator()

			values = self.DB.select_multi_condition('case_info', 'value, value2', f"case_name = '{self.trans(case)}' "\
				f"and value_form = 'party'")
			if values:
				values_uni = [[x['value'], x['value2']] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
				for status, pid in values_uni:
					name = list(self.DB.select('party_info', 'value', 'party_id', pid)[0].values())[0]
					newAction = QAction(name, self)
					newAction.triggered.connect(partial(self.copy_party_info, status, pid))
					sub_menu.addAction(newAction)
			else:
				newAction = QAction("（无）", self)
				sub_menu.addAction(newAction)

			sub_menu = self.case_info_menu.addMenu('邮寄地址..')
			sub_menu.setMinimumWidth(100)
			values = self.DB.select_multi_condition('case_info', 'value2', f"case_name = '{self.trans(case)}' "\
				f"and value_form = 'contact'")
			if values:
				values_uni = [x['value2'] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
				for pid in values_uni:
					name = list(self.DB.select('contact_info', 'value', 'contact_id', pid)[0].values())[0]
					newAction = QAction(name, self)
					newAction.triggered.connect(partial(self.copy_mail_address, pid))
					sub_menu.addAction(newAction)
			else:
				newAction = QAction("（无）", self)
				sub_menu.addAction(newAction)

			self.case_info_menu.addSeparator()
			newAction = QAction("----查看----".center(15), self)
			self.case_info_menu.addAction(newAction)

			sub_menu = self.case_info_menu.addMenu('当事人..')
			sub_menu.setMinimumWidth(100)
			values = self.DB.select_multi_condition('case_info', 'value, value2', f"case_name = '{self.trans(case)}' "\
				f"and value_form = 'party'")
			if values:
				values_uni = [x['value2'] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
				for pid in values_uni:
					which_class, name = list(self.DB.select('party_info', 'class, value', 'party_id', pid)[0].values())
					newAction = QAction(name, self)
					newAction.triggered.connect(partial(self.show_person_info, 'party', which_class, pid))
					sub_menu.addAction(newAction)
			else:
				newAction = QAction("（无）", self)
				sub_menu.addAction(newAction)

			sub_menu = self.case_info_menu.addMenu('联系人..')
			sub_menu.setMinimumWidth(100)
			values = self.DB.select_multi_condition('case_info', 'value, value2', f"case_name = '{self.trans(case)}' "\
				f"and value_form = 'contact'")
			if values:
				values_uni = [x['value2'] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
				for pid in values_uni:
					which_class, name = list(self.DB.select('contact_info', 'class, value', 'contact_id', pid)[0].values())
					newAction = QAction(name, self)
					newAction.triggered.connect(partial(self.show_person_info, 'contact', which_class, pid))
					sub_menu.addAction(newAction)
			else:
				newAction = QAction("（无）", self)
				sub_menu.addAction(newAction)
		
		self.case_info_menu.move(QCursor().pos())
		self.case_info_menu.show()

	def case_info_refresh(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			self.info_view.setHtml(self.DB.generate_case_info_html(case))

		elif current.data():
			project = current.data()
			self.info_view.setHtml(self.DB.generate_project_info_html(project))

	def things_refresh(self):
		self.todo_view.setRowCount(0)
		self.event_view.setRowCount(0)
		self.todo_view.cellChanged.disconnect()
		self.event_view.cellChanged.disconnect()

		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			todos = sorted(self.DB.select_all('todo_list', 'case_name', case), 
				key = lambda x: (x['date'], x['id']))
			events = sorted(self.DB.select_all('event_list', 'case_name', case), 
				key = lambda x: (x['date'], x['id']), reverse = True)
			for k in todos:
				rows = self.todo_view.rowCount()
				date_item = QDateTimeEdit(datetime.strptime(k['date'], '%Y-%m-%d'), self)
				date_item.setCalendarPopup(True)
				date_item.setDisplayFormat('yyyy年MM月dd日')
				self.todo_view.insertRow(rows)
				self.todo_view.setCellWidget(rows, 0, date_item)
				self.todo_view.cellWidget(rows, 0).dateChanged.connect(partial(self.edit_todo, rows, 0))
				self.todo_view.setItem(rows, 1, QTableWidgetItem(k['things']))
				self.todo_view.setItem(rows, 2, QTableWidgetItem(str(k['id'])))
				
			for k in events:
				rows = self.event_view.rowCount()
				date_item = QDateTimeEdit(datetime.strptime(k['date'], '%Y-%m-%d'), self)
				date_item.setCalendarPopup(True)
				date_item.setDisplayFormat('yyyy年MM月dd日')
				self.event_view.insertRow(rows)
				self.event_view.setCellWidget(rows, 0, date_item)
				self.event_view.cellWidget(rows, 0).dateChanged.connect(partial(self.edit_event, rows, 0))
				self.event_view.setItem(rows, 1, QTableWidgetItem(k['things']))
				self.event_view.setItem(rows, 2, QTableWidgetItem(str(k['id'])))

		self.todo_view.cellChanged.connect(self.edit_todo)
		self.event_view.cellChanged.connect(self.edit_event)

	def notepad_refresh(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			s = self.DB.select('case_list', 'notepad_text', 'case_name', case)[0]['notepad_text']
			self.notepad.setText(s)

	# 待办、事件和记事
	def things_showmenu(self, menu):
		menu.move(QCursor().pos())
		menu.show()

	def add_todo(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			project = current.parent().data()
			self.DB.insert('todo_list', 'case_name', case)
			self.DB.update_latest('todo_list', 'project_name', project)
			self.DB.update_latest('todo_list', 'date', datetime.now().strftime('%Y-%m-%d'))
			self.things_refresh()

	def add_event(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			project = current.parent().data()
			self.DB.insert('event_list', 'case_name', case)
			self.DB.update_latest('event_list', 'project_name', project)
			self.DB.update_latest('event_list', 'date', datetime.now().strftime('%Y-%m-%d'))
			self.things_refresh()

	def notepad_input(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			s = self.notepad.toPlainText()
			self.DB.update('case_list', 'case_name', case, 'notepad_text', s)

	def get_index(self, view):
		c_row = view.currentRow()
		c_col = view.currentColumn()
		return (c_row, c_col)

	def get_date(self, view, index):
		return view.cellWidget(index[0], index[1]).date().toString('yyyy-MM-dd')

	def get_data(self, view, index):
		return view.item(index[0], index[1]).text()

	def get_row_id(self, view):
		c_row = view.currentRow()
		return view.item(c_row, 2).text()

	def delete_todo(self):
		current = self.p_c_treeview.currentIndex()
		if self.todo_view.selectedItems() and current.parent().data():
			case = current.data()
			self.DB.delete('todo_list', 'id', self.get_row_id(self.todo_view))
			self.things_refresh()

	def delete_event(self):
		current = self.p_c_treeview.currentIndex()
		if self.event_view.selectedItems() and current.parent().data():
			case = current.data()
			self.DB.delete('event_list', 'id', self.get_row_id(self.event_view))
			self.things_refresh()

	def to_event(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			project = current.parent().data()
			index = self.get_index(self.todo_view)
			date = self.get_date(self.todo_view, (index[0], 0))
			things = self.get_data(self.todo_view, (index[0], 1))

			self.DB.insert('event_list', 'case_name', case)
			self.DB.update_latest('event_list', 'project_name', project)
			self.DB.update_latest('event_list', 'date', date)
			self.DB.update_latest('event_list', 'things', things)
			self.delete_todo()

	def edit_todo(self ,row_n, col_n):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			pid = self.get_row_id(self.todo_view)
			if col_n == 1:
				new_data = self.get_data(self.todo_view, (row_n, col_n))
				self.DB.update('todo_list', 'id', pid, 'things', new_data)
				self.things_refresh()
			elif col_n == 0:
				new_date = self.get_date(self.todo_view, (row_n, col_n))
				self.DB.update('todo_list', 'id', pid, 'date', new_date)
				self.things_refresh()

	def edit_event(self ,row_n, col_n):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			pid = self.get_row_id(self.event_view)
			if col_n == 1:
				new_data = self.get_data(self.event_view, (row_n, col_n))
				self.DB.update('event_list', 'id', pid, 'things', new_data)
				self.things_refresh()
			elif col_n == 0:
				new_date = self.get_date(self.event_view, (row_n, col_n))
				self.DB.update('event_list', 'id', pid, 'date', new_date)
				self.things_refresh()

	def things_menu(self):
		self.todo_menu = QMenu(self.todo_view)
		newAction = QAction('复制', self)
		newAction.triggered.connect(partial(self.things_copy, self.todo_view))
		self.todo_menu.addAction(newAction)

		self.event_menu = QMenu(self.event_view)
		newAction = QAction('复制', self)
		newAction.triggered.connect(partial(self.things_copy, self.event_view))
		self.event_menu.addAction(newAction)

	def things_copy(self, view):
		s = ''
		for data in view.selectedItems():
			row = data.row()
			date = view.cellWidget(row, 0).date().toString('yyyy年MM月dd日')
			thing = self.get_data(view, (row, 1))
			s = s + date + '\t' + thing + '\n'
		QApplication.clipboard().setText(s)

	# 初始化、备份和还原
	def do_init(self):
		reply = QMessageBox.warning(self, "初始化", "是否删除全部数据并初始化？", 
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.p_c_treeview.itemSelectionChanged.disconnect()
			self.DB.init()
			self.read_profile()
			self.p_c_tree_refresh()
			self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def back_up(self):
		path = QFileDialog.getExistingDirectory(self, "请选择存放备份文件的文件夹", self.default_filepath)
		if path:
			NOW = datetime.now().strftime('%Y%m%d%H%M%S')
			BAK_PATH = os.path.join(path, f"DB_{NOW}.bak")
			if BAK_PATH and not os.path.exists(BAK_PATH):
				try:
					copyfile(self.DB_PATH, BAK_PATH)
				except:
					QMessageBox.critical(self, "错误", "备份出错")

	def restore(self):
		BAK_PATH, flag = QFileDialog.getOpenFileName(self, "请选择已备份文件", self.default_filepath)
		if BAK_PATH:
			reply = QMessageBox.warning(self, "还原文件", "将覆盖现有全部数据，是否继续？", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.p_c_treeview.itemSelectionChanged.disconnect()
				self.DB.delete_DB()
				try:
					copyfile(BAK_PATH, self.DB_PATH)
				except:
					QMessageBox.critical(self, "错误", "还原出错")
				else:
					self.read_profile()
					self.p_c_tree_refresh()
				finally:
					self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def change_default_path(self):
		new_path = QFileDialog.getExistingDirectory(self, "请选择默认文件地址", self.default_filepath)
		if new_path:
			self.DB.update('profile', 'id', '2', 'value', new_path)
			self.default_filepath = new_path

	def change_color(self, flag):
		def to_hex(x):
			t = str(hex(x))[2:]
			while len(t) < 2:
				t = '0' + t
			return t

		if flag == 0:
			reply = QMessageBox.question(self, "配色-项目信息", "变更项目信息中项目名的背景颜色：", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply != 65536:
				color = self.DB.select('profile', 'value', 'id', '3')[0]['value']
				c = QColorDialog.getColor(QColor(color), self)
				new_color = f"#{to_hex(c.red())}{to_hex(c.green())}{to_hex(c.blue())}"
				self.DB.update('profile', 'id', '3', 'value', new_color)

		elif flag == 1:
			reply = QMessageBox.question(self, "配色-案件信息", "依次变更案件信息中案件名、分项标题的背景颜色：", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply != 65536:
				for i in range(2):
					t = str(i + 4)
					color = self.DB.select('profile', 'value', 'id', t)[0]['value']
					c = QColorDialog.getColor(QColor(color), self)
					new_color = f"#{to_hex(c.red())}{to_hex(c.green())}{to_hex(c.blue())}"
					self.DB.update('profile', 'id', t, 'value', new_color)

		elif flag == 2:
			reply = QMessageBox.question(self, "配色-今日简报", "依次变更今日简报中标题、次级标题、表格的背景颜色：", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply != 65536:
				for i in range(3):
					t = str(i + 6)
					color = self.DB.select('profile', 'value', 'id', t)[0]['value']
					c = QColorDialog.getColor(QColor(color), self)
					new_color = f"#{to_hex(c.red())}{to_hex(c.green())}{to_hex(c.blue())}"
					self.DB.update('profile', 'id', t, 'value', new_color)


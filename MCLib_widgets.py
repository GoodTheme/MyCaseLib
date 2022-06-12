# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MCLib_widgets_UI import *
from functools import partial, reduce

class ui_execute(QDialog, Ui_execute_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, parent = None):
		super(ui_execute, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.execute_btn.clicked.connect(self.show_execute_result)

	def show_execute_result(self):
		s = self.execute_line.text()
		result = self.DB.execute(s)
		self.execute_result.clear()
		for t in result:
			self.execute_result.append(str(result))

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_new_project(QDialog, Ui_new_project_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, parent = None):
		super(ui_new_project, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.project_name_line.textChanged.connect(self.right_project_name)
		self.project_path_btn.clicked.connect(self.choose_path)
		self.project_ok_btn.clicked.connect(self.create_project)
		self.project_cancel_btn.clicked.connect(self.close)

	def right_project_name(self):
		projects = [p['project_name'] for p in self.DB.select('project_list', 'project_name')]
		s = self.project_name_line.text()
		if s and s not in projects:
			self.project_ok_btn.setEnabled(True)
		else:
			self.project_ok_btn.setEnabled(False)

	def choose_path(self):
		project_path = QFileDialog.getExistingDirectory(self, "选择项目文件夹")
		if project_path:
			self.project_path_line.setText(project_path)

	def create_project(self):
		project_name = self.project_name_line.text()
		project_num = self.project_num_line.text()
		project_path = self.project_path_line.text()
		self.DB.new_project(project_name, project_num, project_path)
		self.close()

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_edit_case_persons(QDialog, Ui_edit_case_persons_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, which_type, case, item, parent = None):
		super(ui_edit_case_persons, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_type_c = '当事人' if which_type == 'party' else '联系人'
		self.case = case
		self.item = item
		self.headers = ['id', '当事人地位', '名称'] if self.which_type == 'party' else ['id', '身份', '名字']
		self.setWindowTitle(self.item)
		self.add_btn.clicked.connect(self.add_person)
		self.delete_btn.clicked.connect(self.delete_person)

		self.view_menu_init()
		self.persons_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.persons_view_menu))

		self.persons_view.setSelectionBehavior(QTableWidget.SelectRows)
		self.persons_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.persons_view.setHorizontalHeaderLabels(self.headers)
		self.persons_view.setColumnHidden(0, True)
		self.persons_view_refresh()

	def get_name(self, pid):
		return self.DB.select(f"{self.which_type}_info", 'value', f"{self.which_type}_id", pid)[0]['value']

	def persons_view_refresh(self):
		def trans(s):
			if not s:
				return ''
			trans = ''
			for t in str(s):
				trans = trans + t if t != "'" else trans + "''"
			return trans

		self.persons_view.setRowCount(0)
		values = self.DB.select_multi_condition('case_info', 'id, value, value2', f"case_name = '{trans(self.case)}'"\
			f"and item = '{trans(self.item)}'")
		for k in values:
			rows = self.persons_view.rowCount()
			self.persons_view.insertRow(rows)
			self.persons_view.setItem(rows, 0, QTableWidgetItem(str(k['id'])))
			self.persons_view.setItem(rows, 1, QTableWidgetItem(k['value']))
			self.persons_view.setItem(rows, 2, QTableWidgetItem(self.get_name(k['value2'])))

	def add_person(self):
		value, flag = QInputDialog.getText(self, self.headers[1], f"该{self.which_type_c}在本案中的身份/地位：")
		if flag:
			self.window_person = ui_persons(DB = self.DB, which_type = self.which_type, flag = 1)
			chosen_id = self.window_person.exec()
			if chosen_id > 0:
				self.DB.insert_value(self.case, self.item, self.which_type, value, chosen_id)
				self.setResult(1)
				self.persons_view_refresh()

	def delete_person(self):
		if self.persons_view.selectedItems():
			pid = self.persons_view.item(self.persons_view.currentRow(), 0).text()
			self.DB.delete('case_info', 'id', pid)
			self.persons_view_refresh()

	def view_showmenu(self, menu):
		menu.move(QCursor().pos())
		menu.show()

	def view_menu_init(self):
		self.persons_view_menu = QMenu(self.persons_view)
		newAction = QAction('上移', self)
		newAction.triggered.connect(self.item_move_up)
		self.persons_view_menu.addAction(newAction)

		newAction = QAction('下移', self)
		newAction.triggered.connect(self.item_move_down)
		self.persons_view_menu.addAction(newAction)

	def item_move_up(self):
		if self.persons_view.selectedItems():
			c_row = self.persons_view.currentRow()
			if c_row > 0:
				c_id = self.persons_view.item(c_row, 0).text()
				up_id = self.persons_view.item(c_row - 1, 0).text()
				self.DB.swap('case_info', 'value', c_id, up_id)
				self.DB.swap('case_info', 'value2', c_id, up_id)
				self.persons_view_refresh()

	def item_move_down(self):
		if self.persons_view.selectedItems():
			c_row = self.persons_view.currentRow()
			rows = self.persons_view.rowCount()
			if c_row + 1 < rows:
				c_id = self.persons_view.item(c_row, 0).text()
				down_id = self.persons_view.item(c_row + 1, 0).text()
				self.DB.swap('case_info', 'value', c_id, down_id)
				self.DB.swap('case_info', 'value2', c_id, down_id)
				self.persons_view_refresh()

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_persons(QDialog, Ui_persons_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, which_type, flag, parent = None):
		super(ui_persons, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_type_c = '当事人' if which_type == 'party' else '联系人'
		self.chosen_id = -1
		
		self.add_btn.clicked.connect(self.add_person)
		self.search_bar.textChanged.connect(self.results_view_refresh)
		self.results_view.itemSelectionChanged.connect(self.infos_view_refresh)
		self.infos_view.cellChanged.connect(self.edit_info)
		self.results_view_refresh()
		self.infos_view_refresh()
		self.view_menu_init()
		self.results_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.results_menu))
		self.infos_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.infos_menu))

		if flag:
			self.results_view.itemDoubleClicked.connect(self.choose_it)
			self.delete_btn.setText('选择')
			self.delete_btn.clicked.connect(self.choose_it)
			self.setWindowTitle(f"双击选择一名{self.which_type_c}..")
		else:
			self.delete_btn.clicked.connect(self.delete_person)
			self.setWindowTitle(self.which_type_c)

	def results_view_refresh(self):
		self.search_bar.textChanged.disconnect()
		self.results_view.setRowCount(0)
		self.results_view.setColumnHidden(0, True)
		self.results_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

		keywords = self.search_bar.text()
		if keywords:
			all_items = self.DB.select_all(f"{self.which_type}_info")
			items = []
			for item in all_items:
				if isinstance(item['value'], str) and item['value'].find(keywords) != -1:
					pid = item[f"{self.which_type}_id"]
					item_name = self.DB.select(f"{self.which_type}_list", 'name', 'id', pid)[0]['name']
					new_item = {'id': pid, 'name': item_name}
					if new_item not in items:
						items.append(new_item)
			items_sorted = sorted(items, key = lambda x:(x['id']), reverse = True)
		else:
			items_sorted = sorted(self.DB.select_all(f"{self.which_type}_list"), key = lambda x:(x['id']), reverse = True)

		for k in items_sorted:
			rows = self.results_view.rowCount()
			self.results_view.insertRow(rows)
			self.results_view.setItem(rows, 0, QTableWidgetItem(str(k['id'])))
			self.results_view.setItem(rows, 1, QTableWidgetItem(k['name']))

		self.search_bar.textChanged.connect(self.results_view_refresh)

	def infos_view_refresh(self):
		self.infos_view.setRowCount(0)
		self.infos_view.setColumnHidden(0, True)
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		if self.results_view.selectedItems():
			c_row = self.results_view.currentRow()
			current_pid = self.results_view.item(c_row, 0).text()
			current_class = self.DB.select(f"{self.which_type}_list", 'class', 'id', current_pid)[0]['class']
			item_list = self.DB.select(f"{self.which_type}_class", 'item', 'class', current_class)

			self.infos_view.setRowCount(len(item_list))
			self.infos_view.setVerticalHeaderLabels([x['item'] for x in item_list])
			self.infos_view.verticalHeader().setMinimumWidth(120)
			all_values = self.DB.select(f"{self.which_type}_info", 'id, item, value', f"{self.which_type}_id", current_pid)
			
			i = 0
			for item in item_list:
				for s in all_values:
					if s['item'] == item['item']:
						self.infos_view.setItem(i, 0, QTableWidgetItem(str(s['id'])))
						self.infos_view.setItem(i, 1, QTableWidgetItem(s['value']))
						break
				i = i + 1

	def add_person(self):
		self.results_view.itemSelectionChanged.disconnect()
		class_list = self.DB.select(f"{self.which_type}_class", 'class')
		class_list_uni = [x['class'] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + class_list)]
		which_class, flag = QInputDialog.getItem(self, self.which_type_c, f"请选择{self.which_type_c}类别", 
			class_list_uni, 0, False)
		if flag:
			name, flag2 = QInputDialog.getText(self, f"新的{self.which_type_c}", 
				f"请输入该{self.which_type_c}的名字：")
			if flag2:
				self.DB.new_person(self.which_type, which_class, name)
				self.results_view_refresh()
		self.results_view.itemSelectionChanged.connect(self.infos_view_refresh)

	def delete_person(self):
		if self.results_view.selectedItems():
			c_row = self.results_view.currentRow()
			pid = self.results_view.item(c_row, 0).text()
			self.DB.delete_person(self.which_type, pid)
			self.results_view_refresh()

	def edit_info(self, row_n, col_n):
		self.infos_view.cellChanged.disconnect()
		if self.infos_view.selectedItems():
			pid = self.infos_view.item(row_n, 0).text()
			new_data = self.infos_view.item(row_n, 1).text()
			self.DB.update(f"{self.which_type}_info", 'id', pid, 'value', new_data)
			self.infos_view_refresh()
			if row_n == 0:
				self.results_view.itemSelectionChanged.disconnect()
				list_pid = self.results_view.item(self.results_view.currentRow(), 0).text()
				self.DB.update(f"{self.which_type}_list", 'id', list_pid, 'name', new_data)
				self.results_view_refresh()
				self.infos_view_refresh()
				self.results_view.itemSelectionChanged.connect(self.infos_view_refresh)
		self.infos_view.cellChanged.connect(self.edit_info)

	def view_showmenu(self, menu):
		menu.move(QCursor().pos())
		menu.show()

	def view_menu_init(self):
		self.results_menu = QMenu(self.results_view)
		newAction = QAction('复制详情', self)
		newAction.triggered.connect(self.info_show)
		self.results_menu.addAction(newAction)
		newAction = QAction('删除', self)
		newAction.triggered.connect(self.delete_person)
		self.results_menu.addAction(newAction)

		self.infos_menu = QMenu(self.results_view)
		newAction = QAction('复制详情', self)
		newAction.triggered.connect(self.info_show)
		self.infos_menu.addAction(newAction)

	def info_show(self):
		if self.results_view.selectedItems():
			c_row = self.results_view.currentRow()
			pid = self.results_view.item(c_row, 0).text()
			infos = self.DB.select(f"{self.which_type}_info", "item, value", f"{self.which_type}_id", pid)
			s = ''
			for x in infos:
				if x['value']:
					s = s + f"{x['item']}：{x['value']}\n"
			QMessageBox.about(self, infos[0]['value'], s)
			QApplication.clipboard().setText(s)

	def choose_it(self):
		if self.results_view.selectedItems():
			self.setResult(int(self.results_view.item(self.results_view.currentRow(), 0).text()))
			self.close()
	
	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_party_contact_template(QDialog, Ui_template_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, which_type, parent = None):
		super(ui_party_contact_template, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_type_c = '当事人' if which_type == 'party' else '联系人'

		if self.which_type == 'party':
			self.setWindowTitle("模板：当事人")
		elif self.which_type == 'contact':
			self.setWindowTitle("模板：联系人")

		self.class_list_refresh()
		if self.class_list_view.item(0):
			self.class_list_view.item(0).setSelected(True)
		self.item_list_refresh()
		self.class_list_view.itemSelectionChanged.connect(self.item_list_refresh)

		self.new_class_btn.clicked.connect(self.new_class)
		self.delete_class_btn.clicked.connect(self.delete_class)
		self.new_item_btn.clicked.connect(self.new_class_item)
		self.delete_item_btn.clicked.connect(self.delete_class_item)
		self.view_menu_init()
		self.item_list_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.view_menu))

	def class_list_refresh(self):
		self.class_list_view.clear()
		class_list = self.DB.select(f"{self.which_type}_class", 'class')
		for t in reduce(lambda x, y: x if y in x else x + [y], [[]] + class_list):
			self.class_list_view.addItem(t['class'])

	def item_list_refresh(self):
		self.item_list_view.setRowCount(0)
		self.item_list_view.setColumnHidden(0, True)
		self.item_list_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		self.item_list_view.setColumnHidden(2, True)
		if self.class_list_view.selectedItems():
			current_class = self.class_list_view.selectedItems()[0].text()
			item_list = self.DB.select(f"{self.which_type}_class", 'item, id', 'class', current_class)
			for t in item_list:
				rows = self.item_list_view.rowCount()
				self.item_list_view.insertRow(rows)
				self.item_list_view.setItem(rows, 0, QTableWidgetItem(current_class))
				self.item_list_view.setItem(rows, 1, QTableWidgetItem(t['item']))
				self.item_list_view.setItem(rows, 2, QTableWidgetItem(str(t['id'])))

	def new_class(self):
		self.class_list_view.itemSelectionChanged.disconnect()
		new_class_name, flag = QInputDialog.getText(self, "新的类别", "请输入新的类别名称：")
		if flag:
			if new_class_name in [p['class'] for p in self.DB.select(f"{self.which_type}_class", 'class')]:
				QMessageBox.warning(self, "错误", "该类别已存在。")
			else:
				fisrt_item_name, flag2 = QInputDialog.getText(self, "基础信息", f"请输入“{new_class_name}”中"\
					f"用于标识个体的信息名，例如“名称”：")
				if flag2:
					self.DB.new_party_contact_class(self.which_type, new_class_name, fisrt_item_name)
					self.class_list_refresh()
					rows = self.class_list_view.count()
					self.class_list_view.item(rows - 1).setSelected(True)
		self.class_list_view.itemSelectionChanged.connect(self.item_list_refresh)

	def delete_class(self):
		self.class_list_view.itemSelectionChanged.disconnect()
		if self.class_list_view.selectedItems():
			current_class = self.class_list_view.selectedItems()[0].text()
			reply = QMessageBox.warning(self, "删除类别", f"是否删除名为“{current_class}”的类型？\n"\
				f"将会删除所有该类别{self.which_type_c}信息。", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.delete_party_contact_class(self.which_type, current_class)
				self.class_list_refresh()
		self.class_list_view.itemSelectionChanged.connect(self.item_list_refresh)

	def new_class_item(self):
		if self.class_list_view.selectedItems():
			current_class = self.class_list_view.selectedItems()[0].text()
			new_item_name, flag = QInputDialog.getText(self, current_class, "请输入新的字段名称：")
			if flag:
				if not self.DB.new_party_contact_item(self.which_type, current_class, new_item_name):
					QMessageBox.warning(self, "错误", f"“{current_class}”已经存在该字段。")
		self.item_list_refresh()

	def delete_class_item(self):
		#无法删除第一项
		if self.class_list_view.selectedItems() and self.item_list_view.selectedItems():
			if self.item_list_view.currentRow() == 0:
				QMessageBox.warning(self, "错误", f"无法删除标识个体的基础信息")
			else:
				current_class = self.class_list_view.selectedItems()[0].text()
				current_item = self.item_list_view.selectedItems()[0].text()
				reply = QMessageBox.warning(self, "删除字段", f"是否删除“{current_class}”中的“{current_item}”？\n"\
					f"将会删除所有“{current_class}”的对应信息。", 
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.DB.delete_party_contact_item(self.which_type, current_class, current_item)
					self.item_list_refresh()
	
	def view_showmenu(self, menu):
		menu.move(QCursor().pos())
		menu.show()

	def view_menu_init(self):
		self.view_menu = QMenu(self.item_list_view)
		newAction = QAction('上移', self)
		newAction.triggered.connect(self.item_move_up)
		self.view_menu.addAction(newAction)

		newAction = QAction('下移', self)
		newAction.triggered.connect(self.item_move_down)
		self.view_menu.addAction(newAction)

	def item_move_up(self):
		if self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			if c_row > 1:
				c_id = self.item_list_view.item(c_row, 2).text()
				up_id = self.item_list_view.item(c_row - 1, 2).text()
				self.DB.swap(f"{self.which_type}_class", 'item', c_id, up_id)
				self.item_list_refresh()

	def item_move_down(self):
		if self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			rows = self.item_list_view.rowCount()
			if c_row + 1 < rows and c_row > 0:
				c_id = self.item_list_view.item(c_row, 2).text()
				down_id = self.item_list_view.item(c_row + 1, 2).text()
				self.DB.swap(f"{self.which_type}_class", 'item', c_id, down_id)
				self.item_list_refresh()

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_type_item_template(QDialog, Ui_template_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, parent = None):
		super(ui_type_item_template, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.setWindowTitle("模板：案件类型")

		self.type_list_refresh()
		if self.class_list_view.item(0):
			self.class_list_view.item(0).setSelected(True)
		self.item_list_refresh()
		self.class_list_view.itemSelectionChanged.connect(self.item_list_refresh)

		self.new_class_btn.clicked.connect(self.new_type)
		self.delete_class_btn.clicked.connect(self.delete_type)
		self.new_item_btn.clicked.connect(self.new_type_item)
		self.delete_item_btn.clicked.connect(self.delete_type_item)
		self.view_menu_init()
		self.item_list_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.view_menu))

	def type_list_refresh(self):
		self.class_list_view.clear()
		type_list = self.DB.select('type_list', 'type_name')
		for t in type_list:
			self.class_list_view.addItem(t['type_name'])

	def item_list_refresh(self):
		self.item_list_view.setRowCount(0)
		self.item_list_view.setColumnHidden(1, True)
		self.item_list_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.item_list_view.setColumnHidden(2, True)
		if self.class_list_view.selectedItems():
			current_type = self.class_list_view.selectedItems()[0].text()
			item_list = self.DB.select('case_type', 'id, item', 'type_name', current_type)
			for t in item_list:
				rows = self.item_list_view.rowCount()
				self.item_list_view.insertRow(rows)
				self.item_list_view.setItem(rows, 0, QTableWidgetItem(t['item']))
				self.item_list_view.setItem(rows, 1, QTableWidgetItem(str(t['id'])))

	def new_type(self):
		new_type_name, flag = QInputDialog.getText(self, "新的类型", "请输入新的类型名称：")
		if flag:
			try:
				self.DB.new_type(new_type_name)
			except:
				QMessageBox.warning(self, "错误", "该类型已存在。")
			else:
				self.type_list_refresh()
				rows = self.class_list_view.count()
				self.class_list_view.item(rows - 1).setSelected(True)

	def delete_type(self):
		if self.class_list_view.selectedItems():
			current_type = self.class_list_view.selectedItems()[0].text()
			reply = QMessageBox.warning(self, "删除类型", f"是否删除名为“{current_type}”的类型？\n"\
				f"将会删除对应的案件。", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.delete_type(current_type)
				self.type_list_refresh()

	def new_type_item(self):
		if self.class_list_view.selectedItems():
			current_type = self.class_list_view.selectedItems()[0].text()
			form_dict = {'纯文字': 'text', '当事人': 'party', '联系人': 'contact'}
			forms = ('纯文字', '当事人', '联系人')
			new_item_name, flag = QInputDialog.getText(self, current_type, "请输入新的字段名称：")
			new_item_form, flag2 = QInputDialog.getItem(self, current_type, "请选择新的字段类型", forms, 0, False)
			if flag & flag2:
				if not self.DB.add_type_item(current_type, new_item_name, form_dict[new_item_form]):
					QMessageBox.warning(self, "错误", f"“{current_type}”已经存在该字段。")
		self.item_list_refresh()

	def delete_type_item(self):
		if self.class_list_view.selectedItems() and self.item_list_view.selectedItems():
			current_type = self.class_list_view.selectedItems()[0].text()
			current_item = self.item_list_view.selectedItems()[0].text()
			reply = QMessageBox.warning(self, "删除字段", f"是否删除“{current_type}”中的“{current_item}”？\n"\
				f"将会删除相关案件的对应信息。", 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.DB.delete_type_item(current_type, current_item)
				self.item_list_refresh()

	def item_move_up(self):
		if self.class_list_view.selectedItems() and self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			if c_row > 0:
				c_id = self.item_list_view.item(c_row, 1).text()
				up_id = self.item_list_view.item(c_row - 1, 1).text()
				self.DB.swap('case_type', 'type_name', c_id, up_id)
				self.DB.swap('case_type', 'item', c_id, up_id)
				self.DB.swap('case_type', 'item_form', c_id, up_id)
				self.item_list_refresh()

	def item_move_down(self):
		if self.class_list_view.selectedItems() and self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			rows = self.item_list_view.rowCount()
			if c_row + 1 < rows:
				c_id = self.item_list_view.item(c_row, 1).text()
				down_id = self.item_list_view.item(c_row + 1, 1).text()
				self.DB.swap('case_type', 'type_name', c_id, down_id)
				self.DB.swap('case_type', 'item', c_id, down_id)
				self.DB.swap('case_type', 'item_form', c_id, down_id)
				self.item_list_refresh()

	def view_showmenu(self, menu):
		menu.move(QCursor().pos())
		menu.show()

	def view_menu_init(self):
		self.view_menu = QMenu(self.item_list_view)
		newAction = QAction('上移', self)
		newAction.triggered.connect(self.item_move_up)
		self.view_menu.addAction(newAction)

		newAction = QAction('下移', self)
		newAction.triggered.connect(self.item_move_down)
		self.view_menu.addAction(newAction)

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_today_news(QDialog, Ui_today_news_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, parent = None):
		super(ui_today_news, self).__init__(parent)
		self.setupUi(self)
		self.message_view.setStyleSheet('background-color: rgb(255,255,255,150);')
		self.message_view.setHtml(DB.generate_report_html())

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_person_info(QDialog, Ui_person_info_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, which_type, which_class, pid, parent = None):
		super(ui_person_info, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_class = which_class
		self.pid = pid
		
		name = self.DB.select(f"{self.which_type}_info", 'value', f"{self.which_type}_id", self.pid)[0]['value']
		self.setWindowTitle(name)
		self.infos_view.cellChanged.connect(self.edit_info)
		self.infos_view_refresh()
		
	def infos_view_refresh(self):
		self.infos_view.setRowCount(0)
		self.infos_view.setColumnHidden(0, True)
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

		current_pid = self.pid
		current_class = self.which_class
		item_list = self.DB.select(f"{self.which_type}_class", 'item', 'class', current_class)

		self.infos_view.setRowCount(len(item_list))
		self.infos_view.setVerticalHeaderLabels([x['item'] for x in item_list])
		self.infos_view.verticalHeader().setMinimumWidth(120)
		all_values = self.DB.select(f"{self.which_type}_info", 'id, item, value', f"{self.which_type}_id", current_pid)
			
		i = 0
		for item in item_list:
			for s in all_values:
				if s['item'] == item['item']:
					self.infos_view.setItem(i, 0, QTableWidgetItem(str(s['id'])))
					self.infos_view.setItem(i, 1, QTableWidgetItem(s['value']))
					break
			i = i + 1

	def edit_info(self, row_n, col_n):
		self.infos_view.cellChanged.disconnect()
		if self.infos_view.selectedItems():
			pid = self.infos_view.item(row_n, 0).text()
			new_data = self.infos_view.item(row_n, 1).text()
			self.DB.update(f"{self.which_type}_info", 'id', pid, 'value', new_data)
			self.infos_view_refresh()
		self.infos_view.cellChanged.connect(self.edit_info)

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

class ui_case_info_edit(QDialog, Ui_person_info_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, case_name, parent = None):
		super(ui_case_info_edit, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.case_name = case_name
		self.type_name = self.DB.select('case_list', 'case_type', 'case_name', self.case_name)[0]['case_type']
		
		self.setWindowTitle(case_name)
		self.infos_view.cellChanged.connect(self.edit_info)
		self.infos_view_refresh()
		
	def trans(self, s):
		if not s:
			return ''
		trans = ''
		for t in str(s):
			trans = trans + t if t != "'" else trans + "''"
		return trans

	def infos_view_refresh(self):
		self.infos_view.setRowCount(0)
		self.infos_view.setColumnHidden(0, True)
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		item_list = self.DB.select_multi_condition('case_type', 'item', 
			f"type_name = '{self.trans(self.type_name)}' and item_form = 'text'")
		
		self.infos_view.setRowCount(len(item_list))
		self.infos_view.setVerticalHeaderLabels([x['item'] for x in item_list])
		self.infos_view.verticalHeader().setMinimumWidth(120)
		all_values = self.DB.select('case_info', 'id, item, value', 'case_name', self.case_name)
					
		i = 0
		for item in item_list:
			self.infos_view.setItem(i, 0, QTableWidgetItem(item['item']))
			for s in all_values:
				if s['item'] == item['item']:
					self.infos_view.setItem(i, 1, QTableWidgetItem(s['value']))
					break
			i = i + 1

	def edit_info(self, row_n, col_n):
		self.infos_view.cellChanged.disconnect()
		if self.infos_view.selectedItems():
			item = self.infos_view.item(row_n, 0).text()
			new_data = self.infos_view.item(row_n, 1).text()
			current = self.DB.select_multi_condition('case_info', 'value', 
				f"case_name = '{self.trans(self.case_name)}' and item = '{self.trans(item)}'")
			if current:
				self.DB.update_multi_condition('case_info', f"case_name = '{self.trans(self.case_name)}' and "\
					f"item = '{self.trans(item)}'", 'value', new_data)
			else:
				self.DB.insert_value(self.case_name, item, 'text', new_data)
			self.infos_view_refresh()
		self.infos_view.cellChanged.connect(self.edit_info)

	def reject(self):
		self.close()

	def closeEvent(self, event):
		self.close_signal.emit()

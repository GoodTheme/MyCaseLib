# -*- coding: utf-8 -*-
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from MCLib_widgets_UI import *
from functools import partial, reduce
import qtawesome

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

class ui_edit_case_persons(QDialog, Ui_edit_case_persons_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, which_type, case, item, color1, color2, color3, parent = None, flag = False):
		super(ui_edit_case_persons, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_type_c = '当事人' if which_type == 'party' else '联系人'
		self.case = case
		self.item = item
		self.headers = ['id', '当事人地位', '名称'] if self.which_type == 'party' else ['id', '身份', '名字']
		self.setWindowTitle(self.item)
		self.color1 = color1
		self.color2 = color2
		self.color3 = color3

		self.setStyleSheet("""
			QWidget {
				background-color: %s;
			}
			QTableWidget {
				border: 1px solid rgb(190, 190, 190);
				border-radius: 10px;
				background-color: %s;
			}
			QToolButton {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
				stop:0 rgb(233, 233, 233), stop:0.5 transparent);
				border: 1px solid rgb(190, 190, 190);
				border-radius: 15px;
				border-style: outset;
			}
			QTableWidget QHeaderView {
				border: 1px solid rgb(100, 100, 100);
				background-color: %s;
			}
			QToolButton::menu-indicator {
				image: none;
			}
			""" % (self.color1, self.color2, self.color3))

		def set_btn_icon(btn, icon, tooltip = ""):
			btn.setIconSize(QSize(28, 28))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.setToolTip(tooltip)
			btn.raise_()

		set_btn_icon(self.add_btn, 'msc.add', "添加")
		self.add_btn.clicked.connect(self.add_person)

		set_btn_icon(self.delete_btn, 'mdi.minus', "删除")
		self.delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.persons_view)
		newAction = QAction("删除该项", self)
		newAction.triggered.connect(self.delete_person)
		newMenu.addAction(newAction)
		self.delete_btn.setMenu(newMenu)

		set_btn_icon(self.up_down_btn, 'ph.arrows-down-up-light', "移动")
		self.up_down_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.persons_view)
		newAction = QAction("上移", self)
		newAction.triggered.connect(self.item_move_up)
		newMenu.addAction(newAction)
		newAction = QAction("下移", self)
		newAction.triggered.connect(self.item_move_down)
		newMenu.addAction(newAction)
		self.up_down_btn.setMenu(newMenu)

		if flag:
			self.close_btn.hide()
		else:
			self.close_btn.setText("继续..")
			self.close_btn.setStyleSheet("""
				font: 14pt;
				border: 1px solid rgb(190, 190, 190);
				border-radius: 5px;
				background-color: none;
				""")
			self.close_btn.clicked.connect(self.close)

		self.persons_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
		self.persons_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
			self.window_person = ui_persons(DB = self.DB, which_type = self.which_type, \
				color1 = self.color1, color2 = self.color2, color3 = self.color3, parent = self)
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
	def __init__(self, DB, which_type, color1, color2, color3, parent = None):
		super(ui_persons, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.which_type = which_type
		self.which_type_c = '当事人' if which_type == 'party' else '联系人'
		self.chosen_id = -1

		self.setStyleSheet("""
			Qwidget {
				background-color: %s;
			}
			#search_bar {
				border: 1px solid rgb(223, 223, 223);
			}
			QTableWidget {
				border: 1px solid rgb(190, 190, 190);
				border-radius: 10px;
				background-color: %s;
			}
			QTableWidget QHeaderView {
				border: 1px solid rgb(100, 100, 100);
				background-color: %s;
			}
			#add_btn {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
				stop:0 rgb(233, 233, 233), stop:0.5 transparent);
				border: 1px solid rgb(190, 190, 190);
				border-radius: 15px;
				border-style: outset;
			}
			#add_btn::menu-indicator {
				image: none;
			}
			#choose_btn {
				font: 14pt;
				border: 1px solid rgb(190, 190, 190);
				border-radius: 5px;
				background-color: none;
			}
			""" % (color1, color2, color3))
		
		newAction = QAction(self.search_bar)
		newAction.setIcon(qtawesome.icon('fa.search'))
		self.search_bar.addAction(newAction, QLineEdit.LeadingPosition)
		self.search_bar.textChanged.connect(self.results_view_refresh)

		self.add_btn.setIconSize(QSize(28, 28))
		self.add_btn.setIcon(qtawesome.icon('msc.add', color = ('black', 160)))
		self.add_btn.setToolTip("添加")
		self.add_btn.clicked.connect(self.add_person)

		self.splitter.setStretchFactor(0, 2)
		self.splitter.setStretchFactor(1, 3)

		self.results_view.itemSelectionChanged.connect(self.infos_view_refresh)
		self.infos_view.cellChanged.connect(self.edit_info)
		self.results_view_refresh()
		self.infos_view_refresh()
		self.view_menu_init()
		self.results_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.results_menu))
		self.infos_view.customContextMenuRequested.connect(partial(self.view_showmenu, self.infos_menu))

		self.results_view.itemDoubleClicked.connect(self.choose_it)
		self.choose_btn.clicked.connect(self.choose_it)
		self.setWindowTitle(f"双击选择一名{self.which_type_c}..")

	def results_view_refresh(self):
		self.search_bar.textChanged.disconnect()
		self.results_view.setRowCount(0)
		self.results_view.setColumnHidden(0, True)
		self.results_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

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
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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

class ui_today_news(QDialog, Ui_today_news_window):
	close_signal = pyqtSignal()
	def __init__(self, DB, color0, color1, color2, color3, parent = None):
		super(ui_today_news, self).__init__(parent)
		self.setupUi(self)
		self.setStyleSheet(f'background-color: {color0};')
		self.message_view.setStyleSheet(f'background-color: {color0};')
		self.message_view.setHtml(DB.generate_report_html(color1, color2, color3))

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
		self.infos_view.setColumnHidden(2, True)
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

		current_pid = self.pid
		current_class = self.which_class
		item_list = self.DB.select(f"{self.which_type}_class", 'item', 'class', current_class)

		self.infos_view.setRowCount(len(item_list))
		self.infos_view.setVerticalHeaderLabels([x['item'] for x in item_list])
		self.infos_view.verticalHeader().setMinimumWidth(120)
		all_values = self.DB.select(f"{self.which_type}_info", f"id, item, value, {self.which_type}_id", f"{self.which_type}_id", current_pid)
			
		i = 0
		for item in item_list:
			for s in all_values:
				if s['item'] == item['item']:
					self.infos_view.setItem(i, 0, QTableWidgetItem(str(s['id'])))
					self.infos_view.setItem(i, 1, QTableWidgetItem(s['value']))
					self.infos_view.setItem(i, 2, QTableWidgetItem(str(s[f"{self.which_type}_id"])))
					break
			i = i + 1

	def edit_info(self, row_n, col_n):
		self.infos_view.cellChanged.disconnect()
		if self.infos_view.selectedItems():
			new_data = self.infos_view.item(row_n, 1).text()
			pid = self.infos_view.item(row_n, 0).text()
			self.DB.update(f"{self.which_type}_info", 'id', pid, 'value', new_data)
			if row_n == 0:
				list_pid = self.infos_view.item(row_n, 2).text()
				self.DB.update(f"{self.which_type}_list", 'id', list_pid, 'name', new_data)
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
		self.infos_view.setColumnHidden(2, True)
		self.infos_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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


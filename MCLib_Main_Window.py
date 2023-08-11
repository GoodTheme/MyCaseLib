#coding=utf-8
import os
import sys
import subprocess
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from functools import partial, reduce
from datetime import datetime
from shutil import copyfile
import qtawesome

from MCLib_UI import Ui_MainWindow
from MCLib_widgets import *
if os.name == 'posix':
	from AppKit import NSApp, NSApplicationActivationPolicyAccessory, NSApplicationActivationPolicyRegular

class ui_main(QMainWindow, Ui_MainWindow):
	def __init__(self, DB, DB_PATH, VERSION, SETTING_PATH, parent = None):
		super(ui_main, self).__init__(parent)
		self.setupUi(self)
		self.DB = DB
		self.DB_PATH = DB_PATH
		self.VERSION = VERSION
		self.SETTING_PATH = SETTING_PATH
		#self.init()
		try:
			self.init()
		except:
			reply = QMessageBox.critical(self, "错误", "是否删除全部数据并初始化？", 
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
			if reply == QMessageBox.StandardButton.Yes:
				self.DB.init()
				self.init()

	# 主界面初始
	def init(self):
		self.read_profile()
		self.window_init()
		self.pages_init()
		self.p_c_tree_init()
		self.case_things_init()
		self.party_contact_init()
		self.templete_init()
		self.bar_app_init()	
		self.shortcut_init()

	def closeEvent(self, event):
		if os.name == 'posix':
			NSApp.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

	def read_profile(self):
		self.DEFAULTS = {
			'is_frameless_window': False,
			'is_show_copy_message': True,
			'default_filepath': '.',

			'color_text': '#383838', 
			'color_left_frame': '#e6e6e6', 
			'color_left_frame_selected': '#d8d8d8', 
			'color_left_frame_animation': '#aeaeae', 
			'color_left_frame_text': '#373737', 

			'color_right_frame': '#f8f8f8', 
			'color_tree': '#f8f8f8', 
			'color_table_background': '#f8f8f8', 
			'color_table_header': '#ebebeb', 
			'color_notepad': '#f8f8f8', 

			'color_menu': '#f8f8f8', 
			'color_menu_selected': '#dfdfdf', 
			'color_menu_selected_text': '#0f0f0f', 

			'color_project': '#9ED2E0', 
			'color_case_title_1': '#DF897F', 
			'color_case_title_2': '#E8DCD2', 
			'color_today_title_1': '#FFAD94', 
			'color_today_title_2': '#BADAFF', 
			'color_today_table': '#EDEEF1',

			'color_templete_frame_selected': '#d8d8d8',
			'color_party_contact_frame_selected': '#d8d8d8'
		}
		def to_bool(x):
			if x.lower() == 'true':
				return True
			elif x.lower() == 'false':
				return False
			else:
				return x

		self.profiles = {}
		for k,v in self.DEFAULTS.items():
			self.profiles[k] = v

		if not os.path.exists(self.SETTING_PATH):
			with open(self.SETTING_PATH, 'w') as f:
				f.write('')
		with open(self.SETTING_PATH, 'r') as f:
			lines = f.read().splitlines()

		for p in lines:
			self.profiles[p.split(' ')[0]] = to_bool(p.split(' ')[1])

		s = ''
		for k, v in self.profiles.items():
			s = s + f'{k} {v}\n'

		with open(self.SETTING_PATH, 'w') as f:
			f.write(s)

	def shortcut_init(self):
		self.shortcut_close = QShortcut(QKeySequence('Ctrl+W'), self)
		self.shortcut_close.activated.connect(self.close)

	# 1.0界面
	def window_init(self):
		if self.profiles['is_frameless_window']:
			self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		else:
			self.setWindowFlags(Qt.WindowType.WindowSystemMenuHint)

		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.setWindowTitle(' ')
		self.setWindowIcon(QtGui.QIcon('MCLib_icon.png'))

		self.style = f"""
			/* 全局 */
			#stylesheet {{
				background-color: none;
			}}
			QWidget {{
				font: 14px;
				color: {self.profiles['color_text']};
				border: none;
				background-color: {self.profiles['color_right_frame']};
			}}
			QMenu {{
				background-color: {self.profiles['color_menu']};
				border-radius: 4px;
			}}
			QMenu:item:selected {{
				background-color: {self.profiles['color_menu_selected']};
				color: {self.profiles['color_menu_selected_text']};
			}}
			QCalendarWidget QToolButton::menu-indicator {{
				image: none;
			}}
			QToolButton::menu-indicator {{
				image: none;
			}}
			QTableWidget {{
				background-color: {self.profiles['color_table_background']};
				color: {self.profiles['color_text']};
			}}
			QTextBrowser {{
				background-color: {self.profiles['color_table_background']};
			}}
			QDateTimeEdit {{
				background-color: {self.profiles['color_table_background']};
			}}
			QTableWidget::item {{
				padding: 6px;
				border-bottom: 1px solid rgb(190, 190, 190);
			}}
			QTableWidget::item:hover {{
				background-color: {self.profiles['color_menu_selected']};
			}}
			QTableWidget::item:selected {{
				background-color: {self.profiles['color_menu_selected']};
				color: {self.profiles['color_text']};
			}}
			QTableWidget QHeaderView {{
				border: 1px solid rgb(100, 100, 100);
				background-color: {self.profiles['color_table_header']};
			}}

			/* 左边栏 */
			#left_frame {{
				background-color: {self.profiles['color_left_frame']};
			}}
			#btn_frame {{
				background-color: none;
			}}
			#icon_label {{
				background-color: none;
			}}
			#left_frame QToolButton{{
				font: 9pt;
				color: {self.profiles['color_left_frame_text']}
			}}

			/* 项目列表 */
			#project_search_bar {{
				border: 1px solid rgb(223, 223, 223);
			}}
			#project_search_bar_frame QToolButton {{
				border: 1px solid rgb(242, 242, 242);
				background-color: rgba(200, 200, 200, 70);
			}}
			#p_c_treeview {{
				background-color: {self.profiles['color_tree']};
			}}
			#p_c_treeview::item {{
				height: 24px;
			}}
			#p_c_treeview::item:hover {{
				background-color: {self.profiles['color_menu_selected']};
			}}
			#p_c_treeview::item:selected {{
				background-color: {self.profiles['color_menu_selected']};
				color: {self.profiles['color_text']};
			}}
			#p_c_treeview::branch {{
				border: none;
			}}

			/* 案件信息 */
			#right_frame {{
				background-color: {self.profiles['color_right_frame']};
			}}
			#case_info_tab QToolButton {{
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
				stop:0 rgb(233, 233, 233), stop:0.5 transparent);
				border: 1px solid rgb(190, 190, 190);
				border-radius: 15px;
				border-style: outset;
			}}
			#note_tab {{
				background-color: rgb(240, 240, 240);
			}}
			#notepad {{
				border: 1px solid rgb(180, 180, 180);
				background-color: {self.profiles['color_notepad']};
			}}
			#right_frame QHeaderView {{
				font: 12pt;
				border: 1px solid rgb(170, 170, 170);
			}}

			/* 当事人联系人页面 */
			#party_contact_search_bar {{
				border: 1px solid rgb(203, 203, 203);
			}}
			#party_contact_top_frame {{
				border-bottom: 1px solid rgb(210, 210, 210);
			}}

			#party_contact_bottom_frame QTableWidget {{
				border: none;
			}}
			#person_list_frame QToolButton {{
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
				stop:0 rgb(233, 233, 233), stop:0.5 transparent);
				border: 1px solid rgb(190, 190, 190);
				border-radius: 15px;
				border-style: outset;
			}}
			#person_list_view::item {{
				border-bottom: none;
				color: rgba(255, 255, 255, 0);
				padding: 0px;
			}}

			#person_info_view QHeaderView {{
				font: 12pt;
				border: 1px solid rgb(170, 170, 170);
				border-top: none;
				border-bottom: none;
			}}

			/* 模板页面 */
			#templete_top_frame {{
				border-bottom: 1px solid rgb(190, 190, 190);
			}}
			#templete_page QToolButton {{
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
				stop:0 rgb(233, 233, 233), stop:0.5 transparent);
				border: 1px solid rgb(190, 190, 190);
				border-radius: 15px;
				border-style: outset;
				font: 12pt;
			}}
			#type_list_view::item {{
				border-bottom: none;
			}}
			#templete_bottom_frame QTableWidget {{
				border: 1px solid rgb(190, 190, 190);
				border-radius: 7px;
			}}

			/* 设置页面 */
			#option_table {{
				background-color: {self.profiles['color_right_frame']};
			}}
			#option_table::item {{
				border-bottom: none;
			}}
			#option_table::item:hover {{
				background-color: none;
			}}

			"""

		if self.profiles['is_frameless_window']:
			self.style += """
				/* 顶级窗口 */
				#stylesheet {
					border-radius: 10px;
				}
				#left_frame {
					border-top-left-radius: 10px;
					border-bottom-left-radius: 10px;
				}
				#btn_frame {
					border-top-left-radius: 10px;
				}
				#icon_label {
					border-top-left-radius: 10px;
				}
				#right_frame {
					border-top-right-radius: 10px;
					border-bottom-right-radius: 10px;
				}
			"""

		self.stylesheet.setStyleSheet(self.style)

		self.icon_label.setPixmap(QtGui.QIcon('MCLib_icon_transparent.png').pixmap(35, 35))
		self.left_btn_selected_stylesheet = f"""
			background-color: {self.profiles['color_left_frame_selected']};
			"""
		self.left_btn_deselected_stylesheet = """
			background-color: none;
			"""
		self.templete_top_btn_selected_stylesheet = f"""
			background-color: {self.profiles['color_templete_frame_selected']};
			"""
		self.templete_top_btn_deselected_stylesheet = """
			background-color: none;
			"""
		self.party_contact_top_btn_selected_stylesheet = f"""
			background-color: {self.profiles['color_party_contact_frame_selected']};
			"""
		self.party_contact_top_btn_deselected_stylesheet = """
			background-color: none;
			"""

		self.mouse_pos = None

	def mousePressEvent(self, event):
		self.mouse_pos = event.globalPosition()

	def mouseMoveEvent(self, event):
		if self.mouse_pos:
			diff = (event.globalPosition() - self.mouse_pos).toPoint()
			self.move(self.pos() + diff)
			self.mouse_pos = event.globalPosition()

	def mouseReleaseEvent(self, event):
		self.mouse_pos = None

	def open_dir(self, dir):
		if os.name == 'posix':
			subprocess.call(["open", dir])
		else:
			os.startfile(dir)

	# 1.0：状态栏app
	def show_main_window(self):
		if os.name == 'posix':
			NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
		self.show()
		self.raise_()

	def bar_app_init(self):
		if os.name == 'posix':
			icon = QIcon('MCLib_Bar_icon.png')
		else:
			icon = QIcon('MCLib_icon_transparent.png')
		self.tray = QSystemTrayIcon()
		self.tray.setIcon(icon)
		self.tray.setVisible(True)
		self.create_bar_menu()

	def create_bar_menu(self):
		self.bar_menu = QMenu(self)

		newAction = QAction('主界面', self)
		newAction.triggered.connect(self.show_main_window)
		self.bar_menu.addAction(newAction)
		newAction = QAction('今日简报', self)
		newAction.triggered.connect(self.show_today_news)
		self.bar_menu.addAction(newAction)
		self.bar_menu.addSeparator()

		sub_menu = self.bar_menu.addMenu('访达..')
		newAction = QAction('项目文件夹', self)
		newAction.triggered.connect(partial(self.open_dir, self.profiles['default_filepath']))
		sub_menu.addAction(newAction)

		newAction = QAction('更新列表..', self)
		newAction.triggered.connect(self.create_bar_menu)
		sub_menu.addAction(newAction)
		sub_menu.addSeparator()

		project_list = self.DB.select('project_list', 'project_name, label')
		for project in [x for x in project_list if x['label'] in '01']:
			name = project['project_name']
			name = name if len(name) <= 10 else name[:10] + "..."
			newAction = QAction(name, self)
			newAction.triggered.connect(partial(self.open_file_by_project_name, project['project_name']))
			sub_menu.addAction(newAction)
		sub_menu.addSeparator()
		for project in [x for x in project_list if x['label'] in '5']:
			name = project['project_name']
			name = name if len(name) <= 10 else name[:10] + "..."
			newAction = QAction(name, self)
			newAction.triggered.connect(partial(self.open_file_by_project_name, project['project_name']))
			sub_menu.addAction(newAction)

		self.bar_menu.addSeparator()

		newAction = QAction('退出', self)
		newAction.triggered.connect(QApplication.quit)
		self.bar_menu.addAction(newAction)

		self.tray.setContextMenu(self.bar_menu)

	# 1.0：分页
	def pages_init(self):
		def set_btn_icon(btn, icon, text):
			btn.setIconSize(QSize(35, 35))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.clicked.connect(self.left_btn_click)
			btn.setText(text)
			btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
			btn.setStyleSheet(self.left_btn_deselected_stylesheet)

		self.main_stacked_widget.setCurrentWidget(self.my_project_page)

		set_btn_icon(self.my_project_btn, 'ph.projector-screen-chart-light', 'PROJECT')
		set_btn_icon(self.case_study_btn, 'ph.books-light', 'KNOWLEDGE')
		set_btn_icon(self.party_contact_btn, 'ph.identification-card-light', 'PERSON')
		set_btn_icon(self.templete_btn, 'mdi6.format-list-bulleted-type', 'TEMPLETE')
		set_btn_icon(self.option_btn, 'ph.gear', 'OPTION')
		self.my_project_btn.setStyleSheet(self.left_btn_selected_stylesheet)

		self.animation_label = QLabel(self)
		self.animation_label.setGeometry(0, 71, 4, 50)
		self.animation_label.setStyleSheet(f"""
			background-color: {self.profiles['color_left_frame_animation']}
			""")

		self.page = 0

	def left_btn_click(self):
		btn = self.sender()
		btn_name = btn.objectName()

		if btn_name == "my_project_btn" and self.page != 0:
			self.page = 0
			self.main_stacked_widget.setCurrentWidget(self.my_project_page)
			self.project_or_study = 'project'
			self.p_c_tree_refresh()
			self.case_info_tab.tabBar().hide()
			self.project_filter_btn.show()
			self.create_project_add_btn_menu()
			self.info_view.setHtml("")
			self.info_view_edit_btn.hide()
			self.info_view_export_btn.hide()
			self.info_view_detail_btn.hide()
		elif btn_name == "case_study_btn" and self.page != 1:
			self.page = 1
			self.main_stacked_widget.setCurrentWidget(self.my_project_page)
			self.project_or_study = 'study'
			self.p_c_tree_refresh()
			self.case_info_tab.tabBar().hide()
			self.project_filter_btn.hide()
			self.create_project_add_btn_menu()
			self.info_view.setHtml("")
			self.info_view_edit_btn.hide()
			self.info_view_export_btn.hide()
			self.info_view_detail_btn.hide()
		elif btn_name == "party_contact_btn" and self.page != 2:
			self.page = 2
			self.main_stacked_widget.setCurrentWidget(self.party_contact_page)
			if self.which_type == 'party':
				self.party_btn.setStyleSheet(self.party_contact_top_btn_selected_stylesheet)
			elif self.which_type == 'contact':
				self.contact_btn.setStyleSheet(self.party_contact_top_btn_selected_stylesheet)
			self.person_list_view_refresh()
			self.person_info_view_refresh()
		elif btn_name == "templete_btn" and self.page != 3:
			self.page = 3
			self.main_stacked_widget.setCurrentWidget(self.templete_page)
			if self.which_templete == 'project':
				self.project_templete_btn.setStyleSheet(self.templete_top_btn_selected_stylesheet)
			elif self.which_templete == 'study':
				self.study_templete_btn.setStyleSheet(self.templete_top_btn_selected_stylesheet)
			elif self.which_templete == 'party':
				self.party_templete_btn.setStyleSheet(self.templete_top_btn_selected_stylesheet)
			elif self.which_templete == 'contact':
				self.contact_templete_btn.setStyleSheet(self.templete_top_btn_selected_stylesheet)
			self.type_list_view_refresh()
			self.item_list_view_refresh()
		elif btn_name == "option_btn" and self.page != 4:
			self.page = 4
			self.main_stacked_widget.setCurrentWidget(self.option_page)
			self.set_option_page()
			
		for b in self.btn_frame.findChildren(QToolButton):
			b.setStyleSheet(self.left_btn_deselected_stylesheet)
		btn.setStyleSheet(self.left_btn_selected_stylesheet)

		animation = QPropertyAnimation(self.animation_label, b"geometry", self)
		start_pos = self.animation_label.geometry()
		btn_pos = btn.geometry()
		end_pos = QRect(btn_pos.x(), btn_pos.y(), 3, btn_pos.height())
		animation.setEndValue(end_pos)
		animation.setDuration(int(abs(start_pos.y() - end_pos.y()) * 1.3) + 90)
		animation.start()

	# 初始化 page 1 & 2
	def p_c_tree_init(self):
		self.my_project_page_splitter.setStretchFactor(0, 4)
		self.my_project_page_splitter.setStretchFactor(1, 7)
		self.project_or_study = 'project'
		self.p_c_order = '升序'
		self.p_c_label = '在办'

		self.case_info_tab.tabBar().hide()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)
		self.p_c_treeview.customContextMenuRequested.connect(self.p_c_showmenu)
		self.p_c_treeview.itemDoubleClicked.connect(self.open_file)
		self.p_c_treeview.itemClicked.connect(self.p_c_tree_change_isexpanded)
		self.p_c_treeview.setExpandsOnDoubleClick(False)
		self.p_c_tree_refresh()

		self.project_filter_btn.setIconSize(QSize(20, 20))		
		self.project_filter_btn.setIcon(qtawesome.icon('mdi.filter-variant-plus'))
		self.project_filter_btn.setPopupMode(QToolButton.InstantPopup)
		self.create_project_filter_btn_menu()
		
		self.project_add_btn.setIconSize(QSize(20, 20))		
		self.project_add_btn.setIcon(qtawesome.icon('msc.add'))
		self.project_add_btn.setPopupMode(QToolButton.InstantPopup)
		self.create_project_add_btn_menu()

		newAction = QAction(self.project_search_bar)
		newAction.setIcon(qtawesome.icon('fa.search'))
		self.project_search_bar.addAction(newAction, QLineEdit.LeadingPosition)
		self.project_search_bar.textChanged.connect(self.search_result)

	def case_things_init(self):
		def set_btn_icon(btn, icon, tooltip = ""):
			btn.setIconSize(QSize(28, 28))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.setToolTip(tooltip)
			btn.raise_()

		set_btn_icon(self.info_view_edit_btn, 'ph.note-pencil-light', "编辑")
		self.info_view_edit_btn.setPopupMode(QToolButton.InstantPopup)
		self.info_view_edit_btn.hide()
		set_btn_icon(self.info_view_export_btn, 'ph.export-light', "导出/复制")
		self.info_view_export_btn.setPopupMode(QToolButton.InstantPopup)
		self.info_view_export_btn.hide()
		set_btn_icon(self.info_view_detail_btn, 'ph.magnifying-glass-plus-light', "详情")
		self.info_view_detail_btn.setPopupMode(QToolButton.InstantPopup)
		self.info_view_detail_btn.hide()

		set_btn_icon(self.todo_add_btn, 'msc.add', "添加")
		self.todo_add_btn.clicked.connect(self.add_todo)
		set_btn_icon(self.todo_export_btn, 'ph.export-light', "导出/复制")
		self.todo_export_btn.clicked.connect(self.export_todo)

		set_btn_icon(self.todo_delete_btn, 'mdi.minus', "删除")
		self.todo_delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.todo_view)
		newAction = QAction("删除该行", self)
		newAction.triggered.connect(self.delete_todo)
		newMenu.addAction(newAction)
		newAction = QAction("转为记录", self)
		newAction.triggered.connect(self.to_event)
		newMenu.addAction(newAction)
		self.todo_delete_btn.setMenu(newMenu)

		set_btn_icon(self.event_add_btn, 'msc.add', "添加")
		self.event_add_btn.clicked.connect(self.add_event)
		set_btn_icon(self.event_export_btn, 'ph.export-light')
		self.event_export_btn.clicked.connect(self.export_event)

		set_btn_icon(self.event_delete_btn, 'mdi.minus', "删除")
		self.event_delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.event_view)
		newAction = QAction("删除该行", self)
		newAction.triggered.connect(self.delete_event)
		newMenu.addAction(newAction)
		self.event_delete_btn.setMenu(newMenu)

		self.things_menu()
		self.todo_view.customContextMenuRequested.connect(partial(self.things_showmenu, self.todo_menu))
		self.event_view.customContextMenuRequested.connect(partial(self.things_showmenu, self.event_menu))	

		self.todo_view.setHorizontalHeaderLabels(['日期', '事项', 'id'])
		self.todo_view.setColumnHidden(2, True)
		self.todo_view.verticalHeader().setHidden(True)
		self.todo_view.cellChanged.connect(self.edit_todo)
		self.todo_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.todo_view.itemChanged.connect(self.todo_view.resizeRowsToContents)
		self.todo_view.setColumnWidth(0, 145)
		self.todo_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

		self.event_view.setHorizontalHeaderLabels(['日期', '事项', 'id'])
		self.event_view.setColumnHidden(2, True)
		self.event_view.verticalHeader().setHidden(True)
		self.event_view.cellChanged.connect(self.edit_event)
		self.event_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
		self.event_view.itemChanged.connect(self.event_view.resizeRowsToContents)
		self.event_view.setColumnWidth(0, 145)
		self.event_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

		self.notepad.textChanged.connect(self.notepad_input)
		self.case_info_tab.setCurrentIndex(0)

	# page 3
	def party_contact_init(self):
		self.party_contact_splitter.setStretchFactor(0, 2)
		self.party_contact_splitter.setStretchFactor(1, 3)

		self.which_type = 'party'
		self.person_list_view.setShowGrid(False)
		self.person_info_view.setShowGrid(False)

		def set_top_btn(btn, icon, text):
			btn.setIconSize(QSize(26, 26))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.clicked.connect(self.party_contact_top_btn_clicked)
			btn.setText(text)
			btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
			btn.setStyleSheet(self.party_contact_top_btn_deselected_stylesheet)

		set_top_btn(self.party_btn, 'ph.buildings', '当事人')
		set_top_btn(self.contact_btn, 'ri.contacts-line', '联系人')

		def set_btn_icon(btn, icon, tooltip = ""):
			btn.setIconSize(QSize(28, 28))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.setToolTip(tooltip)
			btn.raise_()

		set_btn_icon(self.person_list_add_btn, 'msc.add', "添加")
		self.person_list_add_btn.clicked.connect(self.add_person)

		set_btn_icon(self.person_list_delete_btn, 'mdi.minus', "删除")
		self.person_list_delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.person_list_view)
		newAction = QAction("删除该项", self)
		newAction.triggered.connect(self.delete_person)
		newMenu.addAction(newAction)
		self.person_list_delete_btn.setMenu(newMenu)

		set_btn_icon(self.person_list_export_btn, 'ph.export-light', "导出/复制")
		self.person_list_export_btn.clicked.connect(self.export_person)
		
		newAction = QAction(self.party_contact_search_bar)
		newAction.setIcon(qtawesome.icon('fa.search'))
		self.party_contact_search_bar.addAction(newAction, QLineEdit.LeadingPosition)
		self.party_contact_search_bar.textChanged.connect(self.person_list_view_refresh)
		
		self.person_info_view.setColumnHidden(0, True)
		self.person_info_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		self.person_list_view.setColumnHidden(0, True)
		self.person_list_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

		self.person_list_view.itemSelectionChanged.connect(self.person_info_view_refresh)
		self.person_info_view.cellChanged.connect(self.edit_person_info)
		self.person_list_view.customContextMenuRequested.connect(self.person_list_show_menu)

	# page 4 
	def templete_init(self):
		self.templete_splitter.setStretchFactor(0, 4)
		self.templete_splitter.setStretchFactor(1, 5)

		self.which_templete = 'project'
		self.type_list_view.setShowGrid(False)
		self.item_list_view.setShowGrid(False)

		def set_top_btn(btn, icon, text):
			btn.setIconSize(QSize(26, 26))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.clicked.connect(self.templete_top_btn_clicked)
			btn.setText(text)
			btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
			btn.setStyleSheet(self.templete_top_btn_deselected_stylesheet)

		set_top_btn(self.project_templete_btn, 'msc.archive', '项目')
		set_top_btn(self.study_templete_btn, 'msc.library', '主题')
		set_top_btn(self.party_templete_btn, 'ph.buildings', '当事人')
		set_top_btn(self.contact_templete_btn, 'ri.contacts-line', '联系人')

		def set_btn_icon(btn, icon, tooltip = ""):
			btn.setIconSize(QSize(28, 28))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.setToolTip(tooltip)
			btn.raise_()

		set_btn_icon(self.type_list_add_btn, 'msc.add', "添加")
		self.type_list_add_btn.clicked.connect(self.add_type)

		set_btn_icon(self.type_list_delete_btn, 'mdi.minus', "删除")
		self.type_list_delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.type_list_view)
		newAction = QAction("删除该项", self)
		newAction.triggered.connect(self.delete_type)
		newMenu.addAction(newAction)
		self.type_list_delete_btn.setMenu(newMenu)

		set_btn_icon(self.type_list_edit_btn, 'ph.note-pencil-light', "编辑")
		self.type_list_edit_btn.clicked.connect(self.edit_type)

		set_btn_icon(self.item_list_add_btn, 'msc.add', "添加")
		self.item_list_add_btn.clicked.connect(self.add_item)

		set_btn_icon(self.item_list_delete_btn, 'mdi.minus', "删除")
		self.item_list_delete_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.item_list_view)
		newAction = QAction("删除该项", self)
		newAction.triggered.connect(self.delete_item)
		newMenu.addAction(newAction)
		self.item_list_delete_btn.setMenu(newMenu)

		set_btn_icon(self.item_list_edit_btn, 'ph.note-pencil-light', "编辑")
		self.item_list_edit_btn.clicked.connect(self.edit_item)

		set_btn_icon(self.item_list_up_down_btn, 'ph.arrows-down-up-light', "移动")
		self.item_list_up_down_btn.setPopupMode(QToolButton.InstantPopup)
		newMenu = QMenu(self.item_list_view)
		newAction = QAction("上移", self)
		newAction.triggered.connect(self.item_move_up)
		newMenu.addAction(newAction)
		newAction = QAction("下移", self)
		newAction.triggered.connect(self.item_move_down)
		newMenu.addAction(newAction)
		self.item_list_up_down_btn.setMenu(newMenu)
		
		self.type_list_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		self.item_list_view.setColumnHidden(0, True)
		self.item_list_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		self.item_list_view.verticalHeader().setFixedWidth(60)
		self.item_list_view.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		self.type_list_view.itemSelectionChanged.connect(self.item_list_view_refresh)
		self.item_list_view.cellChanged.connect(self.edit_item)

	# 第二窗口
	def close_widgets(self):
		self.p_c_tree_refresh()
		self.case_info_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def show_execute(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		self.window_second = ui_execute(DB = self.DB, parent = self)
		self.window_second.show()
		self.window_second.close_signal.connect(self.close_widgets)

	def show_today_news(self):
		self.window_second = ui_today_news(DB = self.DB, color0 = self.profiles['color_right_frame'], \
			color1 = self.profiles['color_today_title_1'], \
			color2 = self.profiles['color_today_title_2'], color3 = self.profiles['color_today_table'], \
			parent = self)
		self.window_second.show()
		self.window_second.raise_()

	def show_person_info(self, which_type, which_class, pid):
		self.window_second = ui_person_info(DB = self.DB, which_type = which_type, \
			which_class = which_class, pid = pid, parent = self)
		self.window_second.show()
		self.window_second.close_signal.connect(self.case_info_refresh)

	def show_case_info_edit(self, case_name):
		self.window_second = ui_case_info_edit(DB = self.DB, case_name = case_name, parent = self)
		self.window_second.show()
		self.window_second.close_signal.connect(self.case_info_refresh)


	# 案件列表上方工具栏
	def create_project_filter_btn_menu(self):
		newMenu = QMenu(self.project_filter_btn)
		sub_menu = newMenu.addMenu('排序')
		sub_menu.setMinimumWidth(100)
		for s in ('升序', '降序'):
			newAction = QAction(s, self, checkable = True)
			if s == self.p_c_order:
				newAction.setChecked(True)
			newAction.triggered.connect(partial(self.change_current_order, s))
			sub_menu.addAction(newAction)
		sub_menu = newMenu.addMenu('筛选')
		sub_menu.setMinimumWidth(100)
		for s in ('全部', '在办', '搁置', '已结', '其他'):
			newAction = QAction(s, self, checkable = True)
			if s == self.p_c_label:
				newAction.setChecked(True)
			newAction.triggered.connect(partial(self.change_current_label, s))
			sub_menu.addAction(newAction)
		self.project_filter_btn.setMenu(newMenu)
		
	def create_project_add_btn_menu(self):
		newMenu = QMenu(self.project_add_btn)
		if self.project_or_study == 'project':
			newAction = QAction('新的项目', self)
		else:
			newAction = QAction('新的主题', self)
		newAction.triggered.connect(self.new_project)
		newMenu.addAction(newAction)
		if self.project_or_study == 'project':
			newAction = QAction('新的案件', self)
		else:
			newAction = QAction('新的案例', self)
		newAction.triggered.connect(self.new_case)
		newMenu.addAction(newAction)
		self.project_add_btn.setMenu(newMenu)

	def change_current_order(self, current_order):
		self.p_c_order = current_order
		self.p_c_tree_refresh()
		self.create_project_filter_btn_menu()

	def change_current_label(self, current_label):
		self.p_c_label = current_label
		self.p_c_tree_refresh()
		self.create_project_filter_btn_menu()

	def search_result(self):
		self.project_search_bar.textChanged.disconnect()
		keywords = self.project_search_bar.text()
		if keywords == 'execute_':
			self.show_execute()
		else:
			self.p_c_tree_refresh()
		self.project_search_bar.textChanged.connect(self.search_result)

	# 项目/案件列表
	def trans(self, s):
		if not s:
			return ''
		trans = ''
		for t in str(s):
			trans = trans + t if t != "'" else trans + "''"
		return trans
	
	def p_c_tree_fold(self, current_item = None):
		root = self.p_c_treeview.invisibleRootItem()
		for i in range(root.childCount()):
			item = root.child(i)
			if item != current_item:
				item.setExpanded(False)

	def p_c_tree_expanded(self, project_name):
		root = self.p_c_treeview.invisibleRootItem()
		for i in range(root.childCount()):
			if root.child(i).text(0) == project_name:
				root.child(i).setExpanded(True)

	def p_c_tree_change_isexpanded(self):
		current = self.p_c_treeview.currentIndex()
		if not current.parent().data():
			current_item = self.p_c_treeview.currentItem()
			if current_item.isExpanded():
				current_item.setExpanded(False)
			else:
				self.p_c_tree_fold(current_item)
				current_item.setExpanded(True)

	def set_label(self, label):
		current_project = self.p_c_treeview.currentIndex().data()
		self.DB.update('project_list', 'project_name', current_project, 'label', str(label))
		self.p_c_tree_refresh()
		self.p_c_tree_expanded(current_project)

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
			self.open_dir(project_path)

	def open_file_by_project_name(self, project_name):
		if self.DB.select('project_list', 'file_path', 'project_name', project_name):
			project_path = self.DB.select('project_list', 'file_path', 'project_name', 
				project_name)[0]['file_path']
			if project_path:
				self.open_dir(project_path)

	def p_c_showmenu(self):
		localpos = self.p_c_treeview.mapFromGlobal(QCursor().pos())
		if self.p_c_treeview.itemAt(localpos):
			self.p_c_tree_menu()
			self.p_c_menu.move(QCursor().pos())
			self.p_c_menu.show()
	
	def p_c_tree_refresh(self):
		keywords = self.project_search_bar.text()
		current_label = self.p_c_label
		current_order = {'升序': 'id asc', '降序': 'id desc',}[self.p_c_order]

		self.p_c_treeview.clear()
		self.p_c_treeview.setColumnCount(1)
		projects = self.DB.select_by_order('project_list', 'project_name, label', current_order)
		project_list = []
		for project in projects:
			if self.project_or_study == 'project' and current_label == '全部' and project['label'] == '0' \
			or self.project_or_study == 'project' and current_label == '在办' and project['label'] == '0':
				project_list.append(project)
		for project in projects:
			if self.project_or_study == 'project' and current_label == '全部' and project['label'] in '1234' \
			or self.project_or_study == 'project' and current_label == '在办' and project['label'] == '1' \
			or self.project_or_study == 'project' and current_label == '搁置' and project['label'] == '2' \
			or self.project_or_study == 'project' and current_label == '已结' and project['label'] == '3' \
			or self.project_or_study == 'project' and current_label == '其他' and project['label'] == '4' \
			or self.project_or_study == 'study' and project['label'] == '5':
				project_list.append(project)

		for project in project_list:
			if keywords:
				case_selected = []
				case_list = self.DB.select('case_list', 'case_name', 'project_name', project['project_name'])
				for case in case_list:
					case_infos = self.DB.select_all('case_info', 'case_name', case['case_name'])
					flag = False
					if isinstance(project['project_name'], str) and project['project_name'].find(keywords) != -1:
						flag = True
					elif isinstance(case['case_name'], str) and case['case_name'].find(keywords) != -1:
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

				todos = self.DB.select('todo_list', 'case_name, date, things', 
					'project_name', project['project_name'])
				for todo in todos:
					if (isinstance(todo['date'], str) and todo['date'].find(keywords) != -1) \
					or (isinstance(todo['things'], str) and todo['things'].find(keywords) != -1):
						if {'case_name': todo['case_name']} not in case_selected:
							case_selected.append({'case_name': todo['case_name']})

				events = self.DB.select('event_list', 'case_name, date, things', 
					'project_name', project['project_name'])
				for event in events:
					if (isinstance(event['date'], str) and event['date'].find(keywords) != -1) \
					or (isinstance(event['things'], str) and event['things'].find(keywords) != -1):
						if {'case_name': event['case_name']} not in case_selected:
							case_selected.append({'case_name': event['case_name']})

				notes = self.DB.select('case_list', 'case_name, notepad_text', 
					'project_name', project['project_name'])
				for note in notes:
					if isinstance(note['notepad_text'], str) and note['notepad_text'].find(keywords) != -1:
						if {'case_name': note['case_name']} not in case_selected:
							case_selected.append({'case_name': note['case_name']})

				if case_selected:
					root = QTreeWidgetItem(self.p_c_treeview)
					root.setText(0, project['project_name'])
					if project['label'] == '0':
						root.setIcon(0, qtawesome.icon('mdi.arrow-collapse-up'))
					for case in case_selected:
						child = QTreeWidgetItem(root)
						child.setText(0, case['case_name'])
					root.setExpanded(True)

			else:
				root = QTreeWidgetItem(self.p_c_treeview)
				root.setText(0, project['project_name'])
				if project['label'] == '0':
					root.setIcon(0, qtawesome.icon('mdi.arrow-collapse-up'))
				case_list = self.DB.select('case_list', 'case_name', 'project_name', project['project_name'])
				for case in case_list:
					child = QTreeWidgetItem(root)
					child.setText(0, case['case_name'])

		self.p_c_treeview.setStyle(QStyleFactory.create('windows'))

	def p_c_tree_menu(self):
		self.p_c_menu = QMenu(self.p_c_treeview)
		if not self.p_c_treeview.currentIndex().parent().data():
			current_project = self.p_c_treeview.currentIndex().data()
			if self.project_or_study == 'project':
				newAction = QAction('新的案件', self)
			else:
				newAction = QAction('新的案例', self)
			newAction.triggered.connect(partial(self.new_case, current_project))
			self.p_c_menu.addAction(newAction)
			self.p_c_menu.addSeparator()

			sub_menu = self.p_c_menu.addMenu('编辑')
			sub_menu.setMinimumWidth(100)
			if self.project_or_study == 'project':
				newAction = QAction('项目名', self)
			else:
				newAction = QAction('主题名', self)
			newAction.triggered.connect(self.edit_project_name)
			sub_menu.addAction(newAction)
			if self.project_or_study == 'project':
				newAction = QAction('项目号', self)
			else:
				newAction = QAction('备注', self)
			newAction.triggered.connect(self.edit_project_num)
			sub_menu.addAction(newAction)
			newAction = QAction('文件夹', self)
			newAction.triggered.connect(self.edit_project_path)
			sub_menu.addAction(newAction)

			if self.project_or_study == 'project':
				sub_menu = self.p_c_menu.addMenu('设置标签')
				sub_menu.setMinimumWidth(100)
				labels = ['置顶', '在办', '搁置', '已结', '其他']
				for i in range(5):
					current_label = self.DB.select('project_list', 'label', 'project_name', current_project)[0]['label']
					newAction = QAction(labels[i], self, checkable = True)
					if str(i) == current_label:
						newAction.setChecked(True)
					newAction.triggered.connect(partial(self.set_label, i))
					sub_menu.addAction(newAction)
			
			newAction = QAction('删除', self)
			newAction.triggered.connect(self.delete_project)
			self.p_c_menu.addAction(newAction)

		elif self.p_c_treeview.currentIndex().parent().data():
			current_project = self.p_c_treeview.currentIndex().parent().data()
			if self.project_or_study == 'project':
				newAction = QAction('新的案件', self)
			else:
				newAction = QAction('新的案例', self)
			newAction.triggered.connect(partial(self.new_case, current_project))
			self.p_c_menu.addAction(newAction)
			self.p_c_menu.addSeparator()

			sub_menu = self.p_c_menu.addMenu('编辑')
			sub_menu.setMinimumWidth(100)

			case = self.p_c_treeview.currentIndex().data()
			if self.project_or_study == 'project':
				newAction = QAction('案件名', self)
			else:
				newAction = QAction("案例名", self)
			newAction.triggered.connect(partial(self.edit_case_name, case))
			sub_menu.addAction(newAction)
			
			newAction = QAction('基本信息', self)	
			newAction.triggered.connect(partial(self.show_case_info_edit, case))
			sub_menu.addAction(newAction)

			case_type = self.DB.select('case_list', 'case_type', 'case_name', case)[0]['case_type']
			items = self.DB.select('case_type', 'item, item_form', 'type_name', case_type)
			
			for s in items:
				if s['item_form'] != 'text':
					newAction = QAction(s['item'], self)
					newAction.triggered.connect(partial(self.edit_case_value, case, s['item'], s['item_form']))
					sub_menu.addAction(newAction)

			if self.project_or_study == 'project':
				newAction = QAction('变更至项目', self)
			else:
				newAction = QAction('变更至主题', self)
			newAction.triggered.connect(self.change_project)
			self.p_c_menu.addAction(newAction)

			self.p_c_menu.addSeparator()
			newAction = QAction('删除案件', self)
			newAction.triggered.connect(self.delete_case)
			self.p_c_menu.addAction(newAction)

	# 修改项目
	def new_project(self):
		if self.project_or_study == 'project':
			project_name, flag = QInputDialog.getText(self, "新的项目", "输入项目名：")
		else:
			project_name, flag = QInputDialog.getText(self, "新的主题", "输入主题名：")

		if flag:
			projects = [p['project_name'] for p in self.DB.select('project_list', 'project_name')]
			if project_name and project_name not in projects:
				if self.project_or_study == 'project':
					project_num, flag2 = QInputDialog.getText(self, "项目号", "请输入新的项目号：")
				else:
					project_num, flag2 = QInputDialog.getText(self, "备注", "请输入新的备注内容：")

				reply = QMessageBox.question(self, "文件夹", "选择保存的文件夹", 
					QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
				if reply != 65536:
					project_path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.profiles['default_filepath'])
				else:
					project_path = ''
				
				if self.project_or_study == 'project':
					project_label = {'全部': '1', '在办': '1', '搁置': '2', '已结': '3', '其他': '4'}[self.p_c_label]
				else:
					project_label = '5'

				self.DB.new_project(project_name, project_num, project_path, project_label)
				self.p_c_tree_refresh()
			else:
				QMessageBox.warning(self, "错误", "与现有名称重复。")

	def edit_project_name(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.project_or_study == 'project':
			new_project_name, flag = QInputDialog.getText(self, "项目名", "请输入新的项目名：")
		else:
			new_project_name, flag = QInputDialog.getText(self, "主题名", "请输入新的主题名：")
		if flag and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			try:
				self.DB.rename_project(current_project, new_project_name)
			except:
				QMessageBox.warning(self, "错误", "与现有名称重复。")
			finally:
				self.p_c_tree_refresh()
				self.case_info_refresh()
				self.p_c_tree_expanded(new_project_name)
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def edit_project_num(self):
		if self.project_or_study == 'project':
			new_project_num, flag = QInputDialog.getText(self, "项目号", "请输入新的项目号：")
		else:
			new_project_num, flag = QInputDialog.getText(self, "备注", "请输入新的备注内容：")
		if flag and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			self.DB.update('project_list', 'project_name', current_project, 'project_num', new_project_num)
			self.case_info_refresh()

	def edit_project_path(self):
		new_project_path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.profiles['default_filepath'])
		if new_project_path and self.p_c_treeview.currentIndex():
			current_project = self.p_c_treeview.currentIndex().data()
			self.DB.update('project_list', 'project_name', current_project, 'file_path', new_project_path)

	def delete_project(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data():
			if self.p_c_treeview.currentIndex().parent().data():
				current_project = self.p_c_treeview.currentIndex().parent().data()
			else:
				current_project = self.p_c_treeview.currentIndex().data()
			reply = QMessageBox.warning(self, "删除项目", f"是否删除“{current_project}”项目？\n"\
				f"将会删除对应的案件。", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
			if reply == QMessageBox.StandardButton.Yes:
				self.DB.delete_project(current_project)
				self.p_c_tree_refresh()
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	# 修改案件
	def new_case(self, project_name = None):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		title = '新的案件' if self.project_or_study == 'project' else '新的案例'
		if not project_name:
			projects = []
			project_list = self.DB.select('project_list', 'project_name, label')
			current_label = self.p_c_label
			for project in project_list:
				project_label = project['label']
				if self.project_or_study == 'project' and current_label == '全部' and project_label in '01234' \
				or self.project_or_study == 'project' and current_label == '在办' and project_label in '01' \
				or self.project_or_study == 'project' and current_label == '搁置' and project_label in '2' \
				or self.project_or_study == 'project' and current_label == '已结' and project_label in '3' \
				or self.project_or_study == 'project' and current_label == '其他' and project_label in '4' \
				or self.project_or_study == 'study' and project_label in '5':
					projects.append(project['project_name'])
			if self.project_or_study == 'project':
				project_name, flag = QInputDialog.getItem(self, title, "从该项目中新建：", projects, 0, False)
			else:
				project_name, flag = QInputDialog.getItem(self, title, "从该主题中新建：", projects, 0, False)
		else:
			flag = True

		if flag:
			case_name, flag2 = QInputDialog.getText(self, title, "输入案件名：")
			if flag2 and case_name:
				cases = [x['case_name'] for x in self.DB.select('case_list', 'case_name')]
				if case_name in cases:
					QMessageBox.warning(self, "错误", "该案件已存在。")
				else:
					types = [x['type_name'] for x in self.DB.select('type_list', 'type_name', 'projectorstudy', self.project_or_study)]
					case_type, flag3 = QInputDialog.getItem(self, title, "选择案件模板：", types, 0, False)
					if flag3:
						self.DB.new_case(project_name, case_name, case_type)
						reply = QMessageBox.question(self, title, "是否开始输入案件信息？\n"\
							"（任意时刻退出将中止输入）", 
							QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
							
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
									self.window_second = ui_edit_case_persons(DB = self.DB, \
										which_type = item_form, case = case_name, item = item, \
										color1 = self.profiles['color_right_frame'], \
										color2 = self.profiles['color_table_background'], \
										color3 = self.profiles['color_table_header'])
									self.window_second.exec()
						self.p_c_tree_refresh()
						self.p_c_tree_expanded(project_name)

		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)
		
	def delete_case(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			project_name = self.p_c_treeview.currentIndex().parent().data()
			current_case = self.p_c_treeview.currentIndex().data()
			reply = QMessageBox.warning(self, "删除案件", f"是否删除“{current_case}”案件？", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
			if reply == QMessageBox.StandardButton.Yes:
				self.DB.delete_case(current_case)
				self.p_c_tree_refresh()
				self.p_c_tree_expanded(project_name)
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)
		
	def change_project(self):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			current_case = self.p_c_treeview.currentIndex().data()
			current_project = self.p_c_treeview.currentIndex().parent().data()
			project_list = self.DB.select('project_list', 'project_name, label', 'project_name', 
				current_project, '!=')
			if self.project_or_study == 'project':
				projects = [p['project_name'] for p in project_list if p['label'] in '01234']
			else:
				projects = [p['project_name'] for p in project_list if p['label'] == '5']
			if projects:
				new_project, flag = QInputDialog.getItem(self, current_case, 
					"更换至项目：", projects, 0, False)
				if flag:
					self.DB.change_project(current_case, current_project, new_project)
					self.p_c_tree_refresh()
					self.case_info_refresh()
					self.p_c_tree_expanded(new_project)
		self.p_c_treeview.itemSelectionChanged.connect(self.case_things_refresh)

	def edit_case_name(self, n_name):
		self.p_c_treeview.itemSelectionChanged.disconnect()
		if self.p_c_treeview.currentIndex().data() and self.p_c_treeview.currentIndex().parent().data():
			project_name = self.p_c_treeview.currentIndex().parent().data()
			case_name, flag = QInputDialog.getText(self, "案件名", "请输入新案件名：")
			if flag and case_name:
				cases = [x['case_name'] for x in self.DB.select('case_list', 'case_name')]
				if case_name in cases:
					QMessageBox.warning(self, "错误", "该案件已存在。")
				else:
					self.DB.rename_case(n_name, case_name)
					self.p_c_tree_refresh()
					self.case_info_refresh()
					self.p_c_tree_expanded(project_name)
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
			self.window_second = ui_edit_case_persons(DB = self.DB, \
				which_type = item_form, case = case, item = item, flag = True, \
				color1 = self.profiles['color_right_frame'], \
				color2 = self.profiles['color_table_background'], \
				color3 = self.profiles['color_table_header'])
			self.window_second.show()
			self.window_second.close_signal.connect(self.case_info_refresh)
	
	# 案件信息显示
	def create_case_info_btn_menu(self):
		self.info_view_edit_btn.show()
		self.info_view_export_btn.show()

		# button_1
		newMenu = QMenu(self.info_view)
		newMenu.setMinimumWidth(120)
		if self.p_c_treeview.currentIndex().parent().data():
			case = self.p_c_treeview.currentIndex().data()
			if self.project_or_study == 'project':
				newAction = QAction("修改案件名", self)
			else:
				newAction = QAction("修改案例名", self)
			newAction.triggered.connect(partial(self.edit_case_name, case))
			newMenu.addAction(newAction)

			if self.project_or_study == 'project':
				newAction = QAction('变更至项目', self)
			else:
				newAction = QAction('变更至主题', self)
			newAction.triggered.connect(self.change_project)
			newMenu.addAction(newAction)
			newMenu.addSeparator()

			if self.project_or_study == 'study':
				newAction = QAction('编辑基本信息', self)	
				newAction.triggered.connect(partial(self.show_case_info_edit, case))
				newMenu.addAction(newAction)
				newMenu.addSeparator()
			
			case_type = self.DB.select('case_list', 'case_type', 'case_name', case)[0]['case_type']
			items = self.DB.select('case_type', 'item, item_form', 'type_name', case_type)
			actions = []
			for s in items:
				if s['item_form'] != 'text':
					actions.append(s)
			if actions:
				sub_menu = newMenu.addMenu('编辑..')
				sub_menu.setMinimumWidth(100)
				for s in actions:
					if s['item_form'] != 'text':
						newAction = QAction(s['item'], self)
						newAction.triggered.connect(partial(self.edit_case_value, case, s['item'], s['item_form']))
						sub_menu.addAction(newAction)
				newMenu.addSeparator()

			newAction = QAction('删除案件', self)
			newAction.triggered.connect(self.delete_case)
			newMenu.addAction(newAction)

		else:
			project = self.p_c_treeview.currentIndex().data()
			sub_menu = newMenu.addMenu('修改..')
			sub_menu.setMinimumWidth(100)
			if self.project_or_study == 'project':
				newAction = QAction('项目名', self)
			else:
				newAction = QAction('主题名', self)
			newAction.triggered.connect(self.edit_project_name)
			sub_menu.addAction(newAction)
			if self.project_or_study == 'project':
				newAction = QAction('项目号', self)
			else:
				newAction = QAction('备注', self)
			newAction.triggered.connect(self.edit_project_num)
			sub_menu.addAction(newAction)
			newAction = QAction('文件夹', self)
			newAction.triggered.connect(self.edit_project_path)
			sub_menu.addAction(newAction)

			newMenu.addSeparator()
			if self.project_or_study == 'project':
				sub_menu = newMenu.addMenu('设置标签')
				sub_menu.setMinimumWidth(100)
				labels = ['置顶', '在办', '搁置', '已结', '其他']
				for i in range(5):
					current_label = self.DB.select('project_list', 'label', 'project_name', project)[0]['label']
					newAction = QAction(labels[i], self, checkable = True)
					if str(i) == current_label:
						newAction.setChecked(True)
					newAction.triggered.connect(partial(self.set_label, i))
					sub_menu.addAction(newAction)

			if self.project_or_study == 'project':
				newAction = QAction('删除项目', self)
			else:
				newAction = QAction('删除主题',self)
			newAction.triggered.connect(self.delete_project)
			newMenu.addAction(newAction)

		self.info_view_edit_btn.setMenu(newMenu)

		# button_2
		newMenu = QMenu(self.info_view)
		if self.project_or_study == 'project' and self.p_c_treeview.currentIndex().parent().data():
			case = self.p_c_treeview.currentIndex().data()
			sub_menu = newMenu.addMenu('案件信息..')
			sub_menu.setMinimumWidth(100)
			newAction = QAction("不含简称", self)
			newAction.triggered.connect(partial(self.copy_case_info, case, False))
			sub_menu.addAction(newAction)
			newAction = QAction("含简称", self)
			newAction.triggered.connect(partial(self.copy_case_info, case, True))
			sub_menu.addAction(newAction)
			newMenu.addSeparator()

			sub_menu = newMenu.addMenu('当事人..')
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

			sub_menu = newMenu.addMenu('邮寄地址..')
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

		else:
			if self.project_or_study == 'project':
				newAction = QAction("导出项目", self)
			else:
				newAction = QAction("导出主题", self)
			if self.p_c_treeview.currentIndex().parent().data():
				project = self.p_c_treeview.currentIndex().parent().data()
			else:
				project = self.p_c_treeview.currentIndex().data()
			newAction.triggered.connect(partial(self.copy_project_info_all, project))
			newMenu.addAction(newAction)

		self.info_view_export_btn.setMenu(newMenu)

		# button_3
		if self.project_or_study == 'project' and self.p_c_treeview.currentIndex().parent().data():
			newMenu = QMenu(self.info_view)
			newAction = QAction('基本信息', self)	
			newAction.triggered.connect(partial(self.show_case_info_edit, case))
			newMenu.addAction(newAction)
			newMenu.addSeparator()

			sub_menu = newMenu.addMenu('当事人..')
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
				sub_menu.addAction(QAction("（无）", self))

			sub_menu = newMenu.addMenu('联系人..')
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
				sub_menu.addAction(QAction("（无）", self))

			self.info_view_detail_btn.show()
			self.info_view_detail_btn.setMenu(newMenu)
		else:
			self.info_view_detail_btn.hide()

	def case_things_refresh(self):
		self.case_info_refresh()
		self.things_refresh()
		self.notepad_refresh()
		current = self.p_c_treeview.currentIndex()
		if self.project_or_study == 'project' and current.parent().data():
			self.case_info_tab.tabBar().show()
	
		else:
			self.case_info_tab.setCurrentIndex(0)
			self.case_info_tab.tabBar().hide()
		self.create_case_info_btn_menu()

	def copy_mail_address(self, pid):
		s = self.DB.generate_mail_address(pid)
		if self.profiles['is_show_copy_message']:
			reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板：\n\n{s}", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)
		else:
			QApplication.clipboard().setText(s)

	def copy_party_info_all(self, case):
		s = ''
		values = self.DB.select_multi_condition('case_info', 'value, value2', f"case_name = '{self.trans(case)}' "\
			f"and value_form = 'party'")
		values_uni = [[x['value'], x['value2']] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + values)]
		for party, pid in values_uni:
			s = s + f"{party}：{self.DB.generate_party_info(pid)}\n"
		if self.profiles['is_show_copy_message']:
			reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板：\n\n{s}", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)
		else:
			QApplication.clipboard().setText(s)

	def copy_party_info(self, status, pid):
		s = f"{status}：{self.DB.generate_party_info(pid)}"
		if self.profiles['is_show_copy_message']:
			reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板：\n\n{s}", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)
		else:
			QApplication.clipboard().setText(s)

	def copy_case_info(self, case, abbr):
		s = self.DB.generate_case_info(case, abbr)
		if self.profiles['is_show_copy_message']:
			reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板：\n\n{s}", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)
		else:
			QApplication.clipboard().setText(s)

	def copy_project_info_all(self, project):
		s = self.DB.generate_project_info_all(project)
		if self.profiles['is_show_copy_message']:
			t = "项目" if self.project_or_study == 'project' else "主题"
			reply = QMessageBox.question(self, "导出信息", f"将复制全部{t}内容，可粘贴于表格内。", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)
		else:
			QApplication.clipboard().setText(s)

	def case_info_refresh(self):
		current = self.p_c_treeview.currentIndex()
		if current.parent().data():
			case = current.data()
			self.info_view.setHtml(self.DB.generate_case_info_html(case, self.profiles['color_case_title_1'], self.profiles['color_case_title_2']))

		elif current.data():
			project = current.data()
			self.info_view.setHtml(self.DB.generate_project_info_html(project, self.project_or_study, self.profiles['color_project']))

	def things_refresh(self):
		self.todo_view.cellChanged.disconnect()
		self.event_view.cellChanged.disconnect()
		self.todo_view.setRowCount(0)
		self.event_view.setRowCount(0)

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
		if self.todo_view.selectedItems() and current.parent().data():
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

	def export_todo(self):
		if self.p_c_treeview.currentIndex().parent().data():
			case = self.p_c_treeview.currentIndex().data()
			s = self.DB.generate_todo_info(case)
			if self.profiles['is_show_copy_message']:
				reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板，可粘贴于表格：\n\n{s}", 
					QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
				if reply != 65536:
					QApplication.clipboard().setText(s)
			else:
				QApplication.clipboard().setText(s)

	def export_event(self):
		if self.p_c_treeview.currentIndex().parent().data():
			case = self.p_c_treeview.currentIndex().data()
			s = self.DB.generate_event_info(case)
			if self.profiles['is_show_copy_message']:
				reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板，可粘贴于表格：\n\n{s}", 
					QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
				if reply != 65536:
					QApplication.clipboard().setText(s)
			else:
				QApplication.clipboard().setText(s)


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

	# 当事人联系人页面
	def party_contact_top_btn_clicked(self):
		btn = self.sender()
		self.which_type = 'party' if btn.objectName() == 'party_btn' else 'contact'
		
		for b in self.party_contact_top_frame.findChildren(QToolButton):
			b.setStyleSheet(self.party_contact_top_btn_deselected_stylesheet)
		btn.setStyleSheet(self.party_contact_top_btn_selected_stylesheet)

		self.person_list_view_refresh()
		self.person_info_view_refresh()

	def person_list_view_refresh(self):
		self.party_contact_search_bar.textChanged.disconnect()
		self.person_list_view.setRowCount(0)

		keywords = self.party_contact_search_bar.text()
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
			rows = self.person_list_view.rowCount()
			self.person_list_view.insertRow(rows)
			self.person_list_view.setItem(rows, 0, QTableWidgetItem(str(k['id'])))
			self.person_list_view.setItem(rows, 1, QTableWidgetItem(k['name']))

			label = QLabel()
			label.setStyleSheet("background: none; padding: 0px; padding-left: 4px;")
			s = f"""
				<head>
				<style>
				p1 {{
				font-size: 14px;
				}}
				p2 {{
				color: rgba(20, 20, 20, 70);
				font-size: 10px;
				}}
				</style>
				</head>
				<body>
				<p1>{k['name']}</p1> <p2>({k['class']})</p2>
				</body>
			"""
			label.setText(s)
			self.person_list_view.setCellWidget(rows, 1, label)

		self.party_contact_search_bar.textChanged.connect(self.person_list_view_refresh)

	def person_info_view_refresh(self):
		self.person_info_view.setRowCount(0)
		if self.person_list_view.selectedItems():
			self.person_info_view.verticalHeader().setHidden(False)
			c_row = self.person_list_view.currentRow()
			current_pid = self.person_list_view.item(c_row, 0).text()
			current_class = self.DB.select(f"{self.which_type}_list", 'class', 'id', current_pid)[0]['class']
			item_list = self.DB.select(f"{self.which_type}_class", 'item', 'class', current_class)

			self.person_info_view.setRowCount(len(item_list))
			self.person_info_view.setVerticalHeaderLabels([x['item'] for x in item_list])
			self.person_info_view.verticalHeader().setMinimumWidth(120)
			all_values = self.DB.select(f"{self.which_type}_info", 'id, item, value', f"{self.which_type}_id", current_pid)
			
			i = 0
			for item in item_list:
				for s in all_values:
					if s['item'] == item['item']:
						self.person_info_view.setItem(i, 0, QTableWidgetItem(str(s['id'])))
						self.person_info_view.setItem(i, 1, QTableWidgetItem(s['value']))
						break
				i = i + 1
		else:
			self.person_info_view.verticalHeader().setHidden(True)

	def add_person(self):
		self.person_list_view.itemSelectionChanged.disconnect()
		which_type_c = "当事人" if self.which_type == 'party' else "联系人"
		class_list = self.DB.select(f"{self.which_type}_class", 'class')
		class_list_uni = [x['class'] for x in reduce(lambda x, y: x if y in x else x + [y], [[]] + class_list)]
		which_class, flag = QInputDialog.getItem(self, which_type_c, f"请选择{which_type_c}类别", 
			class_list_uni, 0, False)
		if flag:
			name, flag2 = QInputDialog.getText(self, f"新的{which_type_c}", 
				f"请输入该{which_type_c}的名字：")
			if flag2:
				self.DB.new_person(self.which_type, which_class, name)
				self.person_list_view_refresh()
		self.person_list_view.itemSelectionChanged.connect(self.person_info_view_refresh)

	def delete_person(self):
		if self.person_list_view.selectedItems():
			pid = self.person_list_view.item(self.person_list_view.currentRow(), 0).text()
			self.DB.delete_person(self.which_type, pid)
			self.person_list_view_refresh()

	def edit_person_info(self, row_n, col_n):
		self.person_info_view.cellChanged.disconnect()
		if self.person_info_view.selectedItems():
			pid = self.person_info_view.item(row_n, 0).text()
			new_data = self.person_info_view.item(row_n, 1).text()
			self.DB.update(f"{self.which_type}_info", 'id', pid, 'value', new_data)
			self.person_info_view_refresh()
			if row_n == 0:
				self.person_list_view.itemSelectionChanged.disconnect()
				list_pid = self.person_list_view.item(self.person_list_view.currentRow(), 0).text()
				self.DB.update(f"{self.which_type}_list", 'id', list_pid, 'name', new_data)
				self.person_list_view_refresh()
				self.person_info_view_refresh()
				self.person_list_view.itemSelectionChanged.connect(self.person_info_view_refresh)
		self.person_info_view.cellChanged.connect(self.edit_person_info)

	def export_person(self):
		if self.person_list_view.selectedItems():
			pid = self.person_list_view.item(self.person_list_view.currentRow(), 0).text()
			infos = self.DB.select(f"{self.which_type}_info", "item, value", f"{self.which_type}_id", pid)
			s = ''
			for x in infos:
				if x['value']:
					s = s + f"{x['item']}：{x['value']}\n"
			reply = QMessageBox.question(self, "导出信息", f"复制以下内容至剪贴板：\n{s}", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
			if reply != 65536:
				QApplication.clipboard().setText(s)

	def person_list_show_menu(self):
		newMenu = QMenu(self.person_list_view)
		newAction = QAction('复制', self)
		newAction.triggered.connect(self.export_person)
		newMenu.addAction(newAction)
		newAction = QAction('删除', self)
		newAction.triggered.connect(self.delete_person)
		newMenu.addAction(newAction)
		newMenu.move(QCursor().pos())
		newMenu.show()

	# 模板
	def templete_top_btn_clicked(self):
		btn = self.sender()
		self.which_templete = btn.objectName().replace('_templete_btn', '')

		for b in self.templete_top_frame.findChildren(QToolButton):
			b.setStyleSheet(self.templete_top_btn_deselected_stylesheet)
		btn.setStyleSheet(self.templete_top_btn_selected_stylesheet)

		self.type_list_view_refresh()
		self.item_list_view_refresh()

	def type_list_view_refresh(self):
		self.type_list_view.setRowCount(0)

		if self.which_templete in ('project', 'study'):
			type_list = self.DB.select('type_list', 'type_name', 'projectorstudy', self.which_templete)
			for k in type_list:
				rows = self.type_list_view.rowCount()
				self.type_list_view.insertRow(rows)
				self.type_list_view.setItem(rows, 0, QTableWidgetItem(k['type_name']))

		elif self.which_templete in ('party', 'contact'):
			type_list = self.DB.select(f"{self.which_templete}_class", 'class')
			for k in reduce(lambda x, y: x if y in x else x + [y], [[]] + type_list):
				rows = self.type_list_view.rowCount()
				self.type_list_view.insertRow(rows)
				self.type_list_view.setItem(rows, 0, QTableWidgetItem(k['class']))

	def item_list_view_refresh(self):
		self.item_list_view.setRowCount(0)

		if self.type_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			table_name = 'case_type' if self.which_templete in ('project', 'study') else f"{self.which_templete}_class"
			col_name = 'type_name' if self.which_templete in ('project', 'study') else 'class'
			
			item_list = self.DB.select(table_name, 'id, item', col_name, current_type)
			for k in item_list:
				rows = self.item_list_view.rowCount()
				self.item_list_view.insertRow(rows)
				self.item_list_view.setItem(rows, 0, QTableWidgetItem(str(k['id'])))
				self.item_list_view.setItem(rows, 1, QTableWidgetItem(k['item']))
		else:
			self.item_list_view.verticalHeader().setHidden(True)

	def add_type(self):
		if self.which_templete in ('project', 'study'):
			new_type_name, flag = QInputDialog.getText(self, "新的类型", "请输入新的类型名称：")
			if flag:
				try:
					self.DB.new_type(new_type_name, self.which_templete)
				except:
					QMessageBox.warning(self, "错误", "该类型已存在。")
				else:
					self.type_list_view_refresh()

		elif self.which_templete in ('party', 'contact'):
			new_class_name, flag = QInputDialog.getText(self, "新的类别", "请输入新的类别名称：")
			if flag:
				if new_class_name in [p['class'] for p in self.DB.select(f"{self.which_templete}_class", 'class')]:
					QMessageBox.warning(self, "错误", "该类别已存在。")
				else:
					fisrt_item_name, flag2 = QInputDialog.getText(self, "基础信息", f"请输入“{new_class_name}”中"\
						f"用于标识个体的信息名，例如“名称”：")
					if flag2:
						self.DB.new_party_contact_class(self.which_templete, new_class_name, fisrt_item_name)
						self.type_list_view_refresh()

	def delete_type(self):
		if self.type_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			if self.which_templete in ('project', 'study'):
				reply = QMessageBox.warning(self, "删除类型", f"是否删除名为“{current_type}”的类型？\n"\
					f"将会删除对应的案件。", \
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.DB.delete_type(current_type)
					self.type_list_view_refresh()

			elif self.which_templete in ('party', 'contact'):
				t = "当事人" if self.which_templete == 'party' else "联系人"
				reply = QMessageBox.warning(self, "删除类别", f"是否删除名为“{current_type}”的类型？\n"\
					f"将会删除所有该类别{t}信息。", \
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.DB.delete_party_contact_class(self.which_templete, current_type)
					self.type_list_view_refresh()

	def edit_type(self):
		if self.type_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			if self.which_templete in ('project', 'study'):
				new_type_name, flag = QInputDialog.getText(self, "新的名称", "请输入新的类型名称：")
				if flag:
					types = [x['type_name'] for x in self.DB.select('type_list', 'type_name')]
					if new_type_name not in types:
						self.DB.update_type(current_type, new_type_name)
						self.type_list_view_refresh()
					else:
						QMessageBox.warning(self, "错误", "该类型名称已存在。")
					
			elif self.which_templete in ('party', 'contact'):
				new_class_name, flag = QInputDialog.getText(self, "新的名称", "请输入新的类别名称：")
				if flag:
					classes = [x['class'] for x in self.DB.select(f"{self.which_templete}_class", 'class')]
					if new_class_name not in classes:
						self.DB.update_party_contact_class(self.which_templete, current_type, new_class_name)
						self.type_list_view_refresh()
					else:
						QMessageBox.warning(self, "错误", "该类别名称已存在。")

	def add_item(self):
		if self.type_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			if self.which_templete in ('project', 'study'):
				form_dict = {'纯文字': 'text', '当事人': 'party', '联系人': 'contact'}
				forms = ('纯文字', '当事人', '联系人')
				new_item_name, flag = QInputDialog.getText(self, current_type, "请输入新的字段名称：")
				new_item_form, flag2 = QInputDialog.getItem(self, current_type, "请选择新的字段类型", forms, 0, False)
				if flag & flag2:
					if not self.DB.add_type_item(current_type, new_item_name, form_dict[new_item_form]):
						QMessageBox.warning(self, "错误", f"“{current_type}”已经存在该字段。")
					self.item_list_view_refresh()

			elif self.which_templete in ('party', 'contact'):
				new_item_name, flag = QInputDialog.getText(self, current_type, "请输入新的字段名称：")
				if flag:
					if not self.DB.new_party_contact_item(self.which_templete, current_type, new_item_name):
						QMessageBox.warning(self, "错误", f"“{current_type}”已经存在该字段。")
					self.item_list_view_refresh()

	def delete_item(self):
		if self.type_list_view.selectedItems() and self.item_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			current_item = self.item_list_view.selectedItems()[0].text()
			if self.which_templete in ('project', 'study'):
				reply = QMessageBox.warning(self, "删除字段", f"是否删除“{current_type}”中的“{current_item}”？\n"\
					f"将会删除相关案件的对应信息。", 
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.DB.delete_type_item(current_type, current_item)
					self.item_list_view_refresh()

			elif self.which_templete in ('party', 'contact'):
				if self.item_list_view.currentRow() == 0:
					QMessageBox.warning(self, "错误", f"无法删除标识个体的基础信息")
				else:
					reply = QMessageBox.warning(self, "删除字段", f"是否删除“{current_type}”中的“{current_item}”？\n"\
						f"将会删除所有“{current_type}”的对应信息。", 
						QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if reply == QMessageBox.Yes:
						self.DB.delete_party_contact_item(self.which_templete, current_type, current_item)
						self.item_list_view_refresh()

	def edit_item(self):
		if self.type_list_view.selectedItems() and self.item_list_view.selectedItems():
			current_type = self.type_list_view.selectedItems()[0].text()
			current_item = self.item_list_view.selectedItems()[0].text()
			new_data, flag = QInputDialog.getText(self, "新的字段", "请输入新的字段名称：")
			if self.which_templete in ('project', 'study'):
				if flag:
					items = [x['item'] for x in self.DB.select('case_type', 'item', 'type_name', current_type)]
					if new_data not in items:
						self.DB.update_type_item(current_type, current_item, new_data)
						self.item_list_view_refresh()
					else:
						QMessageBox.warning(self, "错误", "与现有字段同名，无法修改。")

			elif self.which_templete in ('party', 'contact'):
				if flag:
					items = [x['item'] for x in self.DB.select(f"{self.which_templete}_class", 'item', 'class', current_type)]
					if new_data not in items:
						self.DB.update_party_contact_item(self.which_templete, current_type, current_item, new_data)
						self.item_list_view_refresh()
					else:
						QMessageBox.warning(self, "错误", "与现有字段同名，无法修改。")

	def item_move_up(self):
		if self.type_list_view.selectedItems() and self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			if self.which_templete in ('project', 'study'):
				if c_row > 0:
					c_id = self.item_list_view.item(c_row, 0).text()
					up_id = self.item_list_view.item(c_row - 1, 0).text()
					self.DB.swap('case_type', 'type_name', c_id, up_id)
					self.DB.swap('case_type', 'item', c_id, up_id)
					self.DB.swap('case_type', 'item_form', c_id, up_id)
					self.item_list_view_refresh()

			elif self.which_templete in ('party', 'contact'):
				if c_row > 1:
					c_id = self.item_list_view.item(c_row, 0).text()
					up_id = self.item_list_view.item(c_row - 1, 0).text()
					self.DB.swap(f"{self.which_templete}_class", 'item', c_id, up_id)
					self.item_list_view_refresh()

	def item_move_down(self):
		if self.type_list_view.selectedItems() and self.item_list_view.selectedItems():
			c_row = self.item_list_view.currentRow()
			rows = self.item_list_view.rowCount()
			if self.which_templete in ('project', 'study'):
				if c_row + 1 < rows:
					c_id = self.item_list_view.item(c_row, 0).text()
					down_id = self.item_list_view.item(c_row + 1, 0).text()
					self.DB.swap('case_type', 'type_name', c_id, down_id)
					self.DB.swap('case_type', 'item', c_id, down_id)
					self.DB.swap('case_type', 'item_form', c_id, down_id)
					self.item_list_view_refresh()

			elif self.which_templete in ('party', 'contact'):
				if c_row + 1 < rows and c_row > 0:
					c_id = self.item_list_view.item(c_row, 0).text()
					down_id = self.item_list_view.item(c_row + 1, 0).text()
					self.DB.swap(f"{self.which_templete}_class", 'item', c_id, down_id)
					self.item_list_view_refresh()

	# 修改设置
	def set_option_page(self):
		def new_btn(icon, text, func, col, row, tooltip = ""):
			btn = QToolButton(self.option_table)
			btn.setIconSize(QSize(26, 26))
			btn.setIcon(qtawesome.icon(icon, color = ('black', 160)))
			btn.setText(text)
			btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
			btn.setStyleSheet("""
				padding: 0px; 
				background-color: none;
				border: 1px solid rgb(200, 200, 200);
				border-radius: 8px;			
				""")
			btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
			btn.clicked.connect(func)
			btn.setToolTip(tooltip)
			self.option_table.setCellWidget(col, row, btn)

		self.option_table.setRowCount(27)

		self.option_table.setItem(0, 0, QTableWidgetItem("1. 备份、还原与初始化数据库     "))
		new_btn('msc.save-as', '备份', self.back_up, 0, 1)
		new_btn('mdi.backup-restore', '还原', self.restore, 0, 2)
		new_btn('msc.debug-restart-frame', '初始化', self.do_init, 0, 3)

		self.option_table.setItem(1, 0, QTableWidgetItem("2. 取消标题栏"))
		self.is_frameless_window_checkbox = QCheckBox()
		self.is_frameless_window_checkbox.setChecked(self.profiles['is_frameless_window'])
		self.is_frameless_window_checkbox.stateChanged.connect(self.change_is_frameless_window)
		self.is_frameless_window_checkbox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.option_table.setCellWidget(1, 1, self.is_frameless_window_checkbox)

		self.option_table.setItem(2, 0, QTableWidgetItem("3. 复制前显示提示"))
		self.is_show_copy_message_checkbox = QCheckBox()
		self.is_show_copy_message_checkbox.setChecked(self.profiles['is_show_copy_message'])
		self.is_show_copy_message_checkbox.stateChanged.connect(self.change_is_show_copy_message)
		self.is_show_copy_message_checkbox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.option_table.setCellWidget(2, 1, self.is_show_copy_message_checkbox)

		self.option_table.setItem(3, 0, QTableWidgetItem("4. 修改默认项目文件夹"))
		new_btn('mdi.file-cog-outline', '文件夹', self.change_default_path, 3, 1)

		text = {
			'color_right_frame': '全局背景', 
			'color_text': '全局文字', 

			'color_tree': '项目列表背景', 
			'color_table_background': '表格背景', 
			'color_table_header': '表头背景', 
			'color_notepad': '记事本背景', 

			'color_left_frame': '左边栏背景', 
			'color_left_frame_selected': '左边栏按钮选中1', 
			'color_left_frame_animation': '左边栏按钮选中2', 
			'color_left_frame_text': '左边栏按钮文字', 

			'color_party_contact_frame_selected': '当事人页面按钮选中',
			'color_templete_frame_selected': '模板页面按钮选中',

			'color_menu': '菜单背景', 
			'color_menu_selected': '菜单选中背景', 
			'color_menu_selected_text': '菜单选中文字', 

			'color_project': '项目信息标题背景', 
			'color_case_title_1': '案件信息标题1', 
			'color_case_title_2': '案件信息标题2', 
			'color_today_title_1': '今日简报标题1', 
			'color_today_title_2': '今日简报标题2', 
			'color_today_table': '今日简报表格'		
		}
		def color_btn(i, name, text):
			self.option_table.setItem(i, 0, QTableWidgetItem(f'    ({i - 4}) {text}'))
			new_btn('msc.symbol-color', '', partial(self.change_color, name), i, 1, "修改")
			new_btn('mdi.select-color', '', partial(self.restore_color, name), i, 2, "还原")			

		self.option_table.setItem(4, 0, QTableWidgetItem("5. 修改/还原界面配色："))
		i = 5
		for k,v in text.items():
			color_btn(i, k, v)
			i += 1
		
		self.option_table.setItem(i, 0, QTableWidgetItem("6. 备份、还原与初始化配置"))
		new_btn('msc.save-as', '备份', self.back_up_profiles, i, 1)
		new_btn('mdi.backup-restore', '还原', self.restore_profiles, i, 2)
		new_btn('msc.debug-restart-frame', '初始化', self.do_init_profiles, i, 3)

		self.option_table.resizeColumnToContents(0)

	def do_init(self):
		reply = QMessageBox.warning(self, "初始化", "是否删除全部数据并初始化？", 
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
		if reply == QMessageBox.StandardButton.Yes:
			self.DB.init()

	def back_up(self):
		path = QFileDialog.getExistingDirectory(self, "请选择存放备份文件的文件夹", self.profiles['default_filepath'])
		if path:
			NOW = datetime.now().strftime('%Y%m%d%H%M%S')
			BAK_PATH = os.path.join(path, f"DB_{NOW}.bak")
			if BAK_PATH and not os.path.exists(BAK_PATH):
				try:
					copyfile(self.DB_PATH, BAK_PATH)
				except:
					QMessageBox.critical(self, "错误", "备份出错")

	def restore(self):
		BAK_PATH, flag = QFileDialog.getOpenFileName(self, "请选择数据库文件地址", self.profiles['default_filepath'])
		if BAK_PATH:
			reply = QMessageBox.warning(self, "还原文件", "将覆盖现有全部数据，是否继续？", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
			if reply == QMessageBox.StandardButton.Yes:
				self.DB.delete_DB()
				try:
					copyfile(BAK_PATH, self.DB_PATH)
				except:
					QMessageBox.Icon.critical(self, "错误", "还原出错")
				

	def change_setting(self, name, value):
		with open(self.SETTING_PATH, 'r') as f:
			lines = f.readlines()

		s = ''
		for p in lines:
			if p.split(' ')[0] == name:
				s = s + f"{name} {value}\n"
			else:
				s = s + p

		with open(self.SETTING_PATH, 'w') as f:
			f.write(s)

	def change_default_path(self):
		new_path = QFileDialog.getExistingDirectory(self, "请选择默认文件地址", self.profiles['default_filepath'])
		if new_path:
			self.profiles['default_filepath'] = new_path
			self.change_setting('default_filepath', new_path)

	def change_is_frameless_window(self):
		self.profiles['is_frameless_window'] = self.is_frameless_window_checkbox.isChecked()
		if self.profiles['is_frameless_window']:
			self.change_setting('is_frameless_window', 'true')
			self.window_init()
			self.show()
		else:
			self.change_setting('is_frameless_window', 'false')
			self.window_init()
			self.show()

	def change_is_show_copy_message(self):
		self.profiles['is_show_copy_message'] = self.is_show_copy_message_checkbox.isChecked()
		if self.profiles['is_show_copy_message']:
			self.change_setting('is_show_copy_message', 'true')
		else:
			self.change_setting('is_show_copy_message', 'false')

	def setting_changed(self):
		self.window_init()
		self.option_btn.setStyleSheet(self.left_btn_selected_stylesheet)
		self.animation_label.setStyleSheet(f"""
			background-color: {self.profiles['color_left_frame_animation']}
			""")
		self.show()

	def change_color(self, name):
		def to_hex(x):
			t = str(hex(x))[2:]
			while len(t) < 2:
				t = '0' + t
			return t

		c = QColorDialog.getColor(QColor(self.profiles[name]), self)
		if c.isValid():
			new_color = f"#{to_hex(c.red())}{to_hex(c.green())}{to_hex(c.blue())}"
			if new_color:
				self.profiles[name] = new_color
				self.change_setting(name, new_color)
				self.setting_changed()

	def restore_color(self, name):
		reply = QMessageBox.question(self, "还原配色", "是否还原配色？", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
		if reply != 65536:
			self.profiles[name] = self.DEFAULTS[name]
			self.change_setting(name, self.DEFAULTS[name])
			self.setting_changed()


	def do_init_profiles(self):
		reply = QMessageBox.warning(self, "初始化", "是否初始化配置？", 
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
		if reply == QMessageBox.StandardButton.Yes:
			with open(self.SETTING_PATH, 'w') as f:
				f.write('')
			self.read_profile()
			self.set_option_page()
			self.setting_changed()


	def back_up_profiles(self):
		path = QFileDialog.getExistingDirectory(self, "请选择存放备份文件的文件夹", self.profiles['default_filepath'])
		if path:
			NOW = datetime.now().strftime('%Y%m%d%H%M%S')
			BAK_PATH = os.path.join(path, f"SETTING_{NOW}.bak")
			if BAK_PATH and not os.path.exists(BAK_PATH):
				try:
					copyfile(self.SETTING_PATH, BAK_PATH)
				except:
					QMessageBox.critical(self, "错误", "备份出错")

	def restore_profiles(self):
		BAK_PATH, flag = QFileDialog.getOpenFileName(self, "请选择配置文件地址", self.profiles['default_filepath'])
		if BAK_PATH:
			reply = QMessageBox.warning(self, "还原文件", "将覆盖现有全部配置，是否继续？", 
				QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
			if reply == QMessageBox.StandardButton.Yes:
				try:
					copyfile(BAK_PATH, self.SETTING_PATH)
				except:
					QMessageBox.Icon.critical(self, "错误", "还原出错")
				else:
					self.read_profile()
					self.set_option_page()
					self.setting_changed()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/l/Documents/Adobe & GTP/python/MyCaseLib/UI/MCLib_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 600)
        MainWindow.setMinimumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(10, 10, 10, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_box = QtWidgets.QComboBox(self.centralwidget)
        self.search_box.setObjectName("search_box")
        self.horizontalLayout_2.addWidget(self.search_box)
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setObjectName("search_bar")
        self.horizontalLayout_2.addWidget(self.search_bar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.p_c_treeview = QtWidgets.QTreeWidget(self.centralwidget)
        self.p_c_treeview.setTabletTracking(False)
        self.p_c_treeview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.p_c_treeview.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.p_c_treeview.setColumnCount(0)
        self.p_c_treeview.setObjectName("p_c_treeview")
        self.p_c_treeview.header().setVisible(False)
        self.verticalLayout.addWidget(self.p_c_treeview)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.case_info_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.case_info_tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.case_info_tab.setObjectName("case_info_tab")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.info_view = QtWidgets.QTextBrowser(self.tab_1)
        self.info_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.info_view.setObjectName("info_view")
        self.horizontalLayout_3.addWidget(self.info_view)
        self.case_info_tab.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.todo_view = QtWidgets.QTableWidget(self.tab_2)
        self.todo_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.todo_view.setTabKeyNavigation(True)
        self.todo_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.todo_view.setColumnCount(3)
        self.todo_view.setObjectName("todo_view")
        self.todo_view.setRowCount(0)
        self.verticalLayout_2.addWidget(self.todo_view)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.todo_add_btn = QtWidgets.QPushButton(self.tab_2)
        self.todo_add_btn.setObjectName("todo_add_btn")
        self.horizontalLayout_4.addWidget(self.todo_add_btn)
        self.todo_delete_btn = QtWidgets.QPushButton(self.tab_2)
        self.todo_delete_btn.setObjectName("todo_delete_btn")
        self.horizontalLayout_4.addWidget(self.todo_delete_btn)
        self.to_event_btn = QtWidgets.QPushButton(self.tab_2)
        self.to_event_btn.setObjectName("to_event_btn")
        self.horizontalLayout_4.addWidget(self.to_event_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.case_info_tab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.event_view = QtWidgets.QTableWidget(self.tab_3)
        self.event_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.event_view.setColumnCount(3)
        self.event_view.setObjectName("event_view")
        self.event_view.setRowCount(0)
        self.verticalLayout_5.addWidget(self.event_view)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.event_add_btn = QtWidgets.QPushButton(self.tab_3)
        self.event_add_btn.setObjectName("event_add_btn")
        self.horizontalLayout_5.addWidget(self.event_add_btn)
        self.event_delete_btn = QtWidgets.QPushButton(self.tab_3)
        self.event_delete_btn.setObjectName("event_delete_btn")
        self.horizontalLayout_5.addWidget(self.event_delete_btn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.case_info_tab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.notepad = QtWidgets.QTextEdit(self.tab_4)
        self.notepad.setObjectName("notepad")
        self.verticalLayout_7.addWidget(self.notepad)
        self.case_info_tab.addTab(self.tab_4, "")
        self.horizontalLayout_6.addWidget(self.case_info_tab)
        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 7)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setMinimumSize(QtCore.QSize(120, 0))
        self.menu.setObjectName("menu")
        self.menuP = QtWidgets.QMenu(self.menu)
        self.menuP.setObjectName("menuP")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setMinimumSize(QtCore.QSize(120, 0))
        self.menu_2.setObjectName("menu_2")
        self.menu_party_contact = QtWidgets.QMenu(self.menu_2)
        self.menu_party_contact.setObjectName("menu_party_contact")
        self.menu_3 = QtWidgets.QMenu(self.menu_2)
        self.menu_3.setMinimumSize(QtCore.QSize(120, 0))
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionx1 = QtWidgets.QAction(MainWindow)
        self.actionx1.setObjectName("actionx1")
        self.actionx2 = QtWidgets.QAction(MainWindow)
        self.actionx2.setObjectName("actionx2")
        self.actionm1 = QtWidgets.QAction(MainWindow)
        self.actionm1.setObjectName("actionm1")
        self.menu_close = QtWidgets.QAction(MainWindow)
        self.menu_close.setObjectName("menu_close")
        self.actionS1 = QtWidgets.QAction(MainWindow)
        self.actionS1.setObjectName("actionS1")
        self.actions2 = QtWidgets.QAction(MainWindow)
        self.actions2.setObjectName("actions2")
        self.menu_execute = QtWidgets.QAction(MainWindow)
        self.menu_execute.setObjectName("menu_execute")
        self.menu_init = QtWidgets.QAction(MainWindow)
        self.menu_init.setObjectName("menu_init")
        self.menu_backup = QtWidgets.QAction(MainWindow)
        self.menu_backup.setObjectName("menu_backup")
        self.menu_restore = QtWidgets.QAction(MainWindow)
        self.menu_restore.setObjectName("menu_restore")
        self.menu_types = QtWidgets.QAction(MainWindow)
        self.menu_types.setObjectName("menu_types")
        self.menu_new_project = QtWidgets.QAction(MainWindow)
        self.menu_new_project.setObjectName("menu_new_project")
        self.menu_new_case = QtWidgets.QAction(MainWindow)
        self.menu_new_case.setObjectName("menu_new_case")
        self.menu_contact = QtWidgets.QAction(MainWindow)
        self.menu_contact.setObjectName("menu_contact")
        self.menu_parties = QtWidgets.QAction(MainWindow)
        self.menu_parties.setObjectName("menu_parties")
        self.menu_contacts = QtWidgets.QAction(MainWindow)
        self.menu_contacts.setObjectName("menu_contacts")
        self.menu_manage_type_item = QtWidgets.QAction(MainWindow)
        self.menu_manage_type_item.setObjectName("menu_manage_type_item")
        self.menu_manage_party_class = QtWidgets.QAction(MainWindow)
        self.menu_manage_party_class.setObjectName("menu_manage_party_class")
        self.menu_manage_contact_class = QtWidgets.QAction(MainWindow)
        self.menu_manage_contact_class.setObjectName("menu_manage_contact_class")
        self.menu_delete_project = QtWidgets.QAction(MainWindow)
        self.menu_delete_project.setObjectName("menu_delete_project")
        self.menu_delete_case = QtWidgets.QAction(MainWindow)
        self.menu_delete_case.setObjectName("menu_delete_case")
        self.menu_color_today = QtWidgets.QAction(MainWindow)
        self.menu_color_today.setObjectName("menu_color_today")
        self.menu_color_project = QtWidgets.QAction(MainWindow)
        self.menu_color_project.setObjectName("menu_color_project")
        self.menu_color_case = QtWidgets.QAction(MainWindow)
        self.menu_color_case.setObjectName("menu_color_case")
        self.menu_default_filepath = QtWidgets.QAction(MainWindow)
        self.menu_default_filepath.setObjectName("menu_default_filepath")
        self.menu_today_news = QtWidgets.QAction(MainWindow)
        self.menu_today_news.setObjectName("menu_today_news")
        self.menu_about = QtWidgets.QAction(MainWindow)
        self.menu_about.setObjectName("menu_about")
        self.menuP.addAction(self.menu_default_filepath)
        self.menuP.addSeparator()
        self.menuP.addAction(self.menu_color_today)
        self.menuP.addAction(self.menu_color_project)
        self.menuP.addAction(self.menu_color_case)
        self.menuP.addSeparator()
        self.menuP.addAction(self.menu_init)
        self.menuP.addAction(self.menu_backup)
        self.menuP.addAction(self.menu_restore)
        self.menu.addAction(self.menu_today_news)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_about)
        self.menu.addAction(self.menuP.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.menu_close)
        self.menu_party_contact.addAction(self.menu_parties)
        self.menu_party_contact.addAction(self.menu_contacts)
        self.menu_3.addAction(self.menu_manage_type_item)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.menu_manage_party_class)
        self.menu_3.addAction(self.menu_manage_contact_class)
        self.menu_2.addAction(self.menu_party_contact.menuAction())
        self.menu_2.addAction(self.menu_3.menuAction())
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.menu_new_project)
        self.menu_2.addAction(self.menu_new_case)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.menu_delete_project)
        self.menu_2.addAction(self.menu_delete_case)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.case_info_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.case_info_tab.setTabText(self.case_info_tab.indexOf(self.tab_1), _translate("MainWindow", "??????"))
        self.todo_view.setSortingEnabled(False)
        self.todo_add_btn.setText(_translate("MainWindow", "????????????"))
        self.todo_delete_btn.setText(_translate("MainWindow", "????????????"))
        self.to_event_btn.setText(_translate("MainWindow", "????????????"))
        self.case_info_tab.setTabText(self.case_info_tab.indexOf(self.tab_2), _translate("MainWindow", "??????"))
        self.event_view.setSortingEnabled(False)
        self.event_add_btn.setText(_translate("MainWindow", "????????????"))
        self.event_delete_btn.setText(_translate("MainWindow", "????????????"))
        self.case_info_tab.setTabText(self.case_info_tab.indexOf(self.tab_3), _translate("MainWindow", "??????"))
        self.case_info_tab.setTabText(self.case_info_tab.indexOf(self.tab_4), _translate("MainWindow", "??????"))
        self.menu.setTitle(_translate("MainWindow", "??????"))
        self.menuP.setTitle(_translate("MainWindow", "??????.."))
        self.menu_2.setTitle(_translate("MainWindow", "??????"))
        self.menu_party_contact.setTitle(_translate("MainWindow", "???.."))
        self.menu_3.setTitle(_translate("MainWindow", "??????.."))
        self.actionx1.setText(_translate("MainWindow", "????????????"))
        self.actionx2.setText(_translate("MainWindow", "????????????"))
        self.actionm1.setText(_translate("MainWindow", "??????.."))
        self.menu_close.setText(_translate("MainWindow", "??????"))
        self.actionS1.setText(_translate("MainWindow", "????????????"))
        self.actions2.setText(_translate("MainWindow", "????????????"))
        self.menu_execute.setText(_translate("MainWindow", "execute.."))
        self.menu_init.setText(_translate("MainWindow", "?????????"))
        self.menu_backup.setText(_translate("MainWindow", "??????"))
        self.menu_restore.setText(_translate("MainWindow", "??????"))
        self.menu_types.setText(_translate("MainWindow", "??????.."))
        self.menu_new_project.setText(_translate("MainWindow", "????????????"))
        self.menu_new_case.setText(_translate("MainWindow", "????????????"))
        self.menu_contact.setText(_translate("MainWindow", "????????????"))
        self.menu_parties.setText(_translate("MainWindow", "?????????"))
        self.menu_contacts.setText(_translate("MainWindow", "?????????"))
        self.menu_manage_type_item.setText(_translate("MainWindow", "????????????"))
        self.menu_manage_party_class.setText(_translate("MainWindow", "?????????"))
        self.menu_manage_contact_class.setText(_translate("MainWindow", "?????????"))
        self.menu_delete_project.setText(_translate("MainWindow", "????????????"))
        self.menu_delete_case.setText(_translate("MainWindow", "????????????"))
        self.menu_color_today.setText(_translate("MainWindow", "??????-????????????"))
        self.menu_color_project.setText(_translate("MainWindow", "??????-????????????"))
        self.menu_color_case.setText(_translate("MainWindow", "??????-????????????"))
        self.menu_default_filepath.setText(_translate("MainWindow", "?????????????????????"))
        self.menu_today_news.setText(_translate("MainWindow", "????????????"))
        self.menu_about.setText(_translate("MainWindow", "??????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

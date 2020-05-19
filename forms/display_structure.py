# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display_structure.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalSlider__currentTime = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider__currentTime.setGeometry(QtCore.QRect(10, 530, 721, 22))
        self.horizontalSlider__currentTime.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider__currentTime.setObjectName("horizontalSlider__currentTime")
        self.spinBox__currentTime = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox__currentTime.setGeometry(QtCore.QRect(750, 530, 42, 22))
        self.spinBox__currentTime.setObjectName("spinBox__currentTime")
        self.tabWidget__left = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget__left.setGeometry(QtCore.QRect(10, 10, 301, 501))
        self.tabWidget__left.setObjectName("tabWidget__left")
        self.tab__displayx = QtWidgets.QWidget()
        self.tab__displayx.setObjectName("tab__displayx")
        self.tableWidget__displayx = QtWidgets.QTableWidget(self.tab__displayx)
        self.tableWidget__displayx.setGeometry(QtCore.QRect(10, 10, 271, 451))
        self.tableWidget__displayx.setObjectName("tableWidget__displayx")
        self.tableWidget__displayx.setColumnCount(0)
        self.tableWidget__displayx.setRowCount(0)
        self.tabWidget__left.addTab(self.tab__displayx, "")
        self.tab__displayu = QtWidgets.QWidget()
        self.tab__displayu.setObjectName("tab__displayu")
        self.tableWidget__displayu = QtWidgets.QTableWidget(self.tab__displayu)
        self.tableWidget__displayu.setGeometry(QtCore.QRect(10, 10, 271, 451))
        self.tableWidget__displayu.setObjectName("tableWidget__displayu")
        self.tableWidget__displayu.setColumnCount(0)
        self.tableWidget__displayu.setRowCount(0)
        self.tabWidget__left.addTab(self.tab__displayu, "")
        self.tabWidget__right = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget__right.setGeometry(QtCore.QRect(320, 10, 471, 501))
        self.tabWidget__right.setObjectName("tabWidget__right")
        self.tab__displayGraph = QtWidgets.QWidget()
        self.tab__displayGraph.setObjectName("tab__displayGraph")
        self.widget__displayGraph = MplWidget(self.tab__displayGraph)
        self.widget__displayGraph.setGeometry(QtCore.QRect(10, 10, 441, 451))
        self.widget__displayGraph.setObjectName("widget__displayGraph")
        self.tabWidget__right.addTab(self.tab__displayGraph, "")
        self.tab__displayConnProb = QtWidgets.QWidget()
        self.tab__displayConnProb.setObjectName("tab__displayConnProb")
        self.tableWidget__displayConnProb = QtWidgets.QTableWidget(self.tab__displayConnProb)
        self.tableWidget__displayConnProb.setGeometry(QtCore.QRect(10, 10, 441, 451))
        self.tableWidget__displayConnProb.setObjectName("tableWidget__displayConnProb")
        self.tableWidget__displayConnProb.setColumnCount(0)
        self.tableWidget__displayConnProb.setRowCount(0)
        self.tabWidget__right.addTab(self.tab__displayConnProb, "")
        self.tab__displayConnPower = QtWidgets.QWidget()
        self.tab__displayConnPower.setObjectName("tab__displayConnPower")
        self.tableWidget__displayConnPower = QtWidgets.QTableWidget(self.tab__displayConnPower)
        self.tableWidget__displayConnPower.setGeometry(QtCore.QRect(10, 10, 441, 451))
        self.tableWidget__displayConnPower.setObjectName("tableWidget__displayConnPower")
        self.tableWidget__displayConnPower.setColumnCount(0)
        self.tableWidget__displayConnPower.setRowCount(0)
        self.tabWidget__right.addTab(self.tab__displayConnPower, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget__left.setCurrentIndex(0)
        self.tabWidget__right.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget__left.setTabText(self.tabWidget__left.indexOf(self.tab__displayx), _translate("MainWindow", "Координаты"))
        self.tabWidget__left.setTabText(self.tabWidget__left.indexOf(self.tab__displayu), _translate("MainWindow", "Управление"))
        self.tabWidget__right.setTabText(self.tabWidget__right.indexOf(self.tab__displayGraph), _translate("MainWindow", "Граф"))
        self.tabWidget__right.setTabText(self.tabWidget__right.indexOf(self.tab__displayConnProb), _translate("MainWindow", "Вероятности соединения"))
        self.tabWidget__right.setTabText(self.tabWidget__right.indexOf(self.tab__displayConnPower), _translate("MainWindow", "Силы соединения"))
from mplwidget import MplWidget

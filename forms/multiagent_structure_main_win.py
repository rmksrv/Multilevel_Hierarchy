# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multiagent_structure_main_win.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 559)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(278, 274))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setHorizontalSpacing(27)
        self.gridLayout.setObjectName("gridLayout")
        self.label__System_nodeAmount = QtWidgets.QLabel(self.groupBox)
        self.label__System_nodeAmount.setObjectName("label__System_nodeAmount")
        self.gridLayout.addWidget(self.label__System_nodeAmount, 0, 0, 1, 1)
        self.lineEdit__nodeAmount = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit__nodeAmount.sizePolicy().hasHeightForWidth())
        self.lineEdit__nodeAmount.setSizePolicy(sizePolicy)
        self.lineEdit__nodeAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit__nodeAmount.setObjectName("lineEdit__nodeAmount")
        self.gridLayout.addWidget(self.lineEdit__nodeAmount, 0, 1, 1, 1)
        self.label__nodesCoords = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label__nodesCoords.sizePolicy().hasHeightForWidth())
        self.label__nodesCoords.setSizePolicy(sizePolicy)
        self.label__nodesCoords.setObjectName("label__nodesCoords")
        self.gridLayout.addWidget(self.label__nodesCoords, 1, 0, 1, 1)
        self.tableWidget__nodesCoords = QtWidgets.QTableWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget__nodesCoords.sizePolicy().hasHeightForWidth())
        self.tableWidget__nodesCoords.setSizePolicy(sizePolicy)
        self.tableWidget__nodesCoords.setMinimumSize(QtCore.QSize(256, 192))
        self.tableWidget__nodesCoords.setColumnCount(2)
        self.tableWidget__nodesCoords.setObjectName("tableWidget__nodesCoords")
        self.tableWidget__nodesCoords.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget__nodesCoords, 2, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tab_container = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_container.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_container.sizePolicy().hasHeightForWidth())
        self.tab_container.setSizePolicy(sizePolicy)
        self.tab_container.setMinimumSize(QtCore.QSize(508, 500))
        self.tab_container.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tab_container.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_container.setElideMode(QtCore.Qt.ElideRight)
        self.tab_container.setDocumentMode(False)
        self.tab_container.setObjectName("tab_container")
        self.tab__drawGraph = QtWidgets.QWidget()
        self.tab__drawGraph.setObjectName("tab__drawGraph")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab__drawGraph)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tab_container.addTab(self.tab__drawGraph, "")
        self.tab__adjMx = QtWidgets.QWidget()
        self.tab__adjMx.setObjectName("tab__adjMx")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab__adjMx)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableWidget__adjacencyMatrix = QtWidgets.QTableWidget(self.tab__adjMx)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget__adjacencyMatrix.sizePolicy().hasHeightForWidth())
        self.tableWidget__adjacencyMatrix.setSizePolicy(sizePolicy)
        self.tableWidget__adjacencyMatrix.setObjectName("tableWidget__adjacencyMatrix")
        self.tableWidget__adjacencyMatrix.setColumnCount(0)
        self.tableWidget__adjacencyMatrix.setRowCount(0)
        self.horizontalLayout_3.addWidget(self.tableWidget__adjacencyMatrix)
        self.tab_container.addTab(self.tab__adjMx, "")
        self.tab__cProbMx = QtWidgets.QWidget()
        self.tab__cProbMx.setObjectName("tab__cProbMx")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab__cProbMx)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget__connectionsProb = QtWidgets.QTableWidget(self.tab__cProbMx)
        self.tableWidget__connectionsProb.setObjectName("tableWidget__connectionsProb")
        self.tableWidget__connectionsProb.setColumnCount(0)
        self.tableWidget__connectionsProb.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tableWidget__connectionsProb)
        self.tab_container.addTab(self.tab__cProbMx, "")
        self.tab__cPowerMx = QtWidgets.QWidget()
        self.tab__cPowerMx.setObjectName("tab__cPowerMx")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab__cPowerMx)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget__connectionsPower = QtWidgets.QTableWidget(self.tab__cPowerMx)
        self.tableWidget__connectionsPower.setObjectName("tableWidget__connectionsPower")
        self.tableWidget__connectionsPower.setColumnCount(0)
        self.tableWidget__connectionsPower.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableWidget__connectionsPower)
        self.tab_container.addTab(self.tab__cPowerMx, "")
        self.gridLayout_3.addWidget(self.tab_container, 0, 1, 3, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(278, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label__maxSlaves = QtWidgets.QLabel(self.groupBox_2)
        self.label__maxSlaves.setTextFormat(QtCore.Qt.AutoText)
        self.label__maxSlaves.setWordWrap(True)
        self.label__maxSlaves.setObjectName("label__maxSlaves")
        self.gridLayout_2.addWidget(self.label__maxSlaves, 0, 0, 1, 1)
        self.lineEdit__maxSlaves = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit__maxSlaves.sizePolicy().hasHeightForWidth())
        self.lineEdit__maxSlaves.setSizePolicy(sizePolicy)
        self.lineEdit__maxSlaves.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit__maxSlaves.setObjectName("lineEdit__maxSlaves")
        self.gridLayout_2.addWidget(self.lineEdit__maxSlaves, 0, 1, 1, 1)
        self.label__treeDepth = QtWidgets.QLabel(self.groupBox_2)
        self.label__treeDepth.setWordWrap(True)
        self.label__treeDepth.setObjectName("label__treeDepth")
        self.gridLayout_2.addWidget(self.label__treeDepth, 1, 0, 1, 1)
        self.lineEdit__treeDepth = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit__treeDepth.sizePolicy().hasHeightForWidth())
        self.lineEdit__treeDepth.setSizePolicy(sizePolicy)
        self.lineEdit__treeDepth.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit__treeDepth.setObjectName("lineEdit__treeDepth")
        self.gridLayout_2.addWidget(self.lineEdit__treeDepth, 1, 1, 1, 1)
        self.checkBox__recalculate_probs = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox__recalculate_probs.setObjectName("checkBox__recalculate_probs")
        self.gridLayout_2.addWidget(self.checkBox__recalculate_probs, 2, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.pushButton__buildStructure = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton__buildStructure.sizePolicy().hasHeightForWidth())
        self.pushButton__buildStructure.setSizePolicy(sizePolicy)
        self.pushButton__buildStructure.setObjectName("pushButton__buildStructure")
        self.gridLayout_3.addWidget(self.pushButton__buildStructure, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action__prob_func = QtWidgets.QAction(MainWindow)
        self.action__prob_func.setObjectName("action__prob_func")
        self.menu.addAction(self.action__prob_func)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tab_container.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Система"))
        self.label__System_nodeAmount.setText(_translate("MainWindow", "Количество узлов"))
        self.label__nodesCoords.setText(_translate("MainWindow", "Координаты узлов"))
        self.tab_container.setTabText(self.tab_container.indexOf(self.tab__drawGraph), _translate("MainWindow", "Граф"))
        self.tab_container.setTabText(self.tab_container.indexOf(self.tab__adjMx), _translate("MainWindow", "Матрица графа"))
        self.tab_container.setTabText(self.tab_container.indexOf(self.tab__cProbMx), _translate("MainWindow", "Матрица вероятностей соединения"))
        self.tab_container.setTabText(self.tab_container.indexOf(self.tab__cPowerMx), _translate("MainWindow", "Матрица сил соединения"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Дополнительные условия"))
        self.label__maxSlaves.setText(_translate("MainWindow", "Макс. количество дочерних узлов"))
        self.label__treeDepth.setText(_translate("MainWindow", "Макс. глубина дерева"))
        self.checkBox__recalculate_probs.setText(_translate("MainWindow", "Пересчитать силы соединения"))
        self.pushButton__buildStructure.setText(_translate("MainWindow", "Построить структуру"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.action__prob_func.setText(_translate("MainWindow", "Функция вероятности"))
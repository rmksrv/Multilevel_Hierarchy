import sys
# Core
from core import StructureBuilder, Utils
import networkx as nx
import numpy as np
# Qt imports
from PyQt5 import QtCore, QtGui, QtWidgets
import forms.multiagent_structure_main_win as forms_mainwin
import forms.prob_function_win as forms_probfunc
# MplWidget imports
#from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

# TODO tasks:
#   Big:
#   - add drawing of graph using matplotlib/networkx (in progress)
#   Small:
#   - add check of value correctness in set_nodesAmount, set_maxSlaves, set_treeDepth 


class ProbFuncWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_probfunc.Ui_Dialog()
        self.ui.setupUi(self)
        self.addToolBar(NavigationToolbar(self.ui.mplwidget.canvas, self))
        # my vars
        self.ca = 500
        self.rolow = 7
        self.roupp = 50
        # fields sync
        self.ui.lineEdit.setText(str(self.rolow))
        self.ui.lineEdit_2.setText(str(self.roupp))
        # Connects
        self.ui.lineEdit.editingFinished.connect(self.set_rolow)
        self.ui.lineEdit_2.editingFinished.connect(self.set_roupp)

    def set_rolow(self):
        calc_amount = self.ca
        self.rolow = float(self.ui.lineEdit.text())
        self.ui.mplwidget.canvas.axes.clear()
        self.ui.mplwidget.canvas.axes.set_ylim([-0.05, 1.1])
        self.ui.mplwidget.canvas.axes.plot(Utils.prob_func_dots(calc_amount, self.rolow, self.roupp)[0], Utils.prob_func_dots(calc_amount, self.rolow, self.roupp)[1])
        self.ui.mplwidget.canvas.draw()

    def set_roupp(self):
        calc_amount = self.ca
        self.roupp = float(self.ui.lineEdit_2.text())
        self.ui.mplwidget.canvas.axes.clear()
        self.ui.mplwidget.canvas.axes.set_ylim([-0.05, 1.1])
        self.ui.mplwidget.canvas.axes.plot(Utils.prob_func_dots(calc_amount, self.rolow, self.roupp)[0], Utils.prob_func_dots(calc_amount, self.rolow, self.roupp)[1])
        self.ui.mplwidget.canvas.draw()


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Base
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_mainwin.Ui_MainWindow()
        self.ui.setupUi(self)
        # Other windows
        self.probfunc_dialog = ProbFuncWin()
        # my vars
        self.nodesCoords = [
            (0.0, 0.0),
            (4.0, 0.0),
            (10.0, 0.0),
            (13.0, 0.0),
            (20.0, 0.0),
            (0.0, 3.0),
            (0.0, 6.0),
            (0.0, -3.0),
            (-5.0, 0.0),
        ]
        self.nodesAmount = 9
        self.maxSlaves = 0
        self.treeDepth = 0
        self.recalculateProbs = False
        # sync up my vars with widget values (table syncs below)
        self.ui.lineEdit__nodeAmount.setText(str(self.nodesAmount))  # nodes amount
        self.ui.lineEdit__maxSlaves.setText(str(self.maxSlaves))  # max slaves
        self.ui.lineEdit__treeDepth.setText(str(self.treeDepth))  # max tree depth
        self.ui.checkBox__recalculate_probs.setChecked(self.recalculateProbs)  # recalculate probs
        # table sync
        self.ui.tableWidget__nodesCoords.setRowCount(self.nodesAmount)
        self.ui.tableWidget__nodesCoords.setHorizontalHeaderLabels(['x', 'y'])
        i = 0
        for node in self.nodesCoords:
            self.ui.tableWidget__nodesCoords.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))  # add x value to `i` row
            self.ui.tableWidget__nodesCoords.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))  # and y value too
            i += 1
        # Something
        self.ui.widget.canvas.axes.clear()
        # Connects
        self.ui.pushButton__buildStructure.clicked.connect(self.build_structure)
        self.ui.lineEdit__nodeAmount.editingFinished.connect(self.set_nodesAmount)
        self.ui.lineEdit__maxSlaves.editingFinished.connect(self.set_maxSlaves)
        self.ui.lineEdit__treeDepth.editingFinished.connect(self.set_treeDepth)
        self.ui.checkBox__recalculate_probs.clicked.connect(self.set_recalculateProbs)
        self.ui.action__prob_func.triggered.connect(self.open_prob_func_win)

    def build_structure(self):
        struct_builder = StructureBuilder()
        # TODO: add field to change number of digits after `,`
        digits_number = 5
        # Remake self.nodesCoords
        self.nodesCoords.clear()
        for i in range(self.nodesAmount):
            x = float(self.ui.tableWidget__nodesCoords.item(i, 0).text())
            y = float(self.ui.tableWidget__nodesCoords.item(i, 1).text())
            node = (x, y)
            self.nodesCoords.append(node)
        # Connection probability matrix
        cprob = struct_builder.connection_probability(self.nodesCoords)
        self.ui.tableWidget__connectionsProb.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsProb.setColumnCount(self.nodesAmount)
        # C-styled array bypass should be rewritten
        for i in range(self.nodesAmount):
            for j in range(self.nodesAmount):
                self.ui.tableWidget__connectionsProb.setItem(i, j,
                    QtWidgets.QTableWidgetItem(str(
                        round(cprob[i][j], digits_number)
                    ))
                )
        self.ui.tableWidget__connectionsProb.resizeColumnsToContents()
        # Connection power matrix
        cpower = struct_builder.connection_power(cprob)
        self.ui.tableWidget__connectionsPower.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsPower.setColumnCount(self.nodesAmount)
        # C-styled array bypass should be rewritten
        for i in range(self.nodesAmount):
            for j in range(self.nodesAmount):
                self.ui.tableWidget__connectionsPower.setItem(i, j,
                    QtWidgets.QTableWidgetItem(str(
                        round(cpower[i][j], digits_number)
                    ))
                )
        self.ui.tableWidget__connectionsPower.resizeColumnsToContents()
        try:
            ## Generating adjacency matrix
            tree = struct_builder.build_tree(cprob, 
                recalculate_probs=self.recalculateProbs,
                max_slaves=self.maxSlaves,
                max_depth=self.treeDepth
            )
            adjmx = nx.to_numpy_array(tree)
            # Print connections power matrix to table
            self.ui.tableWidget__adjacencyMatrix.setRowCount(self.nodesAmount)
            self.ui.tableWidget__adjacencyMatrix.setColumnCount(self.nodesAmount)
            #i, j = 0, 0
            for i in range(self.nodesAmount):
                for j in range(self.nodesAmount):
                    self.ui.tableWidget__adjacencyMatrix.setItem(i, j, 
                        QtWidgets.QTableWidgetItem(str(
                            round(adjmx[i][j], digits_number)
                        ))
                    )
            self.ui.tableWidget__adjacencyMatrix.resizeColumnsToContents()
            ## Drawing graph
            self.ui.widget.canvas.axes.clear()
            nx.draw_networkx(tree, pos=nx.planar_layout(tree), ax=self.ui.widget.canvas.axes)
            self.ui.widget.canvas.draw()
            #import matplotlib.pyplot as plt
            #plt.subplot(111)
            #nx.draw_networkx(tree, pos=nx.planar_layout(tree))
            #plt.show()
        except nx.exception.NetworkXException:
            warning_msg = QtWidgets.QMessageBox()
            warning_msg.setWindowTitle('Ошибка')
            warning_msg.setText('Оптимальное дерево не найдено')
            warning_msg.exec_()

    def set_nodesAmount(self):
        # TODO: add check of value correctness 
        self.nodesAmount = int(self.ui.lineEdit__nodeAmount.text())
        self.ui.tableWidget__nodesCoords.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsProb.clear()
        self.ui.tableWidget__connectionsPower.clear()
        self.ui.tableWidget__connectionsProb.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsProb.setColumnCount(self.nodesAmount)
        self.ui.tableWidget__connectionsPower.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsPower.setColumnCount(self.nodesAmount)



    def set_maxSlaves(self):
        # TODO: add check of value correctness 
        self.maxSlaves = int(self.ui.lineEdit__maxSlaves.text())

    def set_treeDepth(self):
        # TODO: add check of value correctness 
        self.treeDepth = int(self.ui.lineEdit__treeDepth.text())

    def set_recalculateProbs(self):
        self.recalculateProbs = not self.recalculateProbs

    def open_prob_func_win(self):
        self.probfunc_dialog.show()
        calc_amount = 200
        self.probfunc_dialog.ui.mplwidget.canvas.axes.clear()
        rolow = self.probfunc_dialog.rolow
        roupp = self.probfunc_dialog.roupp
        dots = Utils.prob_func_dots(calc_amount, rolow, roupp)
        self.probfunc_dialog.ui.mplwidget.canvas.axes.set_ylim([-0.05, 1.1])
        self.probfunc_dialog.ui.mplwidget.canvas.axes.plot(dots[0], dots[1])
        self.probfunc_dialog.ui.mplwidget.canvas.draw()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

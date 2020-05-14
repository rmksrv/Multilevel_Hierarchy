import sys
from core import MultiagentEnvironment, Utils
import networkx as nx
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import forms.main_win as forms_mainwin
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Base
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_mainwin.Ui_MainWindow()
        self.ui.setupUi(self)
        # Vars
        self.current_time = 1  # cuurent time
        self.max_sub_nodes = 0  # feature: max sub nodes
        self.max_tree_length = 0  # feature: max tree length
        self.prob_depending = False  # feature: probs depends of ourselves
        self.is_structure_built = False
        self.env = MultiagentEnvironment(nodes_amount=5, time=10)  # main environment object
        self.env.rolow = 5
        self.env.roupp = 100
        self.env.A = [
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
        ]
        self.env.B = [
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
        ]
        # coords of nodes ('x')
        self.env.start_node_coords = [
            (0.0, 0.0),
            (4.0, 0.0),
            (10.0, 0.0),
            (13.0, 0.0),
            (20.0, 0.0),
        ]
        # controls ('u')
        self.env.start_controls = [
            (1.0, 1.0),
            (0.0, 0.0),
            (0.0, 0.0),
            (0.0, 0.0),
            (0.0, 0.0),
        ]
        #self.env.calculate_structs_for_each_time()
        self.build_structure()
        # Widgets setup
        self.prepareWidgets()
        # Connects setup
        self.initConnects()

    def prepareWidgets(self):
        # Clear graph plotter
        self.ui.widget__displayGraph.canvas.axes.clear()
        # syncing tables connProb, connPower
        self.ui.tableWidget__displayProbMatrix.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__displayProbMatrix.setColumnCount(self.env.nodes_amount)
        self.ui.tableWidget__displayPowerMatrix.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__displayPowerMatrix.setColumnCount(self.env.nodes_amount)
        # Set minimal time == 1
        self.ui.horizontalSlider__controlTime.setMinimum(1)
        self.ui.spinBox__controlTime.setMinimum(1)
        # Update widgets
        self.updateWidgets()

    def updateWidgets(self):
        # Clear graph
        self.ui.widget__displayGraph.canvas.axes.clear()
        # Syncing lineEdit's text with according vars
        self.ui.lineEdit__inputTime.setText(str(self.env.time))
        self.ui.lineEdit__inputNodeAmount.setText(str(self.env.nodes_amount))
        self.ui.lineEdit__inputDistanceLinkOn.setText(str(self.env.rolow))
        self.ui.lineEdit__inputDistanceLinkOff.setText(str(self.env.roupp))
        self.ui.lineEdit__inputMaxSubNodes.setText(str(self.max_sub_nodes))
        self.ui.lineEdit__inputMaxTreeLength.setText(str(self.max_tree_length))
        # sync checkbox
        self.ui.checkBox__inputProbDepending.setCheckState(self.prob_depending)
        # Syncing 'currentTime' interface
        self.ui.horizontalSlider__controlTime.setValue(self.current_time)
        self.ui.horizontalSlider__controlTime.setMaximum(self.env.time)
        self.ui.spinBox__controlTime.setValue(self.current_time)
        self.ui.spinBox__controlTime.setMaximum(self.env.time)
        #self.build_structure()
        # syncing tables A, B, (x, u, only if structure is built)
        # A
        self.ui.tableWidget__inputA.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__inputA.setColumnCount(2)
        i = 0
        for item in self.env.A:
            self.ui.tableWidget__inputA.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.ui.tableWidget__inputA.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            i += 1
        # B
        self.ui.tableWidget__inputB.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__inputB.setColumnCount(2)
        i = 0
        for item in self.env.B:
            self.ui.tableWidget__inputB.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.ui.tableWidget__inputB.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            i += 1
        # x, u
        self.ui.tableWidget__inputx.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__inputx.setColumnCount(2)
        self.ui.tableWidget__inputu.setRowCount(self.env.nodes_amount)
        self.ui.tableWidget__inputu.setColumnCount(2)
        if self.is_structure_built:
            # Left matrices
            # x
            i = 0
            for coord in self.env.node_coords[self.current_time - 1]:
                self.ui.tableWidget__inputx.setItem(i, 0, QtWidgets.QTableWidgetItem(str(coord[0])))
                self.ui.tableWidget__inputx.setItem(i, 1, QtWidgets.QTableWidgetItem(str(coord[1])))
                i += 1
            # u
            i = 0
            for control in self.env.controls[self.current_time - 1]:
                self.ui.tableWidget__inputu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(control[0])))
                self.ui.tableWidget__inputu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(control[1])))
                i += 1
            # Graph
            tree = self.env.structs[self.current_time - 1]
            nx.draw_networkx(tree, pos=nx.planar_layout(tree), ax=self.ui.widget__displayGraph.canvas.axes)
            self.ui.widget__displayGraph.canvas.draw()
        else:
            # Left matrices
            # x
            i = 0
            for coord in self.env.start_node_coords:
                self.ui.tableWidget__inputx.setItem(i, 0, QtWidgets.QTableWidgetItem(str(coord[0])))
                self.ui.tableWidget__inputx.setItem(i, 1, QtWidgets.QTableWidgetItem(str(coord[1])))
                i += 1
            # u
            i = 0
            for control in self.env.start_controls:
                self.ui.tableWidget__inputu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(control[0])))
                self.ui.tableWidget__inputu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(control[1])))
                i += 1

    def initConnects(self):
        self.ui.lineEdit__inputTime.editingFinished.connect(self.set_time)
        self.ui.lineEdit__inputNodeAmount.editingFinished.connect(self.set_nodes_amount)
        self.ui.lineEdit__inputDistanceLinkOn.editingFinished.connect(self.set_distance_link_on)
        self.ui.lineEdit__inputDistanceLinkOff.editingFinished.connect(self.set_distance_link_off)
        self.ui.lineEdit__inputMaxSubNodes.editingFinished.connect(self.set_max_sub_nodes)
        self.ui.lineEdit__inputMaxTreeLength.editingFinished.connect(self.set_max_tree_length)
        self.ui.checkBox__inputProbDepending.clicked.connect(self.switch_prob_depending)
        self.ui.horizontalSlider__controlTime.valueChanged.connect(self.set_time_by_scrollbar)
        self.ui.spinBox__controlTime.valueChanged.connect(self.set_time_by_spinbox)
        self.ui.pushButton__showProbFunc.clicked.connect(self.show_prob_func)
        self.ui.pushButton__showProbFunc.clicked.connect(self.build_structure)

    def build_structure(self):
        self.env.calculate_structs_for_each_time(
            recalculate_probs=self.prob_depending,
            max_slaves=self.max_sub_nodes,
            max_depth=self.max_tree_length
        )
        self.is_structure_built = True

    def show_prob_func(self):
        calc_amount = 200
        dots = Utils.prob_func_dots(calc_amount, self.env.rolow, self.env.roupp)
        plt.plot(dots[0], dots[1])
        plt.show()

    def set_time(self):
        self.env.time = int(self.ui.lineEdit__inputTime.text())
        # Update spinbox and slider max val
        self.is_structure_built = False
        self.updateWidgets()

    def set_nodes_amount(self):
        self.env.set_nodes_amount(int(self.ui.lineEdit__inputNodeAmount.text()))
        # add new rows to matrices
        #self.ui.tableWidget__inputA.setRowCount(self.env.nodes_amount)
        #self.ui.tableWidget__inputA.setColumnCount(2)
        #self.ui.tableWidget__inputB.setRowCount(self.env.nodes_amount)
        #self.ui.tableWidget__inputB.setColumnCount(2)
        #self.ui.tableWidget__inputx.setRowCount(self.env.nodes_amount)
        #self.ui.tableWidget__inputx.setColumnCount(2)
        #self.ui.tableWidget__inputu.setRowCount(self.env.nodes_amount)
        #self.ui.tableWidget__inputu.setColumnCount(2)
        self.is_structure_built = False
        self.updateWidgets()


    def set_distance_link_on(self):
        self.env.rolow = int(self.ui.lineEdit__inputDistanceLinkOn.text())
        self.is_structure_built = False

    def set_distance_link_off(self):
        self.env.roupp = int(self.ui.lineEdit__inputDistanceLinkOff.text())
        self.is_structure_built = False

    def set_max_sub_nodes(self):
        self.max_sub_nodes = int(self.ui.lineEdit__inputMaxSubNodes.text())
        self.is_structure_built = False

    def set_max_tree_length(self):
        self.max_tree_length = int(self.ui.lineEdit__inputMaxTreeLength.text())
        self.is_structure_built = False

    def switch_prob_depending(self):
        self.prob_depending = not self.prob_depending
        self.is_structure_built = False

    def set_time_by_scrollbar(self):
        self.current_time = int(self.ui.horizontalSlider__controlTime.value())
        self.updateWidgets()

    def set_time_by_spinbox(self):
        self.current_time = int(self.ui.spinBox__controlTime.value())
        self.updateWidgets()

    #def build_structure(self):
    #    struct_builder = StructureBuilder()
    #    # TODO: add field to change number of digits after `,`
    #    digits_number = 5
    #    # Remake self.nodesCoords
    #    self.nodesCoords.clear()
    #    for i in range(self.nodesAmount):
    #        try:
    #            x = float(self.ui.tableWidget__nodesCoords.item(i, 0).text())
    #            y = float(self.ui.tableWidget__nodesCoords.item(i, 1).text())
    #        except AttributeError:
    #            warning_msg = QtWidgets.QMessageBox()
    #            warning_msg.setWindowTitle('Ошибка')
    #            warning_msg.setText('Введите корректные координаты')
    #            warning_msg.exec_()
    #            return
    #        node = (x, y)
    #        self.nodesCoords.append(node)
    #    # Connection probability matrix
    #    rolow = self.probfunc_dialog.rolow
    #    roupp = self.probfunc_dialog.roupp
    #    cprob = struct_builder.connection_probability(self.nodesCoords, rolow, roupp)
    #    self.ui.tableWidget__connectionsProb.setRowCount(self.nodesAmount)
    #    self.ui.tableWidget__connectionsProb.setColumnCount(self.nodesAmount)
    #    # C-styled array bypass should be rewritten
    #    for i in range(self.nodesAmount):
    #        for j in range(self.nodesAmount):
    #            self.ui.tableWidget__connectionsProb.setItem(i, j,
    #                QtWidgets.QTableWidgetItem(str(
    #                    round(cprob[i][j], digits_number)
    #                ))
    #            )
    #    self.ui.tableWidget__connectionsProb.resizeColumnsToContents()
    #    # Connection power matrix
    #    cpower = struct_builder.connection_power(cprob)
    #    self.ui.tableWidget__connectionsPower.setRowCount(self.nodesAmount)
    #    self.ui.tableWidget__connectionsPower.setColumnCount(self.nodesAmount)
    #    ## C-styled array bypass should be rewritten
    #    #for i in range(self.nodesAmount):
    #        for j in range(self.nodesAmount):
    #            self.ui.tableWidget__connectionsPower.setItem(i, j,
    #                QtWidgets.QTableWidgetItem(str(
    #                    round(cpower[i][j], digits_number)
    #                ))
    #            )
    #    self.ui.tableWidget__connectionsPower.resizeColumnsToContents()
    #    try:
    #        ## Generating adjacency matrix
    #        tree = struct_builder.build_tree(cprob,
    #            recalculate_probs=self.recalculateProbs,
    #            max_slaves=self.maxSlaves,
    #            max_depth=self.treeDepth
    #        )
    #        adjmx = nx.to_numpy_array(tree)
    #        #i, j = 0, 0
    #        for i in range(self.nodesAmount):
    #            for j in range(self.nodesAmount):
    #                # if i, j node is used in tree
    #                if adjmx[i][j] != 0:
    #                    self.ui.tableWidget__connectionsProb.item(i, j).setBackground(QtGui.QColor(100, 200, 130))
    #                    self.ui.tableWidget__connectionsPower.item(i, j).setBackground(QtGui.QColor(100, 200, 130))
    #        ## Drawing graph
    #        self.ui.widget.canvas.axes.clear()
    #        nx.draw_networkx(tree, pos=nx.planar_layout(tree), ax=self.ui.widget.canvas.axes)
    #        self.ui.widget.canvas.draw()
    #    except nx.exception.NetworkXException:
    #        warning_msg = QtWidgets.QMessageBox()
    #        warning_msg.setWindowTitle('Ошибка')
    #        warning_msg.setText('Оптимальное дерево не найдено')
    #        warning_msg.exec_()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

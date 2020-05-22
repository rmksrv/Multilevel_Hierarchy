import sys
import pickle
import networkx as nx
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from core import StructureBuilder, Utils
import forms.main_win as forms_mainwin
import forms.display_structure as forms_display
import resources_rc

# DEFAULT PARAMETERS
DEFAULT_TIME = 5
DEFAULT_ROLOW = 5
DEFAULT_ROUPP = 100
DEFAULT_MAX_SUB_NODES = 0
DEFAULT_MAX_TREE_DEPTH = 0
DEFAULT_PROB_DEPENDING = False
DEFAULT_NODE_COORDS = [
    (0.0, 0.0),
    (4.0, 0.0),
    (10.0, 0.0),
    (20.0, 3.0),
    (0.0, 3.0),
    (0.0, 6.0),
    (0.0, -3.0),
    (-5.0, 0.0),
]
DEFAULT_NODE_CONTROLS = [(0.0, 0.0) for i in DEFAULT_NODE_COORDS]
DEFAULT_A = [(1.0, 1.0) for i in DEFAULT_NODE_COORDS]
DEFAULT_B = [(1.0, 1.0) for i in DEFAULT_NODE_COORDS]
DEFAULT_NODES_AMOUNT = len(DEFAULT_NODE_COORDS)
DEFAULT_ROUND_DIGIT = 4
DEFAULT_SMOOTHING_FUNC = 'exp(b-a)/((x-a)(x-b))'

# Displaying structure window
class DisplayWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Base
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_display.Ui_MainWindow()
        self.ui.setupUi(self)
        # Matplotlib Toolbar
        self.addToolBar(NavigationToolbar(self.ui.widget__displayGraph.canvas, self))
        # Vars
        self.builder = StructureBuilder()
        self.current_time = 0
        self.history_coords = []
        self.history_controls = []
        self.history_graphs = []
        self.history_conn_probs = []
        self.history_conn_powers = []
        self.selected_layout = self.ui.comboBox__layoutSelect.currentText()
        # Connects setup
        self.initConnects()

    def initConnects(self):
        self.ui.horizontalSlider__currentTime.valueChanged.connect(self.set_time_by_scrollbar)
        self.ui.spinBox__currentTime.valueChanged.connect(self.set_time_by_spinbox)
        self.ui.comboBox__layoutSelect.activated[str].connect(self.set_selected_layout)

    def prepareWidgets(self):
        self.ui.horizontalSlider__currentTime.setMaximum(self.time - 1)
        self.ui.spinBox__currentTime.setMaximum(self.time - 1)

    def syncWidgets(self):
        self.syncNodeCoordsTable()
        self.syncNodeControlsTable()
        self.syncConnectionProbsTable()
        self.syncConnectionPowersTable()
        self.syncGraph()
        #print('Overall weight = ', nx.algorithms.tree.branchings.branching_weight(self.history_graphs[self.current_time], default=0))

    def syncNodeCoordsTable(self):
        # coords
        self.ui.tableWidget__displayx.setRowCount(self.nodes_amount)
        self.ui.tableWidget__displayx.setColumnCount(2)
        self.ui.tableWidget__displayx.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__displayx.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.history_coords[self.current_time]):
            self.ui.tableWidget__displayx.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__displayx.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))
        self.ui.tableWidget__displayx.resizeColumnsToContents()

    def syncNodeControlsTable(self):
        self.ui.tableWidget__displayu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__displayu.setColumnCount(2)
        self.ui.tableWidget__displayu.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__displayu.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.history_controls[self.current_time]):
            self.ui.tableWidget__displayu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__displayu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))
        self.ui.tableWidget__displayu.resizeColumnsToContents()

    def syncConnectionProbsTable(self):
        # get adjacency matrix to highlight using nodes
        adjacency_matrix = nx.to_numpy_array(self.history_graphs[self.current_time])
        # connection probs
        self.ui.tableWidget__displayConnProb.setRowCount(self.nodes_amount)
        self.ui.tableWidget__displayConnProb.setColumnCount(self.nodes_amount)
        self.ui.tableWidget__displayConnProb.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        self.ui.tableWidget__displayConnProb.setHorizontalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i in range(self.nodes_amount):
            for j in range(self.nodes_amount):
                # Set value of cell
                self.ui.tableWidget__displayConnProb.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(round(self.history_conn_probs[self.current_time][i][j], DEFAULT_ROUND_DIGIT))
                ))
                # If it is actual connection, then highlight it
                if adjacency_matrix[i][j] != 0:
                    self.ui.tableWidget__displayConnProb.item(i, j).setBackground(QtGui.QColor(100, 200, 100))
        self.ui.tableWidget__displayConnProb.resizeColumnsToContents()

    def syncConnectionPowersTable(self):
        # get adjacency matrix to highlight using nodes
        adjacency_matrix = nx.to_numpy_array(self.history_graphs[self.current_time])
        # connection powers
        self.ui.tableWidget__displayConnPower.setRowCount(self.nodes_amount)
        self.ui.tableWidget__displayConnPower.setColumnCount(self.nodes_amount)
        self.ui.tableWidget__displayConnPower.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        self.ui.tableWidget__displayConnPower.setHorizontalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i in range(self.nodes_amount):
            for j in range(self.nodes_amount):
                # Set value of cell
                self.ui.tableWidget__displayConnPower.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(round(self.history_conn_powers[self.current_time][i][j], DEFAULT_ROUND_DIGIT))
                ))
                # If it is actual connection, then highlight it
                if adjacency_matrix[i][j] != 0:
                    self.ui.tableWidget__displayConnPower.item(i, j).setBackground(QtGui.QColor(100, 200, 100))
        self.ui.tableWidget__displayConnPower.resizeColumnsToContents()

    def syncGraph(self):
        # graphs
        self.ui.widget__displayGraph.canvas.axes.clear()
        # Selecting a layout from self.selected_layout
        if self.selected_layout == 'Планарный вид':
            pos = nx.planar_layout(self.history_graphs[self.current_time])
        elif self.selected_layout == 'Декартова плоскость':
            pos = self.cartesian_coordinate_layout()
        # Edge labels
        edge_labels = { (u, v): round(d['weight'], DEFAULT_ROUND_DIGIT) for u, v, d in self.history_graphs[self.current_time].edges(data=True) }
        print(edge_labels)
        # And draw the graph
        nx.draw_networkx_nodes(
            self.history_graphs[self.current_time],
            pos=pos,
            nodelist=range(1,self.nodes_amount),
            node_color='#509bff',
            ax=self.ui.widget__displayGraph.canvas.axes,
        )
        nx.draw_networkx_nodes(
            self.history_graphs[self.current_time],
            pos=pos,
            nodelist=[0],
            node_color='#ff3b3f',
            ax=self.ui.widget__displayGraph.canvas.axes,
        )
        nx.draw_networkx_labels(
            self.history_graphs[self.current_time],
            pos=pos,
            ax=self.ui.widget__displayGraph.canvas.axes,
        )
        nx.draw_networkx_edges(
            self.history_graphs[self.current_time],
            pos=pos,
            ax=self.ui.widget__displayGraph.canvas.axes,
        )
        nx.draw_networkx_edge_labels(
            self.history_graphs[self.current_time],
            pos=pos,
            edge_labels=edge_labels,
            font_size=9,
            ax=self.ui.widget__displayGraph.canvas.axes,
        )
        #self.ui.widget__displayGraph.canvas.axes.axis('off')
        self.ui.widget__displayGraph.canvas.axes.figure.tight_layout()
        self.ui.widget__displayGraph.canvas.draw()

    def build_structure_for_ever(self):
        self.clear_history()
        curr_coords = self.node_coords
        curr_controls = self.node_controls
        for curr_time in range(self.time):
            # Building current struct
            curr_struct = self.build_structure(curr_coords)
            curr_graph = curr_struct['graph']
            curr_cprob = curr_struct['connection_prob']
            curr_cpower = curr_struct['connection_power']
            # Adding it to history
            self.history_coords.append(curr_coords)
            self.history_controls.append(curr_controls)
            self.history_graphs.append(curr_graph)
            self.history_conn_probs.append(curr_cprob)
            self.history_conn_powers.append(curr_cpower)
            # Calculating next coords and controls
            # coords
            next_coords = []
            for node in range(len(curr_coords)):
                next_x = self.A[node][0]*curr_coords[node][0] + self.B[node][0]*curr_controls[node][0]
                next_y = self.A[node][1]*curr_coords[node][1] + self.B[node][1]*curr_controls[node][1]
                next_coords.append((next_x, next_y))
            curr_coords = next_coords
            # controls
            next_controls = []
            for node in range(len(curr_controls)):  # - no changes for now
                next_x = curr_controls[node][0]
                next_y = curr_controls[node][1]
                next_controls.append((next_x, next_y))
            curr_controls = next_controls

    def build_structure(self, coords):
        # Building connection probability matrix
        conn_prob = self.builder.connection_probability(coords, self.rolow, self.roupp, self.smoothing_function)
        # Building connection power matrix
        conn_power = self.builder.connection_power(conn_prob)
        # And building a tree
        struct = self.builder.build_tree(
            cprob=conn_prob,
            recalculate_probs=self.prob_depending,
            max_slaves=self.max_sub_nodes,
            max_depth=self.max_tree_depth
        )
        # Result
        res = {
            'graph': struct,
            'connection_prob': conn_prob,
            'connection_power': conn_power
        }
        return res

    def cartesian_coordinate_layout(self):
        pos = {i: node for i, node in enumerate(self.history_coords[self.current_time])}
        return pos

    def clear_history(self):
        self.history_coords.clear()
        self.history_controls.clear()
        self.history_graphs.clear()
        self.history_conn_probs.clear()
        self.history_conn_powers.clear()

    def set_time_by_scrollbar(self):
        self.current_time = int(self.ui.horizontalSlider__currentTime.value())
        self.ui.spinBox__currentTime.setValue(self.current_time)
        self.syncWidgets()

    def set_time_by_spinbox(self):
        self.current_time = int(self.ui.spinBox__currentTime.value())
        self.ui.horizontalSlider__currentTime.setValue(self.current_time)
        self.syncWidgets()

    def set_selected_layout(self):
        self.selected_layout = self.ui.comboBox__layoutSelect.currentText()
        self.syncWidgets()


# Main Window (where you can set params of system)
class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Base
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_mainwin.Ui_MainWindow()
        self.ui.setupUi(self)
        # other windows
        self.display_window = DisplayWin()
        # Vars
        self.time = DEFAULT_TIME
        self.nodes_amount = DEFAULT_NODES_AMOUNT
        self.rolow = DEFAULT_ROLOW
        self.roupp = DEFAULT_ROUPP
        self.max_sub_nodes = DEFAULT_MAX_SUB_NODES
        self.max_tree_depth = DEFAULT_MAX_TREE_DEPTH
        self.prob_depending = DEFAULT_PROB_DEPENDING
        self.node_coords = DEFAULT_NODE_COORDS
        self.node_controls = DEFAULT_NODE_CONTROLS
        self.smoothing_function = DEFAULT_SMOOTHING_FUNC
        self.A = DEFAULT_A
        self.B = DEFAULT_B
        self.prepareWidgets()
        # Syncing widgets with own values
        self.syncWidgets()
        # Connects setup
        self.initConnects()

    def prepareWidgets(self):
        pixmap = QtGui.QPixmap('resources/next_node.png').scaledToHeight(64)
        self.ui.label__nextNode.setPixmap(pixmap)

    def initConnects(self):
        self.ui.lineEdit__inputTime.editingFinished.connect(self.set_time)
        self.ui.lineEdit__inputNodeAmount.editingFinished.connect(self.set_nodes_amount)
        self.ui.lineEdit__inputDistanceLinkOn.editingFinished.connect(self.set_distance_link_on)
        self.ui.lineEdit__inputDistanceLinkOff.editingFinished.connect(self.set_distance_link_off)
        self.ui.lineEdit__inputMaxSubNodes.editingFinished.connect(self.set_max_sub_nodes)
        self.ui.lineEdit__inputMaxTreeLength.editingFinished.connect(self.set_max_tree_length)
        self.ui.checkBox__inputProbDepending.clicked.connect(self.switch_prob_depending)
        self.ui.pushButton__showProbFunc.clicked.connect(self.show_prob_func)
        self.ui.pushButton__buildStructure.clicked.connect(self.build_structure)
        self.ui.pushButton__saveParams.clicked.connect(self.save_parameters)
        self.ui.pushButton__loadParams.clicked.connect(self.load_parameters)
        self.ui.comboBox__smoothFunc.activated[str].connect(self.set_smoothing_function)

    def syncWidgets(self):
        self.ui.lineEdit__inputTime.setText(str(self.time))
        self.ui.lineEdit__inputNodeAmount.setText(str(self.nodes_amount))
        self.ui.lineEdit__inputDistanceLinkOn.setText(str(self.rolow))
        self.ui.lineEdit__inputDistanceLinkOff.setText(str(self.roupp))
        self.ui.lineEdit__inputMaxSubNodes.setText(str(self.max_sub_nodes))
        self.ui.lineEdit__inputMaxTreeLength.setText(str(self.max_tree_depth))
        self.ui.checkBox__inputProbDepending.setChecked(self.prob_depending)
        self.ui.comboBox__smoothFunc.setCurrentText(self.smoothing_function)
        self.syncNodeCoordsTable()
        self.syncNodeControlsTable()
        self.syncTableA()
        self.syncTableB()

    def syncNodeCoordsTable(self):
        self.ui.tableWidget__inputx.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputx.setColumnCount(2)
        # Horizontal Headers
        self.ui.tableWidget__inputx.setHorizontalHeaderLabels(['x', 'y'])
        # Vertical Headers (default numeration is starting from '1')
        self.ui.tableWidget__inputx.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.node_coords):
            self.ui.tableWidget__inputx.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__inputx.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))

    def syncNodeControlsTable(self):
        self.ui.tableWidget__inputu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputu.setColumnCount(2)
        self.ui.tableWidget__inputu.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__inputu.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.node_controls):
            self.ui.tableWidget__inputu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__inputu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))

    def syncTableA(self):
        self.ui.tableWidget__inputA.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputA.setColumnCount(2)
        self.ui.tableWidget__inputA.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__inputA.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.A):
            self.ui.tableWidget__inputA.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__inputA.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))

    def syncTableB(self):
        self.ui.tableWidget__inputB.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputB.setColumnCount(2)
        self.ui.tableWidget__inputB.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__inputB.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.B):
            self.ui.tableWidget__inputB.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__inputB.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))

    def show_prob_func(self):
        calc_amount = 200
        dots = Utils.prob_func_dots(self.smoothing_function, calc_amount, self.rolow, self.roupp)
        plt.plot(dots[0], dots[1])
        plt.show()

    def set_time(self):
        self.time = int(self.ui.lineEdit__inputTime.text())

    def set_nodes_amount(self):
        self.nodes_amount = int(self.ui.lineEdit__inputNodeAmount.text())
        # Add rows to tables
        self.ui.tableWidget__inputx.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputA.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputB.setRowCount(self.nodes_amount)

    def set_distance_link_on(self):
        self.rolow = int(self.ui.lineEdit__inputDistanceLinkOn.text())

    def set_distance_link_off(self):
        self.roupp = int(self.ui.lineEdit__inputDistanceLinkOff.text())

    def set_max_sub_nodes(self):
        self.max_sub_nodes = int(self.ui.lineEdit__inputMaxSubNodes.text())

    def set_max_tree_length(self):
        self.max_tree_length = int(self.ui.lineEdit__inputMaxTreeLength.text())

    def switch_prob_depending(self):
        self.prob_depending = not self.prob_depending

    def set_smoothing_function(self):
        self.smoothing_function = self.ui.comboBox__smoothFunc.currentText()

    def collect_matrices(self):
        # Collect all inputs from matrices
        # x
        self.node_coords.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputx.item(i, 0).text())
                y = float(self.ui.tableWidget__inputx.item(i, 1).text())
            except AttributeError:
                warning_msg = QtWidgets.QMessageBox()
                warning_msg.setWindowTitle('Ошибка')
                warning_msg.setText('Введите корректные координаты')
                warning_msg.exec_()
                return
            self.node_coords.append((x, y))
        # u
        self.node_controls.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputu.item(i, 0).text())
                y = float(self.ui.tableWidget__inputu.item(i, 1).text())
            except AttributeError:
                warning_msg = QtWidgets.QMessageBox()
                warning_msg.setWindowTitle('Ошибка')
                warning_msg.setText('Введите корректное управление')
                warning_msg.exec_()
                return
            self.node_controls.append((x, y))
        # A
        self.A.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputA.item(i, 0).text())
                y = float(self.ui.tableWidget__inputA.item(i, 1).text())
            except AttributeError:
                warning_msg = QtWidgets.QMessageBox()
                warning_msg.setWindowTitle('Ошибка')
                warning_msg.setText('Введите корректные значения А')
                warning_msg.exec_()
                return
            self.A.append((x, y))
        # B
        self.B.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputB.item(i, 0).text())
                y = float(self.ui.tableWidget__inputB.item(i, 1).text())
            except AttributeError:
                warning_msg = QtWidgets.QMessageBox()
                warning_msg.setWindowTitle('Ошибка')
                warning_msg.setText('Введите корректные значения В')
                warning_msg.exec_()
                return
            self.B.append((x, y))


    def build_structure(self):
        self.display_window.clear_history()
        self.display_window.show()
        # Pass all params to display window
        self.collect_matrices()
        self.display_window.time = self.time
        self.display_window.nodes_amount = self.nodes_amount
        self.display_window.rolow = self.rolow
        self.display_window.roupp = self.roupp
        self.display_window.max_sub_nodes = self.max_sub_nodes
        self.display_window.max_tree_depth = self.max_tree_depth
        self.display_window.prob_depending = self.prob_depending
        self.display_window.node_coords = self.node_coords
        self.display_window.node_controls = self.node_controls
        self.display_window.A = self.A
        self.display_window.B = self.B
        self.display_window.smoothing_function = self.smoothing_function
        # Building structures for every time
        self.display_window.build_structure_for_ever()
        # And syncing its widgets
        self.display_window.prepareWidgets()
        self.display_window.syncWidgets()

    def save_parameters(self):
        self.collect_matrices()
        data_to_save = {
            'time': self.time,
            'nodes_amount': self.nodes_amount,
            'rolow': self.rolow,
            'roupp': self.roupp,
            'max_sub_nodes': self.max_sub_nodes,
            'max_tree_depth': self.max_tree_depth,
            'prob_depending': self.prob_depending,
            'node_coords': self.node_coords,
            'node_controls': self.node_controls,
            'A': self.A,
            'B': self.B,
            'smoothing_function': self.smoothing_function,
        }
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить')
        if filename:
            with open(filename, 'wb') as f:
                pickle.dump(data_to_save, f)

    def load_parameters(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Загрузить')
        if filename:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            self.time = data['time']
            self.nodes_amount = data['nodes_amount']
            self.rolow = data['rolow']
            self.roupp = data['roupp']
            self.max_sub_nodes = data['max_sub_nodes']
            self.max_tree_depth = data['max_tree_depth']
            self.prob_depending = data['prob_depending']
            self.node_coords = data['node_coords']
            self.node_controls = data['node_controls']
            self.A = data['A']
            self.B = data['B']
            self.smoothing_function = data['smoothing_function']
            self.syncWidgets()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

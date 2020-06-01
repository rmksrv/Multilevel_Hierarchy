import sys
import pickle
import networkx as nx
import numpy as np
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from core import StructureBuilder, Utils
import forms.main_win as forms_mainwin
import forms.display_structure as forms_display
import resources_rc

# DEFAULT PARAMETERS
DIM = 2
DEFAULT_TIME = 5
DEFAULT_ROLOW = 5
DEFAULT_ROUPP = 100
DEFAULT_MAX_SUB_NODES = 0
DEFAULT_MAX_TREE_DEPTH = 0
DEFAULT_PROB_DEPENDING = False
DEFAULT_NODE_COORDS = [
    [0.0, 0.0],
    [4.0, 0.0],
    [10.0, 0.0],
    [20.0, 3.0],
    [0.0, 3.0],
    [0.0, 6.0],
    [0.0, -3.0],
    [-5.0, 0.0],
]
DEFAULT_NODES_AMOUNT = len(DEFAULT_NODE_COORDS)
DEFAULT_CONTROL = [0.0, 0.0]
DEFAULT_NODE_CONTROLS = [DEFAULT_CONTROL for i in DEFAULT_NODE_COORDS]
DEFAULT_SINGLE_A = np.eye(DIM).tolist()
DEFAULT_A = [DEFAULT_SINGLE_A  for i in DEFAULT_NODE_COORDS]
DEFAULT_SINGLE_B = np.eye(DIM).tolist()
DEFAULT_B = [DEFAULT_SINGLE_B  for i in DEFAULT_NODE_COORDS]
DEFAULT_ROUND_DIGIT = 4
DEFAULT_SMOOTHING_FUNC = 'cos(ax+b)'
#DEFAULT_SMOOTHING_FUNC = 'exp(b-a)/((x-a)(x-b))'

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
        self.history_A =[]
        self.history_B =[]
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
            self.ui.tableWidget__displayx.setItem(i, 0, QtWidgets.QTableWidgetItem(str(round(node[0], DEFAULT_ROUND_DIGIT))))
            self.ui.tableWidget__displayx.setItem(i, 1, QtWidgets.QTableWidgetItem(str(round(node[1], DEFAULT_ROUND_DIGIT))))
        self.ui.tableWidget__displayx.resizeColumnsToContents()

    def syncNodeControlsTable(self):
        self.ui.tableWidget__displayu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__displayu.setColumnCount(2)
        self.ui.tableWidget__displayu.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__displayu.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.history_controls[self.current_time]):
            self.ui.tableWidget__displayu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(round(node[0], DEFAULT_ROUND_DIGIT))))
            self.ui.tableWidget__displayu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(round(node[1], DEFAULT_ROUND_DIGIT))))
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
        elif self.selected_layout == 'Круговой вид':
            pos = nx.circular_layout(self.history_graphs[self.current_time])
        elif self.selected_layout == 'Вид оболочки':
            pos = nx.shell_layout(self.history_graphs[self.current_time])
        elif self.selected_layout == 'Фрюхтерман-Рейнгольд':
            pos = nx.spring_layout(self.history_graphs[self.current_time])
        # Edge labels
        edge_labels = { (u, v): round(d['weight'], DEFAULT_ROUND_DIGIT) for u, v, d in self.history_graphs[self.current_time].edges(data=True) }
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
            alpha=0.8,
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

    def build_from_yaml(self):
        self.history_graphs.clear()
        self.history_conn_probs.clear()
        self.history_conn_powers.clear()
        for curr_coords in self.history_coords:
            curr_struct = self.build_structure(curr_coords)
            self.history_graphs.append(curr_struct['graph'])
            self.history_conn_probs.append(curr_struct['connection_prob'])
            self.history_conn_powers.append(curr_struct['connection_power'])

    def build_structure_for_ever(self):
        self.clear_history()
        curr_coords = self.node_coords
        curr_controls = self.node_controls
        curr_A = self.A
        curr_B = self.B
        for curr_time in range(self.time):
            # Building current struct
            curr_struct = self.build_structure(curr_coords)
            curr_graph = curr_struct['graph']
            curr_cprob = curr_struct['connection_prob']
            curr_cpower = curr_struct['connection_power']
            # Adding it to history
            self.history_A.append(curr_A)
            self.history_B.append(curr_B)
            self.history_coords.append(curr_coords)
            self.history_controls.append(curr_controls)
            self.history_graphs.append(curr_graph)
            self.history_conn_probs.append(curr_cprob)
            self.history_conn_powers.append(curr_cpower)
            # Calculating next coords and controls
            # A, B
            # NOTE: placeholder, cause A, B does not change now
            # coords
            next_coords = []
            for inode, coords in enumerate(curr_coords):
                #npA = np.array(self.A[inode])
                npA = np.array(curr_A[inode])
                npX = np.array(coords)
                tmp = (npA.dot(npX) + curr_controls[inode]).tolist()
                next_coords.append(tmp)
            curr_coords = next_coords
            # controls
            next_controls = []
            for inode, controls in enumerate(curr_controls):
                #npB = np.array(self.B[inode])
                npB = np.array(curr_B[inode])
                npU = np.array(controls)
                #tmp = (npB.dot(npU)).tolist()
                tmp = npU.tolist()
                next_controls.append(tmp)
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
        # supported extensions
        self.__supported_ext = {
            'Файл Pickle': '.pcl',
            'YAML файл': '.yaml',
        }
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
        self.current_agent = 0
        self.current_A = self.A[self.current_agent]
        self.current_B = self.B[self.current_agent]
        self.prepareWidgets()
        # Syncing widgets with own values
        self.syncWidgets()
        # Connects setup
        self.initConnects()

    def prepareWidgets(self):
        # Title
        self.setWindowTitle('Построение многоагентной среды')
        # Picture on top
        pixmap = QtGui.QPixmap('resources/next_node.png').scaledToHeight(64)
        self.ui.label__nextNode.setPixmap(pixmap)
        # Set min values for spinboxes in inputA/B
        self.ui.spinBox__currA.setMinimum(0)
        self.ui.spinBox__currB.setMinimum(0)
        self.ui.spinBox__currA.setMaximum(self.nodes_amount - 1)
        self.ui.spinBox__currB.setMaximum(self.nodes_amount - 1)

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
        self.ui.spinBox__currA.valueChanged.connect(self.set_current_agent_for_A)
        self.ui.spinBox__currB.valueChanged.connect(self.set_current_agent_for_B)
        self.ui.tableWidget__inputA.cellChanged[int, int].connect(self.set_A_for_current_agent)
        self.ui.tableWidget__inputB.cellChanged[int, int].connect(self.set_B_for_current_agent)

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
        self.ui.tableWidget__inputx.resizeColumnsToContents()

    def syncNodeControlsTable(self):
        self.ui.tableWidget__inputu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputu.setColumnCount(2)
        self.ui.tableWidget__inputu.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__inputu.setVerticalHeaderLabels(str(i) for i in range(self.nodes_amount))
        for i, node in enumerate(self.node_controls):
            self.ui.tableWidget__inputu.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))
            self.ui.tableWidget__inputu.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))
        self.ui.tableWidget__inputu.resizeColumnsToContents()

    # тут где-то проблема
    def syncTableA(self):
        # clear items
        self.ui.tableWidget__inputA.clearContents()
        # and start to fill cells
        self.ui.tableWidget__inputA.setRowCount(DIM)
        self.ui.tableWidget__inputA.setColumnCount(DIM)
        curr_A = self.A[self.current_agent]
        # Need to lock signals, to correctly setting A
        self.__lock_signal = True
        for i, row in enumerate(curr_A):
            for j, node in enumerate(row):
                self.ui.tableWidget__inputA.setItem(i, j, QtWidgets.QTableWidgetItem(str(node)))
        self.__lock_signal = False
        # Dont forget to unlock it
        self.ui.tableWidget__inputA.resizeColumnsToContents()

    def syncTableB(self):
        # clear items
        self.ui.tableWidget__inputB.clearContents()
        # and start to fill cells
        self.ui.tableWidget__inputB.setRowCount(DIM)
        self.ui.tableWidget__inputB.setColumnCount(DIM)
        curr_B = self.B[self.current_agent]
        # Need to lock signals, to correctly setting B
        self.__lock_signal = True
        for i, row in enumerate(curr_B):
            for j, node in enumerate(row):
                self.ui.tableWidget__inputB.setItem(i, j, QtWidgets.QTableWidgetItem(str(node)))
        self.__lock_signal = False
        # Dont forget to unlock it
        self.ui.tableWidget__inputB.resizeColumnsToContents()

    def show_prob_func(self):
        calc_amount = 200
        dots = Utils.prob_func_dots(self.smoothing_function, calc_amount, self.rolow, self.roupp)
        plt.plot(dots[0], dots[1])
        plt.show()

    def set_time(self):
        self.time = int(self.ui.lineEdit__inputTime.text())

    def set_nodes_amount(self):
        # Getting number of added agents
        delta = int(self.ui.lineEdit__inputNodeAmount.text()) - self.nodes_amount
        # If we are increasing amount of agents then extend set of A and B by eye matrices
        if delta > 0:
            self.A.extend(np.eye(DIM).tolist() for i in range(delta))
            self.B.extend(np.eye(DIM).tolist() for i in range(delta))
        # Else if decreasing, then just shrink them
        elif delta < 0:
            for i in range(-delta):
                self.A.pop()
                self.B.pop()
        self.nodes_amount = int(self.ui.lineEdit__inputNodeAmount.text())
        # Add rows to tables
        self.ui.tableWidget__inputx.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputu.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputA.setRowCount(self.nodes_amount)
        self.ui.tableWidget__inputB.setRowCount(self.nodes_amount)
        # Set max values for spinboxes in inputA/B
        self.ui.spinBox__currA.setMaximum(self.nodes_amount - 1)
        self.ui.spinBox__currB.setMaximum(self.nodes_amount - 1)
        self.syncWidgets()

    def set_distance_link_on(self):
        self.rolow = float(self.ui.lineEdit__inputDistanceLinkOn.text())

    def set_distance_link_off(self):
        self.roupp = float(self.ui.lineEdit__inputDistanceLinkOff.text())

    def set_max_sub_nodes(self):
        self.max_sub_nodes = int(self.ui.lineEdit__inputMaxSubNodes.text())

    def set_max_tree_length(self):
        self.max_tree_length = int(self.ui.lineEdit__inputMaxTreeLength.text())

    def switch_prob_depending(self):
        self.prob_depending = not self.prob_depending

    def set_smoothing_function(self):
        self.smoothing_function = self.ui.comboBox__smoothFunc.currentText()

    def set_current_agent_for_A(self):
        self.current_agent = int(self.ui.spinBox__currA.value())
        self.syncTableA()

    def set_current_agent_for_B(self):
        self.current_agent = int(self.ui.spinBox__currB.value())
        self.syncTableB()

    def set_A_for_current_agent(self):
        if not self.__lock_signal:
            self.A[self.current_agent].clear()
            for i in range(DIM):
                row = []
                for j in range(DIM):
                    try:
                        row.append(float(self.ui.tableWidget__inputA.item(i, j).text()))
                    except AttributeError:
                        self.error_message('Введите корректные значения А')
                        return
                self.A[self.current_agent].append(row)

    def set_B_for_current_agent(self):
        if not self.__lock_signal:
            self.B[self.current_agent].clear()
            for i in range(DIM):
                row = []
                for j in range(DIM):
                    try:
                        row.append(float(self.ui.tableWidget__inputB.item(i, j).text()))
                    except AttributeError:
                        self.error_message('Введите корректные значения А')
                        return
                self.B[self.current_agent].append(row)

    def error_message(self, text):
        warning_msg = QtWidgets.QMessageBox()
        warning_msg.setWindowTitle('Ошибка')
        warning_msg.setText(text)
        warning_msg.exec_()

    def collect_matrices(self):
        # Collect all inputs from matrices
        # x
        self.node_coords.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputx.item(i, 0).text())
                y = float(self.ui.tableWidget__inputx.item(i, 1).text())
            except AttributeError:
                self.error_message('Введите корректные значения А')
                return
            self.node_coords.append([x, y])
        # u
        self.node_controls.clear()
        for i in range(self.nodes_amount):
            try:
                x = float(self.ui.tableWidget__inputu.item(i, 0).text())
                y = float(self.ui.tableWidget__inputu.item(i, 1).text())
            except AttributeError:
                self.error_message('Введите корректные значения А')
                return
            self.node_controls.append([x, y])

    def build_structure_silent(self):
        self.display_window.clear_history()
        # Pass all params to display window
        self.pass_common_parameters()
        self.collect_matrices()
        self.display_window.node_coords = self.node_coords
        self.display_window.node_controls = self.node_controls
        self.display_window.A = self.A
        self.display_window.B = self.B
        # Building structures for every time
        self.display_window.build_structure_for_ever()

    def pass_common_parameters(self):
        self.display_window.time = self.time
        self.display_window.nodes_amount = self.nodes_amount
        self.display_window.rolow = self.rolow
        self.display_window.roupp = self.roupp
        self.display_window.max_sub_nodes = self.max_sub_nodes
        self.display_window.max_tree_depth = self.max_tree_depth
        self.display_window.smoothing_function = self.smoothing_function
        self.display_window.prob_depending = self.prob_depending

    def build_structure(self):
        self.display_window.clear_history()
        self.display_window.show()
        # Pass all params to display window
        self.pass_common_parameters()
        self.collect_matrices()
        self.display_window.node_coords = self.node_coords
        self.display_window.node_controls = self.node_controls
        self.display_window.A = self.A
        self.display_window.B = self.B
        # Building structures for every time
        self.display_window.build_structure_for_ever()
        # And syncing its widgets
        self.display_window.prepareWidgets()
        self.display_window.syncWidgets()

    def save_parameters(self):
        self.collect_matrices()
        supported_ext_str = ';;'.join('{text} (*{ext})'.format(text=key, ext=val) for key, val in self.__supported_ext.items())
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', '', supported_ext_str)
        if filename:
            ext = filename.split('.')[-1]
            # Pickle save
            if ext == 'pcl':
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
                with open(filename, 'wb') as f:
                    pickle.dump(data_to_save, f)
            # Text save (saving coords and controls only!!)
            elif ext == 'yaml':
                with open(filename, 'w') as f:
                    # First, we calculate x and u for each time
                    self.build_structure_silent()
                    # Then bypassing each time and write x and u
                    to_yaml = dict()
                    # rolow, roupp and smoothing func writing aswell
                    to_yaml.update({
                        'settings':{
                            'smoothing_function': self.smoothing_function,
                            'rolow': self.rolow,
                            'roupp': self.roupp,
                            'max_sub_nodes': self.max_sub_nodes,
                            'max_tree_depth': self.max_tree_depth,
                            'prob_depending': self.prob_depending,
                        }
                    })
                    to_yaml.update({'structure': {
                        t: {
                            'coordinates': {
                                i: coord for i, coord in enumerate(self.display_window.history_coords[t])
                            },
                            'controls': {
                                i: control for i, control in enumerate(self.display_window.history_controls[t])
                            },
                        } for t in range(self.time)
                    } })
                    yaml.dump(to_yaml, f, default_flow_style=False, indent=4)

    def load_parameters(self):
        supported_ext_str = ';;'.join('{text} (*{ext})'.format(text=key, ext=val) for key, val in self.__supported_ext.items())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Загрузить', '', supported_ext_str)
        if filename:
            ext = filename.split('.')[-1]
            # Pickle load
            if ext == 'pcl':
                self.load_from_pickle(filename)
                self.ui.spinBox__currA.setMaximum(self.nodes_amount - 1)
                self.ui.spinBox__currB.setMaximum(self.nodes_amount - 1)
                self.syncWidgets()
            # Text load (no opportunity to change system)
            elif ext == 'yaml':
                self.display_window.clear_history()
                try:
                    self.load_from_yaml(filename)
                except Exception as e:
                    #self.error_message(str(e))
                    #return
                    raise
                self.pass_common_parameters()
                self.display_window.build_from_yaml()
                self.display_window.prepareWidgets()
                self.display_window.show()
                self.display_window.syncWidgets()

    def load_from_pickle(self, filename):
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

    def load_from_yaml(self, filename):
        with open(filename, 'r') as f:
            loaded_yaml = yaml.safe_load(f)
            ## MAIN THINGS
            # Time
            try:
                self.time = loaded_yaml['settings']['time']
            except KeyError:
                self.time = len(loaded_yaml['structure'])
                #self.time = DEFAULT_TIME
            # Nodes amount
            # TODO: add prtection if not exist key
            self.nodes_amount = len(loaded_yaml['structure'][0]['coordinates'])
            # Features
            try:
                self.smoothing_function = loaded_yaml['settings']['smoothing_function']
            except KeyError:
                self.smoothing_function = DEFAULT_SMOOTHING_FUNC
            try:
                self.rolow = loaded_yaml['settings']['rolow']
            except KeyError:
                self.rolow = DEFAULT_ROLOW
            try:
                self.roupp = loaded_yaml['settings']['roupp']
            except KeyError:
                self.roupp = DEFAULT_ROUPP
            try:
                self.max_sub_nodes = loaded_yaml['settings']['max_sub_nodes']
            except KeyError:
                self.max_sub_nodes = DEFAULT_MAX_SUB_NODES
            try:
                self.max_tree_depth = loaded_yaml['settings']['max_tree_depth']
            except KeyError:
                self.max_tree_depth = DEFAULT_MAX_TREE_DEPTH
            try:
                self.prob_depending = loaded_yaml['settings']['prob_depending']
            except KeyError:
                self.prob_depending = DEFAULT_PROB_DEPENDING
            #
            ## STRUCTURE
            for t, vect in loaded_yaml['structure'].items():
                #print('t = ', t)
                # A
                curr_A = []
                try:
                    for node, A in sorted(vect['A'].items()):
                        curr_A.append(A)
                except KeyError:
                    if t == 0:
                        # If t == 0 then set it default for each node (diagonal one)
                        curr_A = [DEFAULT_SINGLE_A for i in range(self.nodes_amount)]
                    else:
                        # else current A's == previous A's
                        curr_A = self.display_window.history_A[t-1]
                finally:
                    self.display_window.history_A.append(curr_A)
                    #print('curr_A =\n', curr_A)
                # B
                curr_B = []
                try:
                    for node, B in sorted(vect['B'].items()):
                        curr_B.append(B)
                except KeyError:
                    if t == 0:
                        # If t == 0 then set it default for each node (diagonal one)
                        curr_B = [DEFAULT_SINGLE_B for i in range(self.nodes_amount)]
                    else:
                        # else current B's == previous B's
                        curr_B = self.display_window.history_B[t-1]
                finally:
                    self.display_window.history_B.append(curr_B)
                    #print('curr_B =\n', curr_B)
                # Controls
                curr_controls = []
                try:
                    for node, controls in sorted(vect['controls'].items()):
                        curr_controls.append(controls)
                except KeyError:
                    if t == 0:
                        curr_controls = [DEFAULT_CONTROL for i in range(self.nodes_amount)]
                    else:
                        curr_controls = self.display_window.history_controls[t-1]
                finally:
                    self.display_window.history_controls.append(curr_controls)
                    #print('curr_controls =\n', curr_controls)
                # Coords
                curr_coords = []
                try:
                    for node, coords in sorted(vect['coordinates'].items()):
                        curr_coords.append(coords)
                except KeyError:
                    if t == 0:
                        # if we don't found it for 1st t, raise exception
                        self.error_message('YAML файл не содержит стартовых координат')
                        raise
                        # NOTE: actually we can set it by zeroes, but we have to get nodes_amount
                    else:
                        # 1. get previous coords
                        prev_coords = self.display_window.history_coords[t-1]
                        # 2. calculate new coords basing on prev coords
                        curr_coords = []
                        for inode, coords in enumerate(prev_coords):
                            #npA = np.array(self.display_window.history_A[t][inode])
                            npA = np.array(self.display_window.history_A[t][inode])
                            npX = np.array(coords)
                            tmp = (npA.dot(npX) + self.display_window.history_controls[t][inode]).tolist()
                            curr_coords.append(tmp)
                finally:
                    self.display_window.history_coords.append(curr_coords)
                    #print('curr_coords =\n', curr_coords)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

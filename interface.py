import sys
# Core
from core import StructureBuilder, Utils
# Qt imports
from PyQt5 import QtCore, QtGui, QtWidgets
import forms.multiagent_structure_main_win as forms_mainwin


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Base
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = forms_mainwin.Ui_MainWindow()
        self.ui.setupUi(self)
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
        #vert_labels = [str(i) for i in range(self.nodesAmount)]
        #self.ui.tableWidget__nodesCoords.setVerticalHeaderLabels(vert_labels)
        i = 0
        for node in self.nodesCoords:
            self.ui.tableWidget__nodesCoords.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node[0])))  # add x value to `i` row
            self.ui.tableWidget__nodesCoords.setItem(i, 1, QtWidgets.QTableWidgetItem(str(node[1])))  # and y value too
            i += 1
        # Connects
        self.ui.pushButton__buildStructure.clicked.connect(self.build_structure)
        self.ui.lineEdit__nodeAmount.editingFinished.connect(self.set_nodesAmount)
        self.ui.lineEdit__maxSlaves.editingFinished.connect(self.set_nodesAmount)
        self.ui.lineEdit__treeDepth.editingFinished.connect(self.set_nodesAmount)
        self.ui.checkBox__recalculate_probs.clicked.connect(self.set_recalculateProbs)

    def build_structure(self):
        struct_builder = StructureBuilder()
        cprob = struct_builder.connection_probability(self.nodesCoords)
        adjmx = struct_builder.build_tree(cprob, as_matrix=True, 
                recalculate_probs=self.recalculateProbs,
                max_slaves=self.maxSlaves,
                max_depth=self.treeDepth
        )
        # Print matrix to table

        self.ui.tableWidget__connectionsPower.setRowCount(self.nodesAmount)
        self.ui.tableWidget__connectionsPower.setColumnCount(self.nodesAmount)
        # TODO: add field to change number of digits after `,`
        digits_number = 5
        i, j = 0, 0
        for i in range(self.nodesAmount):
            for j in range(self.nodesAmount):
                self.ui.tableWidget__connectionsPower.setItem(i, j, 
                    QtWidgets.QTableWidgetItem(str(
                        round(adjmx[i][j], digits_number)
                    ))
                )


    def set_nodesAmount(self):
        # TODO: add check of value correctness 
        self.nodesAmount = int(self.ui.lineEdit__nodeAmount.text())
        self.ui.tableWidget__nodesCoords.setRowCount(self.nodesAmount)

    def set_maxSlaves(self):
        # TODO: add check of value correctness 
        self.maxSlaves = int(self.ui.lineEdit__maxSlaves.text())

    def set_treeDepth(self):
        # TODO: add check of value correctness 
        self.treeDepth = int(self.ui.lineEdit__treeDepth.text())

    def set_recalculateProbs(self):
        self.recalculateProbs = not self.recalculateProbs




if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

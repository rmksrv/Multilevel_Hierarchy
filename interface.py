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
        self.nodesAmount = 5
        # sync my vars with widget values
        self.ui.lineEdit__nodeAmount.setText(str(self.nodesAmount))  # nodes amount
        self.ui.tableWidget__nodesCoords.setHorizontalHeaderLabels(['x', 'y'])
        self.ui.tableWidget__nodesCoords.setRowCount(self.nodesAmount)
        # Connects
        self.ui.pushButton__buildStructure.clicked.connect(self.build_structure)
        self.ui.lineEdit__nodeAmount.editingFinished.connect(self.set_nodesAmount)

    def build_structure(self):
        pass

    def set_nodesAmount(self):
        # TODO: add check of value correctness 
        self.nodesAmount = int(self.ui.lineEdit__nodeAmount.text())
        self.ui.tableWidget__nodesCoords.setRowCount(self.nodesAmount)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())

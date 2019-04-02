import os
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow,QWidget
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMenuBar
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import QEventLoop
import time
from mib_dialog.new_connection_dlg import NewConnectionDlg
from db_tree.mib_tree_widget import MibTreeWidget
from data_widget.data_widget import DataWidget
from task.mibload_task import MibLoadTask
from mib.mib import Mib
from frame.entity_parser import EntityParser
from utils.utils import to_python_str
from onu.connection_manager import ConnectionManager

ICON_IDR = os.path.join(os.path.dirname(__file__),'../icon/')
class MibMainwindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.__setup_ui()
        self.__connect_slot()
        self.__entity_parser = EntityParser()
        self.__entity_parser.parse()


    def __setup_ui(self):
        self.resize(1024,768)
        self.__setup_menu()

        split = QSplitter()
        self.__mib_tree_widget = MibTreeWidget()
        split.addWidget(self.__mib_tree_widget)
        #
        self.__data_widget = DataWidget()
        split.addWidget(self.__data_widget)
        split.setHandleWidth(2)
        split.setStretchFactor(0,1)
        split.setStretchFactor(1,200)

        la = QVBoxLayout()
        self.__progress_bar = QProgressBar()
        self.__progress_bar.setValue(0)
        self.__progress_bar.setVisible(False)
        la.addWidget(self.__progress_bar,1)
        la.addWidget(split,1)

        cw = QWidget()
        cw.setLayout(la)

        self.setCentralWidget(cw)



    def __setup_menu(self):
        fileMenu = QMenu("Db", self)
        profileMenu = QMenu('Profiles',self)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(profileMenu)

        self.__new_action = QAction(QIcon(ICON_IDR + 'add_database.png'),"&New", fileMenu)
        fileMenu.addAction(self.__new_action)

        self.__profile_action = QAction(QIcon(ICON_IDR + 'profiles.png'),"&Open profiles", profileMenu)
        profileMenu.addAction(self.__profile_action)

        tool_bar = QToolBar()
        tool_bar.setMovable(False)
        tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        tool_bar.addAction(self.__new_action)
        tool_bar.addAction(self.__profile_action)
        tool_bar.setIconSize(QSize(30,30))
        #tool_bar.setStyleSheet("QToolButton { padding-left: 5px; padding-right: 5px; }  QToolBar{padding-left: 5px; padding-right: 5px}")

        self.addToolBar(tool_bar)

    def __connect_slot(self):
        self.connect(self.__new_action,SIGNAL('triggered()'), self, SLOT('__on_new_action()'))
        self.connect(self.__mib_tree_widget,
                     SIGNAL('table_double_clicked(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'),
                     self, SLOT('__on_table_double_clicked(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'))

    @pyqtSlot()
    def __on_new_action(self):
        new_dlg = NewConnectionDlg()
        if new_dlg.exec_():



            # for i in range(0,100):
            #     self.__progress_bar.setValue(i)
            #     time.sleep(0.01)
            #     QApplication.processEvents()
            # self.__progress_bar.setValue(100)

            olt_key = ConnectionManager().add_dolt_connection('192.168.200.131', 9192, '111')
            onu_key = ConnectionManager().add_onu_communicator(olt_key, slot_id=1, intf_id=0, onu_id=1)
            task = MibLoadTask()

            self.__progress_bar.setVisible(True)
            for i,n in task.do(onu_key):
                self.__progress_bar.setValue(i*100/n)
                QApplication.processEvents()

            self.__progress_bar.setValue(100)
            self.__progress_bar.setVisible(False)
            mib = task.get_mib()

            # mib = Mib()
            # mib.load_from_file()
            keys = []
            for k in mib.get_keys():
                keys.append(self.__entity_parser.get_cls_name_by_id(k))
            self.__mib_tree_widget.add_mib_tree('192.168.200.131',9192,1,0,1,keys)

    @pyqtSlot('PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    def __on_table_double_clicked(self, identify, me_name,label_color):
        # table_name type is PyQt4.QtCore.QString,con_key type is str
        mib = Mib()
        mib.load_from_file()
        #self.__data_widget.add_tab(identify, to_python_str(con_key), to_python_str(table_name), label_color)
        me_id = self.__entity_parser.get_me_id_by_me_name(me_name)
        self.__data_widget.add_tab(identify,self.__entity_parser.get_cls_by_id(me_id),mib.get_entity_class_value(me_id),label_color)
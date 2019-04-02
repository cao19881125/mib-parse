import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QRegExpValidator
from utils.utils import to_python_str

class NewConnectionDlg(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.host = ''
        self.port = 0
        self.schema = ''
        self.__host_reg = QRegExp("^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\."
                                + "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
                                + "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
                                + "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$")
        self.__port_reg = QRegExp("[1-9][0-9]{0,4}")
        self.__host_correct = False
        self.__port_correct = False
        self.__setup_ui()
        self.__connect_slot()


    def __setup_ui(self):
        self.setMaximumSize(300,300)
        self.setMinimumSize(300,300)
        vlayout = QVBoxLayout()

        host_layout = QHBoxLayout()
        port_layout = QHBoxLayout()
        slotid_layout = QHBoxLayout()
        intfid_layout = QHBoxLayout()
        onuid_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        host_layout.addWidget(QLabel('Host'),3)
        self.__host_edit = QLineEdit('192.168.184.128')
        #self.__host_edit = QLineEdit()
        self.__host_edit.setValidator(QRegExpValidator(self.__host_reg))
        host_layout.addWidget(self.__host_edit,7)

        port_layout.addWidget(QLabel('Port'),3)
        self.__port_edit = QLineEdit('6641')
        #self.__port_edit = QLineEdit()
        self.__port_edit.setValidator(QRegExpValidator(self.__port_reg))
        port_layout.addWidget(self.__port_edit,7)

        slotid_layout.addWidget(QLabel('Slot id'), 3)
        # self.__port_edit = QLineEdit('6641')
        self.__slotid_edit = QLineEdit('1')
        self.__slotid_edit.setValidator(QRegExpValidator(QRegExp("[0-9]")))
        slotid_layout.addWidget(self.__slotid_edit, 7)

        intfid_layout.addWidget(QLabel('Intf id'), 3)
        self.__intfid_edit = QLineEdit('0')
        self.__intfid_edit.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
        intfid_layout.addWidget(self.__intfid_edit, 7)

        onuid_layout.addWidget(QLabel('Intf id'), 3)
        # self.__port_edit = QLineEdit('6641')
        self.__onuid_edit = QLineEdit('1')
        self.__onuid_edit.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
        onuid_layout.addWidget(self.__onuid_edit, 7)

        self.ok_btn = QPushButton('ok')
        #self.ok_btn.setFlat(True)
        #self.ok_btn.setEnabled(False)
        self.cancel_btn = QPushButton('cancel')
        btn_layout.addWidget(self.ok_btn,5)
        btn_layout.addWidget(self.cancel_btn,5)

        vlayout.addLayout(host_layout)
        vlayout.addLayout(port_layout)
        vlayout.addLayout(slotid_layout)
        vlayout.addLayout(intfid_layout)
        vlayout.addLayout(onuid_layout)
        vlayout.addLayout(btn_layout)

        self.setLayout(vlayout)

    def __connect_slot(self):
        self.connect(self.ok_btn,SIGNAL('clicked()'),self,SLOT('__on_ok_btn()'))
        self.connect(self.cancel_btn,SIGNAL('clicked()'),self,SLOT('reject()'))
        self.connect(self.__host_edit,SIGNAL('textChanged(QString)'),self,SLOT('__on_host_edit_change(QString)'))
        self.connect(self.__port_edit,SIGNAL('textChanged(QString)'),self,SLOT('__on_port_edit_change(QString)'))

    @pyqtSlot()
    def __on_ok_btn(self):
        self.host = to_python_str(self.__host_edit.text())
        self.port = int(self.__port_edit.text() if (self.__port_edit.text() != '') else '0')
        self.slotid = int(self.__slotid_edit.text() if (self.__slotid_edit.text() != '') else '1' )
        self.intfid = int(self.__intfid_edit.text() if (self.__intfid_edit.text() != '') else '0' )
        self.onuid = int(self.__onuid_edit.text() if (self.__onuid_edit.text() != '') else '1' )
        self.accept()

    @pyqtSlot('QString')
    def __on_host_edit_change(self, text):
        if self.__host_reg.exactMatch(text):
            self.__host_edit.setStyleSheet('border: 2px groove ;border-color: green;')
            self.__host_correct = True
        else:
            self.__host_edit.setStyleSheet('border: 2px groove ;border-color: red;')
            self.__host_correct = False

        self.__check_ok()

    @pyqtSlot('QString')
    def __on_port_edit_change(self, text):
        if self.__port_reg.exactMatch(text):
            self.__port_edit.setStyleSheet('border: 2px groove ;border-color: green;')
            self.__port_correct = True
        else:
            self.__port_edit.setStyleSheet('border: 2px groove ;border-color: red;')
            self.__port_correct = False
        self.__check_ok()

    def __check_ok(self):
        if self.__host_correct and self.__port_correct:
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)


if __name__== '__main__':
    app = QApplication(sys.argv)

    test_widget = NewConnectionDlg()

    test_widget.show()
    sys.exit(app.exec_())

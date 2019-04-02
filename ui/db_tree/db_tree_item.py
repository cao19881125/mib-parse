import os
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QIcon
from utils.utils import get_uuid
ICON_IDR = os.path.join(os.path.dirname(__file__),'../../icon/')

class DbTreeItem(QTreeWidgetItem):
    def __init__(self, con_name, onu_info, me_names,label_color):
        QTreeWidgetItem.__init__(self)
        self.__con_name = con_name
        self.__onu_info = onu_info
        self.__me_names = me_names
        self.__label_color = label_color
        self.__uuid = get_uuid()
        self.__setup_ui()


    def __setup_ui(self):
        #self.setText(0, self.__con_name)
        self.setIcon(0,QIcon(ICON_IDR + 'database.png'))


        self.__db_item = QTreeWidgetItem(self)
        self.__db_item.setIcon(0,QIcon(ICON_IDR + 'dir_close.png'))
        self.__db_item.setText(0, self.__onu_info)

        for table in self.__me_names:
            table_item = QTreeWidgetItem(self.__db_item)
            table_item.setIcon(0,QIcon(ICON_IDR + 'table.png'))
            table_item.setText(0, str(table))

    def get_default_expand_items(self):
        items = []
        items.append(self)
        items.append(self.__db_item)
        return items

    def item_expand(self,item):
        if item is self:
            # do nothing
            return

        for i in range(self.childCount()):
            if item is self.child(i):
                item.setIcon(0,QIcon(ICON_IDR + 'dir_open.png'))
    def item_collapsed(self, item):
        if item is self:
            # do nothing
            return

        for i in range(self.childCount()):
            if item is self.child(i):
                item.setIcon(0,QIcon(ICON_IDR + 'dir_close.png'))

    def item_double_click(self, item):
        if item is self:
            # do nothing
            return None

        for i in range(self.childCount()):
            # database layer
            if item is self.child(i):
                return None
            child_item = self.child(i)
            for d in range(child_item.childCount()):
                if item is child_item.child(d):
                    return item.text(0)

    def get_uuid(self):
        return self.__uuid

    def get_label_color(self):
        return self.__label_color
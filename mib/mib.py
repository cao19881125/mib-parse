import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from frame.omci_messages import OmciMibUploadNextResponse
from me import Me
class Mib(object):
    def __init__(self):
        self.__mib = {}

    def put_me(self,omci_frame):
        if type(omci_frame.omci_message) is not OmciMibUploadNextResponse:
            return


        entity_class_id = int(omci_frame.omci_message.object_entity_class)
        entity_id = int(omci_frame.omci_message.object_entity_id)

        if not self.__mib.has_key(entity_class_id):
            eclass = {}
            self.__mib[entity_class_id] = eclass
        else:
            eclass = self.__mib[entity_class_id]

        if not eclass.has_key(entity_id):
            me = Me()
        else:
            me = eclass[entity_id]

        me.entity_class_id = entity_class_id
        me.entity_id = entity_id
        me.obj_data.update(omci_frame.omci_message.object_data)

        eclass[entity_id] = me


    def show(self):
        for class_id,v in self.__mib.items():
            for entity_id,me in v.items():
                print me

    def save_to_file(self):
        f = open('mib_cache.txt','w')
        mib_str_dic = self.__mib.copy()
        for class_id,v in mib_str_dic.items():
            for entity_id,me in v.items():
                mib_str_dic[class_id][entity_id] = str(me)

        f.write(str(mib_str_dic))

    def load_from_file(self):
        f = open('mib_cache.txt','r')
        mib_str = f.readline()
        mib_str_dic = eval(mib_str)
        for class_id,v in mib_str_dic.items():
            for entity_id,me_str in v.items():
                me = Me()
                me.from_str(me_str)
                mib_str_dic[class_id][entity_id] = me
        self.__mib = mib_str_dic

    def get_keys(self):
        return self.__mib.keys()

    def get_entity_class_value(self,entity_class_id):
        if not self.__mib.has_key(entity_class_id):
            return None
        return self.__mib[entity_class_id]

if __name__ == '__main__':
    m = Mib()
    m.load_from_file()
    m.show()


class Me(object):
    def __init__(self):
        self.entity_class_id = 0
        self.entity_id = 0
        self.obj_data = {}

    def __str__(self):
        return str({'entity_class_id':self.entity_class_id,'entity_id':self.entity_id,'obj_data':str(self.obj_data)})

    def from_str(self,me_str):
        me_dic = eval(me_str)
        self.entity_class_id = me_dic['entity_class_id']
        self.entity_id = me_dic['entity_id']
        self.obj_data = eval(me_dic['obj_data'])
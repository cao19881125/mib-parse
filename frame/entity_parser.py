import omci_entities

class EntityParser(object):

    def __init__(self):
        self.__entity_classes = {}

    def parse(self):
        for attr_name in dir(omci_entities):
            cls = getattr(omci_entities, attr_name)
            if not isinstance(cls, type) or not issubclass(cls, omci_entities.EntityClass):
                continue
            self.__entity_classes[cls.class_id] = cls

    def get_cls_by_id(self,id):
        if self.__entity_classes.has_key(id):
            return self.__entity_classes[id]
        return None

    def get_cls_name_by_id(self,id):
        if self.__entity_classes.has_key(id):
            return self.__entity_classes[id].__name__
        return None

    def get_me_id_by_me_name(self,me_name):
        for k,v in self.__entity_classes.items():
            if v.__name__ == me_name:
                return k

        return None
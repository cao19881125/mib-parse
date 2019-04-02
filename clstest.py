
from frame import omci_entities

if __name__ == '__main__':
    for attr_name in dir(omci_entities):
        cls = getattr(omci_entities,attr_name)
        if not isinstance(cls,type) or not issubclass(cls,omci_entities.EntityClass):
            continue
        #print cls,cls.class_id,cls.__name__
        for attr in cls.attributes:
            print attr.field.name
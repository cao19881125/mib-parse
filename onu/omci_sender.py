from proto.dolt_pb2 import OmciMsg,Empty
from common import hexify


class OmciSender(object):
    def __init__(self,con,**kwargs):
        self.__con = con
        self.__kwargs = kwargs

    def send(self,omci_frame):

        def construct_msg(msg):
            omci_msg = OmciMsg(olt_id=self.__kwargs['olt_id'],
                               slot_id=self.__kwargs['slot_id'],
                               intf_id=self.__kwargs['intf_id'],
                               onu_id=self.__kwargs['onu_id'],
                               pkt=str(msg))
            yield omci_msg

        #msg = hexify(str(omci_frame))
        msg = str(omci_frame)
        iterator = construct_msg(msg)

        self.__con.SendOmci(iterator)
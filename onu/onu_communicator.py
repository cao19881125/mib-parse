import grpc
from omci_sender import OmciSender
from omci_receiver import OmciReceiver
from proto.dolt_pb2_grpc import dOLTStub

class OnuCommuincator(object):
    def __init__(self,stub,olt_id,slot_id,intf_id,onu_id):
        self.__onu_info = {'olt_id':olt_id,
                           'slot_id':slot_id,
                           'intf_id':intf_id,
                           'onu_id':onu_id}
        # con = grpc.insecure_channel(dolt_ip + ":" + str(port))
        # self.__stub = dOLTStub(channel=con)
        self.__stub = stub
        self.__sender = OmciSender(self.__stub, **self.__onu_info)
        self.__receiver = OmciReceiver(self.__stub, **self.__onu_info)



    def run(self):
        self.__receiver.start()


    def stop(self):
        pass


    def send_omci_msg(self,omci_frame):
        self.__sender.send(omci_frame)

    def recv_omci_msg(self,block=True,timeout=None):

        return self.__receiver.get_msg(block,timeout)

    def clear_onu_cache(self):
        while True:
            res = self.__receiver.get_msg(True,0.5)
            if res is None:
                break
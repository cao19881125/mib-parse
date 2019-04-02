import grpc
from utils.utils import singleton,olt_con_hash_code,onu_con_has_code
from proto.dolt_pb2_grpc import dOLTStub
from onu_communicator import OnuCommuincator

@singleton
class ConnectionManager(object):
    def __init__(self):
        self.__connections = {}
        self.__onu_communicators = {}

    def add_dolt_connection(self,ip,port,olt_id):
        olt_key = olt_con_hash_code(ip,port)
        con = grpc.insecure_channel(ip + ":" + str(port))
        stub = dOLTStub(channel=con)
        olt_info = {'ip':ip,'port':port,'olt_id':olt_id,'stub':stub}
        self.__connections[olt_key] = olt_info

        return olt_key



    def add_onu_communicator(self,olt_key,slot_id,intf_id,onu_id):
        if not self.__connections.has_key(olt_key):
            return None

        olt_stub = self.__connections[olt_key]['stub']

        onu_key = onu_con_has_code(olt_key,slot_id,intf_id,onu_id)
        onu_com = OnuCommuincator(olt_stub,self.__connections[olt_key]['olt_id'],slot_id,intf_id,onu_id)
        onu_info = {'olt_key':olt_key,'slot_id':slot_id,'intf_id':intf_id,'onu_id':onu_id,'communicator':onu_com}
        self.__onu_communicators[onu_key] = onu_info

        onu_com.run()

        return onu_key

    def get_onu_communicator_by_onu_key(self,onu_key):
        if not self.__onu_communicators.has_key(onu_key):
            return None

        return self.__onu_communicators[onu_key]['communicator']

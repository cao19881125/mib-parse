import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from onu.onu_communicator import OnuCommuincator
from frame.me_frame import MEFrame
from frame import omci_entities
import time
from mib.mib import Mib
from onu.connection_manager import ConnectionManager

class MibLoadTask(object):
    def __init__(self):
        self.__mib = Mib()

    def do(self,onu_key):

        # onu_con = OnuCommuincator(dolt_ip='192.168.200.131',
        #                           port=9192,
        #                           olt_id='0001796bcf3dee05',
        #                           slot_id=1,
        #                           intf_id=0,
        #                           onu_id=1)
        #
        # onu_con.run()
        onu_con = ConnectionManager().get_onu_communicator_by_onu_key(onu_key)

        if not onu_con:
            return

        onu_con.clear_onu_cache()

        mf = MEFrame(transaction_id=0, entity_class=omci_entities.OntData, entity_id=0, data={})
        f = mf.mib_upload()


        onu_con.send_omci_msg(f)

        response = onu_con.recv_omci_msg()
        print response.show()

        for i in range(0,int(response.omci_message.number_of_commands)):
            mf = MEFrame(transaction_id=i+1, entity_class=omci_entities.OntData, entity_id=0,
                         data={'mib_data_sync': i})
            f = mf.mib_upload_next()
            onu_con.send_omci_msg(f)
            yield i,int(response.omci_message.number_of_commands)



        while True:
            response = onu_con.recv_omci_msg(timeout=0.1)
            if response is not None:
                #print response.show()
                self.__mib.put_me(response)
            else:
                break

        #self.__mib.save_to_file()


    def get_mib(self):
        return self.__mib


if __name__ == '__main__':
    olt_key = ConnectionManager().add_dolt_connection('192.168.200.131',9192,'111')
    onu_key = ConnectionManager().add_onu_communicator(olt_key,slot_id=1,intf_id=0,onu_id=1)
    task = MibLoadTask()
    task.do(onu_key)
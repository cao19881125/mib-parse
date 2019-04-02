import sys
import time
import thread
import grpc
from proto.dolt_pb2_grpc import dOLTStub
from proto.dolt_pb2 import OmciMsg,Empty
from frame.me_frame import MEFrame,OmciFrame
import frame.omci_entities

olt_id = '0001d46bf22df737'
onu_id = 1

def hexify(buffer):
    """
    Return a hexadecimal string encoding of input buffer
    """
    return ''.join('%02x' % ord(c) for c in buffer)

def send_msg(msg):

    omci_msg = OmciMsg(olt_id=olt_id,slot_id=1,intf_id=0,onu_id=1,pkt=str(msg))
    yield omci_msg

def recv_msg(stub):
    response = stub.ReceiveOmci(Empty())

    try:
        for r in response:
            print hexify(r.pkt)
            print OmciFrame(r.pkt).show()
    except Exception,e:
        print "To OmciFrame Failed"


def recv_thread(stub):
    while True:
        recv_msg(stub)

def main():
    con = grpc.insecure_channel("192.168.200.131:9192")
    channel_ready_future = grpc.channel_ready_future(con)
    client = dOLTStub(channel=con)
    channel_ready_future.result()


    thread.start_new_thread(recv_thread,(client,))

    mf = MEFrame(transaction_id=0, entity_class=frame.omci_entities.OntData, entity_id=0, data={})
    f = mf.mib_upload()
    msg = hexify(str(f))
    iterrator = send_msg(msg)

    client.SendOmci(iterrator)

    #recv_msg(client)

    trn_id = 1

    for i in range(0,20):
        mf = MEFrame(transaction_id=trn_id, entity_class=frame.omci_entities.OntData, entity_id=0, data={'mib_data_sync':i})
        f = mf.mib_upload_next()
        msg = hexify(str(f))
        iterrator = send_msg(msg)
        client.SendOmci(iterrator)
        #recv_msg(client)
        trn_id += 1

if __name__ == '__main__':
    sys.exit(main())

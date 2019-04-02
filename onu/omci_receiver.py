import thread
import time
import Queue
from proto.dolt_pb2 import OmciMsg,Empty
from frame.omci_frame import OmciFrame
from common import hexify

class OmciReceiver(object):
    def __init__(self,con,**kwargs):
        self.__con = con
        self.__kwargs = kwargs
        self.__omci_cache = Queue.Queue()



    def start(self):
        thread.start_new_thread(self.__recv_msg,())

    def __recv_msg(self):
        while True:
            response = self.__con.ReceiveOmci(Empty())

            for r in response:
                try:
                    #print hexify(r.pkt)
                    #print OmciFrame(r.pkt).show()
                    self.__omci_cache.put(OmciFrame(r.pkt))
                except Exception, e:
                    print "To OmciFrame Failed"


    def get_msg(self,block=True,timeout=None):
        try:
            res = self.__omci_cache.get(block,timeout)
            return res
        except Queue.Empty:
            return None

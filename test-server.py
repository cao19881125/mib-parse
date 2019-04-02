import grpc
import time
from concurrent import futures
from proto.dolt_pb2_grpc import dOLTServicer,add_dOLTServicer_to_server
from proto.dolt_pb2 import OmciMsg,Empty

class MsgServer(dOLTServicer):
    def SendOmci(self,request_iterator, context):
        for msg in request_iterator:
            print msg


        return Empty()


if __name__=='__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_dOLTServicer_to_server(MsgServer(),server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)  # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)


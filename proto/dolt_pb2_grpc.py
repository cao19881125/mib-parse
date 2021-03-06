# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import dolt_pb2 as dolt__pb2


class dOLTStub(object):
  """dOLT service
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SendOmci = channel.stream_unary(
        '/dOLT.dOLT/SendOmci',
        request_serializer=dolt__pb2.OmciMsg.SerializeToString,
        response_deserializer=dolt__pb2.Empty.FromString,
        )
    self.ReceiveOmci = channel.unary_stream(
        '/dOLT.dOLT/ReceiveOmci',
        request_serializer=dolt__pb2.Empty.SerializeToString,
        response_deserializer=dolt__pb2.OmciMsg.FromString,
        )


class dOLTServicer(object):
  """dOLT service
  """

  def SendOmci(self, request_iterator, context):
    """Send omci message from vOMCI to dOLT
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReceiveOmci(self, request, context):
    """Recv omci message from dOLT to vOMCI
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_dOLTServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SendOmci': grpc.stream_unary_rpc_method_handler(
          servicer.SendOmci,
          request_deserializer=dolt__pb2.OmciMsg.FromString,
          response_serializer=dolt__pb2.Empty.SerializeToString,
      ),
      'ReceiveOmci': grpc.unary_stream_rpc_method_handler(
          servicer.ReceiveOmci,
          request_deserializer=dolt__pb2.Empty.FromString,
          response_serializer=dolt__pb2.OmciMsg.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'dOLT.dOLT', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

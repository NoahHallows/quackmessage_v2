# Main file for quackmessage, run this to start server


import grpc
from concurrent import futures
import quackmessage_pb2_grpc
from auth import AuthServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    quackmessage_pb2_grpc.add_QuackMessageAuthServicer_to_server(AuthServicer(), server)

    server.add_insecure_port("[::]:5555")
    print("Server started")
    server.start()
    server.wait_for_termination()

serve()

# Main file for quackmessage, run this to start server


import grpc
from concurrent import futures
import auth_pb2_grpc
from auth import AuthService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    auth_pb2_grpc.add_QuackMessageAuthServicer_to_server(AuthService.AuthServicer(), server)

    server.add_insecure_port("[::]:5555")
    print("Server started")
    server.start()
    server.wait_for_termination()

serve()

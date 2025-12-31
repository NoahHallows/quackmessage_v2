# Main file for quackmessage, run this to start server


import grpc
from concurrent import futures
import auth_pb2_grpc
import message_pb2_grpc
from auth import AuthService
from message import MessageService
import _credentials
import logging
from sys import stdout

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stdout)
    ]
)

_LISTEN_ADDRESS_TEMPLATE = "0.0.0.0:%d"

def serve():
    port = 5555
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=25))

    auth_pb2_grpc.add_QuackMessageAuthServicer_to_server(AuthService.AuthServicer(), server)
    message_pb2_grpc.add_MessagerServicer_to_server(MessageService.MessageServicer(), server)

    server_credentials = grpc.ssl_server_credentials(
       (
        (
            _credentials.SERVER_CERTIFICATE_KEY,
            _credentials.SERVER_CERTIFICATE,
        ),
    )
    )

    # Pass down credentials
    port = server.add_secure_port(
        _LISTEN_ADDRESS_TEMPLATE % port, server_credentials
    )


    logging.info("Server started")
    server.start()
    server.wait_for_termination()

serve()

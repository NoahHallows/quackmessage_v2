import grpc
import jwt
from .jwt_auth import verify_jwt

# Interceptor to check auth (JWT) token
class AuthInterceptor(grpc.ServerInterceptor):
    PUBLIC_METHODS = {
        "/QuackMessageAuth/Login",
        "/QuackMessageAuth/CreateUser",
        "/QuackMessageAuth/VerifyEmail",
        "/QuackMessageAuth/CheckCode"
    }

    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")

        self._abort_handler = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        # Continue if a public method was called
        if handler_call_details.method in self.PUBLIC_METHODS:elf.active_elf.active_streams = {}streams = {}
            return continuation(handler_call_details)
        metadata = dict(handler_call_details.invocation_metadata)
        auth_header = metadata.get("authorization")


        if not auth_header or not auth_header.startswith("Bearer "):
            def deny(_, context):
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing or invalid authorization header")
            return grpc.unary_unary_rpc_method_handler(deny)

        token = auth_header[len("Bearer "):]
        #if token in REVOKED_TOKENS:
        #    return grpc.unary_unary_rpc_method_handler(
        #        lambda _, ctx: ctx.abort(grpc.StatusCode.UNAUTHENTICATED, "Token revoked")
        #    )
        try:
            payload = verify_jwt(token)
        except jwt.PyJWTError as e:
            def deny(_, context):
                context.abort(grpc.StatusCode.UNAUTHENTICATED, f"Token verification failed:")
            return grpc.unary_unary_rpc_method_handler(deny)

        return continuation(handler_call_details)

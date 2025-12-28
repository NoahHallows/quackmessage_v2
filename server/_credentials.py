import os


def _load_credential_from_file(filepath):
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()

# Load from docker secret
SERVER_CERTIFICATE = _load_credential_from_file("/run/secrets/cert")
SERVER_CERTIFICATE_KEY = _load_credential_from_file("/run/secrets/privkey")

# Authentication service

# Login: main function calls function here to hash password and then compare with db, returns true/false
# and generates jwt
# Signup: main function calls function here to hash password and store password, username ect in
# db. Returns true/false on user account creation success and returns jwt

from argon2 import PasswordHasher
import psycopg2
import jwt


# Convert the list of bytes to a single variable
def db_binary_to_binary(db_binary):
    binary = b''
    for collumn in db_binary:
        for byte in collumn:
            binary = binary + byte
    return binary

# Create token for auth
def create_jwt(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iss": AuthServerName,
        "aud": AudienceName,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

# Verify token for auth
def verify_jwt(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AudienceName, issuer=AuthServerName)

# Login function
def loginHelper(username: str, password: str, cursor: psycopg2.extensions.cursor) -> tuple[bool, str]:
    print("Login helper")
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        password_hash = db_binary_to_binary(cursor.fetchall())

    except:
        print("Password not found", file=stderr)

    try:
        ph = PasswordHasher()
        ph.verify(password, password_hash)
        print("Passwords match")
        token = generate_jwt(username)
        return (True, token)

    except Exception:
        print("Passwords do not match")
        return (False, "")

def createAccountHelper(username: str, password: str, email: str, cursor: cursor: psycopg2.extensions.cursor) -> tuple[bool, str]:
    cur.execute("SELECT 1 FROM users WHERE username = %s;", (request.username,))
    if cur.fetchone() is None:
        ph = PasswordHasher()
        password_hash = ph.hash(password)
        try:
            cur.execute("INSERT INTO users (email, username, password_hash, account_creation_date,
                    messages_sent, messages_received) VALUES (%s, %s, %s, NOW()), %s,
                    %s)", (email, username, password_hash, 0, 0))
            print("Done")
            token = generate_jwt(username)
            return (True, token)
        except:
            print("Error inserting user into database", file=stderr)
    else:
        print("User exists", file=stderr)

    return (False, "")




# Authentication service

# Login: main function calls function here to hash password and then compare with db, returns true/false
# and generates jwt
# Signup: main function calls function here to hash password and store password, username ect in
# db. Returns true/false on user account creation success and returns jwt

import argon2
import psycopg2


def login(username: str, password: str, cursor: ):
    if type(username) !=
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username))


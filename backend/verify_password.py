import hashlib
import secrets

def verify_password():
    # Password to test
    password_to_test = "1111"

    # Stored hash and salt for fati.salman31@gmail.com (from the output above)
    stored_hash = "0a2a718e24d707d9eb405766a263a826da5813dce000a7880dd00020e8ff5d30"
    salt = "0fb97035a4e600c8282b00dd216bff7a"

    # Recompute the hash using the same method as in auth.py
    computed_hash = hashlib.pbkdf2_hmac('sha256', password_to_test.encode('utf-8'), bytes.fromhex(salt), 100000).hex()

    print(f"Stored hash: {stored_hash}")
    print(f"Computed hash: {computed_hash}")
    print(f"Passwords match: {stored_hash == computed_hash}")

if __name__ == "__main__":
    verify_password()
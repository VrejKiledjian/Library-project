from hashlib import sha256
from config import AppConfig



full_name = input("full n=name:")
password = input("password")

salt = AppConfig.SALT_KEY
salted_password = f"{salt}.{full_name}:{password}.{salt}"
hashed_password = sha256(salted_password.encode())
print(hashed_password.hexdigest())


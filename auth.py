import jwt
from dotenv import load_dotenv
import os
# import pandas as pd
# from cryptography.fernet import Fernet
# import bcrypt
# import base64
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


load_dotenv()


def jwt_verify(auth_header):
    jwt_token = auth_header.split(' ')[1]
    secret_key = os.getenv("SECRET")
    try:
        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'invalid'
    user = decoded_jwt.get('name')
    role = decoded_jwt.get('role')
    if user is None:
        return 'invalid'
    else:
        return user, role

# when we implement encryption

# password = b'password'
# salt = os.urandom(16)
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
# )
# key = kdf.derive(password)
# bskey = base64.urlsafe_b64encode(key)
# # hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
# # key = base64.urlsafe_b64encode()
# f = Fernet(bskey)

# # kdf = PBKDF2HMAC(
# #     algorithm=hashes.SHA256(),
# #     length=32,
# #     salt=salt,
# #     iterations=100000,
# # )
# # print(f.decrypt(token))
# # print(kdf.verify(password, key))

# print(bskey)
# # ecrypt the csv
# df = pd.read_csv('./uploads/mpesa_marto.csv')
# df_e = df.apply(lambda x: x.astype(str))
# token = df_e.applymap(lambda x: f.encrypt(x.encode('utf-8')))
# token.to_csv('./uploads/mpesa_marto_encrypted.csv', index=False)

# # decrypt the csv
# df = pd.read_csv('./uploads/mpesa_marto_encrypted.csv')
# df_e = df.applymap(lambda x: bytes(x[2:-1], 'utf-8'))
# token = df_e.applymap(lambda x: f.decrypt(x))
# final = token.applymap(lambda x: x.decode('utf-8'))
# print(final.head())
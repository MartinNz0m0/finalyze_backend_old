import jwt


def jwt_verify(auth_header):
    jwt_token = auth_header.split(' ')[1]
    secret_key = 'your_jwt_secret'
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

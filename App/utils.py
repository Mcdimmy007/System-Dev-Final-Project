import hashlib

def hash_password(password):
    salt = 'somesaltvalue'
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed_password

def verify_password(password, hashed_password):
    return hashed_password == hash_password(password)

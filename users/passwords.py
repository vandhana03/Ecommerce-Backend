import bcrypt

def hash_password(raw_password:str)->str:
    salt=bcrypt.gensalt()
    hashed_password= bcrypt.hashpw(
        raw_password.encode('utf-8'),
        salt
    )
    return hashed_password.decode('utf-8')

def check_password(raw_password,hashed_password):
    print(hashed_password)
    return bcrypt.checkpw(
        raw_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

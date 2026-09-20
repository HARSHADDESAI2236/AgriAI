from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_pwd(password: str):
    return password_hash.hash(password)


def verify_pwd(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

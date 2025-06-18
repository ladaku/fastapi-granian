import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)

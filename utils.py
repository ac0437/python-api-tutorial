from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def find_index(posts, id):
    for post in posts:
        if post['id'] == id:
            return post['id'] - 1


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

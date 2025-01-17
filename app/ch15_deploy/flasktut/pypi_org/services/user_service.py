from typing import Optional

import flask
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from pypi_org.data import db_session
from pypi_org.data.users import User


def get_user_count() -> int:
    session = db_session.create_session()
    return session.query(User).count()


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.email == email).first()


def find_user_by_id(user_id: int) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.id == user_id).first()


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        return None

    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_text(password)

    session = db_session.create_session()
    session.add(user)
    session.commit()

    return user


def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def login_user(email: str, password: str) -> Optional[User]:
    user = find_user_by_email(email)
    if not user:
        return None

    if not verify_hash(user.hashed_password, password):
        return None

    return user

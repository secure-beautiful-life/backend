from os import getenv
from urllib.parse import quote

import bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.auth.model import AuthRole, AuthRoleHierarchy
from app.user.model import User, UserInfo
from core.config import config
from core.db.session import Base


def init_db() -> None:
    db_url = f"mysql+pymysql://{quote(getenv('DB_USERNAME'))}:{quote(getenv('DB_PASSWORD'))}@" \
             f"{quote(getenv('DB_HOST'))}:{getenv('DB_PORT')}/{quote(getenv('DB_NAME'))}"
    engine = create_engine(url=db_url, pool_recycle=3600)
    Base.metadata.create_all(engine)
    create_superuser(engine)
    engine.dispose()


def safe_commit(session, model) -> None:
    try:
        session.add(model)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def create_superuser(engine) -> None:
    username = config.ADMIN_USERNAME
    password = config.ADMIN_PASSWORD

    session = sessionmaker(bind=engine)()
    query = select(User).where(User.username == username)
    if session.execute(query).scalar():
        return

    query = select(AuthRole).where(AuthRole.id == 1)
    if session.execute(query).scalar():
        return

    safe_commit(session=session, model=AuthRole(name="admin", description="최고관리자"))

    query = select(AuthRoleHierarchy).where(AuthRoleHierarchy.id == 1)
    if session.execute(query).scalar():
        return

    safe_commit(session=session, model=AuthRoleHierarchy(parent_role_id=1))
    safe_commit(session=session, model=User(
        username=username,
        password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        role_id=1
    ))
    safe_commit(session=session, model=UserInfo(
        user_id=1,
        name="관리자",
        type="admin",
        gender="남성",
        email="admin@example.com",
        phone="01012345678",
        address="admin address"
    ))
    session.close()


if __name__ == "__main__":
    init_db()

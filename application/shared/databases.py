from sqlalchemy.ext.declarative import declared_attr, declarative_base
from typing import ClassVar
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databases import Database

from ..config import get_config


class Base:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class DatabaseConnectionLayer:
    Base: ClassVar = declarative_base(
        cls=Base,
        metadata=MetaData(
            naming_convention={
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s",
            }
        ),
    )
    engine: ClassVar = create_engine(get_config().database_uri)
    Session: ClassVar = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    async_db: ClassVar[Database] = Database(get_config().database_uri)

    def __setattr__(self, *args):
        raise TypeError("Values are immutable!")

    def __delattr__(self, *args):
        raise TypeError("Values cannot be deleted!")


Base = DatabaseConnectionLayer.Base  # noqa F811


def init_db():
    print(f"Building on Database: {get_config().database_uri}")
    print("Creating the following tables:")
    for i in Base.metadata.sorted_tables:
        print(i.name)
    Base.metadata.create_all(bind=DatabaseConnectionLayer.engine)


def close_db():
    Base.metadata.drop_all(bind=DatabaseConnectionLayer.engine)


def orm_session():
    db = DatabaseConnectionLayer.Session()
    try:
        yield db
    finally:
        db.close()


def core_connection():
    conn = DatabaseConnectionLayer.engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def async_db():
    return DatabaseConnectionLayer.async_db

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///mybase2.db')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Branches(Base):
    __tablename__='Branches'
    id = Column(Integer, primary_key=True)
    Type = Column(String)
    address = Column(String)
    lon = Column(String)
    lat = Column(String)
    Type2 = Column(String)
    def __repr__(self):
        return '<Mac {}; {}; {}>'.format(address, lon, lat)

class Users(Base):
    __tablename__='Users'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer)
    chosen = Column(String)
    def __repr__(self):
        return '<users {}; {}; {}>'.format(address, lon, lat)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
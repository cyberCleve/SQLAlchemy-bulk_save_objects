#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import time


Base = declarative_base()
class Test(Base):
    __tablename__ = "test"
    col_1 = Column(Integer, primary_key=True)
    col_2 = Column(String(256))

def build_db(x):
    engine = create_engine("mysql+pymysql://root:password@localhost:3307/test", echo=True)
    session = scoped_session(sessionmaker(bind=engine))
    meta = MetaData()
    meta.drop_all(engine, Base.metadata.tables.values())
    meta.create_all(engine, Base.metadata.tables.values())

    # insert records
    start = time.time()
    for x in range(x):
        session.add(Test(col_2="test_string"))
    session.commit()
    print(time.time() - start)

    # insert records with bulk_save_objects
    start = time.time()
    buffer = []
    for x in range(x):
        buffer.append(Test(col_2="test_string"))

    session.bulk_save_objects(buffer)
    session.commit()
    print(time.time() - start)

build_db(100000)

# 29.079105615615845
# 2.41864013671875

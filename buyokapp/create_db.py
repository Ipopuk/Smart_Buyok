from model import Base
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
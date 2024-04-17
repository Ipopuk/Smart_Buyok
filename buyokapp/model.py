from sqlalchemy import Column, Integer, String, Time, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import buyokapp.config as config

Base = declarative_base()


class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    time = Column(Time, nullable=False)
    ll = Column(String, nullable=False)
    depth = Column(Float, nullable=False)


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# @app.before_first_request
# def create_tables():
#     db.create_all()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class ServerConfig(Base):
    __tablename__ = "server_configs"
    id = Column(Integer, primary_key=True)
    server_id = Column(String, unique=True)
    prefix = Column(String, default="!")

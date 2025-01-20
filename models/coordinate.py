# models/coordinate.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

Base = declarative_base()


class Coordinate(Base):
    __tablename__ = "coordinates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    waypoints = relationship("Waypoint", back_populates="coordinate")

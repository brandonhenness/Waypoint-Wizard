# models/waypoint.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.coordinate import Coordinate

Base = declarative_base()


class Waypoint(Base):
    __tablename__ = "waypoints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    color = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)
    dimension = Column(String, nullable=False)
    file = Column(String, nullable=False)
    coordinate_id = Column(Integer, ForeignKey("coordinates.id"), nullable=False)

    coordinate = relationship("Coordinate", back_populates="waypoints")

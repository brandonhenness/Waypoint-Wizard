# database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.coordinate import Base as CoordinateBase
from models.waypoint import Base as WaypointBase

DATABASE_URL = "sqlite:///bot.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Use a session factory instead of a single session instance
def session():
    return Session()


# Create all tables
CoordinateBase.metadata.create_all(bind=engine)
WaypointBase.metadata.create_all(bind=engine)

# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StoreStatus(Base):
    __tablename__ = 'store_status'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timestamp_utc = Column(DateTime)
    status = Column(Boolean)

class BusinessHours(Base):
    __tablename__ = 'business_hours'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    day_of_week = Column(Integer)
    start_time_local = Column(DateTime)
    end_time_local = Column(DateTime)

class Timezone(Base):
    __tablename__ = 'timezone'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timezone_str = Column(String)


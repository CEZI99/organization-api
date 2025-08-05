from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

organization_activity = Table(
    'organization_activity', Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Building(BaseModel):
    __tablename__ = 'buildings'
    address = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    organizations = relationship("Organization", back_populates="building")

class Activity(BaseModel):
    __tablename__ = 'activities'
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('activities.id'))
    children = relationship("Activity", back_populates="parent", remote_side="Activity.id")
    parent = relationship("Activity", back_populates="children", remote_side="Activity.id")
    organizations = relationship("Organization", secondary=organization_activity, back_populates="activities")

class Organization(BaseModel):
    __tablename__ = 'organizations'
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", back_populates="organization")
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")

class Phone(BaseModel):
    __tablename__ = 'phones'
    phone = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship("Organization", back_populates="phones")
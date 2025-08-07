from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Ассоциативная таблица для связи Organization-Activity
organization_activity = Table(
    'organization_activity', 
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)

class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    organizations = relationship("Organization", back_populates="building")

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('activities.id'))
    level = Column(Integer, default=1)

    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side=[id]
    )
    children = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))

    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", back_populates="organization")
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations"
    )

class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship("Organization", back_populates="phones")

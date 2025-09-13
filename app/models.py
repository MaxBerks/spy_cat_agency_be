from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class SpyCat(Base):
    __tablename__ = "spy_cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Float, nullable=False)

    missions = relationship("Mission", back_populates="cat", cascade="all, delete-orphan")

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    is_complete = Column(Boolean, default=False)

    cat = relationship("SpyCat", back_populates="missions")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"
    __table_args__ = (UniqueConstraint("mission_id", "name", name="uq_target_per_mission"),)

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(Text, default="")
    is_complete = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")

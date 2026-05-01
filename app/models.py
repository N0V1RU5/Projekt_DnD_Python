from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    encounters = relationship("Encounter", back_populates="owner")

class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="encounters")
    elements = relationship("EncounterElement", back_populates="encounter", cascade="all, delete-orphan")

class EncounterElement(Base):
    __tablename__ = "encounter_elements"

    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    type = Column(String)  # 'monster', 'item', 'spell'
    api_index = Column(String) # The 'index' field from D&D API
    name = Column(String) # Display name

    encounter = relationship("Encounter", back_populates="elements")

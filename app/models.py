from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# tabulka pro uzivatele
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    encounters = relationship("Encounter", back_populates="owner")

# tabulka pro seznamy (encovery)
class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="encounters")
    elements = relationship("EncounterElement", back_populates="encounter", cascade="all, delete-orphan")

# tabulka pro jednotlive polozky v oblibenych
class EncounterElement(Base):
    __tablename__ = "encounter_elements"

    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    type = Column(String) 
    api_index = Column(String) 
    name = Column(String) 

    encounter = relationship("Encounter", back_populates="elements")

#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
import models
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")

    if os.getenv('HBNB_TYPE_STORAGE') == 'fs':
        @property
        def cities(self):
            """getter attribute returns list of City instances w/ state_id
            equal to the current State.id -> it will be the FileStorage
            relationship between State and City"""
            instanceslist = []
            allcitiesdict = models.storage.all(City)
            for cty in allcitiesdict.values():
                if cty.state_id == self.id:
                    instanceslist.append(cty)
            return instanceslist

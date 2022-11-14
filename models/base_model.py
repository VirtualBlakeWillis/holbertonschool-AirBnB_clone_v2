#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """A base class for all hbnb models"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime(), nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime(), nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if 'updated_at' in kwargs.items():
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         '%Y-%m-%d\
                                                         T%H:%M:%S.%f')
            if 'created_at' in kwargs.items():
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%d\
                                                         T%H:%M:%S.%f')
            if '__class__' in kwargs.items():
                del kwargs['__class__']
            self.__dict__.update(kwargs)
            if 'created_at' not in kwargs.keys():
                self.created_at = datetime.now()
                self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            dictionary.pop('_sa_instance_state', 0)
        return dictionary

    def delete(self):
        """ Deletes current instance from storage """
        from models import storage
        storage.delete(self)

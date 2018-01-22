import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Transcription(Base):
    __tablename__ =  'transcriptions'
    id = Column(Integer, primary_key = True)
    filename = Column(String(80))
    filepath = Column(String(255))
    text = Column(String(80))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'filename' : self.filename,
            'filepath' : self.filepath,
            'text' : self.text,
        }

engine = create_engine('sqlite:///transcription.db')
Base.metadata.create_all(engine)

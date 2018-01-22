import IPython
import pathlib
import io
import glob

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Transcription, Base

from google.cloud import vision
from google.cloud.vision import types

engine = create_engine('sqlite:///transcription.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

client = vision.ImageAnnotatorClient()

paths = glob.glob("/Users/jforce/Pictures/ocr_testing/*")
files = []

for path in paths:
    files.append( { 'filename': pathlib.PurePosixPath(path).name, 'filepath': str(path) } )


for dict in files:
    with io.open(dict['filepath'], 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content = content)

    response = client.document_text_detection(image = image)
    transcribed_text = response.text_annotations[0].description
    transcription = Transcription(filepath = dict['filepath'],
                                 filename = dict['filename'],
                                 text = transcribed_text)
    session.add(transcription)
    session.commit()


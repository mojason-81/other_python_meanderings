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

for path in paths:
    dict = { 'filename': pathlib.PurePosixPath(path).name, 'filepath': str(path) }

    with io.open(dict['filepath'], 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content = content)

    req = {
        'image': image,
        'features': [
            {
                'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION
            },{
                'type': vision.enums.Feature.Type.LABEL_DETECTION
            },{
                'type': vision.enums.Feature.Type.WEB_DETECTION
            }
        ]
    }

    response = client.annotate_image(req)
    transcribed_text = response.text_annotations[0].description

    label_list = list(
        map((lambda lst: lst.description), response.label_annotations)
    )
    labels = ','.join(label_list)

    web_entitiy_descriptions = list(
        map((lambda lst: lst.description), response.web_detection.web_entities)
    )
    entities = ','.join(web_entitiy_descriptions)

    pages_with_matching_images = list(
        map(
            (lambda wpObj: wpObj.url),
            response.web_detection.pages_with_matching_images
        )
    )

    full_matching_images = list(
        map(
            (lambda wpObj: wpObj.url),
            response.web_detection.full_matching_images
        )
    )

    partial_matching_images = list(
        map(
            (lambda wpObj: wpObj.url),
            response.web_detection.partial_matching_images
        )
    )

    matching_images_aggregate = pages_with_matching_images + full_matching_images + partial_matching_images

    urls = ','.join(matching_images_aggregate)

    transcription = Transcription(filepath = dict['filepath'],
                                 filename = dict['filename'],
                                 labels = labels,
                                 entities = entities,
                                 urls = urls,
                                 text = transcribed_text)
    session.add(transcription)
    session.commit()


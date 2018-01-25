import io
import glob

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Transcription
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from google.cloud import vision
from google.cloud.vision import types
from database_setup import Transcription

app = Flask(__name__)
engine = create_engine('sqlite:///transcription.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/transcriptions')
def transcriptionsIndex():
    transcriptions = session.query(Transcription).all()
    return render_template('transcriptions/index.html', transcriptions = transcriptions)

@app.route('/transcriptions/json')
def transcriptionsIndexJSON():
    transcriptions = session.query(Transcription).all()
    return jsonify(Transcriptions=[t.serialize for t in transcriptions])

@app.route('/transcriptions/new', methods = ['GET', 'POST'])
def transcriptionsNew():
    if request.method == 'POST':
        pass
    else:
        return render_template('transcriptions/new.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

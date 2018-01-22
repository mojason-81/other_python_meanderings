# google-vision-test-flask

Testing out usage of the google-vision API in Python / Flask

### NOTE:

You WILL have to have an env var exported for your credentials to connect to the service.

i.e. `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/cred_file.json`

Also, in `seed.py`, the program is looking for a specific path for the pictures.  You'll have to change this to wherever you store your pics.

After installing requirements (`pip install -r requirements.txt`), you should be able to `flask run` and have things up and running.  There's only a `GET` route, so you'll probably want to `python seed.py` before you run the application though.

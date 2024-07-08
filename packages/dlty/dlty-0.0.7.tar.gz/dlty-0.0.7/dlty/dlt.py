import os
from datetime import datetime

from google.cloud import storage


class DataLeakTest:
    run = os.getenv('RUN')
    pipeline = os.getenv('PIPELINE')
    step =  os.getenv('STEP')
    date = str(datetime.datetime.today())
    client = storage.Client()
    bucket = client.get_bucket('data-leak-test')
    blob = bucket.blob(run)
    blob.upload_from_string(f'LeakTest was able to sneak out some data (this text) into the public world:\nDate: {date}\nPipeline: {pipeline}\nRun: {run}\nStep: {step}')
    print("!")

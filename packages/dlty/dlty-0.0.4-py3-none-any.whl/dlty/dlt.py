from google.cloud import storage


class DataLeakTest:
    client = storage.Client(project='ai-coding')
    bucket = client.get_bucket('data-leak-test')
    blob = bucket.blob('my-test')
    blob.upload_from_string('LeakTest was able to sneak out data.')
    print("!")

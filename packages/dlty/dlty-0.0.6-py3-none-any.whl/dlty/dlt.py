from google.cloud import storage


class DataLeakTest:
    client = storage.Client()
    bucket = client.get_bucket('data-leak-test')
    blob = bucket.blob('my-test-2')
    blob.upload_from_string('LeakTest was FINALLY able to sneak out data.')
    print("!")

from google.cloud import storage


def create_bucket(bucket_name):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="us-central1")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )


def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print("Bucket {} deleted".format(bucket.name))


def return_bucket_object(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket


if __name__ == "__main__":
    bucket_name = "prueba-vision-response"
    create_bucket_class_location(bucket_name)

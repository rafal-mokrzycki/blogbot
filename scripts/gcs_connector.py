"""
Functions to access GCP Storage.
"""

from datetime import datetime

import numpy as np
from google.cloud import storage
from validators import is_valid_bucket_bucket_name


class GSC_Connector:
    def __init__(self) -> None:
        pass

    def get_project_id(self) -> str:
        """Return project name from client
        google.storage.client object."""
        pass

    def write_file_to_bucket(self, bucket: str, text: str) -> None:
        pass

    def create_unique_bucket_name(client: storage.Client) -> str:
        """Creates an unique bucket name
        based on the client account email.

        Args:
            client (storage.Client): _description_

        Raises:
            NameError: if bucket name does not follow Google requirements

        Returns:
            str: unique bucket name
        """
        service_account = (
            client.get_service_account_email()
            .replace("@", "-")
            .replace(".", "-")
        )
        name = (
            service_account + "-" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        )

        if is_valid_bucket_bucket_name(name):
            return name
        else:
            raise NameError(
                "Bucket name does not follow Google requirements \
                    (see: https://cloud.google.com/storage/docs/buckets#naming"
            )

    def create_unique_blob_name() -> str:
        """Creates an unique blob name
        based on the timestamp.

        Returns:
            str: blob name in format '20230311124542597264.txt'
        """
        return datetime.now().strftime("%Y%m%d%H%M%S%f") + ".txt"

    def create_bucket_class_location(bucket_name):
        """
        Create a new bucket in the US region with the coldline storage
        class
        """
        # bucket_name = "your-new-bucket-name"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "COLDLINE"
        new_bucket = storage_client.create_bucket(bucket, location="us")

        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket

    def delete_blob(bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        generation_match_precondition = None

        # Optional: set a generation-match precondition to avoid
        # potential race conditions and data corruptions. The request
        # to delete is aborted if the object's generation number
        # does not match your precondition.
        blob.reload()
        # Fetch blob metadata to use in generation_match_precondition.
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)

        print(f"Blob {blob_name} deleted.")

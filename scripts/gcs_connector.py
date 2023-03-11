"""
Functions to access GCP Storage.
"""

import time
from datetime import datetime

from google.cloud import storage

from scripts.validators import is_valid_bucket_name


class GCS_Connector:
    def __init__(self) -> None:
        # TODO: adjust to project needs.
        pass

    def get_project_id(self) -> str:
        """Return project name from client
        google.storage.client object"""
        pass

    def write_file_to_bucket(
        self, input_text: str, bucket_name: str = None, file_name: str = None
    ) -> None:
        """Writes a string into a .txt file in a given bucket.

        Args:
            input_text (str): a blog post (output of
            Transformer.transform method)
            bucket_name (str, optional): user's bucket name.
            Defaults to None.
            file_name (str, optional): .txt file name. Defaults to None.
        """
        if bucket_name is None:
            bucket_name = self.create_unique_bucket_name()
            # TODO: check if a bucket for that client exists,
            # if not, create it
        if file_name is None:
            file_name = self.create_unique_blob_name()
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(input_text)

    def create_unique_bucket_name(self, client: storage.Client) -> str:
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

        if is_valid_bucket_name(name):
            return name
        else:
            raise NameError(
                "Bucket name does not follow Google requirements \
                    (see: https://cloud.google.com/storage/docs/buckets#naming"
            )

    def create_unique_blob_name(self) -> str:
        """Creates an unique blob name
        based on the timestamp.

        Returns:
            str: blob name in format '20230311124542597264.txt'
        """
        time.sleep(0.1)
        return datetime.now().strftime("%Y%m%d%H%M%S%f") + ".txt"

    def create_bucket_class_location(self, bucket_name):
        """
        Create a new bucket in the US region with the coldline storage
        class
        """
        # TODO: adjust to project needs.
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

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket"""
        # TODO: adjust to project needs.
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

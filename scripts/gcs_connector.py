"""
Functions to access GCP Storage.
"""

import logging
import time
from datetime import datetime

from google.cloud import storage
from google.oauth2 import service_account

from scripts.validators import is_valid_bucket_name


class GCS_Connector:
    def __init__(
        self,
        project_id: None | str = None,
        key_path: None | str = None,
    ) -> None:
        if project_id is None and key_path is None:
            self.client = storage.Client()
            self.project_id = self.get_project_id()
        else:
            try:
                self.credentials = (
                    service_account.Credentials.from_service_account_file(
                        key_path
                    )
                )
                self.client = storage.Client(
                    project_id, credentials=self.credentials
                )
            except FileNotFoundError:
                self.log = logging.getLogger("GCS_Connector")  # Generic log
                self.log.error("Keyfile not found.")
                self.project_id = None
                return
            else:
                self.project_id = self.get_project_id()
        self.log = logging.getLogger(f"GCS_Connector {self.project_id}")

    def get_project_id(self) -> str:
        """Return project name from client google.storage.client object."""
        return self.client.project

    def create_unique_bucket_name(self) -> str:
        """Creates an unique bucket name
        based on the client account email.

        Raises:
            NameError: if bucket name does not follow Google requirements

        Returns:
            str: unique bucket name
        """
        time.sleep(0.1)
        service_account = (
            self.client.get_service_account_email()
            .replace(".", "-")
            .split("@")[0]
        )
        name = (
            service_account + "-" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        )

        if is_valid_bucket_name(name):
            return name
        else:
            raise NameError(
                f"Bucket name '{name}' does not follow Google requirements \
                    (see: https://cloud.google.com/storage/docs/buckets#naming"
            )

    def create_new_bucket(
        self,
        bucket_name: str,
        storage_class: str = "STANDARD",
        location: str = "us",
    ):
        """Creates a new bucket.
        Used when a new client registers to the app.

        Args:
            bucket_name (str): new bucket name
            storage_class (str, optional): storage class.
            Defaults to "STANDARD".
            location (str, optional): bucket location. Defaults to "us".

        Returns:
            _type_: new bucket
        """
        bucket = self.client.bucket(bucket_name)
        bucket.storage_class = storage_class
        new_bucket = self.client.create_bucket(bucket, location=location)
        return new_bucket

    def list_buckets(self):
        """Lists all buckets."""
        buckets = self.client.list_buckets()
        return [bucket.name for bucket in buckets]

    def delete_bucket(self, bucket_name: str) -> None:
        """Deletes a bucket.
        Used when a client closes their account.

        Args:
            bucket_name (str): bucket to be deleted.
        """
        bucket = self.client.get_bucket(bucket_name)
        bucket.delete()

    def create_unique_blob_name(self) -> str:
        """Creates an unique blob name
        based on the timestamp.

        Returns:
            str: blob name in format 'YYYYMMDDhhmmssffffff.txt'
        """
        time.sleep(0.1)
        return datetime.now().strftime("%Y%m%d%H%M%S%f") + ".txt"

    def write_blob_to_bucket(
        self, input_text: str, bucket_name: str = None, blob_name: str = None
    ) -> None:
        """Writes a string into a .txt file in a given bucket.

        Args:
            input_text (str): a blog post (output of
            Transformer.transform method)
            bucket_name (str, optional): user's bucket name.
            Defaults to None.
            blob_name (str, optional): .txt file name. Defaults to None.
        """
        if bucket_name is None:
            bucket_name = self.create_unique_bucket_name()
            # TODO: check if a bucket for that client exists,
            # if not, create it
        if blob_name is None:
            blob_name = self.create_unique_blob_name()
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(input_text)

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        blobs = self.client.list_blobs(bucket_name)
        return [blob.name for blob in blobs]

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        self.log.warning(
            f"Object {blob_name} deleted in bucket: {bucket_name}"
        )
        blob.delete()

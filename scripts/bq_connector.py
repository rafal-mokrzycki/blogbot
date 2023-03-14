#!/usr/bin/env python
"""
Functions to access GCP BigQuery.
"""

import logging
import pathlib
import time
from datetime import datetime
from time import sleep

import pandas
from google.cloud import bigquery, exceptions, storage
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from pandas_gbq import gbq

from scripts.validators import is_valid_bucket_name

log = logging.getLogger(__name__)

PROJECT_ID = "thinking-glass-380312"


class ConnectBigQuery:
    def __init__(self, project_id=None, key_file=""):

        self.credentials = (
            service_account.Credentials.from_service_account_file(key_file)
        )
        self.client = bigquery.Client(project_id, credentials=self.credentials)
        self.project_id = PROJECT_ID  # self.get_project_id()

    def if_tbl_exists(self, dataset_id="blogbot", table_id="users"):
        """Return true if table with this name exists."""
        try:
            table_ref = f"{self.project_id}.{dataset_id}.{table_id}"
            self.client.get_table(table_ref)
            # print('table found', table_id)
            return True
        except NotFound:
            return False

    def create_table_if_not_exists(
        self, dataset_id="blogbot", table_id="users"
    ):
        if self.if_tbl_exists(dataset_id=dataset_id, table_id=table_id):
            schema = [
                bigquery.SchemaField("username", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("password", "STRING", mode="REQUIRED"),
            ]

            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)  # Make an API request.
            log.info(
                "Created table {}.{}.{}".format(
                    table.project, table.dataset_id, table.table_id
                )
            )

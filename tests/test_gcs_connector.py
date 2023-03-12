"""
to run: python -m pytest -vv tests\test_gcs_connector.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker)
to debug VScode: pytest --collect-only
"""
import pytest

from scripts.gcs_connector import GCS_Connector

TEST_BUCKET_NAME = "this_is_a_bucket"
TEST_BLOB_NAME = "this_is_a_file.txt"


@pytest.fixture(scope="module")
def gcs():
    """Creates and returns a Google Cloud Storage connection"""
    return GCS_Connector()


def test_create_unique_bucket_name(gcs):
    unique_names = []
    for _ in range(3):
        unique_names.append(gcs.create_unique_bucket_name())
    assert len(unique_names) == len(set(unique_names))


def test_create_unique_test_blob_name(gcs):
    unique_names = []
    for _ in range(3):
        unique_names.append(gcs.create_unique_blob_name())
    assert len(unique_names) == len(set(unique_names))


def test_get_project_id(gcs):
    assert gcs.get_project_id() == "thinking-glass-380312"


def test_write_blob_to_bucket(gcs):
    gcs.create_new_bucket(TEST_BUCKET_NAME)
    gcs.write_blob_to_bucket("input text", TEST_BUCKET_NAME, TEST_BLOB_NAME)
    assert TEST_BLOB_NAME in gcs.list_blobs(TEST_BUCKET_NAME)
    gcs.delete_blob(TEST_BUCKET_NAME, TEST_BLOB_NAME)


def test_list_blobs(gcs):
    gcs.write_blob_to_bucket("input text", TEST_BUCKET_NAME, TEST_BLOB_NAME)
    assert len(gcs.list_blobs(TEST_BUCKET_NAME)) == 1
    gcs.delete_blob(TEST_BUCKET_NAME, TEST_BLOB_NAME)


def test_delete_blob(gcs):
    gcs.write_blob_to_bucket("input text", TEST_BUCKET_NAME, TEST_BLOB_NAME)
    gcs.delete_blob(TEST_BUCKET_NAME, TEST_BLOB_NAME)
    assert TEST_BLOB_NAME not in gcs.list_blobs("tmp-bucket")



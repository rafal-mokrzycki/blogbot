"""
to run: python -m pytest -vv tests\test_gcs_connector.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker)
to debug VScode: pytest --collect-only
"""
import pytest

from scripts.gcs_connector import GCS_Connector


@pytest.fixture(scope="module")
def gcs():
    """Creates and returns a Google Cloud Storage connection"""
    return GCS_Connector()


def test_create_unique_bucket_name(gcs):
    pass


def test_create_unique_blob_name(gcs):
    unique_names = []
    for _ in range(3):
        unique_names.append(gcs.create_unique_blob_name())
    assert len(unique_names) == len(set(unique_names))


def test_get_project_id(gcs):
    assert gcs.get_project_id() == "thinking-glass-380312"


def test_write_file_to_bucket(gcs):
    bucket_name = "tmp-bucket"
    file_name = "tmp-file.txt"
    gcs.write_file_to_bucket("input text", bucket_name, file_name)
    assert "tmp-file.txt" in gcs.list_blobs("tmp-bucket")
    gcs.delete_blob(bucket_name, file_name)


def test_list_blobs(gcs):
    bucket_name = "tmp-bucket"
    file_name = "tmp-file.txt"
    gcs.write_file_to_bucket("input text", bucket_name, file_name)
    assert len(gcs.list_blobs("tmp-bucket")) == 1
    gcs.delete_blob(bucket_name, file_name)


def test_delete_blob(gcs):
    pass

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


def test_create_unique_blob_name(gcs):
    unique_names = []
    for _ in range(3):
        unique_names.append(gcs.create_unique_blob_name())
    assert len(unique_names) == len(set(unique_names))


def test_get_project_id(gcs):
    assert gcs.get_project_id() == "thinking-glass-380312"


def test_write_file_to_bucket(gcs):
    gcs.write_file_to_bucket("input text", "tmp-bucket", "tmp-file.txt")
    assert "tmp-file.txt" in gcs.list_blobs("tmp-bucket")

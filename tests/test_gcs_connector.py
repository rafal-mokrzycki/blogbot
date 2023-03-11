"""
to run: python -m pytest -vv tests\test_gcs_connector.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker)
to debug VScode: pytest --collect-only
"""
import pytest

from scripts.gcs_connector import GCS_Connector


@pytest.fixture(scope="module")
def gcs_connection():
    """Creates and returns a Google Cloud Storage connection"""
    return GCS_Connector()


def test_create_unique_blob_name(gcs_connection):
    unique_names = []
    for _ in range(3):
        unique_names.append(gcs_connection.create_unique_blob_name())
    assert len(unique_names) == len(set(unique_names))

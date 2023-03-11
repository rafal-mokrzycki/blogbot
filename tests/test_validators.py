"""
to run: python -m pytest -vv tests\test_validators.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker)
to debug VScode: pytest --collect-only
"""

from scripts.validators import is_valid_bucket_name


def test_is_valid_bucket_name():
    assert is_valid_bucket_name("this-is-a-valid-bucket-name-99") is True


def test_is_valid_bucket_name_false_google0():
    assert (
        is_valid_bucket_name("google-this-is-an-invalid-bucket-name") is False
    )


def test_is_valid_bucket_name_false_google1():
    assert (
        is_valid_bucket_name("gOOgle-this-is-an-invalid-bucket-name") is False
    )


def test_is_valid_bucket_name_false_google2():
    assert (
        is_valid_bucket_name("g00gle-this-is-an-invalid-bucket-name") is False
    )


def test_is_valid_bucket_name_false_google3():
    assert is_valid_bucket_name("goog-this-is-an-invalid-bucket-name") is False


def test_is_valid_bucket_name_false_char0():
    assert is_valid_bucket_name("this-is-an-invalid-bucket.name") is False


def test_is_valid_bucket_name_false_char1():
    assert is_valid_bucket_name("this-is-an-invalid-bucket@name") is False

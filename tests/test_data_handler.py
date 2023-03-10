"""
to run: python -m pytest -vv tests\test_data_handler.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker)
to debug VScode: pytest --collect-only
"""
import datetime
import os
import pathlib
import random
import tempfile
from time import time

import numpy as np
import pandas
import pytest

from scripts.data_handler import Transformer


@pytest.fixture(scope="module")
def input_string():
    yield "Today the weather is beautiful."


def test_transform_correct_start(input_string):
    string = Transformer.transform(input_string, temperature=0.6, max_length=100, n_sentences=1)[0]["generated_text"]
    assert string.startswith(input_string)


def test_transform_correct_length(input_string):
    string = Transformer.transform(input_string, temperature=0.0001, max_length=100, n_sentences=1)[0]["generated_text"]
    assert len(string.split(" ")) == 81


def test_transform_correct_n_sentences(input_string):
    sentences = Transformer.transform(input_string, temperature=0.6, max_length=100, n_sentences=5)
    assert len(sentences) == 5

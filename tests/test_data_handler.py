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


def test_transform():
    string = Transformer.transform("Today the weather is beautiful.")[0]["generated_text"]
    print(string)
    assert string.startswith("Today the weather is beautiful.")


def test_transform_wrong_input():
    pass


def test_transform_wrong_max_length():
    pass


def test_transform_wrong_n_sentences():
    pass

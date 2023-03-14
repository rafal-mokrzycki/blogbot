import re


def is_valid_bucket_name(bucket_name: str) -> bool:
    """
    _summary_

    Args:
        bucket_name (str): _description_

    Returns:
        bool: _description_
    s"""
    MAX_LENGTH = 63
    MIN_LENGTH = 3
    forbidden_pattern = r"^g[oO0]{2}g(le)?[a-z0-9_\-]*[a-z0-9]?$"
    if len(bucket_name) > MAX_LENGTH or len(bucket_name) < MIN_LENGTH:
        return False
    if re.fullmatch(forbidden_pattern, bucket_name):
        return False
    valid_pattern = r"^[a-z0-9][a-z0-9_\-]*[a-z0-9]$"
    return bool(re.fullmatch(valid_pattern, bucket_name))

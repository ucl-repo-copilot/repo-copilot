# utils.py
import re

"""
Contains a utility function validate_email that uses regular expressions to validate email addresses.
"""
def validate_email(email):
    pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.match(pattern, email):
        return True
    return False

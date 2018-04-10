from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

import requests


def validate_url(value):
    url_validator = URLValidator()
    reg_val = value
    if "http" in reg_val:
        new_value = reg_val
    else:
        new_value = "http://" + value
    try:
        url_validator(new_value)
    except:
        raise ValidationError("Invalid URL for this field!")
    try:
        requests.get(new_value)
    except:
        raise ValidationError("This URL does not exist!")
    return new_value

def validate_dot_com(value):
    if not "com" in value:
        raise ValidationError("Not .com in URL")
    return value
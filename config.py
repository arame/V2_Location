import re

class Hyper:
    _date = "_2021_apr_03"
    db = f"../sql/twitter{_date}.db"
    language = "en"

class Constants:
    USER_HANDLES_REGEX = re.compile(r"@\S+")
    NEW_LINE_REGEX = re.compile(r'\s+|\\n')
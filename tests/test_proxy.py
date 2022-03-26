import datetime
import re
import time
import pytest
from re import error as RegexException
from utils import proxy_globals
HOST = proxy_globals.HOST


def get_time_stamp():
    return f"{HOST} - - [{str(datetime.datetime.fromtimestamp(time.time()).strftime('%d/%b/%Y %H:%M:%S'))}]"


class TestHandler:

    # copy of Handler funcion to support "parse_content" method dependency
    def append_TM(self, string: str):
        try:
            reg_ex = re.compile(r"(\b\w{6}\b)", re.IGNORECASE)
            match = reg_ex.match(string) or None
            match_string = match.group() if match is not None else str()
            if match_string.isalpha():
                return reg_ex.sub(f'{match_string}™', string, count=1)
        except RegexException as err:
            print(
                f"{get_time_stamp()} Regex error, invalid regular expression , reason: [{err}]")
        return string

    # test TradeMark append function &#x2122;
    @pytest.mark.parametrize("test_input, expected", [
        ("Search:\n", "Search™:\n"),
        ('Пришел, ', 'Пришел™, '),
    ])
    def test_append_TM(self, handler, test_input, expected):
        assert handler.append_TM(self, test_input) == expected

    @pytest.mark.parametrize("test_input, expected", [
        (
            """
<html lang="en" op="item">
<head>
<meta name="referrer" content="origin">
<title>The Scientific Case for Two Spaces After a Period (2018)</title>
</head>
<body>
<center>
<table class="fatitem" border="0">
<tr class='athing' id='25581282'>
<td class="title">
<a class="titlelink">The Scientific Case for Two Spaces After a Period (2018)</a>
</td>
</tr>
</table>
</center>
</body>
</html>
""",
            b"""
<html lang="en" op="item">
<head>
<meta content="origin" name="referrer"/>
<title>The Scientific Case for Two Spaces\xe2\x84\xa2 After a Period\xe2\x84\xa2 (2018)</title>
</head>
<body>
<center>
<table border="0" class="fatitem">
<tr class="athing" id="25581282">
<td class="title">
<a class="titlelink">The Scientific Case for Two Spaces\xe2\x84\xa2 After a Period\xe2\x84\xa2 (2018)</a>
</td>
</tr>
</table>
</center>
</body>
</html>
"""
        )
    ])
    def test_parse_content(self, handler, test_input, expected):
        assert handler.parse_content(self, test_input) == expected

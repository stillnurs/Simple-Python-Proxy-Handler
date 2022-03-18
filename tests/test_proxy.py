import pytest


class TestHandler:

    # test TradeMark append function &#x2122;
    @pytest.mark.parametrize("test_input, expected", [
        ("Search:\n", "Search&#x2122;:\n"),
        ('Пришел, ', 'Пришел&#x2122;, '),
    ])
    def test_append_TM(self, handler, test_input, expected):
        assert handler.append_TM(self, test_input) == expected

    # Make sure to check TARGET_URL before running this test.
    @pytest.mark.parametrize("test_input, expected", [
        ('href="https://news.ycombinator.com">', 'href="https://127.0.0.1:8080">'),
        ('href="favicon.ico">', 'href="https://news.ycombinator.com/favicon.ico">'),
    ])
    def test_replace_urls(self, handler, test_input, expected):
        assert handler.replace_urls(self, test_input) == expected

    @pytest.mark.parametrize("test_input, expected", [
        (
            '<p>This domain is for use in illustrative examples in documents. You may use this ' +
            'domain in literature without prior coordination or asking for permission.</p>',
            ['', '<p>', 'This', 'domain', 'is', 'for', 'use', 'in',
             'illustrative', 'examples', 'in', 'documents.', 'You', 'may', 'use', 'this', 'domain', 'in', 'literature', 'without', 'prior', 'coordination',
             'or', 'asking', 'for', 'permission.', '</p>', '']
        )
    ])
    def test_split_content(self, handler, test_input, expected):
        assert handler.split_content(self, test_input) == expected

    @pytest.mark.parametrize("test_input, expected", [
        (
            ['', '<p>', 'This', 'domain', 'is', 'for', 'use', 'in',
             'illustrative', 'examples', 'in', 'documents.', 'You', 'may', 'use', 'this', 'domain', 'in', 'literature', 'without', 'prior', 'coordination',
             'or', 'asking', 'for', 'permission.', '</p>', ''],
            b'<p>This domain is for use in illustrative examples in documents. You may use this ' +
            b'domain in literature without prior coordination or asking for permission.</p>'
        )
    ])
    def test_compose_new_content(self, handler, test_input, expected):
        assert handler.compose_new_content(self, test_input) == expected

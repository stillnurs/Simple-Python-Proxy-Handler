import pytest

class TestHandler:

    # test TradeMark append function &#x2122;
    # @pytest.mark.parametrize("test_input, expected", [
    #     ("Search:\n", "Search&#x2122;:\n"),
    #     ('Пришел, ', 'Пришел&#x2122;, '),
    #     ])
    # def test_append_TM(self, handler, test_input, expected):
    #     assert handler.append_TM(self, test_input) == expected

    # @pytest.mark.parametrize("test_input, expected", [
    #     ('href="https://news.ycombinator.com">', 'href="https://127.0.0.1:8080">'),
    #     ('href="favicon.ico">', 'href="https://news.ycombinator.com/favicon.ico">'),
    # ])
    # def test_replace_urls(self, handler, test_input, expected):
    #     assert handler.replace_urls(self, test_input) == expected

    
#     @pytest.mark.parametrize("test_input, expected", [
#     ('<body><div><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents. You may use this '+
# 'domain in literature without prior coordination or asking for permission.</p><p><a href="https://www.iana.org/domains/example">'+
# 'More information...</a></p></div></body>',
# '<body><div><h1>Example Domain&#x2122;</h1><p>This domain&#x2122; is for use in illustrative examples in documents. You may use this '+
# 'domain&#x2122; in literature without prior coordination or asking&#x2122; for permission.</p><p><a href="https://www.iana.org/domains/example">'+
# 'More information...</a></p></div></body>'
#     )])
#     def test_modify_content_list(self, handler, test_input, expected):
#         assert handler.modify_content_list(self, test_input)
#         return expected

    @pytest.mark.parametrize("test_input, expected", [
    (
'<body><div><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents. You may use this '+
'domain in literature without prior coordination or asking for permission.</p><p><a href="https://www.iana.org/domains/example">'+
'More information...</a></p></div></body>',
['<body>\n<div>\n', '', '', '', '<h1>Example', 'Domain</h1>\n', '', '', '', '<p>This', 'domain', 'is', 'for', 'use', 'in', 'illustrative',
 'examples', 'in', 'documents.', 'You', 'may', 'use', 'this\n', '', '', '', 'domain', 'in', 'literature', 'without', 'prior', 'coordination',
 'or', 'asking', 'for', 'permission.</p>\n', '', '', '', '<p><a', 'href="https://www.iana.org/domains/example">More', 'information...</a></p>\n</div>\n</body>']

    )
    ])
    def test_split_content(self, handler, test_input, expected):
        assert handler.split_content(self, test_input) == expected
        # expected output with words which length equals 6 apeended with "&#x2122;"(TradeMark) logo 
            # input content

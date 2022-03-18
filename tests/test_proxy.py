import pytest
import ssl
#test TradeMark append function &#x2122;
class TestHandler:

    @pytest.mark.parametrize("test_input, expected",[
        ("Search:\n", "Search&#x2122;:\n")])
    def test_append_TM(self, handler, test_input, expected):
        assert handler.append_TM(self, test_input) 
        return expected

    # @pytest.mark.parametrize("test_")
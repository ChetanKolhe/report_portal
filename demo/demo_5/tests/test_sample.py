"""Sample test case to demonstrate execution with Report Portal .

How to execute .

Set bellow env
export REPORT_IO_ENDPOINT="http://localhost:8080"
export REPORT_IO_PROJECT="my_project"
export REPORT_IO_TOKEN="0bbf9a2f-b0fd-4f3b-8f1d-4e3f5d0fba30"

# Execute the bellow command from root location
python -m pytest demo/demo_5/tests/test_sample.py

"""
from logging import Logger

import pytest


@pytest.mark.parametrize("payload", [pytest.param("payload", id="1232:Test case description")])
def test_read_all_has_kent(payload, logger: Logger):
    """Single test function ."""
    assert "lskdjflk" == " "
    pass


class TestDemo:
    """Test Demo functionality .
    which have split line .
    """

    @pytest.mark.parametrize("payload", [pytest.param("payload", id="1232:Test case description")])
    def test_1(self, logger: Logger, payload):
        print(logger)
        print(payload)
        pass

    @pytest.mark.parametrize("payload", [pytest.param("payload", id="1234:Test case description")])
    def test_2(self, logger: Logger, payload):
        print(logger)
        print(payload)
        pass

from datetime import datetime, timedelta
import pytest


def test_read_all_has_kent(logger):
    """ Test on hitting People GET API, we get a user named kent in the list of people
    """
    response = "kent"

    # assert_that(response.status_code).is_equal_to(requests.codes.ok)
    logger.info("User successfully read")
    # logger.debug("This is info message")

    # assert_people_have_person_with_first_name(response, first_name='Kent')
    assert response == "kent", "Issue occur"


def test_logger_with_attachment(logger):
    """Memory with Attachment
   """
    response = "kent"

    assert response == "kent", "Issue occur"


def test_logger_all_message_print(logger):
    """It  will check all possible combination .
   """

    logger.info("Info message")
    logger.debug("this is debug message")
    logger.error("this is error message")
    logger.exception("this is exception message")
    response = "kent"

    # assert_that(response.status_code).is_equal_to(requests.codes.ok)
    logger.info("Memory Usage Attachment",
                attachment={
                    "name": "free_memory.txt",
                    "data": "This is large data set",
                    "mime": "application/octet-stream",
                }
                )
    # logger.debug("This is info message")

    # assert_people_have_person_with_first_name(response, first_name='Kent')
    assert response == "Kent", "Issue occur"


def test_large_message_dump(logger):
    """It  will check all possible combination .
   """

    logger.info("Info message " * 10000)
    logger.debug("this is debug message")
    logger.error("this is error message")
    logger.exception("this is exception message")
    response = "kent"

    assert response == "kent", "Issue occur"


testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]


@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected, logger):
    logger.debug("this is debug message")
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_v1(a, b, expected, logger):
    logger.debug("this is debug message")
    diff = a - b
    assert diff == expected


def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime("%Y%m%d")


@pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
def test_timedistance_v2(a, b, expected):
    diff = a - b
    assert diff == expected

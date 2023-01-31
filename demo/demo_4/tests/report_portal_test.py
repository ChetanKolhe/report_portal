from lib.report_portal_logger import ReportPortalLogger
from reportportal_client import step


def test_read_all_has_kent(logger: ReportPortalLogger):
    """ Test on hitting People GET API, we get a user named kent in the list of people
    """
    logger.test_begin("test_id_3", description="", module="Sample")
    logger.info("This is sample application ")
    logger.info("User successfully read")
    assert "Kent" == "demo", "error occur"


class TestDemo:
    def test_1(self, logger: ReportPortalLogger):
        logger.test_begin("test_id_1", description="", module="Sample")
        logger.info("This is sample application ", attachment="")
        logger.info("User successfully read")

    def test_2(self, logger: ReportPortalLogger):
        logger.test_begin("test_id_2", description="", module="Sample")
        logger.info("This is sample application ")
        logger.info("User successfully read")
        assert "chetan" == "demo", "error occur"


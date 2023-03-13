"""Logging Plugin to report the result ."""
import logging
import uuid
from logging import Logger

import pytest
from _pytest.fixtures import SubRequest
from pytest import Config, StashKey

from lib.report_portal_logger import ReportPortalClient

all_key = StashKey["all_key"]
_test_session = StashKey["test_session"]
session_name = "Test Demo Launch"
session_description = "Test Demo description"


class LogPlugin:
    """Plugin for adding markers to slow running tests."""

    def __init__(self, config):
        """Initialise plugin with config object."""
        self.config: Config = config
        self.config.services = [ReportPortalClient()]

        for each_session in self.config.services:
            each_session.start_session(session_name=session_name, session_description=session_description)

    def pytest_sessionstart(self, session: pytest.Session) -> None:
        """Start the pytest session."""
        session.stash[all_key] = self.config.services

        for each_session in session.stash[all_key]:
            each_session.start_session(session_name=session_name, session_description=session_description)

    def pytest_sessionfinish(self, session: pytest.Session):
        """Terminate the session object ."""
        for each_session in session.stash[all_key]:
            each_session.finish_session()

    @pytest.fixture(scope="function")
    def logger(self, request: SubRequest):
        """Logger object to dump the changes."""
        print("Logger generated 2 ")
        request.node.stash[all_key] = "sample"

        u_id = uuid.uuid1()

        logger = logging.getLogger(str(u_id))

        # Set the logger level to logging.INFO
        logger.setLevel(logging.INFO)

        yield logger

        # Mark the test fail as exception raised
        for each_session in request.node.stash[_test_session]:
            request.node.stash[_test_session][each_session].stop_test_session()

    def pytest_runtest_call(self, item: pytest.Item) -> None:
        """Run each test case , It modifies the logger and handler to dump the changes."""
        logger: Logger = item.funcargs.get("logger")
        # Get the test session

        module_name = self.get_module_name(item)
        test_case_id = self.get_test_case_id(item)
        test_case_description = self.get_description(item)

        item.stash[_test_session] = {}

        each_session: ReportPortalClient
        for each_session in item.session.stash[all_key]:
            test_session = each_session.get_test_session()
            handler = test_session.get_handler(
                test_case_id=test_case_id, module=module_name, description=test_case_description
            )
            logger.addHandler(handler)

            # Save the test session
            item.stash[_test_session][each_session] = test_session

    def pytest_exception_interact(self, node, call, report):
        """Log any test failures to the logger and mark the test as failed."""
        # Get the logger object from the local variables
        logger_obj = call.excinfo.traceback[0].locals.get("logger")

        # Log the longreprtext of the report to the logger
        logger_obj.error(report.longreprtext)

        # Mark the test fail as exception raised
        for each_session in node.stash[_test_session]:
            node.stash[_test_session][each_session].stop_test_session(status="failed")

    def get_module_name(self, item: pytest.Item):
        """Retrieve module/feature information so test can be categories ."""
        module_name = ""

        try:
            if item.cls:
                module_name = item.cls.__doc__.split("\n")[0]
        except Exception:
            pass

        if module_name:
            return module_name

        try:
            module_name = item.module.__doc__.split("\n")[0]
        except Exception:
            pass

        if module_name:
            return module_name

        if item.cls:
            return item.cls.__name__

        # Return module file name
        return item.module.__name__

    def get_test_case_id(self, item: pytest.Item):
        """Return test case id."""
        try:
            test_case_id = item.callspec.id
            test_id = test_case_id.split(":")[0]
            return test_id
        except Exception:
            raise ValueError("Please provide the id for test case {}".format(item))

    def get_description(self, item: pytest.Item):
        """Return description of given test case item."""
        try:
            test_case_id = item.callspec.id
            description = test_case_id.split(":")[1]
            return description
        except Exception:
            return "No Description"

import uuid
from logging import Logger
from typing import Union
import sys
import os

import pytest
import logging

from reportportal_client.client import RPClient

sys.path.append(os.getcwd())
from lib.report_portal_logger import ReportPortalLogger, time_stamp



launch_name = "Test Launch with custom logger"
launch_doc = "Testing logging with attachment."


@pytest.fixture(scope="session")
def launch(request):
    logging.setLoggerClass(ReportPortalLogger)
    client = RPClient(endpoint=os.environ.get("REPORT_IO_ENDPOINT"), project=os.environ.get("REPORT_IO_PROJECT"),
                      token=os.environ.get("REPORT_IO_TOKEN"))
    launch_id = client.start_launch(name=launch_name, start_time=time_stamp(), description="Description")
    print(client.get_launch_ui_url())
    yield launch_id
    client.finish_launch(end_time=time_stamp())
    client.terminate()


@pytest.fixture(scope="function")
def logger(launch):
    u_id = uuid.uuid1()
    logger: Union[ReportPortalLogger, Logger] = logging.getLogger(str(u_id))
    logger.setLevel(logging.INFO)
    logger.launch_id = launch
    yield logger
    logger.test_end()


def pytest_exception_interact(node, call, report):
    logger_obj = call.excinfo.traceback[0].locals.get("logger")
    logger_obj.error(report.longreprtext)
    logger_obj.test_end(status='failed')

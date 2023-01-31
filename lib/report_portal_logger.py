import logging
from logging import Logger
from time import time
from reportportal_client import RPLogger, RPLogHandler
from reportportal_client.client import RPClient
import os

from lib.reportio import ReportIO


def time_stamp():
    return str(int(time() * 1000))


"""
{
  "launch_id":{
        "module_name":"suit_id"
        }
}

"""
_TestSuitCache = {}


class ReportPortalClient:
    def __init__(self, report_io_endpoint=None, report_io_project=None, report_io_token=None, launch_id=None):
        self.launch_id = launch_id
        self.client: [RPClient, None] = None
        self.service = ReportIO(launch_id=self.launch_id)

        if report_io_endpoint is None:
            self._report_io_end_point = os.environ.get("REPORT_IO_ENDPOINT")
            if self._report_io_end_point is None:
                raise ValueError("Please set env REPORT_IO_ENDPOINT")
        else:
            self._report_io_end_point = report_io_endpoint

        if report_io_project is None:
            self._report_io_project = os.environ.get("REPORT_IO_PROJECT")
            if self._report_io_project is None:
                raise ValueError("Please set env REPORT_IO_PROJECT or Provide explicitly to report_io client")
        else:
            self._report_io_project = report_io_project

        if report_io_token is None:
            self._report_io_token = os.environ.get("REPORT_IO_TOKEN")
            if self._report_io_token is None:
                raise ValueError("Please set env REPORT_IO_PROJECT or Provide explicitly to report_io client")
        else:
            self._report_io_token = report_io_token

    def get_client(self, launch_id=None, project=None, token=None):

        launch_id = launch_id if launch_id else self.launch_id
        project = project if project else self._report_io_project
        token = token if token else self._report_io_token

        if self.client is None:
            self.client = RPClient(endpoint=self._report_io_end_point,
                                   project=project,
                                   token=token,
                                   launch_id=launch_id)

            self.service = ReportIO(launch_id=self.launch_id,
                                    report_io_project=project,
                                    report_io_endpoint=self._report_io_end_point,
                                    report_io_token=token
                                    )

        return self.client

    def get_test_module_id(self, module: str):
        suite_info = _TestSuitCache.get(self.launch_id)

        if suite_info is None:
            _TestSuitCache[self.launch_id] = {}
            suite_info = _TestSuitCache[self.launch_id]

        if suite_info.get(module.strip()):
            return suite_info.get(module.strip())

        item_id = self.service.create_test_suit(suit_name=module, suit_descr="")
        suite_info[module.strip()] = item_id
        return item_id


class ReportPortalLogger(RPLogger):

    def __init__(self, name, level=0):
        """
        Initialize RPLogger instance.

        :param name:  logger name
        :param level: level of logs
        """
        self._report_portal_client: [ReportPortalClient, None] = None
        self.launch_id = None
        self.project = None
        self.test_case_id = None
        self._test_status = None
        super(RPLogger, self).__init__(name, level=level)

    def test_begin(self, test_case_id, description, module):

        # Add logic to create module .
        if self.launch_id is None:
            self._report_portal_client = ReportPortalClient(report_io_project=self.project)
        else:
            self._report_portal_client = ReportPortalClient(launch_id=self.launch_id,
                                                            report_io_project=self.project)

        client = self._report_portal_client.get_client()

        if self.launch_id is None:
            # Launch id not define create default launch
            self.launch_id = client.start_launch("Default-Launch", start_time=time_stamp())

        # Add logic to create task suit
        # task_suite_id = client.start_test_item("Default-Task-Suit", start_time=time_stamp(), item_type="SUITE")
        task_suite_id = self._report_portal_client.get_test_module_id(module=module)

        self.test_case_id = client.start_test_item(name=test_case_id, start_time=time_stamp(), item_type="STEP",
                                                   description=description, parent_item_id=task_suite_id)

        client.log(time=time_stamp(), message="Hello World!", level="INFO", item_id=test_case_id)
        client.start()

        handler = RPLogHandler(rp_client=client)
        self.addHandler(handler)
        return client

    def test_end(self, status="passed"):
        client = self._report_portal_client.get_client()

        if self._test_status is None:
            client.finish_test_item(item_id=self.test_case_id, status=status, end_time=time_stamp())
            self._test_status = status

        if status == "failed":
            client.finish_test_item(item_id=self.test_case_id, status=status, end_time=time_stamp())
            self._test_status = status

        client.terminate()

        del client

    def __repr__(self):
        return f"<{self.__class__}(INFO)>"


if __name__ == '__main__':
    logging.setLoggerClass(ReportPortalLogger)

    logger: [ReportPortalLogger, Logger] = logging.getLogger("sdsafsdf")
    logger.setLevel(logging.INFO)

    logger: ReportPortalLogger
    logger.test_begin("demo", "ksdjkls", "lskjdlsjkdf")
    logger.info("this is infor message " * 100)
    logger.warning("this is warning message")
    try:
        raise ValueError("This is some exception occur ")
    except Exception as e:
        logger.exception(e)
    logger.test_end()

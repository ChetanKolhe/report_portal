import os
import threading
from copy import deepcopy
from datetime import datetime
from mimetypes import guess_type
from time import time

from reportportal_client import ReportPortalService

"""
How to set env 
export REPORT_IO_ENDPOINT="<Report io end point">    
export REPORT_IO_PROJECT="<Report io project">    
export REPORT_IO_TOKEN="<Report io token for Authentication">          

"""

report_io_lock = threading.Lock()


class ReportIO:
    # Bellow are test suit information tracker, which store the test suit id . It acts like test suit cache,
    """
    { "feature_name":"test_suit_id"}
    """

    def __init__(self, launch_name=None, description=" ", launch_id=None, attributes: dict = None,
                 report_io_endpoint=None, report_io_project=None, report_io_token=None):

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

        self._attributes = {}
        self._set_attributes()

        if attributes:
            self._attributes.update(attributes)

        self._launch_name = launch_name
        self._launch_descr = description

        # Storing current launch id and current test id makes non-supports of multithreading . Issue introduce from
        # racetrack .
        self._current_launch_id = launch_id
        self._current_test_id = None
        self._service = ReportPortalService(endpoint=self._report_io_end_point,
                                            project=self._report_io_project,
                                            token=self._report_io_token,
                                            launch_id=launch_id)

        self._test_suit = {}

    def _set_attributes(self):
        current_date = datetime.now()
        self._attributes["YEAR"] = current_date.year
        self._attributes["DAY"] = current_date.day
        self._attributes["MONTH"] = current_date.strftime("%b").upper()
        self._attributes["WEEK"] = current_date.strftime("%U")

    @property
    def launch_id(self):
        return self._current_launch_id

    def start_launch(self, launch_name=None, description="", attributes: dict = None):
        launch_name = launch_name if launch_name else self._launch_name
        description = description if description else self._launch_descr

        # attributes = attributes if attributes else self._attributes

        new_attributes = deepcopy(self._attributes)
        if attributes:
            new_attributes.update(new_attributes)

        if launch_name is None:
            raise ValueError("Please provide the launch while object creation or explicitly pass to start launch")
        self._current_launch_id = self._service.start_launch(
            name=launch_name, start_time=ReportIO._timestamp(), description=description, attributes=new_attributes
        )

    def terminate_launch(self):
        # print(self._service.get_launch_info())
        self._service.finish_launch(end_time=self._timestamp())

        # Due to async nature of the service we need to call terminate() method which
        # ensures all pending requests to server are processed.
        # Failure to call terminate() may result in lost data.
        self._service.terminate()

    # Bellow method are related to test suit methods
    def create_test_suit(self, suit_name: str, suit_descr=""):
        test_suite_id = self._service.start_test_item(
            name=suit_name,
            description=suit_descr,
            start_time=self._timestamp(),
            item_type="SUITE",
        )

        # Stored in cache which define in init section
        self._test_suit[suit_name.strip()] = test_suite_id
        return test_suite_id

    def get_test_suit(self, suit_name, suit_desc=""):

        with report_io_lock:
            test_suit_id = self._test_suit.get(suit_name.strip())

            if test_suit_id:
                return test_suit_id
            else:
                return self.create_test_suit(suit_name, suit_desc)

    # Bellow are test case Related method
    def test_case_begin(self, name, feature, description, attributes: dict = None):

        new_attribute = None
        if attributes:
            new_attribute = deepcopy(self._attributes)
            new_attribute.update(attributes)

        if attributes is None:
            new_attribute = self._attributes

        self._current_test_id = self._service.start_test_item(
            name=name,
            description=description,
            start_time=self._timestamp(),
            item_type="Step",
            attributes=new_attribute,
            parent_item_id=self.get_test_suit(suit_name=feature),
        )

    def test_case_end(self, test_case_id=None, result="PASS"):
        test_case_id = test_case_id if test_case_id else self._current_test_id

        if result.upper() == "PASS":
            result = "PASSED"
        elif result.upper() == "FAIL":
            result = "FAILED"
        else:
            result = "FAILED"

        self._service.finish_test_item(item_id=test_case_id, end_time=self._timestamp(), status=result)
        self._current_test_id = None

    def log(self, message, level="Info", attachment=None):

        if attachment:
            with open(attachment, "rb") as fh:
                attachment = {
                    "name": os.path.basename(attachment),
                    "data": fh.read(),
                    "mime": guess_type(attachment)[0] or "application/octet-stream",
                }
                self._service.log(
                    self._timestamp(),
                    message=message,
                    level=level,
                    attachment=attachment,
                    item_id=self._current_test_id,
                )
                return

        self._service.log(
            time=self._timestamp(), message=message, level=level, attachment=attachment, item_id=self._current_test_id
        )

    def get_launch_url(self):
        return self._service.get_launch_ui_url()

    @staticmethod
    def _timestamp():
        return str(int(time() * 1000))

    def get_launches(self, number_of_launches=None, year=None, month=None, day=None, week_day=None,
                     launch_name=None, **kwargs):
        """It returns the launch by mention filter

        @param launch_name:
        @param number_of_launches:
        @param year:
        @param month:
        @param day:
        @param week_day:
        @return:
        """
        params = {
            'page.page': 1,
            'page.size': 50,
            'page.sort': 'startTime,number,DESC',
            # 'filter.has.compositeAttribute': 'DAY:11',
        }

        if launch_name:
            params["filter.cnt.name"] = launch_name

        filter_attributes = ""

        if number_of_launches:
            params["page.size"] = number_of_launches

        if year:
            filter_attributes = f",YEAR:{year}" if filter_attributes else f"YEAR:{year}"

        if month:
            filter_attributes = f",MONTH:{month}" if filter_attributes else f"MONTH:{month}"

        if day:
            filter_attributes = f",DAY:{day}" if filter_attributes else f"DAY:{day}"

        if week_day:
            wk = "WK" + f"0{week_day}" if week_day > 0 else f"{week_day}"
            filter_attributes = f",WEEK:{wk}" if filter_attributes else f"WEEK:{wk}"

        if kwargs:
            for key, value in kwargs.items():
                filter_attributes = f",{key}:{value}" if filter_attributes else f"{key}:{value}"

        if filter_attributes:
            params['filter.has.compositeAttribute'] = filter_attributes

        url = self._report_io_end_point + f"/api/v1/{self._report_io_project}/launch"
        response = self._service.session.get(url=url, params=params, verify=self._service.verify_ssl)

        try:
            return response.json()['content']
        except Exception as e:
            print("Exception Occur while fetching launch information ", e)
            print("Response : ", response)
            return []

    def get_task_from_suite(self, launch_id, parent_id=None):
        """It returns the test task related to suite

        @param launch_id:
        @param parent_id: it used to make relation between task suit and task
        @return:
        """
        params = {
            'filter.level.path': 1,
            'page.page': 1,
            'page.size': 300,
            'page.sort': 'startTime,ASC',
            'providerType': 'launch',
            'launchId': launch_id,
        }

        if parent_id:
            params["filter.eq.parentId"] = parent_id
            del params["filter.level.path"]

        url = self._report_io_end_point + f"/api/v1/{self._report_io_project}/item/v2"
        response = self._service.session.get(url=url, params=params, verify=self._service.verify_ssl)

        return response.json()["content"]

    def delete_task_from_suite(self, task_id):

        if type(task_id) == int:
            task_id = [task_id]

        params = {
            'ids': ",".join([str(value) for value in task_id]),
        }
        url = self._report_io_end_point + f"/api/v1/{self._report_io_project}/item/"
        response = self._service.session.delete(url=url, params=params, verify=self._service.verify_ssl)

        # print(response.json())

        if response.status_code == 200:
            return True

        return False

    def merge_launches(self, merge_name, merge_description,
                       launches: list, attributes: dict = None, merge_type="DEEP", start_time=None, end_time=None):
        body = {
            "launches": launches,
            "mergeType": merge_type,
            "name": merge_name,
            "description": merge_description,
            "endTime": int(self._timestamp()) + 10,
            "startTime": self._timestamp(),
            "attributes": None,
            "extendSuitesDescription": True
        }

        if start_time and end_time:
            body["startTime"] = start_time
            body["endTime"] = end_time

        if attributes:
            attribute_result_list = []
            for key, value in attributes.items():
                attribute_result_list.append({"key": key, "value": value})
            body["attributes"] = attribute_result_list

        url = self._report_io_end_point + f"/api/v1/{self._report_io_project}/launch/merge"
        response = self._service.session.post(url=url, json=body, verify=self._service.verify_ssl)

        if response.status_code == 200:
            return response.json()
        return None


if __name__ == "__main__":
    report_io = ReportIO(
        launch_name="Library Test Launch",
        description="Library Test Launch Description",
        launch_id="dde7e84f-dac6-44f0-8771-124f5326086c",
    )
    # report_io.get_launches()
    task_from_suit = report_io.get_task_from_suite(launch_id="115")
    # print(task_from_suit)
    report_io.start_launch()

    print(report_io.get_launch_url())

    report_io.test_case_begin(name="Sample Test scenario", feature="Alert Check ", description="test case description")

    report_io.log("This is log message ")
    report_io.log("This is log message ")
    report_io.log("This is log message ", level="Debug")
    report_io.log("This is log message ", level="Error")
    report_io.test_case_end(result="Failed")

    report_io.terminate_launch()

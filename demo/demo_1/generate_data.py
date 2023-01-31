import datetime
import time
import os

from lib.reportio import ReportIO

failed_test_case = [1, 2]

error = {
    1: "Not able to create the user , please check again ",
    2: "Multiple user get created .",

}

alert_error = {
    1: "This error specific to user information retrieval, for test case 1",
    2: "User not get created with this given information ",

}

old_time = datetime.datetime(day=28, month=12, year=2023)
time_delta = datetime.timedelta(days=2)

for number_of_launch in range(1):

    old_time = old_time + time_delta
    week = old_time.strftime("%U")

    week = "WK" + str(week)

    report_io = ReportIO(
        launch_name="Regression Task Suit",
        description="Regression Task Suit Description ",
        attributes={"TYPE": "API", "ENV": "PROD", "NATURE": "REGRESSION", "COMPONENT": "PUBLISHER",
                    "WEEK": week, "DAY": old_time.day,
                    "MONTH": old_time.strftime("%b").upper(), "YEAR": old_time.year
                    },

    )
    report_io.start_launch(attributes={"WEEKDAY": week, "DAY": old_time.day, "MONTH": old_time.strftime("%b"), "YEAR": old_time.year})
    print(report_io.get_launch_url())

    for i in range(10):
        # start the test case
        report_io.test_case_begin(name=f"Create User Test Case {i}",
                                  feature="Task Suit: Create User ",
                                  description=f"Test case description {i}",
                                  attributes={"WEEKDAY": week, "DAY": old_time.day,
                                              "MONTH": old_time.strftime("%b"), "YEAR": old_time.year})

        # Add the log message
        report_io.log("This is log message ")
        report_io.log("This is log message ")
        report_io.log("This is log message ", level="Debug")

        # Mark the test case failed or passed
        if i in failed_test_case:
            report_io.log(error.get(i), level="Error")
            report_io.test_case_end(result="Failed")
            report_io.log("Error Snapshot", attachment=os.path.join(os.path.dirname(__file__), "img.png"))
            report_io.log("Error File", attachment=os.path.join(os.path.dirname(__file__), "error.txt"))
            time.sleep(2)
            report_io.log(error.get(i), level="Error")
            report_io.test_case_end(result="Failed")
        else:
            report_io.test_case_end()

    for i in range(10):
        # start the test case
        report_io.test_case_begin(name=f"Get employee info Test Case  {i}",
                                  feature="Task Suit: Employee information ",
                                  description=f"Employee Information Test Case {i}")

        # Add the log message
        report_io.log("This is log message ")
        report_io.log("This is log message ")
        report_io.log("This is log message ", level="Debug")

        # Mark the test case failed or passed
        if i in failed_test_case:
            report_io.log(alert_error.get(i), level="Error")
            report_io.test_case_end(result="Failed")
        else:
            report_io.test_case_end()
    report_io.terminate_launch()
    del report_io
    # time.sleep(5)

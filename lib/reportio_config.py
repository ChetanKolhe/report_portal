"""Report Portal configuration Reader library .

This library will get updated with vault reader instead of environment in the future.
"""
import os


class ReportPortalConfig:
    """Class used to read the default config information of Report Portal.

    Attributes:
        report_io_endpoint (str): The endpoint URL of the Report Portal API.
        report_io_project (str): The name of the Report Portal project.
        report_io_token (str): The Report Portal API token.
    """

    def __init__(self, report_io_endpoint=None, report_io_project=None, report_io_token=None):
        """Initialize ReportPortalConfig with the given data.

        Args:
            report_io_endpoint (str, optional): The endpoint URL of the Report Portal API. Defaults to None.
            report_io_project (str, optional): The name of the Report Portal project. Defaults to None.
            report_io_token (str, optional): The Report Portal API token. Defaults to None.

        Raises:
            ValueError: If `report_io_endpoint`, `report_io_project`, or `report_io_token` are not provided as
            environment variables or as arguments to the class.
        """
        if report_io_endpoint is None:
            self.report_io_endpoint = os.environ.get("REPORT_IO_ENDPOINT")
            if self.report_io_endpoint is None:
                raise ValueError(
                    "Please set the environment variable 'REPORT_IO_ENDPOINT'"
                    " or provide the endpoint URL as an argument to the class."
                )
        else:
            self.report_io_endpoint = report_io_endpoint

        if report_io_project is None:
            self.report_io_project = os.environ.get("REPORT_IO_PROJECT")
            if self.report_io_project is None:
                raise ValueError(
                    "Please set the environment variable 'REPORT_IO_PROJECT' or "
                    "provide the project name as an argument to the class."
                )
        else:
            self.report_io_project = report_io_project

        if report_io_token is None:
            self.report_io_token = os.environ.get("REPORT_IO_TOKEN")
            if self.report_io_token is None:
                raise ValueError(
                    "Please set the environment variable 'REPORT_IO_TOKEN' or "
                    "provide the API token as an argument to the class."
                )
        else:
            self.report_io_token = report_io_token

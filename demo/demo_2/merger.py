from lib.launch_merger import LaunchMerger
from lib.reportio import ReportIO

client = ReportIO()
launch_merger = LaunchMerger(report_io_client=client)
id_ = launch_merger.merge(merge_name="Week:Regression Task Suit",
                          merge_description="No description",
                          launch_names="Regression Task Suit",
                          WEEK="WK03")

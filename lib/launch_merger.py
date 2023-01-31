from lib.reportio import ReportIO


class LaunchMerger:

    def __init__(self, report_io_client: ReportIO):
        self._report_io = report_io_client

    def merge(self, merge_name, merge_description="description", launch_names=None, merge_attributes: dict = None,
              **kwargs):
        if merge_attributes is None:
            merge_attributes = {}
            merge_attributes.update(kwargs)

        launches = []
        # Step1 , Fetch launch information
        if launch_names:
            if type(launch_names) == str:
                launches = launches + self._report_io.get_launches(launch_name=launch_names, **kwargs)
            else:
                for each_launch in launch_names:
                    launches = launches + self._report_io.get_launches(launch_name=each_launch, **kwargs)

        if not launches:
            print("Launches not found with given filter value ", kwargs, "launch name:", launch_names)
            return None

        # Get 1 launch merge start and end time, so it will get replace with that latest merge.
        start_time = launches[0]["startTime"]
        end_time = launches[0]["endTime"]

        launches_id = [launch["id"] for launch in launches]

        # Step2, Merge launch information
        merge_response = self._report_io.merge_launches(merge_name=merge_name, merge_description=merge_description,
                                                        attributes=merge_attributes,
                                                        launches=launches_id,
                                                        start_time=start_time,
                                                        end_time=end_time)

        if merge_response is None:
            print("Failed to run the test cases")
            return

        merge_id = merge_response["id"]

        self.delete_duplicate(launch_id=merge_id)
        return merge_id

    def delete_duplicate(self, launch_id):
        task_suit = self._report_io.get_task_from_suite(launch_id=launch_id)

        task_suit = filter(lambda value: value.get("type") == "SUITE", task_suit)

        task_from_suite = []
        for value in task_suit:
            task_suit_temp = self._report_io.get_task_from_suite(launch_id=launch_id, parent_id=value["id"])

            # Add suit name
            for task in task_suit_temp:
                task["suite_name"] = value["name"]

            task_from_suite = task_from_suite + task_suit_temp

        # Generate data structure where key name "feature->task_name"
        filter_dict = {}
        for value in task_from_suite:
            # Generate key
            key = f"{value['suite_name']}->{value['name']}"

            if filter_dict.get(key):
                filter_dict[key].append(value)
            else:
                filter_dict[key] = [value]

        print(filter_dict)

        for filter_key in filter_dict:
            filter_dict[filter_key] = list(sorted(filter_dict[filter_key], key=lambda x: x["endTime"], reverse=True))

        # Filter deleted item id
        delete_item_id = []
        for key in filter_dict:
            delete_item_id = delete_item_id + [value["id"] for value in filter_dict[key][1:]]

        # Delete the duplicate data by chunk size
        chunk_size = 10
        deleted_chunk = [delete_item_id[i:i + chunk_size] for i in range(0, len(delete_item_id), chunk_size)]

        for list_id in deleted_chunk:
            self._report_io.delete_task_from_suite(task_id=list_id)

        # Step3, Remove duplicate test case


if __name__ == '__main__':
    client = ReportIO()
    launch_merger = LaunchMerger(report_io_client=client)
    launch_merger.merge(merge_name="Week:Content Delivery Regression Run", merge_description="No description",
                        launch_name="Content Delivery Regression Run",
                        DAY=19)

from typing import List, Any
import csv
import json

class ReportService:

    def __init__(self, objects_list: List[Any]):
        self.objects_list = objects_list

    def csv_dump(self, path, encoding="utf8"):
        with open(path, mode='w', encoding=encoding) as csv_file:
            writer = csv.writer(csv_file)
            headers = None
            for row in self.objects_list:
                if isinstance(row, dict):
                    if headers is None:
                        writer.writerow(row.keys())
                        headers = True
                    writer.writerow(row.values())
                else:
                    writer.writerow(row)

        return self

    def json_dump(self, path, encoding="utf8"):
        with open(path, "w", encoding=encoding) as f:
            json.dump(self.objects_list, f, indent=4, sort_keys=True)

        return self

from pathlib import Path
import os
import json


class Datafile():

    def __init__(self, pattern, integration_file, search_folder, askomics_client, type="csv"):
        current_args = locals()
        self.pattern = pattern
        self.search_folder = search_folder
        self.files = {}
        self.type = type
        self.askomics_client = askomics_client
        self.files_to_integrate = []

        with open(integration_file) as datafile:
            self.integration_template = json.load(datafile)

    def get_files(self):
        file_dict = {}
        for path in Path(self.search_folder).rglob(self.pattern):
            head, tail = os.path.split(path)
            if head not in file_dict:
                file_dict[head] = []
            file_dict[head].append({"file": tail, "time": os.path.getctime(path)})

        self.files = file_dict

    def cleanup_askomics(self):
        datasets = self.askomics_client.dataset.list()
        files = self.askomics_client.file.list()

        names_to_delete = []
        files_to_delete = []
        keys_to_delete = []

        for key, path in self.files.items():
            for value in path:
                file_name = value["file"]
                for file in files:
                    if file["name"] == file_name:
                        if file["date"] < value["time"]:
                            files_to_delete.append(file["id"])
                            names_to_delete.append(file_name)
                            print("Deleting remote obsolete file " + file_name)
                        else:
                            print("Skipping older local file " + file_name)
                            keys_to_delete.append(key)

        datasets_to_delete = [dataset["id"] for dataset in datasets if dataset["name"] in names_to_delete]

        if datasets_to_delete:
            self.askomics_client.dataset.delete(datasets_to_delete)
        if files_to_delete:
            self.askomics_client.file.delete(files_to_delete)

        if keys_to_delete:
            for key in keys_to_delete:
                self.files.pop(key, None)

        self.files_to_integrate = []
        for key, paths in self.files.items():
            for path in paths:
                self.files_to_integrate.append(os.path.join(key, path['file']))

    def upload_files(self):
        for file_path in self.files_to_integrate:
            self.askomics_client.file.upload(file_path=file_path)

    def integrate_files(self):
        uploaded_files = set([os.path.basename(file) for file in self.files_to_integrate])
        files = self.askomics_client.file.list()
        file_ids = set()

        for file in files:
            if file["name"] in uploaded_files:
                file_ids.add(file["id"])
        for id in file_ids:
            try:
                if self.type == "csv":
                    self.askomics_client.file.integrate_csv(id, columns=self.integration_template["columns"], headers=self.integration_template["headers"], force=True)
                elif self.type == "gff":
                    self.askomics_client.file.integrate_gff(id, entities=self.integration_template["columns"])
            except Exception as e:
                print(id)
                raise e

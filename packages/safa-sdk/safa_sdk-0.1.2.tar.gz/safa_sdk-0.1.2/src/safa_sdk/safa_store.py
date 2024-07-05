import json
from typing import Dict

from safa_sdk.util import read_json_file

ProjectData = Dict


class SafaStore:
    CREDENTIAL_KEY = "creds"
    PROJECT_KEY = "projects"

    def __init__(self, cache_file_path: str = None):
        self.cache_file_path = cache_file_path
        self.project_data = self.__create_empty_data()
        self.__load_cache_file()

    def store_project(self, version_id: str, project_data: ProjectData) -> None:
        self.project_data[SafaStore.PROJECT_KEY][version_id] = project_data
        self.save()

    def get_project(self, version_id: str) -> ProjectData:
        self.has_project(version_id, assert_contains=True)
        return self.project_data[SafaStore.PROJECT_KEY][version_id]

    def has_project(self, version_id: str, assert_contains: bool = False) -> bool:
        has_creds = version_id in self.project_data[SafaStore.PROJECT_KEY]
        if assert_contains and not has_creds:
            raise Exception(f"Project {version_id} does not have credentials.")
        return has_creds

    def store_credentials(self, email: str, token: str):
        self.project_data[SafaStore.CREDENTIAL_KEY][email] = token
        self.save()

    def get_credentials(self, email: str) -> str:
        self.has_credentials(email, assert_contains=True)
        return self.project_data[SafaStore.CREDENTIAL_KEY][email]

    def has_credentials(self, email: str, assert_contains: bool = False) -> bool:
        has_creds = email in self.project_data[SafaStore.CREDENTIAL_KEY]
        if assert_contains and not has_creds:
            raise Exception(f"Project {email} does not have credentials.")
        return has_creds

    def save(self) -> None:
        if self.cache_file_path is None:
            return
        with open(self.cache_file_path, "w") as f:
            f.write(json.dumps(self.project_data, indent=4))

    def __load_cache_file(self):
        if self.cache_file_path is None:
            return
        json_data = read_json_file(self.cache_file_path)
        cached_project_data = json_data.get(SafaStore.PROJECT_KEY, {})
        cached_credential_data = json_data.get(SafaStore.CREDENTIAL_KEY, {})
        self.project_data[SafaStore.PROJECT_KEY].update(cached_project_data)
        self.project_data[SafaStore.CREDENTIAL_KEY].update(cached_credential_data)

    @staticmethod
    def __create_empty_data() -> Dict:
        return {
            SafaStore.CREDENTIAL_KEY: {},
            SafaStore.PROJECT_KEY: {}
        }

from typing import List

from safa_sdk.base_client import BaseClient
from safa_sdk.safa_store import SafaStore


class Safa:
    BASE_URL = "https://api.safa.ai"
    TOKEN = 'SAFA-TOKEN'

    def __init__(self, store: SafaStore = None):
        self.client = BaseClient(Safa.BASE_URL)
        self.project_store = store

    def login(self, email, password):
        if self.project_store and self.project_store.has_credentials(email):
            self.client.set_auth_cookie(self.project_store.get_credentials(email))
        else:
            self.client.post("login", {"email": email, "password": password})
            if Safa.TOKEN not in self.client.session.cookies:
                raise Exception("Login failed, SAFA-TOKEN not found in cookies")
            auth_token = self.client.get_cookie(Safa.TOKEN, error="Login failed, cookie not found in base client.")
            self.client.set_auth_cookie(auth_token)
            if self.project_store:
                self.project_store.store_credentials(email, auth_token)

    def get_project_data(self, version_id: str, nocache: bool = False):
        if not nocache and self.project_store and self.project_store.has_project(version_id):
            project_data = self.project_store.get_project(version_id)
        else:
            project_data = self.client.get(f"projects/versions/{version_id}")
            if not nocache and self.project_store:
                self.project_store.store_project(version_id, project_data)
        return project_data

    def search_by_prompt(self, query: str, version_id: str, search_types: List[str]) -> List[str]:
        """
        Searches artifacts against query.
        :param query: The prompt used to search for related artifacts.
        :param version_id: ID of the version of the project to search.
        :param search_types: The types of artifacts to search in.
        :return: Artifact Ids of related artifacts.
        """
        payload = {
            "mode": "PROMPT",
            "prompt": query,
            "searchTypes": search_types
        }
        res = self.client.post(f"search/{version_id}", payload)
        return res["artifactIds"]

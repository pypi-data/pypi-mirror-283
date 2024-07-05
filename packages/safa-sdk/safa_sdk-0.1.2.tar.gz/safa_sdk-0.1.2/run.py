import os
import sys

from dotenv import load_dotenv

sys.path.append("src/safa_sdk")
from safa_sdk.safa_client import Safa
from safa_sdk.safa_store import SafaStore

if __name__ == '__main__':
    load_dotenv()
    VERSION_ID = os.environ["VERSION_ID"]
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    CACHE_FILE_PATH = os.path.expanduser(os.environ["CACHE_FILE_PATH"])

    project_store = SafaStore(CACHE_FILE_PATH)
    client = Safa(store=project_store)
    client.login(USERNAME, PASSWORD)

    project = client.get_project_data(VERSION_ID)

    query = "summarize commit"
    search_types = [t['name'] for t in project["artifactTypes"]]
    artifact_ids = client.search_by_prompt(query, VERSION_ID, search_types)

    queried_artifacts = [a for a in project["artifacts"] if a["id"] in artifact_ids]
    print("Artifact Ids:", artifact_ids)
    # project_store.store_project("p1", project_data)

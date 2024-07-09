# type: ignore
import os
import sys
from typing import Callable, Dict

from dotenv import load_dotenv

ROOT_PATH = os.environ.get("SAFA_SDK_ROOT_PATH", "src")
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from safa_sdk.safa_client import SafaClient

StateType = Dict


def get_projects(client: SafaClient, state: StateType):
    projects = client.get_projects()
    project_map = {p['name']: p for p in projects}
    print("Projects: ", "\n".join(list(project_map.keys())))
    return project_map


def create_project(client: SafaClient, state: StateType) -> None:
    project_created = client.create_project("test_project", "test_description")
    print("Project created: ", project_created["projectId"])


def delete_project(client: SafaClient, state: StateType) -> None:
    project_id = get_or_query(state, "project_id")
    delete_response = client.delete_project(project_id)
    print("Project deleted: ", delete_response)


def get_version(client: SafaClient, state: StateType):
    version_id = input("Version ID:")
    version_data = client.get_version(version_id)

    state["version_data"] = version_data
    print("Project Data was retrieved!", version_data["projectVersion"])


def get_project_versions(client: SafaClient, state: StateType):
    project_id = get_or_query(state, "project_id")
    project_versions = client.get_project_versions(project_id)
    versions = [f"{v}" for v in project_versions]
    print("\n".join(versions))


def search_version(client: SafaClient, state: Dict):
    version_id = get_or_query(state, "version_id")
    version_data = client.get_version(version_id)
    search_types = [t['name'] for t in version_data["artifactTypes"]]
    query = input("Query:")
    artifact_ids = client.search_by_prompt(query, version_id, search_types)
    selected_artifacts = [a["name"] for a in version_data["artifacts"] if a["id"] in artifact_ids]
    print("Search Results" if len(artifact_ids) > 0 else "No results")
    print("\n".join(selected_artifacts))


def hgen(client: SafaClient, state: StateType):
    project_map = get_projects(client, state)
    project_name = input("Project Name:")
    project_data = project_map[project_name]

    project_version = client.get_project_versions(project_data["projectId"])[0]
    version_id = project_version["versionId"]

    artifact_ids = [a["id"] for a in project_data["artifacts"]]
    client.hgen(version_id, {
        "artifacts": artifact_ids,
        "targetTypes": ["Functional Requirement", "Feature"]
    })


def commit_artifact(client: SafaClient, state: StateType):
    project_map = get_projects(client, state)
    project_name = input("Project Name:")
    project_data = project_map[project_name]

    project_id = project_data["projectId"]
    project_versions = client.get_project_versions(project_id)
    project_version = project_versions[0]
    version_id = project_version["versionId"]
    commit_data = {
        "artifacts": {
            "added": [
                {
                    "name": "artifact.py",
                    "summary": "",
                    "body": "print('hi')",
                    "type": "Code"
                }
            ],
            "modified": [],
            "removed": []
        },
        "traces": {
            "added": [],
            "modified": [],
            "removed": []
        }
    }
    response_data = client.commit(version_id, commit_data)
    artifact_ids = [a["id"] for a in response_data["artifacts"]["added"]]
    client.hgen(version_id, {
        "artifacts": artifact_ids,
        "targetTypes": ["Functional Requirement", "Feature"]
    })


def get_or_query(state: Dict[str, str], key_id: str) -> str | Dict:
    if key_id in state:
        return state[key_id]
    return input(f"{key_id}:")


def input_with_default(prompt: str, default_value: str) -> str:
    """
    Prompts user for value with option to select default value.
    :param prompt: The prompt shown to user.
    :param default_value: Value to use if empty response from user.
    :return: Value.
    """
    response = input(f"{prompt} ({default_value}):")
    if response == "":
        return default_value
    return response


def run_actions(actions: Dict[str, Callable]) -> None:
    action_keys = list(actions.keys()) + ["exit"]
    exit_idx = len(action_keys) - 1
    state = {}
    running = True

    c = SafaClient()
    c.login(USERNAME, PASSWORD, use_store=False)

    while running:
        print("\n".join([f"{i}. {action}" for i, action in enumerate(action_keys)]))
        action_idx = int(input("Action:"))
        if action_idx == exit_idx:
            return
        action_key = action_keys[action_idx]
        actions[action_key](c, state)


if __name__ == '__main__':
    load_dotenv()
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    CACHE_FILE_PATH = os.path.expanduser(os.environ["CACHE_FILE_PATH"])

    run_actions({
        "get_projects": get_projects,
        "create_project": create_project,
        "get_version_data": get_version,
        "delete_project": delete_project,
        "search_version": search_version,
        "get_versions": get_project_versions,
        "hgen": hgen,
        "commit": commit_artifact
    })

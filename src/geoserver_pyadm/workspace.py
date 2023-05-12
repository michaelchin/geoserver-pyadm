from . import _auth as a
import requests
from ._auth import auth
from ._exceptions import (
    WorkspaceAlreadyExists,
    FailedToCreateWorkspace,
    WorkspaceDoesNotExist,
    FailedToDeleteWorkspace,
)


@auth
def create_workspace(workspace_name, quiet_on_exist=True):
    """create a workspace by name

    :param workspace_name: the name of the workspace which you would like to create
    :param quiet_on_exist: flag to indicate if raise exception when the workspace already
        exists.

    """

    url = f"{a.server_url}/rest/workspaces"
    data = f"<workspace><name>{workspace_name}</name></workspace>"
    headers = {"content-type": "text/xml"}
    r = requests.post(url, data=data, auth=(a.username, a.passwd), headers=headers)

    if r.status_code == 201:
        print(f"The workspace {workspace_name} has been created successfully!")
    elif r.status_code in [401, 409]:
        if quiet_on_exist:
            print(f"The workspace {workspace_name} already exists.")
        else:
            raise WorkspaceAlreadyExists(workspace_name)
    else:
        raise FailedToCreateWorkspace(workspace_name)
    return r


@auth
def delete_workspace(workspace_name, quiet_on_not_exist=True):
    """delete a workspace by name

    :param workspace_name: the name of the workspace which you would like to delete
    :param quiet_on_not_exist: flag to indicate if raise exception when trying to
        delete an non-exist workspace

    """

    payload = {"recurse": "true"}
    url = f"{a.server_url}/rest/workspaces/{workspace_name}"
    r = requests.delete(url, auth=(a.username, a.passwd), params=payload)

    if r.status_code == 200:
        print(f"Workspace {workspace_name} has been deleted.")
    elif r.status_code == 404:
        if quiet_on_not_exist:
            print(f"Workspace {workspace_name} does not exist.")
        else:
            raise WorkspaceDoesNotExist(workspace_name)
    else:
        raise FailedToDeleteWorkspace(workspace_name)
    return r


@auth
def get_all_workspaces():
    """Get the names of all workspaces"""
    url = f"{a.server_url}/rest/workspaces"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "workspace" in data["workspaces"]:
            ret = [d["name"] for d in data["workspaces"]["workspace"]]
        return ret
    else:
        return None


@auth
def get_workspace(name):
    """Get the definition of a workspace

    :param name: the name of the workspace in which you are interested

    """
    url = f"{a.server_url}/rest/workspaces/{name}"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        return r.json()
    else:
        return None

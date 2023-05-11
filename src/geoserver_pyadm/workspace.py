import auth as a
import requests
from auth import auth


@auth
def create_workspace(workspace_name):
    """create a workspace by name

    :param workspace_name: the name of the workspace which you would like to create

    """

    print(a.server_url)

    url = f"{a.server_url}/rest/workspaces"
    data = f"<workspace><name>{workspace_name}</name></workspace>"
    headers = {"content-type": "text/xml"}
    r = requests.post(url, data=data, auth=(a.username, a.passwd), headers=headers)

    if r.status_code == 201:
        print(f"The workspace {workspace_name} has been created!")
    elif r.status_code in [401, 409]:
        print(f"The workspace {workspace_name} already exists.")
    else:
        print(f"Unable to create workspace {workspace_name}.")
    return r


@auth
def delete_workspace(workspace_name):
    """delete a workspace by name

    :param workspace_name: the name of the workspace which you would like to delete

    """
    # username, passwd, server_url = get_cfg()
    payload = {"recurse": "true"}
    url = f"{a.server_url}/rest/workspaces/{workspace_name}"
    r = requests.delete(url, auth=(a.username, a.passwd), params=payload)

    if r.status_code == 200:
        print(f"Workspace {workspace_name} has been deleted.")
    elif r.status_code == 404:
        print(f"Workspace {workspace_name} does not exist.")
    else:
        print(f"Error: {r.status_code} {r.content}")
    return r

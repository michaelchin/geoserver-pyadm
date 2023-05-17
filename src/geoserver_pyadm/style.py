import json

import requests

from . import _auth as a
from ._auth import auth


@auth
def add_style(style_name, workspace=None):
    """Add an empty style globally or into a workspace.

    :param style_name: the name of the style which you would like to create
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the new style will be a global one.

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{a.server_url}/rest/styles/"

    style_xml = (
        f"<style><name>{style_name}</name><filename>{style_name}.sld</filename></style>"
    )
    headers = {"content-type": "text/xml"}
    r = requests.post(
        url=url, data=style_xml, auth=(a.username, a.passwd), headers=headers
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to create new style {style_name}. {r.content}")
    return r


@auth
def modify_style(style_name, style_data, workspace=None):
    """Change an existing style.

    :param style_name: the name of the style
    :param style_data: the new data for the style
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the style is a global one.

    """
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{a.server_url}/rest/styles/{style_name}"

    header = {"content-type": "application/vnd.ogc.sld+xml"}

    r = requests.put(
        url,
        data=style_data,
        auth=(a.username, a.passwd),
        headers=header,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to modify style {style_name}. {r.content}")
    return r


@auth
def delete_style(style_name, workspace=None):
    """Delete a style by name

    :param style_name: the name of the style which you would like to delete
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the style is a global one.

    """
    # a.username, a.passwd, a.server_url = get_cfg()

    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{a.server_url}/rest/styles/{style_name}"

    r = requests.delete(
        url, auth=(a.username, a.passwd), params={"recurse": True, "purge": True}
    )

    if r.status_code in [200, 201]:
        print(f"Style {style_name} has been deleted. {r.status_code} {r.content}")
    else:
        print(f"Unable to delete {style_name}. {r.status_code} {r.content}")
    return r


@auth
def set_default_style(full_layer_name: str, full_style_name: str):
    """set the default style for a layer

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name
    :param full_style_name: str: the style name including the workspace_name,
        such as workspace_name:style_name

    """
    # a.username, a.passwd, a.server_url = get_cfg()

    headers = {"content-type": "application/json"}
    # headers = {"content-type": "text/xml"}
    url = f"{a.server_url}/rest/layers/{full_layer_name}"
    # style_xml = (
    #    f"<layer><defaultStyle><name>{full_style_name}</name></defaultStyle></layer>"
    # )
    # print(json_style)
    # json_style = {"defaultStyle": {"name": full_style_name}}
    json_style = {
        "layer": {"defaultStyle": {"name": full_style_name}},
    }

    r = requests.put(
        url,
        data=json.dumps(json_style),
        # data=style_xml,
        auth=(a.username, a.passwd),
        headers=headers,
    )

    if r.status_code in [200, 201]:
        print(
            f"The default style for layer {full_layer_name } has been set to {full_style_name}. {r.status_code} {r.content}"
        )
    else:
        print(
            f"Unable to set default style {full_style_name} for layer {full_layer_name}. {r.status_code} {r.text}"
        )


@auth
def add_additional_style(full_layer_name: str, full_style_name: str):
    """Add an additional style to a layer.

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name
    :param full_style_name: str: the style name including the workspace_name,
        such as workspace_name:style_name

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/layers/{full_layer_name}"

    headers = {"content-type": "text/xml"}
    r = requests.put(
        url,
        data=f"<layer><styles><style><name>{full_style_name}</name></style></styles></layer>",
        auth=(a.username, a.passwd),
        headers=headers,
    )

    if r.status_code in [200, 201]:
        print(
            f"The additional style {full_style_name} for layer {full_layer_name } has been added. {r.status_code} {r.content}"
        )
    else:
        print(
            f"Unable to add additional style {full_style_name} for layer {full_layer_name}. {r.status_code} {r.content}"
        )


@auth
def get_styles(workspace=None):
    """Get all global styles or all styles in a workspace

    :param workspace:  (Default value = None) If the workspace name is not given,
        all global styles will be returned.

    """
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{a.server_url}/rest/styles"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "style" in data["styles"]:
            ret = [d["name"] for d in data["styles"]["style"]]
        return ret
    else:
        return None

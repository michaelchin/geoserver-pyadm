class WorkspaceAlreadyExists(Exception):
    """Raise this exception when trying to create a workspace,
    but the workspace with the same name already exists

    :param workspace_name: the name of workspace

    """

    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        super().__init__(f"The workspace {self.workspace_name} already exists.")


class FailedToCreateWorkspace(Exception):
    """Raise this exception when creating workspace failed with unknown reason

    :param workspace_name: the name of workspace

    """

    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        super().__init__(f"Unable to create the workspace {self.workspace_name}.")


class WorkspaceDoesNotExist(Exception):
    """Raise this exception when trying to delete a workspace,
    but the workspace does not exist

    :param workspace_name: the name of workspace

    """

    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        super().__init__(f"The workspace {self.workspace_name} already exists.")


class FailedToDeleteWorkspace(Exception):
    """Raise this exception when deleting workspace failed with unknown reason

    :param workspace_name: the name of workspace

    """

    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        super().__init__(f"Unable to delete the workspace {self.workspace_name}.")

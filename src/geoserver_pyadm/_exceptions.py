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


class DatastoreAlreadyExists(Exception):
    """Raise this exception when trying to create a data store,
    but the data store with the same name already exists

    :param datastore_name: the name of data store

    """

    def __init__(self, datastore_name):
        self.datastore_name = datastore_name
        super().__init__(f"The datastore {self.datastore_name} already exists.")


class FailedToCreateDatastore(Exception):
    """Raise this exception when creating data store failed with unknown reason

    :param datastore_name: the name of datastore

    """

    def __init__(self, datastore_name):
        self.datastore_name = datastore_name
        super().__init__(f"Unable to create the datastore {self.datastore_name}.")


class DatastoreDoesNotExists(Exception):
    """Raise this exception when trying to delete a data store,
    but the data store with the same name does not exist

    :param datastore_name: the name of data store

    """

    def __init__(self, datastore_name):
        self.datastore_name = datastore_name
        super().__init__(f"The datastore {self.datastore_name} does not exist.")


class FailedToDeleteDatastore(Exception):
    """Raise this exception when deleting data store failed with unknown reason

    :param datastore_name: the name of datastore

    """

    def __init__(self, datastore_name):
        self.datastore_name = datastore_name
        super().__init__(f"Unable to delete the datastore {self.datastore_name}.")

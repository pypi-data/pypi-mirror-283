import pandas as pd
import requests
import json

from nemo_library.sub_symbols import *
from nemo_library.sub_connection_handler import *
from nemo_library.sub_config_handler import *
from nemo_library.sub_password_handler import *

DEFAULT_PROJECT_NAME = "Business Processes"

def getProjectList(config):
    """
    Retrieves a list of projects from the server and returns it as a DataFrame.

    Args:
        config: Configuration object that contains necessary connection settings.

    Returns:
        pd.DataFrame: DataFrame containing the list of projects.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)

    response = requests.get(
        config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_ALL, headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(config, projectname: str):
    """
    Retrieves the project ID for a given project name.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The ID of the specified project.

    Raises:
        Exception: If the project name is not found or if multiple projects match the given name.
    """
    if projectname is None:
        projectname = DEFAULT_PROJECT_NAME
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        raise Exception(f"could not identify project name {projectname}")
    project_id = crmproject["id"].to_list()[0]
    return project_id
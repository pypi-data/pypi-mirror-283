import json
import math
import os
import time

import boto3
from botocore.exceptions import NoCredentialsError

import pandas as pd
import requests

import gzip
import shutil
import re

from nemo_library.sub_symbols import *
from nemo_library.sub_connection_handler import *
from nemo_library.sub_config_handler import *
from nemo_library.sub_password_handler import *
from nemo_library.sub_project_handler import *
from nemo_library.sub_file_upload_handler import *


class NemoLibrary:

    def __init__(
        self,
        nemo_url=None,
        tenant=None,
        userid=None,
        password=None,
        environment=None,
        config_file="config.ini",
    ):

        with open(r"./nemo_library/sql_keywords.json", "r") as f:
            self.sql_keywords = set(json.load(f))

        self.config = ConfigHandler(
            nemo_url=nemo_url,
            tenant=tenant,
            userid=userid,
            password=password,
            environment=environment,
            config_file=config_file,
        )

        super().__init__()

    def getProjectList(self):
        """
        Retrieves a list of projects from the server.

        Returns:
            pd.DataFrame: DataFrame containing the list of projects.
        """
        return getProjectList(self.config)

    def getProjectID(self, projectname: str):
        """
        Retrieves the project ID for a given project name.

        Args:
            projectname (str): The name of the project for which to retrieve the ID.

        Returns:
            str: The ID of the specified project.
        """
        return getProjectID(self.config, projectname)

    def ReUploadFile(
        self,
        projectname: str,
        filename: str,
        update_project_settings: bool = True,
        datasource_ids: list[dict] = None,
        global_fields_mapping: list[dict] = None,
        version: int = 2,
        trigger_only: bool = False,
    ):
        """
        Uploads a file to a project and optionally updates project settings or triggers analyze tasks.

        Args:
            projectname (str): Name of the project.
            filename (str): Name of the file to be uploaded.
            update_project_settings (bool, optional): Whether to update project settings after ingestion. Defaults to True.
            datasource_ids (list[dict], optional): List of datasource identifiers for V3 ingestion. Defaults to None.
            global_fields_mapping (list[dict], optional): Global fields mapping for V3 ingestion. Defaults to None.
            version (int, optional): Version of the ingestion process (2 or 3). Defaults to 2.
            trigger_only (bool, optional): Whether to trigger only without waiting for task completion. Applicable for V3. Defaults to False.
        """
        
        ReUploadFileIngestion(
            config=self.config,
            projectname=projectname,
            filename=filename,
            update_project_settings=update_project_settings,
            datasource_ids=datasource_ids,
            global_fields_mapping=global_fields_mapping,
            version=version,
            trigger_only=trigger_only,
        )

    #################################################################################################################################################################

    def getImportedColumns(self, projectname: str):
        project_id = None

        try:
            project_id = self.getProjectID(projectname)

            # initialize reqeust
            headers = connection_get_headers(self.config)
            response = requests.get(
                self.config.config_get_nemo_url()
                + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                    projectId=project_id
                ),
                headers=headers,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            if project_id == None:
                raise Exception("process stopped, no project_id available")
            raise Exception("process aborted")



    #################################################################################################################################################################

    def LoadReport(self, projectname: str, report_guid: str, max_pages=None):
        project_id = self.getProjectID(projectname)

        print(f"Loading report: {report_guid} from project {projectname}")

        headers = connection_get_headers(self.config)

        # INIT REPORT PAYLOAD (REQUEST BODY)
        report_params = {"id": report_guid, "project_id": project_id}

        response_report = requests.post(
            self.config.config_get_nemo_url() + ENDPOINT_URL_REPORT_EXPORT,
            headers=headers,
            json=report_params,
        )

        if response_report.status_code != 200:
            raise Exception(
                f"request failed. Status: {response_report.status_code}, error: {response_report.text}"
            )

        # extract download URL from response
        csv_url = response_report.text.strip('"')
        print(f"Downloading CSV from: {csv_url}")

        # download the file into pandas
        try:
            result = pd.read_csv(csv_url)
            if "_RECORD_COUNT" in result.columns:
                result.drop(columns=["_RECORD_COUNT"], inplace=True)
        except Exception as e:
            raise Exception(f"download failed. Status: {e}")
        return result

    #################################################################################################################################################################

    def synchronizeCsvColsAndImportedColumns(self, projectname: str, filename: str):
        importedColumns = self.getImportedColumns(projectname)
        project_id = self.getProjectID(projectname)

        # Read the first line of the CSV file to get column names
        with open(filename, "r") as file:
            first_line = file.readline().strip()

        # Split the first line into a list of column names
        csv_column_names = first_line.split(";")

        # Check if a record exists in the DataFrame for each column
        for column_name in csv_column_names:
            displayName = column_name
            column_name = self.clean_column_name(
                column_name, RESERVED_KEYWORDS
            )  # Assuming you have the clean_column_name function from the previous script

            # Check if the record with internal_name equal to the column name exists
            if not importedColumns[
                importedColumns["internalName"] == column_name
            ].empty:
                print(f"Record found for column '{column_name}' in the DataFrame.")
            else:
                print(
                    f"******************************No record found for column '{column_name}' in the DataFrame."
                )
                new_importedColumn = {
                    "id": "",
                    "internalName": column_name,
                    "displayName": displayName,
                    "importName": displayName,
                    "description": "",
                    "dataType": "string",
                    "categorialType": False,
                    "businessEvent": False,
                    "unit": "",
                    "columnType": "ExportedColumn",
                    "tenant": connection_get_tenant(self.config),
                    "projectId": project_id,
                }

                self.createImportedColumn(new_importedColumn, project_id)

    #################################################################################################################################################################

    def clean_column_name(self, column_name, reserved_keywords):
        # If csv column name is empty, return "undefined_name"
        if not column_name:
            return "undefined_name"

        # Replace all chars not matching regex [^a-zA-Z0-9_] with empty char
        cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "", column_name)

        # Convert to lowercase
        cleaned_name = cleaned_name.lower()

        # If starts with a number, concatenate "numeric_" to the beginning
        if cleaned_name[0].isdigit():
            cleaned_name = "numeric_" + cleaned_name

        # Replace all double "_" chars with one "_"
        cleaned_name = re.sub(r"_{2,}", "_", cleaned_name)

        # If length of csv column name equals 1 or is a reserved keyword, concatenate "_" to the end
        if len(cleaned_name) == 1 or cleaned_name in reserved_keywords:
            cleaned_name += "_"

        return cleaned_name

    #################################################################################################################################################################

    def createImportedColumn(self, importedColumn: json, project_id: str):
        try:

            # initialize reqeust
            headers = connection_get_headers(self.config)
            response = requests.post(
                self.config.config_get_nemo_url()
                + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
                headers=headers,
                json=importedColumn,
            )
            if response.status_code != 201:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            raise Exception("process aborted")

    #################################################################################################################################################################

    def convert_internal_name(self, name: str) -> str:
        # Remove special chars and replace with unterscores
        pattern = r"[^a-zA-Z0-9_]+"
        internal_name = re.sub(pattern, "_", name)

        # Use a regular expression to find lowercase characters followed by uppercase characters
        pattern = re.compile(r"([a-z])([A-Z]+)")

        # Use re.sub to insert an underscore between the matched groups
        internal_name = re.sub(pattern, r"\1_\2", internal_name)

        internal_name = internal_name.lower()

        # multiple underscores to one underscore
        internal_name = re.sub("_{2,}", "_", internal_name)

        if internal_name.startswith("_"):
            internal_name = internal_name[1:]

        # column must not be an sql keyword
        if internal_name in self.sql_keywords:
            internal_name = f"name_{internal_name}"

        return internal_name

    def create_attribute_group(
        self, headers, project_id, group_name, parent_group_internal_name
    ) -> str:
        """
        Perform the desired action for each group by making an API call.

        :param headers: The headers for the API call.
        :param project_id: The project ID for the API call.
        :param group_name: Name of the current group.
        :param parent_group_internal_name: Internal name of the parent group.
        """

        api_url = (
            self.config.config_get_nemo_url()
            + "/api/nemo-persistence/metadata/AttributeGroup"
        )
        group_internal_name = self.convert_internal_name(group_name)
        payload = {
            "displayName": group_name,
            "displayNameTranslations": {
                "de": group_name  # Assuming 'en' is the default language
            },
            "internalName": group_internal_name,
            "parentAttributeGroupInternalName": parent_group_internal_name,
            "projectId": project_id,
        }

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 201:
            print(
                f"Successfully created group: {group_name} as child of {parent_group_internal_name}"
            )
            return group_internal_name
        else:
            print(
                f"Failed to create group: {group_name}. Status code: {response.status_code}, Error: {response.text}"
            )

    def process_groups(
        self,
        df,
        headers,
        projectId,
        current_group=None,
        parent_group_internal_name=None,
    ):
        """
        Recursively process groups starting from the root level.

        :param df: DataFrame containing the group information.
        :param headers: The headers for the API call.
        :param project_id: The project ID for the API call.
        :param current_group: The UUID of the current group to process. None indicates root level.
        :param parent_group_uuid: UUID of the parent group, None indicates root level.
        :param level: The current level in the hierarchy.
        """
        if current_group is None:
            # remove existing groups first
            api_url = (
                self.config.config_get_nemo_url()
                + f"/api/nemo-persistence/metadata/AttributeGroup/project/{projectId}/attributegroups"
            )
            response = requests.get(api_url, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            attributegroups = pd.json_normalize(resultjs)
            for index, row in attributegroups.iterrows():
                print("delete attribute group", row["internalName"])
                api_url = (
                    self.config.config_get_nemo_url()
                    + "/api/nemo-persistence/metadata/AttributeGroup/"
                    + row["id"]
                )
                response = requests.delete(api_url, headers=headers)
                if response.status_code != 204:
                    raise Exception(
                        f"request failed. Status: {response.status_code}, error: {response.text}"
                    )

            # create groups from scratch starting with root level
            root_groups = df[df["Enthalten in Gruppe (mit UUID)"].isna()]
            for index, row in root_groups.iterrows():
                nemo_group_internal_name = self.create_attribute_group(
                    headers, projectId, row["Attributname"], parent_group_internal_name
                )
                self.process_groups(
                    df,
                    headers,
                    projectId,
                    current_group=row["UUID"],
                    parent_group_internal_name=nemo_group_internal_name,
                )
        else:
            # Process sub-groups contained in the current group
            sub_groups = df[
                df["Enthalten in Gruppe (mit UUID)"].str.contains(
                    current_group, na=False
                )
            ]
            for index, row in sub_groups.iterrows():
                nemo_group_internal_name = self.create_attribute_group(
                    headers, projectId, row["Attributname"], parent_group_internal_name
                )
                self.process_groups(
                    df,
                    headers,
                    projectId,
                    current_group=row["UUID"],
                    parent_group_internal_name=nemo_group_internal_name,
                )

    def synchMetadataWithFocus(self, metadatafile: str, projectId: str):
        try:

            # headers for all requests
            headers = connection_get_headers(self.config)

            # read meta data from fox file
            foxmetadata = pd.read_excel(
                metadatafile,
                usecols=[
                    "Attribut",
                    "UUID",
                    "Attributname",
                    "Importname",
                    "Definition",
                    "Enthalten in Gruppe",
                    "Enthalten in Gruppe (mit UUID)",
                ],
            )
            foxmetadata.set_index("Attribut", inplace=True)

            # Filter rows where Definition is 'Gruppe' and create groups first
            foxmetadata_groups = foxmetadata[foxmetadata["Definition"] == "Gruppe"]
            # self.process_groups(foxmetadata_groups, headers, projectId)

            # read meta data from NEMO project
            response = requests.get(
                self.config.config_get_nemo_url()
                + f"/api/nemo-persistence/metadata/Columns/project/{projectId}/exported",
                headers=headers,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            nemometadatadf = pd.json_normalize(resultjs)

            # process attributes

            previous_attr = None
            for idx, row in foxmetadata.iterrows():

                print(
                    "processing attibute",
                    idx,
                    row["Attributname"],
                    "type:",
                    row["Definition"],
                )

                # search for twin in meta data
                if row["Definition"] not in ["Einfaches Attribut", "Gruppe"]:
                    print(
                        "attribute "
                        + row["Attributname"]
                        + " ignored, due to unsupported type "
                        + row["Definition"]
                    )
                else:
                    meta = nemometadatadf[
                        nemometadatadf["importName"]
                        == (
                            row["Attributname"]
                            if row["Definition"] == "Gruppe"
                            else row["Importname"]
                        )
                    ]
                    if len(meta) == 0:
                        print(
                            "could not find attribute "
                            + row["Attributname"]
                            + " in meta data!"
                        )
                    else:
                        if len(meta) > 1:
                            print(
                                "multiple matches of attribute "
                                + row["Attributname"]
                                + " in meta data. Type : "
                                + row["Definition"]
                                + ". First one will be selected"
                            )
                        first_meta = meta.iloc[0]
                        source_id_meta = first_meta["id"]

                        if pd.isna(row["Enthalten in Gruppe"]):
                            group_name = None
                        else:
                            group_name = self.convert_internal_name(
                                row["Enthalten in Gruppe"]
                            )

                        # lets move the attribute now
                        api_url = (
                            self.config.config_get_nemo_url()
                            + f"/api/nemo-persistence/metadata/AttributeTree/projects/{projectId}/attributes/move"
                        )
                        payload = {
                            "sourceAttributes": [source_id_meta],
                            "targetPreviousElementId": previous_attr,
                            "groupInternalName": group_name,
                        }

                        response = requests.put(api_url, headers=headers, json=payload)
                        if response.status_code != 204:
                            raise Exception(
                                f"request failed. Status: {response.status_code}, error: {response.text}"
                            )

                        previous_attr = source_id_meta

        except Exception as e:
            raise Exception(f"process aborted: {str(e)}")

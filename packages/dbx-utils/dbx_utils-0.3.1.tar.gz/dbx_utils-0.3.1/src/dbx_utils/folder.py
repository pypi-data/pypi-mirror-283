import requests
from databricks_api import DatabricksAPI

def create_databricks_folder(url, token, folder_path):
    """
    Creates a folder in Databricks workspace.

    Parameters:
    - url (str): The Databricks workspace URL.
    - token (str): The Databricks API token.
    - folder_path (str): The path of the folder to create.

    Returns:
    - str: The ID of the created folder.
    """
    # Initialize the Databricks API client
    api = DatabricksAPI(
        host=url,
        token=token
    )
    
    try:
        # Create the folder
        api.workspace.mkdirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
        
        # Get the folder ID
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        folder_status = requests.get(f'{url}/api/2.0/workspace/get-status', headers=headers, json={"path": folder_path})
        folder_status.raise_for_status()
        folder_id = folder_status.json().get('object_id')
        
        print(f"Folder ID for '{folder_path}' is {folder_id}.")
        return folder_id
    except Exception as e:
        print(f"Error creating folder '{folder_path}': {str(e)}")
        return None

def set_folder_permissions(url, token, folder_id):
    """
    Sets read permissions for all users on a Databricks folder.

    Parameters:
    - url (str): The Databricks workspace URL.
    - token (str): The Databricks API token.
    - folder_id (str): The ID of the folder to set permissions for.

    Returns:
    - None
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "access_control_list": [
            {
                "group_name": "users",
                "permission_level": "CAN_READ"
            }
        ]
    }
    
    try:
        # Correct endpoint for setting permissions on a directory
        response = requests.put(f'{url}/api/2.0/permissions/directories/{folder_id}', headers=headers, json=data)
        response.raise_for_status()  # Raise exception for non-2xx responses
        print(f"Permissions set for folder with ID '{folder_id}' successfully.")
        print(response.json())  # Print response content for confirmation
    except requests.exceptions.RequestException as e:
        print(f"Error setting permissions for folder with ID '{folder_id}': {e}")
        if response and response.status_code != 404:
            print(response.text)  # Print response content for debugging

def get_databricks_folder_id(url, token, folder_path):
    """
    Retrieves the ID of a folder in Databricks workspace.

    Parameters:
    - url (str): The Databricks workspace URL.
    - token (str): The Databricks API token.
    - folder_path (str): The path of the folder.

    Returns:
    - str: The ID of the folder if it exists, None otherwise.
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        # Getting the folder status to retrieve the folder ID
        get_status_response = requests.get(f'{url}/api/2.0/workspace/get-status', headers=headers, params={"path": folder_path})
        
        if get_status_response.status_code == 200:
            folder_id = get_status_response.json().get('object_id')
            print(f"Folder ID for '{folder_path}' is {folder_id}.")
            return folder_id
        else:
            print(f"Folder '{folder_path}' not found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving folder '{folder_path}': {e}")
        return None

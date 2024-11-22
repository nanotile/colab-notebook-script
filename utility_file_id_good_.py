# -*- coding: utf-8 -*-
"""UTILITY_File_id-GOOD .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IHPbf7mZVTJnCmoY-Pr_opKALqDnIlpa

OpenAI 01-preview   11/17/2024

# **Mount Google Drive to access files**
"""

# Mount Google Drive to access files
from google.colab import drive
drive.mount('/content/drive')

"""# **RETURN FILE_ID FROM SHARE ADDRESS**

Below is a Google Colab function that extracts the file_ID from a Google Drive share URL. The function extract_file_id takes a Google Drive share address as input and returns the file_ID as a string.

https://drive.google.com/file/d/1u6JV8WqY-l-Oef7iJOmb7mDy-xO8pEw_/view?usp=drive_link
"""

def extract_file_id(share_url):
    import re
    """
    Extracts the file_ID from a Google Drive share URL.

    Parameters:
    share_url (str): The Google Drive share URL.

    Returns:
    str: The extracted file_ID.
    """
    # Regular expression patterns to match different URL formats
    patterns = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',  # Pattern for /file/d/FILE_ID
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',  # Pattern for open?id=FILE_ID
        r'https://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)',    # Pattern for uc?id=FILE_ID
        r'id=([a-zA-Z0-9_-]+)',  # General pattern for id=FILE_ID
        r'/d/([a-zA-Z0-9_-]+)',  # General pattern for /d/FILE_ID
    ]

    for pattern in patterns:
        match = re.search(pattern, share_url)
        if match:
            file_id = match.group(1)
            return file_id
    raise ValueError("Invalid Google Drive URL. Cannot extract file ID.")
share_url = 'https://drive.google.com/file/d/1u6JV8WqY-l-Oef7iJOmb7mDy-xO8pEw_/view?usp=drive_link'
file_id = extract_file_id(share_url)
#file_id = extract_file_id('https://drive.google.com/file/d/1u6JV8WqY-l-Oef7iJOmb7mDy-xO8pEw_/view?usp=drive_link')
print("file_id:", file_id)

"""# **Get full path on Gdrive given file_id**  """

def get_full_file_path(file_ID):
    # Authenticate and create the PyDrive client.
    from google.colab import auth
    auth.authenticate_user()

    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth import default

    creds, _ = default()
    drive_service = build('drive', 'v3', credentials=creds)

    # Get the file metadata
    file = drive_service.files().get(fileId=file_ID, fields='name, parents').execute()
    path_parts = [file['name']]
    parent_ids = file.get('parents', [])

    # Build the full path
    while parent_ids:
        parent_id = parent_ids[0]  # Assuming only one parent
        if parent_id == 'root':
            break
        parent = drive_service.files().get(fileId=parent_id, fields='name, parents').execute()
        path_parts.insert(0, parent['name'])
        parent_ids = parent.get('parents', [])

    full_file_path = '/' + '/'.join(path_parts)

    # Print file_info containing the file_name retrieved and its full_file_path
    print(f"file_ID: {file_ID}")
    print(f"file_name: {file['name']}")
    print(f"full_file_path: {full_file_path}")

    # Return the full_file_path as a string variable
    return full_file_path

full_file_path = get_full_file_path(file_id)
print("Full file path:", full_file_path)

full_file_path
type(full_file_path)

"""2

# **Get parent Folders given file_id**
"""

def get_parent_folders(file_ID):
    """
    Retrieves the parent folder(s) containing the specified file.

    Parameters:
    file_ID (str): The ID of the file.

    Returns:
    list: A list of dictionaries containing 'id' and 'name' of parent folders.
    """
    # Authenticate and create the Drive service.
    from google.colab import auth
    auth.authenticate_user()

    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth import default

    creds, _ = default()
    drive_service = build('drive', 'v3', credentials=creds)

    try:
        # Get the file metadata including parents
        file = drive_service.files().get(fileId=file_ID, fields='name, parents').execute()
        file_name = file.get('name')
        parent_ids = file.get('parents', [])

        parent_folders = []

        # Get the parent folder(s) information
        for parent_id in parent_ids:
            parent = drive_service.files().get(fileId=parent_id, fields='id, name').execute()
            parent_folders.append({'id': parent['id'], 'name': parent['name']})

        # Debugging information
        print(f"File Name: {file_name}")
        if parent_folders:
            print("Parent Folder(s):")
            for parent in parent_folders:
                print(f" - {parent['name']} (ID: {parent['id']})")
        else:
            print("This file is in the root directory.")

        return parent_folders

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

get_parent_folders(file_id)

"""# **Example usage FOR NOTEBOOK:**"""

# Example usage:


file_id = extract_file_id(share_url)
print("File   id1:", file_id)

full_file_path = get_full_file_path(file_id)
print("Full file path:", full_file_path)

parent_folders = get_parent_folders(file_id)
print("Parent folders:", parent_folders)


Chapter 5: Google Drive Authentication
======================================
- `5.1. Activating Google Drive API`_
- `5.2. Creating a Service Account`_
- `5.3. Sharing Google Drive Folder`_
- `5.4. (Legacy) OAuth2.0 for Authentication`_

5.1. Activating Google Drive API
--------------------------------
| Adapted from `PyDrive2 documentation <https://pythonhosted.org/PyDrive2/quickstart.html>`_
|
1. Go to `Google APIs Console <https://console.developers.google.com/iam-admin/projects>`_ to make your own project.
2. Enter an appropriate project name and click "Create".
3. Search for "Google Drive API", select the entry, and click "Enable".

5.2. Creating a Service Account
-------------------------------
1. Go to `Google Cloud Console <https://console.cloud.google.com/>`.
2. In your project, navigate to "IAM & Admin" > "Service Accounts".
3. Navigate to "Service Accounts" and create a new service account.
4. Enter an appropriate service account name and click "Create and Continue".
5. Grant the "Editor" or "Owner" role to the service account.
6. Select the newly created service account and navigate to "Keys".
7. Select "Add Key", click "Create new key", then select a JSON key.
8. Upon clicking "Create", the JSON key file will be downloaded to your computer.

5.3. Sharing Google Drive Folder
--------------------------------
1. Go to your Google Drive.
2. Right-click the folder you want the service account to access.
3. Click "Share" and enter the service account's email address (found in the JSON key file).

5.4. (Legacy) OAuth2.0 for Authentication
-----------------------------------------
| Originally recommended by PyDrive2 for a quickstart, requires manual authentication which doesn't fit our use case.
| **YOU DO NOT NEED TO FOLLOW THESE STEPS, THEY ARE LEGACY INSTRUCTIONS.**
|
| Adapted from `PyDrive2 documentation <https://pythonhosted.org/PyDrive2/quickstart.html>`_
|
1. Go to `Google Cloud Console <https://console.cloud.google.com/>`.
2. In your project, navigate to "IAM & Admin" > "APIs & Services".
3. Select "Credentials" from the left menu, click "Create Credentials", then select "OAuth client ID".
4. Click "Configure Consent Screen" and follow the instructions.
5. Select "Application type" to be "Web Application".
6. Enter an appropriate name.
7. Input http://localhost:8080/ for "Authorized redirect URIs".
8. Click "Create".
9. Click "Download JSON" on the right side of Client ID to download client_secret_<really long ID>.json.
10. Rename the file to "client_secrets.json" and place it in your working directory.
11. Running the following code will open a web browser asking you for authentication:

  .. code-block:: python
  
    from pydrive2.auth import GoogleAuth
  
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

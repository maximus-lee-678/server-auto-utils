import stop
import start
import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

import common_server_auto


common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def gdrive_auth(path_service_account_json):
    """
    Authenticate with Google Drive using a service account JSON file.
    Returns an object that can be used to interact with Google Drive.
    API reference: https://developers.google.com/drive/api/guides/ref-search-terms

    :param string path_service_account_json: Path to the service account JSON file.
    """

    scope = ["https://www.googleapis.com/auth/drive"]
    gauth = GoogleAuth()
    gauth.auth_method = "service"
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_service_account_json, scope)
    drive = GoogleDrive(gauth)

    return drive


def gdrive_upload(drive, path_to_file, title, folder_id):
    """
    Upload a file to Google Drive.

    :param GoogleDrive drive: GoogleDrive object.
    :param string path_to_file: Path to the file to upload.
    :param string title: Title of the file to upload.
    :param string folder_id: ID of the folder to upload the file to.
    """

    file = drive.CreateFile({"title": title, "parents": [{"id": folder_id}]})
    file.SetContentFile(path_to_file)
    file.Upload()


def gdrive_manage_backups(drive, folder_id, service_account_email, backup_count):
    """
    Remove oldest Google Drive backup if the number of backups exceeds the limit.

    :param GoogleDrive drive: GoogleDrive object.
    :param string folder_id: ID of the Google Drive folder where backups are stored.
    :param string service_account_email: Email of the service account.
    :param int backup_count: Number of backups to keep.

    :return: List of IDs of the backups that are kept.
    """

    query = {"q": f"\"{folder_id}\" in parents and '{service_account_email}' in owners and trashed=false"}
    file_list = drive.ListFile(query).GetList()

    sorted_file_list = sorted(file_list, key=lambda x: x["createdDate"])
    if len(file_list) > int(backup_count):
        gdrive_object_id_to_remove = sorted_file_list[0]["id"]
        # cannot use gdrive_object_to_remove["title"] as it would have been deleted
        gdrive_object_name_to_remove = sorted_file_list[0]["title"]
        gdrive_object_to_remove = drive.CreateFile({"id": gdrive_object_id_to_remove})

        logger.info(f"Removing oldest backup {gdrive_object_name_to_remove}.")
        gdrive_object_to_remove.Delete()
        sorted_file_list.pop(0)
        logger.info(f"""Removed oldest backup {gdrive_object_name_to_remove}.""")
    logger.info(f"Google Drive owned file count: {len(file_list) - 1 if len(file_list) > int(backup_count) else len(file_list)}.")

    return [file["id"] for file in sorted_file_list]


def gdrive_housekeeping(drive, service_account_email, ids_to_keep):
    """
    Delete all files owned by the service account except for the ones in ids_to_keep.
    Needed as users can delete files owned by the service account, but this action does not move the files to the trash or delete them.

    :param GoogleDrive drive: GoogleDrive object.
    :param string service_account_email: Email of the service account.
    :param list ids_to_keep: List of IDs of the files to keep.
    """

    query = {"q": f"'{service_account_email}' in owners"}
    file_list = drive.ListFile(query).GetList()

    for file in file_list:
        if file["id"] not in ids_to_keep:
            logger.info(f"""Deleting file {file["title"]}.""")
            file_to_delete = drive.CreateFile({"id": file["id"]})
            file_to_delete.Delete()
            logger.info(f"""Deleted file {file["title"]}.""")


def main():
    datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")

    dict_dotenv = common_server_auto.get_dotenv()
    if not dict_dotenv:
        logger.error(common_server_auto.LOGGER_FAILED_TO_READ_ENV_MSG)
        return

    path_utils_location = dict_dotenv["PATH_UTILS_LOCATION"]
    service_account_json_name = dict_dotenv["SERVICE_ACCOUNT_JSON_NAME"]
    gdrive_backup_folder_id = dict_dotenv["GDRIVE_BACKUP_FOLDER_ID"]
    path_server_folder = dict_dotenv["PATH_SERVER_FOLDER"]
    path_backup_folder = dict_dotenv["PATH_BACKUP_FOLDER"]
    backup_count = dict_dotenv["BACKUP_COUNT"]
    backup_compression_level = dict_dotenv["BACKUP_COMPRESSION_LEVEL"]
    tmux_session_name = dict_dotenv["TMUX_SESSION_NAME"]
    force_shutdown_delay_seconds = int(dict_dotenv["FORCE_SHUTDOWN_DELAY_SECONDS"])

    session_was_running = False
    if common_server_auto.check_for_tmux_session(tmux_session_name):
        session_was_running = True

    if session_was_running:
        logger.info(f"tmux session is running, stopping before running the backup.")
        common_server_auto.send_tmux_input(
            tmux_session_name, "/say A Manual backup has been triggered, the server will shutdown in 3 seconds."
        )
        stop.stop(force_shutdown_delay_seconds)

        # wait for tmux session to actually close
        while 1:
            if not common_server_auto.check_for_tmux_session(tmux_session_name):
                break
            time.sleep(1)

        logger.info(f"tmux session stopped.")

    service_account_json_path = Path(f"{path_utils_location}/{service_account_json_name}")
    drive = gdrive_auth(service_account_json_path)
    service_account_email = json.loads(open(service_account_json_path).read())["client_email"]

    # Create a local backup
    # pushd changes the current directory to the path stored in $world_path.
    # popd returns to the original directory that the script was in before the pushd command.
    # > /dev/null suppresses the output of the pushd/popd command to avoid cluttering the console.
    zip_file_name = f"world_{datetime_now}.zip"
    zip_file_path = f"{path_backup_folder}/{zip_file_name}"
    logger.info(f"Creating backup at {zip_file_path}.")
    output, error = common_server_auto.run_command(
        f"pushd {path_server_folder}/world > /dev/null && zip -q -r -{backup_compression_level} {zip_file_path} . && popd > /dev/null")
    logger.info(f"Backup created, stdout: [{output}], stderr: [{error}]")

    # Remove oldest local backup if the number of backups exceeds the limit
    backup_list = sorted(Path(path_backup_folder).iterdir(), key=os.path.getmtime)
    if len(backup_list) > int(backup_count):
        local_filepath_to_remove = backup_list[0]
        logger.info(f"Removing oldest backup {local_filepath_to_remove}.")
        os.remove(local_filepath_to_remove)
        backup_list.remove(local_filepath_to_remove)
        logger.info(f"Removed oldest backup.")
    logger.info(f"Local backup count: {len(backup_list)}.")

    # Upload the backup to Google Drive
    logger.info(f"Uploading backup {zip_file_name} to Google Drive.")
    gdrive_upload(
        drive=drive, path_to_file=zip_file_path, title=zip_file_name, folder_id=gdrive_backup_folder_id
    )
    logger.info("""Uploaded to Google Drive.""")

    # Prune backups in Google Drive
    logger.info("Pruning backups in Google Drive.")
    ids_backup_list = gdrive_manage_backups(
        drive=drive, folder_id=gdrive_backup_folder_id, service_account_email=service_account_email, backup_count=backup_count
    )
    logger.info("Pruned backups in Google Drive.")

    # Housekeeping in Google Drive
    logger.info("Housekeeping files deleted by other users in Google Drive.")
    gdrive_housekeeping(
        drive=drive, service_account_email=service_account_email, ids_to_keep=ids_backup_list
    )
    logger.info("Housekeeping complete.")

    # Display storage info
    about = drive.GetAbout()
    logger.info(f"Storage: {int(about["quotaBytesUsed"]) / (1024 ** 3):.2f} GB of {int(about["quotaBytesTotal"]) / (1024 ** 3):.2f} GB used.")

    logger.info("Backup process complete.")

    if session_was_running:
        logger.info(f"tmux session was running before backup, restarting server.")
        start.start()
        logger.info(f"tmux session started.")


if __name__ == "__main__":
    main()

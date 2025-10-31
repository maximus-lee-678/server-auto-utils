import sys
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
import stop
import start

GDRIVE_AWAIT_UPLOAD_DETECTED_INTERVALS = [1, 2, 4, 8, 16, 32, 64]

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main(filter_instances=None):
    """
    :param list/None filter_instances: List of instance names to backup, or None to backup all instances available in configuration file.
    """

    logger.info(f"SCRIPT {__name__} STARTED.")

    datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")

    env_data = common_server_auto.get_env_json()
    if not env_data:
        return

    if filter_instances:
        instances = filter_instances
        logger.info(f"""Filtering to backup only instances: {instances}""")

        # verify specified instance(s) exists
        for instance_name in instances:
            if instance_name not in env_data["instances"]:
                logger.critical(f"Instance name '{instance_name}' not found in env.json.")
                return
    else:
        instances = env_data["instances"].keys()
        logger.info(f"""Backing up all instances: {instances}""")

    # details global to all instances
    path_utils_location = env_data["path_utils_location"]
    service_account_json_name = env_data["service_account_json_name"]
    force_shutdown_delay_seconds = int(env_data["force_shutdown_delay_seconds"])

    # init gdrive
    service_account_json_path = Path(f"{path_utils_location}/{service_account_json_name}")
    drive = gdrive_auth(service_account_json_path)
    try:
        service_account_email = json.loads(open(service_account_json_path).read())["client_email"]
    except Exception as e:
        logger.critical(f"Error reading service account email: Caught {e.__class__.__name__} Exception: {e}")
        return

    # loop through instances to backup
    count_instances = len(instances)
    ids_to_not_housekeep = []
    for i, instance_name in enumerate(instances):
        logger.info(f"[{i + 1}/{count_instances}] Starting backup for instance '{instance_name}'.")

        session_was_running = False

        # details for each instance
        instance_details = env_data["instances"][instance_name]
        do_backup = instance_details["backup"]["do"]
        target_backup_folder_gdrive_id = instance_details["backup"]["SECRET_target_backup_folder_gdrive_id"]
        path_folder_to_backup = instance_details["backup"]["path_folder_to_backup"]
        target_backup_folder_local_path = instance_details["backup"]["target_backup_folder_local_path"]
        backup_count = instance_details["backup"]["backup_count"]
        backup_compression_level = instance_details["backup"]["backup_compression_level"]
        arc_name_template = instance_details["backup"]["arc_name_template"]
        tmux_session_name = instance_details["tmux_session_name"]

        if not do_backup:
            logger.info(f"[{i + 1}/{count_instances}] Backup disabled for instance '{instance_name}', skipping.")
            continue

        arc_name = arc_name_template.format(timestamp=datetime_now)
        zip_file_path = f"{target_backup_folder_local_path}/{arc_name}"

        if common_server_auto.check_for_tmux_session(tmux_session_name):
            session_was_running = True
            logger.info(f"[{i + 1}/{count_instances}] tmux session is running, stopping before running the backup.")
            stop.main(countdown_seconds=force_shutdown_delay_seconds, filter_instances=[instance_name])

        if not Path(target_backup_folder_local_path).exists():
            logger.info(f"[{i + 1}/{count_instances}] Creating local backup folder at {target_backup_folder_local_path}.")
            os.makedirs(target_backup_folder_local_path)
            logger.info(f"[{i + 1}/{count_instances}] Created local backup folder.")

        # local: make backup
        local_make_backup(
            path_source_folder=path_folder_to_backup, path_backup_folder=target_backup_folder_local_path,
            arc_name=arc_name, backup_compression_level=backup_compression_level
        )

        # local: manage backups (keep only n most recent)
        local_manage_backups(path_backup_folder=target_backup_folder_local_path, backup_count=backup_count)

        # occassionally after upload, the new file will not be listed by gdrive's GetList() call immediately.
        # this causes the removal of the oldest backup by gdrive_manage_backups() to fail,
        # which then causes the newly uploaded file to be pruned by gdrive_housekeeping() since it wasnt in the old list.
        # to mitigate this, we record the original file list length before upload and wait for the new file to appear in the list after upload.
        gdrive_backup_count_original = len(gdrive_get_file_list(
            drive=drive, folder_id=target_backup_folder_gdrive_id, service_account_email=service_account_email
        ))

        # gdrive: upload
        logger.info(f"[{i + 1}/{count_instances}] Uploading backup {zip_file_path} to Google Drive.")
        gdrive_upload(
            drive=drive, path_to_file=zip_file_path, title=arc_name, folder_id=target_backup_folder_gdrive_id
        )
        logger.info(f"[{i + 1}/{count_instances}] Uploaded to Google Drive.")

        # gdrive: await upload detected
        upload_successful = False
        logger.info(f"[{i + 1}/{count_instances}] Awaiting upload detection in Google Drive.")
        for await_interval in GDRIVE_AWAIT_UPLOAD_DETECTED_INTERVALS:
            gdrive_backup_count_new = len(gdrive_get_file_list(
                drive=drive, folder_id=target_backup_folder_gdrive_id, service_account_email=service_account_email
            ))
            if gdrive_backup_count_new > gdrive_backup_count_original:
                upload_successful = True
                break
            else:
                logger.info(f"[{i + 1}/{count_instances}] Upload not yet detected, backing off for {await_interval} seconds.")
                time.sleep(await_interval)
        logger.info(f"[{i + 1}/{count_instances}] Upload found in Google Drive.")

        if not upload_successful:
            logger.critical(
                f"[{i + 1}/{count_instances}] Upload to Google Drive not detected after waiting for {GDRIVE_AWAIT_UPLOAD_DETECTED_INTERVALS} seconds.")
            raise RuntimeError(
                f"[{i + 1}/{count_instances}] Upload to Google Drive not detected after waiting for {GDRIVE_AWAIT_UPLOAD_DETECTED_INTERVALS} seconds."
            )

        # gdrive: prune old backups (keep only n most recent)
        logger.info(f"[{i + 1}/{count_instances}] Pruning backups in Google Drive.")
        ids_backup_list = gdrive_manage_backups(drive=drive, folder_id=target_backup_folder_gdrive_id,
                                                service_account_email=service_account_email, backup_count=backup_count)
        logger.info(f"[{i + 1}/{count_instances}] Pruned backups in Google Drive.")

        ids_to_not_housekeep.extend(ids_backup_list)

        if session_was_running:
            logger.info(f"[{i + 1}/{count_instances}] tmux session was running before backup, restarting server.")
            start.main(filter_instances=[instance_name])
            logger.info(f"[{i + 1}/{count_instances}] tmux session started.")

    # gdrive: housekeeping (delete files deleted by other users)
    logger.info(f"[{i + 1}/{count_instances}] Housekeeping files deleted by other users in Google Drive.")
    gdrive_housekeeping(
        drive=drive, service_account_email=service_account_email, ids_to_keep=ids_to_not_housekeep
    )
    logger.info(f"[{i + 1}/{count_instances}] Housekeeping complete.")

    about = drive.GetAbout()
    logger.info(
        f"""Storage: {int(about["quotaBytesUsed"]) / (1024 ** 3):.2f} GB \
of {int(about["quotaBytesTotal"]) / (1024 ** 3):.2f} GB used."""
    )

    logger.info(f"SCRIPT {__name__} FINISHED.")


def gdrive_auth(path_service_account_json):
    """
    Authenticate with Google Drive using a service account JSON file.
    Returns an object that can be used to interact with Google Drive.
    API reference: https://developers.google.com/drive/api/guides/ref-search-terms

    :param string path_service_account_json: Path to the service account JSON file.

    :return: GoogleDrive object.
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

    :return: None
    """

    file = drive.CreateFile({"title": title, "parents": [{"id": folder_id}]})
    file.SetContentFile(path_to_file)
    file.Upload()


def gdrive_get_file_list(drive, folder_id, service_account_email):
    """
    Get a list of files in a Google Drive folder owned by the service account.

    :param GoogleDrive drive: GoogleDrive object.
    :param string folder_id: ID of the Google Drive folder.
    :param string service_account_email: Email of the service account.

    :return: List of files in the folder owned by the service account.
    """

    query = {"q": f"\"{folder_id}\" in parents and '{service_account_email}' in owners and trashed=false"}
    file_list = drive.ListFile(query).GetList()

    return file_list


def gdrive_manage_backups(drive, folder_id, service_account_email, backup_count):
    """
    Remove oldest Google Drive backup if the number of backups exceeds the limit.

    :param GoogleDrive drive: GoogleDrive object.
    :param string folder_id: ID of the Google Drive folder where backups are stored.
    :param string service_account_email: Email of the service account.
    :param int backup_count: Number of backups to keep.

    :return: List of IDs of the backups that are kept.
    """

    file_list = gdrive_get_file_list(drive, folder_id, service_account_email)

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

    :return: None
    """

    query = {"q": f"'{service_account_email}' in owners"}
    file_list = drive.ListFile(query).GetList()

    for file in file_list:
        if file["id"] not in ids_to_keep:
            logger.info(f"""Deleting file {file["title"]}.""")
            file_to_delete = drive.CreateFile({"id": file["id"]})
            file_to_delete.Delete()
            logger.info(f"""Deleted file {file["title"]}.""")


def local_make_backup(path_source_folder, path_backup_folder, arc_name, backup_compression_level):
    """
    Create a backup of a folder.

    :param string path_source_folder: Path to the folder to backup.
    :param string path_backup_folder: Path to the folder where the backup will be stored.
    :param string arc_name: Name of the backup archive.
    :param int backup_compression_level: Compression level for the backup (0-9).

    :return: None
    """

    if backup_compression_level < 0:
        backup_compression_level = 0
    if backup_compression_level > 9:
        backup_compression_level = 9

    # pushd changes the current directory to the path stored in $world_path.
    # popd returns to the original directory that the script was in before the pushd command.
    # > /dev/null suppresses the output of the pushd/popd command to avoid cluttering the console.
    zip_file_path = f"{path_backup_folder}/{arc_name}"
    logger.info(f"Creating backup {zip_file_path} from source folder {path_source_folder}.")
    output, error = common_server_auto.run_command(
        f"pushd {path_source_folder} > /dev/null && zip -q -r -{backup_compression_level} {zip_file_path} . && popd > /dev/null"
    )
    logger.info(f"Backup created at {zip_file_path}, stdout: [{output}], stderr: [{error}]")


def local_manage_backups(path_backup_folder, backup_count):
    """
    Ensures that the number of local backups does not exceed the limit.

    :param string path_backup_folder: Path to the folder where backups are stored.
    :param int backup_count: Number of backups to keep.

    :return: None
    """

    # Remove oldest local backup if the number of backups exceeds the limit
    backup_list = sorted(Path(path_backup_folder).iterdir(), key=os.path.getmtime)
    if len(backup_list) > int(backup_count):
        local_filepath_to_remove = backup_list[0]
        logger.info(f"Removing oldest backup {local_filepath_to_remove}.")
        os.remove(local_filepath_to_remove)
        backup_list.remove(local_filepath_to_remove)
        logger.info(f"Removed oldest backup.")
    logger.info(f"Local backup count: {len(backup_list)}.")


if __name__ == "__main__":
    arg = [sys.argv[input_arg] for input_arg in range(1, len(sys.argv))] if len(sys.argv) > 1 else None
    main(arg)

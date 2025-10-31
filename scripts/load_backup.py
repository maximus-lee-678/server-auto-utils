import logging
import sys
import os
from pathlib import Path

import common_server_auto
import stop
import start

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main(restoring_instance_name, archive_name=None):
    """
    :param string restoring_instance_name: Name of the instance to restore.
    :param string/None archive_name: Name of the archive to restore from, or None to prompt user for input.
    """

    logger.info(f"SCRIPT {__name__} STARTED.")

    env_data = common_server_auto.get_env_json()
    if not env_data:
        return

    # verify specified instance exists
    if restoring_instance_name not in env_data["instances"]:
        logger.critical(f"Instance name '{restoring_instance_name}' not found in env.json.")
        return

    # details global to all instances
    force_shutdown_delay_seconds = int(env_data["force_shutdown_delay_seconds"])

    # details for one instance
    instance_details = env_data["instances"][restoring_instance_name]
    path_current_folder = instance_details["backup"]["path_folder_to_backup"]
    path_backup_folder = instance_details["backup"]["target_backup_folder_local_path"]
    tmux_session_name = instance_details["tmux_session_name"]

    full_path_restore_from = get_restore_point(path_backup_folder, archive_name)
    if not full_path_restore_from:
        logger.critical(f"Restore point not found, aborting restore operation.")
        return

    session_was_running = False
    if common_server_auto.check_for_tmux_session(tmux_session_name):
        session_was_running = True

    if session_was_running:
        logger.info(f"tmux session is running, stopping before running the restore.")
        stop.main(countdown_seconds=force_shutdown_delay_seconds, filter_instances=[restoring_instance_name])

    # Remove existing world folder
    logger.info(f"Removing existing world folder.")
    output, error = common_server_auto.run_command(f"rm -rf {path_current_folder}")
    logger.info(f"Existing world folder removed, stdout: [{output}], stderr: [{error}]")

    # Load backup
    logger.info(f"Loading backup from {full_path_restore_from}.")
    output, error = common_server_auto.run_command(f"unzip -q {full_path_restore_from} -d {path_current_folder}")
    logger.info(f"Backup restored, stdout: [{output}], stderr: [{error}]")

    if session_was_running:
        logger.info(f"tmux session was running before restore, restarting server.")
        start.main(filter_instances=[restoring_instance_name])
        logger.info(f"tmux session started.")

    logger.info(f"SCRIPT {__name__} FINISHED.")


def get_restore_point(path_backup_folder, restore_from_arg):
    """
    If restore_from_arg is provided, ascertain the path to the restore point.
    If restore_from_arg is not provided, prompt the user for input to ascertain the path to the restore point.
    Returns the absolute path to the restore point, or None if the restore point is not found.

    :param string path_backup_folder: Path to the backup folder.
    :param string/None restore_from_arg: Name of the archive to restore from, or None if not provided.

    :return: Absolute Path to the restore point, or None if the restore point is not found.
    """

    restore_from = None

    # no restore_from argument provided, prompt user for input
    if not restore_from_arg:
        logger.info("No restore_from argument provided, prompting user for input.")
        restore_from = input("Enter the exact name of the archive in the backup folder to restore from (leave blank for most-recent): ")
    else:
        logger.info(f"User provided restore_from argument: {restore_from_arg}")
        restore_from = restore_from_arg

    # no restore_from path provided by user, use most recent backup
    if not restore_from.strip():
        logger.info("User specified to use most recent backup.")
        backup_list = sorted(Path(path_backup_folder).iterdir(), key=os.path.getmtime, reverse=True)
        if not backup_list:
            logger.error(f"No backups found in backup folder.")
            return None

        restore_from = backup_list[0]
    # user specified an archive name to restore from
    else:
        if not Path(f"{path_backup_folder}/{restore_from}").exists():
            logger.error(f"User-specified archive {restore_from} not found in backup folder.")
            return None

        restore_from = f"{path_backup_folder}/{restore_from}"

    logger.info(f"Archive found at: {restore_from}")
    return restore_from


if __name__ == "__main__":
    args = []
    if len(sys.argv) == 1:
        raise RuntimeError("No instance name provided.")
    if len(sys.argv) > 1:
        args.append(sys.argv[1])
    if len(sys.argv) > 2:
        args.append(sys.argv[2])
    if len(sys.argv) > 3:
        raise RuntimeError("Too many arguments provided.")

    main(*args)

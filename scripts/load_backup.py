import logging
import sys
import os
import time
from pathlib import Path

import common_server_auto, stop, start

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


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


def main(restore_from=None):
    dict_dotenv = common_server_auto.get_dotenv()
    if not dict_dotenv:
        logger.error(common_server_auto.LOGGER_FAILED_TO_READ_ENV_MSG)
        return

    path_utils_location = dict_dotenv["PATH_UTILS_LOCATION"]
    path_server_folder = dict_dotenv["PATH_SERVER_FOLDER"]
    path_backup_folder = dict_dotenv["PATH_BACKUP_FOLDER"]
    tmux_session_name = dict_dotenv["TMUX_SESSION_NAME"]
    force_shutdown_delay_seconds = int(dict_dotenv["FORCE_SHUTDOWN_DELAY_SECONDS"])

    full_path_restore_from = get_restore_point(path_backup_folder, restore_from)

    session_was_running = False
    if common_server_auto.check_for_tmux_session(tmux_session_name):
        session_was_running = True

    if session_was_running:
        logger.info(f"tmux session is running, stopping before running the restore.")
        common_server_auto.send_tmux_input(
            tmux_session_name, "/say A Manual restore has been triggered, the server will shutdown in 3 seconds."
        )
        stop.stop(force_shutdown_delay_seconds)

        # wait for tmux session to actually close
        while 1:
            if not common_server_auto.check_for_tmux_session(tmux_session_name):
                break
            time.sleep(1)

        logger.info(f"tmux session stopped.")

    # Remove existing world folder
    logger.info(f"Removing existing world folder.")
    output, error = common_server_auto.run_command(f"rm -rf {path_server_folder}/world")
    logger.info(f"Existing world folder removed, stdout: [{output}], stderr: [{error}]")

    # Load backup
    logger.info(f"Loading backup from {full_path_restore_from}.")
    output, error = common_server_auto.run_command(f"unzip -q {full_path_restore_from} -d {path_server_folder}/world")
    logger.info(f"Backup restored, stdout: [{output}], stderr: [{error}]")

    if session_was_running:
        logger.info(f"tmux session was running before restore, restarting server.")
        start.start()
        logger.info(f"tmux session started.")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)

import common_server_auto, start
from pathlib import Path
import os


def main():
    logger = common_server_auto.start_logger(os.path.basename(__file__))

    dict_dotenv = common_server_auto.get_dotenv()
    if not dict_dotenv:
        logger.error(common_server_auto.LOGGER_FAILED_TO_READ_ENV_MSG)
        return

    path_utils_location = dict_dotenv["PATH_UTILS_LOCATION"]
    reboot_temp_file_ind = dict_dotenv["REBOOT_TEMP_FILE_IND"]

    common_server_auto.add_file_logger(os.path.basename(__file__), path_utils_location)

    local_filepath_to_check = Path(f"{path_utils_location}/{reboot_temp_file_ind}")
    if not local_filepath_to_check.exists():
        logger.info(f"No {reboot_temp_file_ind} file found, skipping post-startup server restart.")
        return
    
    logger.info(f"{reboot_temp_file_ind} file found, restarting server.")
    start.start()
    logger.info(f"tmux session started.")

    Path(local_filepath_to_check).unlink()
    logger.info(f"Removed {reboot_temp_file_ind} file.")

    logger.info("Server restart complete.")


if __name__ == "__main__":
    main()
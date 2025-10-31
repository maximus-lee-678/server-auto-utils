import logging
from pathlib import Path

import common_server_auto
import start

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main():
    logger.info(f"SCRIPT {__name__} STARTED.")

    env_data = common_server_auto.get_env_json()
    if not env_data:
        return

    # details global to all instances
    path_utils_location = env_data["path_utils_location"]
    reboot_temp_file = env_data["reboot_temp_file"]

    local_filepath_to_check = Path(f"""{path_utils_location}/{reboot_temp_file}""")
    if not local_filepath_to_check.exists():
        logger.info(f"No {reboot_temp_file} file found, skipping post-startup server restart(s).")
        return

    logger.info(f"{reboot_temp_file} file found, restarting server(s).")
    start.main()
    logger.info(f"tmux session(s) started.")

    Path(local_filepath_to_check).unlink()
    logger.info(f"Removed {reboot_temp_file} file.")

    logger.info(f"SCRIPT {__name__} FINISHED.")


if __name__ == "__main__":
    main()

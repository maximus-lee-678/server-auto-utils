import os
import logging

import common_server_auto

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main():
    dict_dotenv = common_server_auto.get_dotenv()
    if not dict_dotenv:
        logger.error(common_server_auto.LOGGER_FAILED_TO_READ_ENV_MSG)
        return

    path_utils_location = dict_dotenv["PATH_UTILS_LOCATION"]
    path_server_folder = dict_dotenv["PATH_SERVER_FOLDER"]
    tmux_session_name = dict_dotenv["TMUX_SESSION_NAME"]
    startup_command = dict_dotenv["STARTUP_COMMAND"]

    if common_server_auto.check_for_tmux_session(tmux_session_name):
        logger.info(f"tmux session is already running, skipping server start.")
        return

    logger.info(f"Starting server.")
    output, error = common_server_auto.run_command(
        f"cd {path_server_folder} && tmux new-session -d -s {tmux_session_name} '{startup_command}'"
    )
    logger.info("Server startup command invoked.")


def start():
    """
    Calls the main function. For use by other scripts.
    """

    main()


if __name__ == "__main__":
    main()

import time
import sys
import os
import logging

import common_server_auto

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)

SHUTDOWN_MESSAGE = "/say Server will shutdown in {0}m{1}s."
FINAL_SHUTDOWN_MESSAGE = "/say Server will now shutdown!"
DEFAULT_STOP_COMMAND = "/stop"


def main(countdown_seconds=None):
    dict_dotenv = common_server_auto.get_dotenv()
    if not dict_dotenv:
        logger.error(common_server_auto.LOGGER_FAILED_TO_READ_ENV_MSG)
        return

    path_utils_location = dict_dotenv["PATH_UTILS_LOCATION"]
    tmux_session_name = dict_dotenv["TMUX_SESSION_NAME"]

    shutdown_delay_seconds = int(dict_dotenv["SHUTDOWN_DELAY_SECONDS"]) if not countdown_seconds else countdown_seconds

    if not common_server_auto.check_for_tmux_session(tmux_session_name):
        logger.info(f"tmux session not found, assuming server already stopped.")
        return

    logger.info(f"Stopping server in {shutdown_delay_seconds} seconds.")
    tmux_send_shutdown_countdown(tmux_session_name, shutdown_delay_seconds)
    time.sleep(1)
    common_server_auto.send_tmux_input(tmux_session_name, FINAL_SHUTDOWN_MESSAGE)
    common_server_auto.send_tmux_input(tmux_session_name, DEFAULT_STOP_COMMAND)

    # wait for tmux session to actually close
    while 1:
        if not common_server_auto.check_for_tmux_session(tmux_session_name):
            break
        time.sleep(1)

    logger.info("Server stopped.")


def tmux_send_shutdown_countdown(tmux_session_name, seconds):
    """
    Sends shutdown messages to the specified tmux session.
    After an initial message is sent containing exact time to shutdown, has 4 modes of messaging frequency:
    - If time left is more than 10 minutes, notify at the 10 minute mark.
    - If time left is more than 1 minute, notify every minute.
    - If time left is more than 10 seconds, notify every 10 seconds.
    - If time left is less than 10 seconds, notify every second.

    :param string tmux_session_name: Name of the tmux session.
    :param int seconds: Number of seconds to wait before shutting down.
    """

    common_server_auto.send_tmux_input(tmux_session_name, SHUTDOWN_MESSAGE.format(seconds // 60, seconds % 60))

    while seconds > 0:
        seconds_to_sleep = 0

        # if time left is more than 10 minutes, sleep until 10 minutes
        if seconds > 600:
            seconds_to_sleep = seconds - 600
        # if time left is more than 1 minute, notify every minute
        elif seconds > 60:
            seconds_to_sleep = 60 if seconds % 60 == 0 else seconds % 60
        # if time left is more than 10 seconds, notify every 10 seconds
        elif seconds > 10:
            seconds_to_sleep = 10 if seconds % 10 == 0 else seconds % 10
        # if time left is less than 10 seconds, notify every second
        else:
            seconds_to_sleep = 1

        time.sleep(seconds_to_sleep)
        seconds -= seconds_to_sleep
        common_server_auto.send_tmux_input(tmux_session_name, SHUTDOWN_MESSAGE.format(seconds // 60, seconds % 60))


def stop(countdown_seconds=None):
    """
    Calls the main function. For use by other scripts.

    :param int/None countdown_seconds: Number of seconds to wait before stopping the server, or None to use the default.
    """

    main(countdown_seconds)


if __name__ == "__main__":
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(arg)

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import os
import subprocess
import logging

# List of environment variables that are expected to be set in the .env file.
EXPECTED_ENV_VARS = [
    "GDRIVE_BACKUP_FOLDER_ID",
    "PATH_UTILS_LOCATION",
    "SERVICE_ACCOUNT_JSON_NAME",
    "PATH_SERVER_FOLDER",
    "PATH_BACKUP_FOLDER",
    "BACKUP_COUNT",
    "BACKUP_COMPRESSION_LEVEL",
    "TMUX_SESSION_NAME",
    "STARTUP_COMMAND",
    "SHUTDOWN_DELAY_SECONDS",
    "FORCE_SHUTDOWN_DELAY_SECONDS",
    "REBOOT_TEMP_FILE_IND"
]
LOGGER_FAILED_TO_READ_ENV_MSG = "Failed to read .env file."
DIR_NAME_LOGS = "logs"
LOG_FORMAT = "[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s"

logger = None

def start_logger(script_name):
    """
    Starts a logger for a script.

    :param script_name: name of the script to log for. usually passed in as os.path.basename(__file__).

    :return: logger object.
    """

    logger = logging.getLogger(script_name)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)

    logger.propagate = False

    return logger


def add_file_logger(script_name, path_utils_location):
    """
    Adds a file logger to the logger object. 
    In order to log to a file, the logger must first be created with start_logger().

    :param script_name: name of the script to log for. usually passed in as os.path.basename(__file__).
    :param path_utils_location: path to the utils folder. used to determine where to store logs.
    """

    logger = logging.getLogger(script_name)
    if any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        return

    log_directory = Path(f"{path_utils_location}/{DIR_NAME_LOGS}")
    log_filename = Path(f"{log_directory}/{datetime.now().strftime('%Y-%m-%d')}.log")
    log_directory.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def _get_common_logger(path_utils_location):
    """
    Internal function to get a logger for use specifically by this script. Updates the global logger variable.
    Since this logger may be used before log file locations are set, it may not log to a file. If so, it will log this information to the stdout logger.

    :param path_utils_location: path to the utils folder. used to determine where to store logs.
    """

    global logger
    logger = start_logger(os.path.basename(__file__))

    if path_utils_location:
        add_file_logger(os.path.basename(__file__), path_utils_location)
    else:
        logger.error("path_utils_location not set, cannot log to file.")


def run_command(command):
    """
    Run a command in the shell and return the stdout and stderr.

    :param command: the command to run.

    :return: tuple of stdout and stderr.
    """
    # Open a subprocess to run the command
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # wait for the process to complete, capture outputs
    stdout, stderr = process.communicate()
    return stdout, stderr


def get_dotenv(dotenv_path=None):
    """
    Ascertain the existence of the .env file and all required environment variables.
    If any are missing, log an error containing which environment variables have not been set and return None.

    :param dotenv_path: path to the .env file. Defaults to "./.env".

    :return: dictionary of environment variables if all are initialised, None otherwise.
    """

    global logger
    dotenv_path = dotenv_path or "./.env"

    if not Path(dotenv_path).exists():
        # log to root logger, can't find anywhere to log to
        logging.error("No .env file found, please configure one using provided .env.example.")
        return None

    load_dotenv()

    if not logger:
        _get_common_logger(os.getenv("PATH_UTILS_LOCATION"))

    uninitialised_env_values = [var for var in EXPECTED_ENV_VARS if not os.getenv(var)]

    if uninitialised_env_values:
        logger.error(f"""Uninitialised environment variables: {", ".join(uninitialised_env_values)}""")
        return None
    else:
        logger.info("All environment variables initialised.")
        return {var: os.getenv(var) for var in EXPECTED_ENV_VARS}


def check_for_tmux_session(session_name):
    """
    Check if a tmux session exists with the given name.
    Keep in mind that this function can only check for sessions started by the user that ran the script.

    :param session_name: name of the tmux session to check for.

    :return: True if the session exists, False otherwise.
    """

    output, error = run_command(f"tmux list-session -F \"#S\" 2> /dev/null | grep \"^{session_name}$\"")

    return output.strip() == session_name


def send_tmux_input(session_name, input):
    """
    Sends input to a tmux session.
    Keep in mind that this function can only access sessions started by the user that ran the script.

    :param session_name: name of the tmux session to send input to.

    :param input: input to send to the tmux session.
    """

    run_command(f"tmux send-keys -t {session_name} \"{input}\" Enter")

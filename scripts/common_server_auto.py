from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

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

LOG_DIRECTORY = Path("logs")
LOG_NAME = Path(f"""{LOG_DIRECTORY}/{datetime.now().strftime('%Y-%m-%d')}.log""")
LOG_FORMAT = "[%(asctime)s] [%(filename)s/%(levelname)s]: %(message)s"


def setup_logger(write_to_file=True):
    """
    Setup a simple logger.

    :param write_to_file: whether to write logs to file.

    :return: logger object.
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Clear existing handlers to avoid duplicates
    if getattr(root_logger, "_is_configured", False):
        return root_logger

    # Normal single-process logging setup (multithreading logging is thread-safe)
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if write_to_file:
        LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_NAME, "a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    root_logger._is_configured = True

    return root_logger


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

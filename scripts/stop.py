import time
import sys
import logging
import threading

import common_server_auto

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main(countdown_seconds=None, filter_instances=None):
    """
    :param int/None countdown_seconds: Number of seconds to wait before stopping the server, or None to use the default.
    :param list/None filter_instances: List of instance names to stop, or None to stop all instances available in configuration file.
    """

    logger.info(f"SCRIPT {__name__} STARTED.")

    env_data = common_server_auto.get_env_json()
    if not env_data:
        return

    if filter_instances:
        instances = filter_instances
        logger.info(f"""Filtering to stop only instances: {instances}""")

        # verify specified instance(s) exists
        for instance_name in instances:
            if instance_name not in env_data["instances"]:
                logger.critical(f"Instance name '{instance_name}' not found in env.json.")
                return
    else:
        instances = list(env_data["instances"].keys())
        logger.info(f"""Stopping all instances: {instances}""")

    # details global to all instances
    shutdown_delay_seconds = int(env_data["routine_shutdown_delay_seconds"]) if not countdown_seconds else countdown_seconds

    threads = []
    active_tmux_sessions = []

    # loop through instances to stop
    count_instances = len(instances)
    for i, instance_name in enumerate(instances):
        # details for each instance
        instance_details = env_data["instances"][instance_name]
        tmux_session_name = instance_details["tmux_session_name"]
        command_shutdown_warning = instance_details["shutdown_commands"]["timed_warn"]
        command_shutdown_imminent = instance_details["shutdown_commands"]["timed_imminent"]
        command_shutdown_execute = instance_details["shutdown_commands"]["execute"]

        logger.info(f"[{i + 1}/{count_instances}] Starting shutdown sequence for '{instance_name}'.")

        if not common_server_auto.check_for_tmux_session(tmux_session_name):
            logger.info(f"[{i + 1}/{count_instances}] tmux session not found, assuming server already stopped.")
        else:
            active_tmux_sessions.append(tmux_session_name)

            # Threaded shutdown
            thread = threading.Thread(
                target=shutdown_sequence,
                args=(
                    logger, instance_name, tmux_session_name, command_shutdown_warning, command_shutdown_imminent,
                    command_shutdown_execute, shutdown_delay_seconds
                )
            )
            thread.start()
            threads.append(thread)
            logger.info(f"[{i + 1}/{count_instances}] Shutdown thread started for '{instance_name}'.")

        logger.info(f"[{i + 1}/{count_instances}] Finished shutdown sequence for '{instance_name}'.")

    logger.info(f"Waiting for all shutdown sequences to complete.")

    # wait for all threads to complete
    for thread in threads:
        thread.join()
    logger.info(f"All shutdown sequences completed.")

    # wait for all tmux sessions to actually close
    while active_tmux_sessions:
        logger.info(f"Current tmux sessions still active: {len(active_tmux_sessions)}")
        for tmux_session_name in active_tmux_sessions[:]:
            if not common_server_auto.check_for_tmux_session(tmux_session_name):
                active_tmux_sessions.remove(tmux_session_name)
        time.sleep(1)

    logger.info(f"SCRIPT {__name__} FINISHED.")


def tmux_send_shutdown_countdown(tmux_session_name, seconds, shutdown_message):
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

    common_server_auto.send_tmux_input(tmux_session_name, shutdown_message.format(seconds // 60, seconds % 60))

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
        common_server_auto.send_tmux_input(tmux_session_name, shutdown_message.format(seconds // 60, seconds % 60))


def shutdown_sequence(
        logger, instance_name, tmux_session_name, command_shutdown_warning, command_shutdown_imminent, command_shutdown_execute,
        shutdown_delay_seconds
):
    """Thread worker function to perform the shutdown sequence."""

    logger.info(f"Stopping server '{instance_name}' in {shutdown_delay_seconds} seconds.")

    tmux_send_shutdown_countdown(tmux_session_name, shutdown_delay_seconds, command_shutdown_warning)  # long running function
    time.sleep(1)
    common_server_auto.send_tmux_input(tmux_session_name, command_shutdown_imminent)
    common_server_auto.send_tmux_input(tmux_session_name, command_shutdown_execute)


if __name__ == "__main__":
    countdown_seconds = None
    filter_instances = []

    if len(sys.argv) > 1:
        try:
            countdown_seconds = int(sys.argv[1])
        except ValueError:
            logger.critical(f"Invalid countdown_seconds argument provided: {sys.argv[1]}")
            sys.exit(1)
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            filter_instances.append(arg)

    main(countdown_seconds, filter_instances if filter_instances else None)

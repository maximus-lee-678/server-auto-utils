import sys
import logging

import common_server_auto

common_server_auto.setup_logger()
logger = logging.getLogger(__name__)


def main(filter_instances=None):
    """
    :param list/None filter_instances: List of instance names to start, or None to start all instances available in configuration file.
    """

    logger.info(f"SCRIPT {__name__} STARTED.")

    env_data = common_server_auto.get_env_json()
    if not env_data:
        return

    if filter_instances:
        instances = filter_instances
        logger.info(f"""Filtering to start only instances: {instances}""")

        # verify specified instance(s) exists
        for instance_name in instances:
            if instance_name not in env_data["instances"]:
                logger.critical(f"Instance name '{instance_name}' not found in env.json.")
                return
    else:
        instances = env_data["instances"].keys()
        logger.info(f"""Starting all instances: {instances}""")

    # loop through instances to start
    count_instances = len(instances)
    for i, instance_name in enumerate(instances):
        # details for each instance
        instance_details = env_data["instances"][instance_name]
        tmux_session_name = instance_details["tmux_session_name"]
        startup_command = instance_details["startup_command"]
        path_server_folder = instance_details["path_server_folder"]

        logger.info(f"""[{i + 1}/{count_instances}] Starting launch sequence for '{instance_name}'.""")

        if common_server_auto.check_for_tmux_session(tmux_session_name):
            logger.info(f"[{i + 1}/{count_instances}] tmux session is already running, skipping server launch.")
        else:
            logger.info(f"[{i + 1}/{count_instances}] Starting server.")
            output, error = common_server_auto.run_command(
                f"cd {path_server_folder} && tmux new-session -d -s {tmux_session_name} '{startup_command}'"
            )
            logger.info(f"[{i + 1}/{count_instances}] Server startup command invoked.")

        logger.info(f"[{i + 1}/{count_instances}] Finished launch sequence for '{instance_name}'.")

    logger.info(f"SCRIPT {__name__} FINISHED.")


if __name__ == "__main__":
    args = sys.argv[1:]

    main(filter_instances=args if args else None)

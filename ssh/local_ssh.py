import sys
import subprocess
import time
import logging.config

logger = logging.getLogger(__name__)


def execute_shell(shell_cmd, error_msg):
    try:
        subprocess.check_call(shell_cmd, shell=True)

    except subprocess.CalledProcessError:
        logger.error(error_msg)
        sys.exit(1)


def execute_shell_retry(shell_cmd, error_msg, retry_count):
    count = 0
    while count < retry_count:
        try:
            subprocess.check_call(shell_cmd, shell=True)
            break

        except subprocess.CalledProcessError:
            count += 1
            logger.error(error_msg)
            logger.info("run command \" %s \" exception, retrying %d", shell_cmd, count)
            if count == retry_count:
                sys.exit(1)
            time.sleep(5)


def execute_shell_return(shell_cmd, error_msg):
    try:
        subprocess.check_call(shell_cmd, shell=True)

    except subprocess.CalledProcessError:
        logger.warning(error_msg)
        return False

    return True

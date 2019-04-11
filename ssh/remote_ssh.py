import os
import sys
import paramiko
import socket
import logging.config

logger = logging.getLogger(__name__)


def ipv4_address_validation(ipv4_addr):
    try:
        socket.inet_aton(ipv4_addr)
        ret = True

    except socket.error:
        ret = False
        logger.error("{0} is not a correct ipv4 address!".format(ipv4_addr))

    return ret


def port_validation(port):
    if str(port).isdigit() is True and 0 <= int(port) <= 65535:
        ret = True

    else:
        ret = False
        logger.error("{0} is not a correct port. A port can only contain digits!".format(str(port)))

    return ret


# Support command with sudo? : No
# Could you get the command result as the return value? : No
def ssh_shell_paramiko(host_config, commandline):
    result_stdout, result_stderr = ssh_shell_paramiko_with_result(host_config, commandline)

    if result_stdout is None or result_stderr is None:
        return False

    return True


# Support command with sudo? : No
# Could you get the command result as the return value? : Yes
def ssh_shell_paramiko_with_result(host_config, commandline):
    hostip = str(host_config['hostip'])
    if not ipv4_address_validation(hostip):
        return False

    username = str(host_config['username'])
    password = str(host_config['password'])
    port = 22

    if 'sshport' in host_config:
        if not port_validation(host_config['sshport']):
            return None, None
        port = int(host_config['sshport'])

    key_filename = None

    if 'keyfile-path' in host_config and host_config['keyfile-path'] is not None:
        if os.path.isfile(str(host_config['keyfile-path'])):
            key_filename = str(host_config['keyfile-path'])
        else:
            logger.warn("The key file: {0} specified doesn't exist".format(host_config['keyfile-path']))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostip, port=port, key_filename=key_filename, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(commandline, get_pty=True)
    logger.info("Executing the command on host [{0}]: {1}".format(hostip, commandline))
    result_stdout = ""

    for response_msg in stdout:
        result_stdout += response_msg
        print(response_msg.encode('utf-8').strip('\n'))

    result_stderr = ""

    for response_msg in stderr:
        result_stderr += response_msg

    exit_code_ssh = stdout.channel.recv_exit_status()

    if exit_code_ssh != 0:
        sys.exit(exit_code_ssh)

    ssh.close()
    return result_stdout, result_stderr


# Support command with sudo? : Yes
# Could you get the command result as the return value? : No
def ssh_shell_with_password_input_paramiko(host_config, commandline):
    hostip = str(host_config['hostip'])

    if not ipv4_address_validation(hostip):
        return False

    username = str(host_config['username'])
    password = str(host_config['password'])
    port = 22

    if 'sshport' in host_config:
        if not port_validation(host_config['sshport']):
            return False
        port = int(host_config['sshport'])

    key_filename = None

    if 'keyfile-path' in host_config:
        if os.path.isfile(str(host_config['keyfile-path'])) and host_config['keyfile-path'] is not None:
            key_filename = str(host_config['keyfile-path'])
        else:
            logger.warn("The key file: {0} specified doesn't exist".format(host_config['keyfile-path']))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostip, port=port, key_filename=key_filename, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(commandline, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    logger.info("Executing the command on host [{0}]: {1}".format(hostip, commandline))

    for response_msg in stdout:
        print(response_msg.encode('utf-8').strip('\n'))

    exit_code_ssh = stdout.channel.recv_exit_status()

    if exit_code_ssh != 0:
        sys.exit(exit_code_ssh)

    ssh.close()
    return True

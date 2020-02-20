#!/usr/bin/env python3

import paramiko
import argparse
from multiprocessing import Pool


parser = argparse.ArgumentParser(description='Hosts and command')
parser.add_argument('-u', dest='user', help='Username', required=True)
parser.add_argument('-p', dest='password', help='Password', required=True)
parser.add_argument('-H', dest='hosts', help='Host Ip adresses', required=True)
parser.add_argument('-c', dest='command', help='Command to execute', required=True)
args = parser.parse_args()
user = args.user
secret = args.password
host = args.hosts.split(':')
cmd = args.command



def ssh_conn(host):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=22)
        
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        stdout_output = stdout.read().decode('utf8').rstrip('\n')
        stderr_output = stderr.read().decode('utf8').rstrip('\n')
        client.close()
        if exit_status == 0:
            print(host + ": " + stdout_output)
        else:
            print(f'---ERROR--- Exit status: {exit_status}')
            print(host + ": " + stderr_output)
    except (
        Exception,
        paramiko.BadHostKeyException,
        paramiko.AuthenticationException,
        paramiko.SSHException,
    ) as e:
        print("Cannot connect to host: " + host)
        print(e)


with Pool() as pool:
    result = pool.map(ssh_conn, host)

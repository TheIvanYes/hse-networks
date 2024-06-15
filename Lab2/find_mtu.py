#!/usr/bin/env python3

import argparse
import platform
import subprocess

ICMP_PLUS_IP_HEADERS_SIZE = 28


def send_ping(host, mtu):
    command = None
    system = platform.system().lower()


    if system == 'darwin':
        command = f'ping -c 1 {host} -s {mtu} -D    -W 2000' # 2 sec timeout
    elif system == 'windows':
        command = f'ping -n 1 {host} -s {mtu} -M do -W 2'
    else: ## linux
        command = f'ping -c 1 {host} -s {mtu} -M do -W 2'

    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True) == 0


def find_mtu(host):
    if not send_ping(host, 0):
        print(f"Host {host} is unavailable")
        exit(0)

    l = 0
    r = 1501 - ICMP_PLUS_IP_HEADERS_SIZE

    while r - l > 1:
        m = (l + r) // 2

        print(f'send ping (size={m})')

        if send_ping(host, m):
            l = m
        else:
            r = m

    return l + ICMP_PLUS_IP_HEADERS_SIZE


def main():
    parser = argparse.ArgumentParser(description='MTU finder')
    parser.add_argument(
        '--host',
        required=True,
        help='host for which minimal MTU is being searched'
    )
    args = parser.parse_args()

    min_mtu = find_mtu(args.host)
    print(f"result: {min_mtu}")


if __name__ == '__main__':
    main()

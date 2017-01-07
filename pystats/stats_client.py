#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import time
import os
import random


class UDPClient(object):
    def __init__(self, server_ip, server_port):
        """Initalize client"""
        self.server_ip = server_ip
        self.server_port = server_port

        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

    def send_msg(self, msg):
        """Send message"""
        self.sock.sendto(msg, (self.server_ip, self.server_port))


def main():
    """MAIN"""
    remote_addr = os.environ.get("STATSD_REMOTE_ADDRESS", 'localhost')

    # <TODO>: exception catch.
    remote_port = int(os.environ.get("STATSD_REMOTE_PORT", 5090))

    client = UDPClient(remote_addr, remote_port)

    msgs = []

    msg = '{"metric_name": "cfbroker.app_trace", \
    "metric_type": "counter", "count": "1"}'
    msg1 = '{"metric_name": "cfbroker.trace", "metric_type": "trace", \
    "username": "behzad_dastur", "stage": "initialize"}'
    msg2 = '{"metric_name": "cfbroker.trace", "metric_type": "trace", \
    "username": "behzad_dastur", "stage": "error"}'
    msgs.append(msg)
    msgs.append(msg1)
    msgs.append(msg2)

    for count in range(0, 1000):
        if count % 50 == 0:
            time.sleep(1)

        msg = msgs[random.randrange(3)]
        client.send_msg(msg)


if __name__ == '__main__':
    main()

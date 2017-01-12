#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import json
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



    msg_counter = {
        "metric_name": "cfbroker.app_trace",
        "metric_type": "counter",
        "count": 1,
        "username": "behzad_dastur",
        "stage": "success"
    }

    msg_trace_1 = {
        "metric_name": "cfbroker.trace",
        "metric_type": "trace",
        "username": "behzad_dastur",
        "stage": "initialize"
    }
    msg_trace_2 = {
        "metric_name": "cfbroker.trace",
        "metric_type": "trace",
        "username": "behzad_dastur",
        "stage": "error"
    }

    msg_guage = {
        "metric_name": "cfbroker.latency",
        "metric_type": "guage",
        "value": 43,
        "username": "behzad_dastur",
        "stage": "success"
    }

    msgs.append(msg_counter)
    msgs.append(msg_trace_1)
    msgs.append(msg_trace_2)
    msgs.append(msg_guage)

    for count in range(0, 1000):
        if count % 50 == 0:
            time.sleep(1)
        idx = random.randrange(4)
        msg = msgs[idx]
        if 'value' in msg.keys():
            msg['value'] = random.randrange(40)

        jdata = json.dumps(msg)
        client.send_msg(jdata)


if __name__ == '__main__':
    main()

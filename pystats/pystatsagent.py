#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import pystat_config

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

class TraceAgent(object):
    def __init__(self):
        self.cfg = pystat_config.PyStatConfig()
        self.remote_addr = self.cfg.parsedyaml.get('bind_address', 'localhost')
        self.remote_port = self.cfg.parsedyaml.get('bind_port', 5090)
        self.host = socket.gethostname()
        self.udpclient = UDPClient(self.remote_addr, self.remote_port)

    def trace(self, metric_name, trace_info):
        msg = trace_info
        msg['metric_name'] = metric_name
        msg['metric_type'] = "trace"
        msg['host'] = self.host
        jdata = json.dumps(msg)
        self.udpclient.send_msg(jdata)

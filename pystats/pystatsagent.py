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


class PystatAgent(object):
    def __init__(self):
        self.cfg = pystat_config.PyStatConfig()
        if self.cfg.parsedyaml is not None:
            self.remote_addr = self.cfg.parsedyaml.get('bind_address',
                                                       'localhost')
            self.remote_port = self.cfg.parsedyaml.get('bind_port', 5090)
        else:
            self.remote_addr = 'localhost'
            self.remote_port = 5090

        self.host = socket.gethostname()
        self.udpclient = UDPClient(self.remote_addr, self.remote_port)

    def trace(self, metric_name, trace_info):
        data = self.format_msg_data(metric_name, 'trace', trace_info, None)
        self.udpclient.send_msg(data)

    def guage(self, metric_name, value, trace_info):
        data = self.format_msg_data(metric_name, 'guage', trace_info, value)
        self.udpclient.send_msg(data)

    def format_msg_data(self, metric_name, metric_type, trace_info, value):
        msg = trace_info
        msg['metric_name'] = metric_name
        msg['metric_type'] = metric_type
        msg['host'] = self.host

        # Attach additional user provided tags to the msg.
        if self.cfg.parsedyaml is not None and \
            self.cfg.parsedyaml.get('agent', None) is not None:
            agent_tags = self.cfg.parsedyaml['agent'].get('tags', None)
            if agent_tags is not None:
                for tag in agent_tags:
                    msg[tag] = agent_tags[tag]

        if metric_type == "guage":
            msg['value'] = value

        jdata = json.dumps(msg)
        return jdata

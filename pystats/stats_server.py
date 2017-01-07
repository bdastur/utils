#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stats Server:

Default Bind IP: localhost
Default Bind Port: 5090

metric data should be be a json string.
Mandator keys:
'metric_name'
'metric_type'

For Metric type counter:
   mandator key: 'count'

"""
import sys
import os
import signal
import socket
import json
import multiprocessing


class CounterMetric(object):
    def __init__(self, jdata):
        self.metric_name = jdata['metric_name']
        self.metric_type = jdata['metric_type']
        self.metric_counter = 1

    def update_metric(self, jdata):
        self.metric_counter += int(jdata['count'])

    def display_metric_info(self):
        print "Name: %s, Type: %s, Counter: %d " % \
         (self.metric_name, self.metric_type, self.metric_counter)


class MetricsManager(object):
    METRIC_TYPES = {
    'counter': 'CounterMetric',
    'trace': 'TraceMetric'
    }

    def __init__(self):
        self.metrics = {}

    def init_metric(self, jdata):
        metric_name = jdata['metric_name']
        metric_type = jdata['metric_type']
        # if jdata['metric_type'] == "counter":
        #     self.metrics[metric_name] = Metric(jdata)
        print "sys modules: ", sys.modules.keys()

        metric_cls = getattr(sys.modules['__main__'],
                      MetricsManager.METRIC_TYPES[metric_type])
        print "metric cls: ", metric_cls
        self.metrics[metric_name] = metric_cls(jdata)

    def add_metric(self, jdata):
        metric_name = jdata['metric_name']
        if self.metrics.get(metric_name, None) is None:
            self.init_metric(jdata)
        else:
            self.metrics[metric_name].update_metric(jdata)

    def display_metric_info(self, jdata):
        metric_name = jdata['metric_name']
        if self.metrics.get(metric_name, None) is not None:
            self.metrics[metric_name].display_metric_info()


class UDPServer(object):
    """
    Stats UDP Server.
    """

    BUFSIZE = 1024

    def __init__(self, bind_ip, bind_port):
        """Initalize UDPServer"""
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((self.bind_ip, self.bind_port))

    def start_listener(self):
        """Listener"""
        metricsm = MetricsManager()

        while True:
            try:
                data, addr = self.sock.recvfrom(UDPServer.BUFSIZE)
            except KeyboardInterrupt:
                print "KeyboardInterrupt: Terminate Server!"
                sys.exit()
            print "Data: ", data
            try:
                jdata = json.loads(data)
            except ValueError:
                print "Data is not correct json string"
                continue

            metricsm.add_metric(jdata)

            metricsm.display_metric_info(jdata)


class StatsServer(object):
    def __init__(self):
        self.bind_ip = os.environ.get('STATSD_BIND_ADDRESS', 'localhost')

        # TODO: catch exception
        self.bind_port = int(os.environ.get('STATSD_BIND_PORT', 5090))

        self.udpworker = None

        # Handle Keyboard Interrupt
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        print "Signal caught: ", signum
        self.udpworker.terminate()
        print "UDP Server Terminated!"

    def udpserver_initiate(self):
        self.udpserver = UDPServer(self.bind_ip, self.bind_port)
        self.udpserver.start_listener()

    def run(self):
        self.udpworker = multiprocessing.Process(target=self.udpserver_initiate)
        self.udpworker.start()
        print "UDP Server Started!"



def main():
    """Main Function"""
    statserver = StatsServer()
    statserver.run()


if __name__ == '__main__':
    main()

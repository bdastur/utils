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
import time
import signal
import socket
import json
import multiprocessing
import hashlib

class KafkaPublisher(object):
    pass


class StatsForwarder(object):
    DEFAULT_INTERVAL = 60
    FORWARDERS = {
        'kafka': 'KafkaPublisher',
        'logstash': 'LogstashForwarder'
    }

    def __init__(self):
        self.interval = StatsForwarder.DEFAULT_INTERVAL

    def start(self):
        while True:
            print "Forwarded Wokeup"
            # Perform Action.
            time.sleep(self.interval)



class TraceMetric(object):
    """
    Manage metric_type: TraceMetric
    """

    def __init__(self, jdata):
        self.metric_name = jdata['metric_name']
        self.metric_type = jdata['metric_type']
        self.trace_info = {}

    def update_metric(self, jdata):
        hashstr = ""
        traceobj = {}
        for key in jdata:
            # skip metric_name and type, copy rest.
            if key in ['metric_name', 'metric_type']:
                continue
            traceobj[key] = jdata[key]
            hashstr += key + jdata[key]

        objhash = hashlib.md5(hashstr)
        hash_key = objhash.hexdigest()

        if self.trace_info.get(hash_key, None) is None:
            self.trace_info[hash_key] = traceobj
            self.trace_info[hash_key]['count'] = 1
        else:
            self.trace_info[hash_key]['count'] += 1


    def display_metric_info(self):
        print "Name: %s Traceinfo: %s " % (self.metric_name, self.trace_info)

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

        metric_cls = getattr(sys.modules['__main__'],
                      MetricsManager.METRIC_TYPES[metric_type])
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

        self.udpserver = None
        self.udpworker = None
        self.forwarder = None
        self.fwdworker = None

        # Handle Keyboard Interrupt
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        print "Signal caught: ", signum
        self.udpworker.terminate()
        print "UDP Server Terminated!"

        self.fwdworker.terminate()
        print "Fowarder Terminated!"

    def udpserver_initiate(self):
        self.udpserver = UDPServer(self.bind_ip, self.bind_port)
        self.udpserver.start_listener()

    def forwarder_initiate(self):
        self.forwarder = StatsForwarder()
        self.forwarder.start()

    def run(self):
        self.udpworker = multiprocessing.Process(target=self.udpserver_initiate)
        self.udpworker.start()
        print "UDP Server Started!"

        self.fwdworker = multiprocessing.Process(target=self.forwarder_initiate)
        self.fwdworker.start()
        print "Fowarder Started!"




def main():
    """Main Function"""
    statserver = StatsServer()
    statserver.run()


if __name__ == '__main__':
    main()

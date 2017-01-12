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
from threading import Thread
import multiprocessing
import hashlib
import shelve
import pystat_config


class TimerMonitor(Thread):
    DEFAULT_INTERVAL = 10
    def __init__(self, duration, metricsmgr):
        super(TimerMonitor, self).__init__()
        self.sleep_interval = duration
        self.metricsmgr = metricsmgr

    def run(self):
        print "Timer Monitor start"
        while True:
            time.sleep(self.sleep_interval)
            print "TimerMonitor Wokeup"
            self.metricsmgr.forward_metrics()


class ShelveDB(object):
    SHELVE_PATH = "/tmp"
    def __init__(self):
        self.shelve_files = {}

    def add_to_db(self, metric_name, data):
        shelve_file = os.path.join(ShelveDB.SHELVE_PATH, metric_name)
        self.shelve_files[metric_name] = shelve_file
        db = shelve.open(shelve_file)
        db['data'] = data
        db.close()

    def get_data_from_db(self):
        for shelve_file in self.shelve_files:
            db = shelve.open(shelve_file)
            data = db['data']
            db.close()
            yield data



class StatsForwarder(object):
    TIMEOUT = 3
    FORWARDERS = {
        'kafka': {'module': 'kafka_publisher', 'classname': 'KafkaPublisher'}
    }

    def __init__(self, common_queue):
        self.queue = common_queue
        self.cfg = pystat_config.PyStatConfig()
        self.forwarders = {}
        self.debug_mode = self.cfg.parsedyaml.get('debug_mode', True)

        for forwarder in self.cfg.parsedyaml['forwarders'].keys():
            fwobj = self.cfg.parsedyaml['forwarders'][forwarder]
            mod = __import__(StatsForwarder.FORWARDERS[forwarder]['module'])
            classobj = getattr(
                mod, StatsForwarder.FORWARDERS[forwarder]['classname'])
            if forwarder == "kafka":
                kafka_broker = fwobj['kafka_broker']
                kafka_apikey = fwobj['kafka_apikey']
                kafka_tenant_id = fwobj['kafka_tenant_id']
                kafka_topic = fwobj['kafka_topic']
                self.forwarders[forwarder] = classobj(kafka_broker,
                                                      kafka_apikey,
                                                      kafka_tenant_id,
                                                      kafka_topic)

    def start(self):
        while True:
            objdata = None
            try:
                objdata = self.queue.get(timeout=StatsForwarder.TIMEOUT)
            except multiprocessing.queues.Empty:
                continue

            if objdata is None:
                print "No data. Continue"
                continue

            # Forward metrics.
            if objdata['metric_type'] == "trace":
                self.forward_trace_metrics(objdata)
            elif objdata['metric_type'] == "guage":
                self.forward_guage_metrics(objdata)

    def forward_trace_metrics(self, objdata):
        metric_name = objdata['metric_name']
        tags = {}
        for key in objdata['trace_info'].keys():
            value = objdata['trace_info'][key]['count']
            for tag in objdata['trace_info'][key].keys():
                if tag == "count":
                    continue
                tags[tag] = objdata['trace_info'][key][tag]
            self.forwarders['kafka'].forward_metrics(
                metric_name, value, tags, debug=self.debug_mode)

    def forward_guage_metrics(self, objdata):
        metric_name = objdata['metric_name']
        tags = {}
        for key in objdata['guage_info'].keys():
            value = objdata['guage_info'][key]['value']
            for tag in objdata['guage_info'][key].keys():
                if tag == "value":
                    continue
                tags[tag] = objdata['guage_info'][key][tag]
            self.forwarders['kafka'].forward_metrics(
                metric_name, value, tags, debug=self.debug_mode)


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

    def get_metric_info(self):
        metricobj = {}
        metricobj['metric_name'] = self.metric_name
        metricobj['metric_type'] = self.metric_type
        metricobj['trace_info'] = self.trace_info
        return metricobj


class GuageMetric(object):
    def __init__(self, jdata):
        self.metric_name = jdata['metric_name']
        self.metric_type = jdata['metric_type']
        self.guage_info = {}

    def update_metric(self, jdata):
        self.metric_value = int(jdata['value'])
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

        if self.guage_info.get(hash_key, None) is None:
            self.guage_info[hash_key] = traceobj
            self.guage_info[hash_key]['value'] = jdata['value']
        else:
            self.guage_info[hash_key]['value'] = jdata['value']

    def display_metric_info(self):
        print "Name: %s Traceinfo: %s " % (self.metric_name, self.guage_info)


    def get_metric_info(self):
        metricobj = {}
        metricobj['metric_name'] = self.metric_name
        metricobj['metric_type'] = self.metric_type
        metricobj['guage_info'] = self.guage_info
        return metricobj


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

    def get_metric_info(self):
        metricobj = {}
        metricobj['metric_name'] = self.metric_name
        metricobj['metric_type'] = self.metric_type
        metricobj['metric_counter'] = self.metric_counter
        return metricobj


class MetricsManager(object):
    METRIC_TYPES = {
        'counter': 'CounterMetric',
        'trace': 'TraceMetric',
        'guage': 'GuageMetric'
    }

    def __init__(self, common_queue):
        self.metrics = {}
        self.queue = common_queue
        self.db = ShelveDB()
        self.last_sent_trace = []

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

    def put_metric_data_on_queue(self, jdata):
        print "put data on queue: ", jdata
        metric_name = jdata['metric_name']
        metricobj = self.metrics[metric_name].get_metric_info()
        self.queue.put(metricobj)

    def shelve_current_metric_info(self):
        print "Shelve ALL Metrics"
        for metric_name in self.metrics.keys():
            print "Shelve Metrics: ", metric_name
            metricobj = self.metrics[metric_name].get_metric_info()
            self.db.add_to_db(metric_name, metricobj)
            self.queue.put(metric_name)

    def forward_metrics(self):
        for metric_name in self.metrics.keys():
            metricobj = self.metrics[metric_name].get_metric_info()

            hashstr = str(metricobj)
            objhash = hashlib.md5(hashstr)
            hash_key = objhash.hexdigest()
            if hash_key in self.last_sent_trace:
                print "(%d) skip sending: %s" % \
                (len(self.last_sent_trace), hash_key)
                continue

            self.queue.put(metricobj)
            self.last_sent_trace.append(hash_key)

            # Keep only the last n(10) elements in this list.
            # as it is unlikely anything more than that has not been sent.
            length = len(self.last_sent_trace)
            if length > 10:
                self.last_sent_trace.pop(0)


class UDPServer(object):
    """
    Stats UDP Server.
    """

    BUFSIZE = 1024

    def __init__(self, bind_ip, bind_port, common_queue):
        """Initalize UDPServer"""
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((self.bind_ip, self.bind_port))
        self.metricsmgr = MetricsManager(common_queue)
        self.timermonitor = None

    def start_timer(self):
        print "Start Timer Monitor"
        self.timermonitor = TimerMonitor(10, self.metricsmgr)
        self.timermonitor.start()

    def start_listener(self):
        """Listener"""
        self.start_timer()

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

            self.metricsmgr.add_metric(jdata)
            #self.metricsmgr.display_metric_info(jdata)


class StatsServer(object):
    def __init__(self):
        self.cfg = pystat_config.PyStatConfig()

        self.bind_ip = self.cfg.parsedyaml.get(
            'bind_address',
            os.environ.get('STATSD_BIND_ADDRESS', 'localhost'))

        # TODO: catch exception
        self.bind_port = int(self.cfg.parsedyaml.get(
            'bind_port',
            os.environ.get('STATSD_BIND_PORT', 5090)))

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

    def udpserver_initiate(self, common_queue):
        self.udpserver = UDPServer(self.bind_ip,
                                   self.bind_port,
                                   common_queue)
        self.udpserver.start_listener()

    def forwarder_initiate(self, common_queue):
        self.forwarder = StatsForwarder(common_queue)
        self.forwarder.start()

    def run(self):
        common_queue = multiprocessing.Queue()

        self.udpworker = multiprocessing.Process(target=self.udpserver_initiate,
                                                 args=(common_queue,))
        self.udpworker.start()
        print "UDP Server Started!"

        self.fwdworker = multiprocessing.Process(target=self.forwarder_initiate,
                                                 args=(common_queue,))
        self.fwdworker.start()
        print "Fowarder Started!"



def main():
    """Main Function"""
    statserver = StatsServer()
    statserver.run()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
kafka Publisher:

"""

import datetime
import json
from kafka import SimpleProducer, KafkaClient
import socket
import pystats_log

class KafkaPublisher(object):
    def __init__(self,
                 kafka_broker,
                 kafka_apikey,
                 kafka_tenant_id,
                 kafka_topic):
        self.kafka_broker = kafka_broker
        self.kafka_apikey = kafka_apikey
        self.kafka_tenant_id = kafka_tenant_id
        self.kafka_topic = kafka_topic

    def forward_metrics(self, metric_name, value, tags, debug=True):
        self.publish_to_kafka_broker(metric_name,
                                     self.kafka_topic,
                                     value, tags, debug=debug)

    def publish_to_kafka_broker(self, metric_name,
                                kafka_topic, value, tags, debug=True):
        """
        Generate a payload and publish the data to kafka broker.
        """
        now = datetime.datetime.utcnow()
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        metric = {}
        metric['apikey'] = self.kafka_apikey
        metric['tenant_id'] = self.kafka_tenant_id
        #host should be passed by the caller. statsd might not be
        # running on the same host as the caller.
        #metric['host'] = socket.gethostname()
        metric['name'] = metric_name
        metric['value'] = value
        metric['@version'] = '1'
        metric['@timestamp'] = timestamp
        for tag in tags:
            metric[tag] = tags[tag]

        if debug:
            msg = "DEBUG-ON: Kafka metrics tobe sent: %s" % (metric)
            pystats_log.print_msg(msg)
        else:
            kafka = KafkaClient(self.kafka_broker)
            try:
                producer = SimpleProducer(kafka)
                result = producer.send_messages(kafka_topic, json.dumps(metric))
                msg = "Kafka Metrics Pushed: [%s] [%s]" % (metric, str(result))
                pystats_log.print_msg(msg)
            except socket.gaierror as gaierror:
                msg = "Publish metric [%s] failed. [%s]" % \
                    (metric, str(gaierror))
                pystats_log.print_msg(msg)

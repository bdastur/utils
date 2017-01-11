#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
kafka Publisher:

"""

import datetime
import json
import socket
from kafka import SimpleProducer, KafkaClient


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

        print "Kafka Publisher Initialized!"

    def forward_metrics(self, metric_name, value, tags):
        self.publish_to_kafka_broker(metric_name,
                                     self.kafka_topic,
                                     value, tags)

    def publish_to_kafka_broker(self, metric_name,
                                kafka_topic, value, tags):
        """
        Generate a payload and publish the data to kafka broker.
        """
        now = datetime.datetime.utcnow()
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        metric = {}
        metric['apikey'] = self.kafka_apikey
        metric['tenant_id'] = self.kafka_tenant_id
        metric['host'] = socket.gethostname()
        metric['name'] = metric_name
        metric['value'] = value
        metric['@version'] = '1'
        metric['@timestamp'] = timestamp
        for tag in tags:
            metric[tag] = tags[tag]

        kafka = KafkaClient(self.kafka_broker)
        producer = SimpleProducer(kafka)
        result = producer.send_messages(kafka_topic, json.dumps(metric))

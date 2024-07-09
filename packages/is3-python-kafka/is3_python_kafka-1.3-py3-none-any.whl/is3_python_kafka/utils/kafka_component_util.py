import json
import logging
import os
import time

from confluent_kafka import Consumer, Producer, KafkaError

from .load_config import load_config


class kafkaComponent:
    def __init__(self, topic, group_id):
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        configPath = os.path.join(parent_dir, 'is3_config', 'is3_sys_config.ini')
        kafka_config = load_config(configPath)['kafka']
        self.consumer = Consumer({
            'bootstrap.servers': kafka_config['bootstrap_servers'],
            'group.id': group_id,
            'auto.offset.reset': kafka_config['auto_offset_reset']
        })
        self.consumer.subscribe([topic])
        self.producer = Producer({'bootstrap.servers': kafka_config['bootstrap_servers']})

    def receive(self):
        try:
            while True:
                print("等待数据...")
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.info(msg.error())
                        break
                message_content = json.loads(msg.value().decode('utf-8'))
                logging.info(f"消息：{message_content}")
                return message_content
        except KeyboardInterrupt:
            pass

    def send(self, topic, message, max_retries=3, retry_delay=1):
        attempts = 0
        while attempts < max_retries:
            delivery_success = False

            def delivery_report(err, msg):
                nonlocal delivery_success
                if err is not None:
                    logging.info(f"Message delivery failed: {err}")
                else:
                    logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")
                    delivery_success = True

            self.producer.produce(topic, json.dumps(message, ensure_ascii=False), callback=delivery_report)
            self.producer.flush()

            # Check for any message delivery errors asynchronously
            while self.producer.poll(0):
                pass

            if delivery_success:
                logging.info("is3_kafka 消息发送成功！")
                return  # If message is delivered successfully, exit the function

            attempts += 1
            time.sleep(retry_delay)

        logging.error("Maximum retry attempts reached. Message delivery failed.")

#! /usr/bin/python
import os
import time
import json
import config
from kafka import KafkaProducer

def main():
    startTime = time.time()

    KAFKA_TOPIC   = config.KAFKA_CONFIG['topic'] 
    KAFKA_BROKERS = config.KAFKA_CONFIG['brokers'] 
    IMAGES_DIR    = config.IMAGES_DIR
    
    producer = KafkaProducer(bootstrap_servers = KAFKA_BROKERS,
                             value_serializer = lambda m: json.dumps(m).encode('UTF-8'))
    
    record_number = 1
    for directory, subdirectories, files in os.walk(IMAGES_DIR):
        for filePath in files:
            image_path = os.path.join(directory,filePath)
            producer.send(KAFKA_TOPIC, [record_number, image_path])

            print(record_number)
            record_number += 1
            time.sleep(1.0/150)

    duration = time.time() - startTime
    return duration

if __name__ == '__main__':
    """Command-line execution for producer.py"""
    
    duration = main()
    print('DONE in {0:10g} seconds of wall clock time'.format(duration))

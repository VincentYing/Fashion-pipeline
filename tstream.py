import os
import config

# Spark
os.environ['PYSPARK_PYTHON']='python'
os.environ['PYSPARK_DRIVER_PYTHON']='python'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Kafka
from kafka import KafkaConsumer
import json

# Tensorflow
import tensorflow as tf
from tensorflow.python.platform import gfile

# Cassandra
import pyspark_cassandra
import logging
log = logging.getLogger()
log.setLevel('CRITICAL')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import BatchStatement
from cassandra.query import BatchType

# --------------------
# Kafka related initializations:
KAFKA_TOPIC   = config.KAFKA_CONFIG['topic']
KAFKA_BROKERS = config.KAFKA_CONFIG['brokers']
MODEL_DIR     = config.MODEL_DIR
IMAGES_DIR    = config.IMAGES_DIR

# --------------------
# Cassandra related initializations:
KEYSPACE = config.KEYSPACE
cluster = Cluster(config.CASS_CLUSTER)
session = cluster.connect()

log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)

update_stats = session.prepare("UPDATE stats SET count = count + ?, acc_score = acc_score + ? WHERE prediction = ? ")


def sendCassandra(item):
    print("send to cassandra")
    cluster = Cluster(config.CASS_CLUSTER)
    session = cluster.connect()
    session.execute('USE ' + config.KEYSPACE)

    # batch insert into cassandra database
    batch = BatchStatement(batch_type=BatchType.COUNTER)
    for record in item:
        batch.add(update_stats, (int(record[1][0]), float(record[1][1]), str(record[0]) ))

    session.execute(batch)
    session.shutdown()

def createContext():
    sc = SparkContext(appName="TensorStream")
    sc.setLogLevel("ERROR")
    sc.addPyFile('tflow.py')
    sc.addPyFile('config.py')
    import tflow
    infer = tflow.infer

    model_data_bc = None
    model_path = os.path.join(MODEL_DIR, 'classify_image_graph_def.pb') #
    with gfile.FastGFile(model_path, 'rb') as f:
        model_data = f.read()
        model_data_bc = sc.broadcast(model_data)

    ssc = StreamingContext(sc, 15)

    # Define Kafka Consumer
    kafkaStream = KafkaUtils.createDirectStream(
                      ssc,
                      [KAFKA_TOPIC],
                      {"metadata.broker.list":'localhost:9092'}
                                                )
    #kafkaStream.pprint()
    # Count number of requests in the batch
    count_this_batch = kafkaStream.count().map(
                           lambda x:('Number of requests this batch: %s' % x)
                                             )
    count_this_batch.pprint()

    # Print the path requests this batch
    reparted = kafkaStream.repartition(9)
    #reparted.pprint()

    paths  = reparted.map(lambda m: json.loads(m[1])[1])
    #paths.pprint()

    inferred = paths.mapPartitions(lambda x: infer(x, model_data_bc))
    inferred.pprint()

    # (id, (prediction, accuracy))
    #reduced = inferred.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))
    #reduced.pprint()

    #reduced.foreachRDD(lambda rdd: rdd.foreachPartition(sendCassandra))

    return ssc

ssc = createContext()
ssc.start()
ssc.awaitTermination()

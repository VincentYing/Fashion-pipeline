import os, sys
sys.path.append(os.path.dirname(os.path.abspath('.')) + '/lib')
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

# --------------------
# Cassandra related initializations:
KEYSPACE = config.KEYSPACE
cluster = Cluster(config.CASS_CLUSTER)
session = cluster.connect()

log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)

insert_stats = session.prepare("INSERT INTO clothes (uid, image, pred1, pred2, pred3, conf1, conf2, conf3) VALUES (now(), ?, ?, ?, ?, ?, ?, ?)") 

def sendCassandra(item):
    cluster = Cluster(config.CASS_CLUSTER)
    session = cluster.connect()
    session.execute('USE ' + config.KEYSPACE)

    # batch insert into cassandra database
    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    for record in item:
        for i in range(10):
            if record[1][i][0] != "err":
                batch.add(insert_stats, (str(record[0][i][0]), \
                    str(record[1][i][0]), str(record[1][i][1]), str(record[1][i][2]), \
                    float(record[2][i][0]), float(record[2][i][1]), float(record[2][i][2])))

    session.execute(batch)
    session.shutdown()

def createContext():
    sc = SparkContext(appName="TensorStream")
    sc.setLogLevel("ERROR")
    sc.addPyFile('tflow.py')
    sc.addPyFile('../lib/config.py')
    import tflow
    infer = tflow.infer

    model_data_bc = None
    model_path = os.path.join(MODEL_DIR, 'clothing-deploy.pb')
    with gfile.FastGFile(model_path, 'rb') as f:
        model_data = f.read()
        model_data_bc = sc.broadcast(model_data)

    ssc = StreamingContext(sc, 15)

    # Define Kafka Consumer
    kafkaStream = KafkaUtils.createDirectStream(ssc, [KAFKA_TOPIC],
                      {"metadata.broker.list":'localhost:9092'} )
    #kafkaStream.pprint()

    # Count number of requests in the batch
    batch_count = kafkaStream.count().map(
                        lambda x:('Number of requests this batch: %s' % x) )
    batch_count.pprint()

    # Print the path requests this batch
    reparted = kafkaStream.repartition(36)
    #reparted.pprint()

    paths = reparted.map(lambda m: json.loads(m[1])[1])
    #paths.pprint()

    inferred = paths.mapPartitions(lambda x: infer(x, model_data_bc))
    #inferred.pprint()

    inferred.foreachRDD(lambda rdd: rdd.foreachPartition(sendCassandra))

    return ssc

ssc = createContext()
ssc.start()
ssc.awaitTermination()

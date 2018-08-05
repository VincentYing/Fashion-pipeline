#! /usr/bin/python
import config
import logging
from cassandra.cluster import Cluster

log = logging.getLogger()
log.setLevel('CRITICAL')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

KEYSPACE = config.KEYSPACE
cluster = Cluster(config.CASS_CLUSTER)
session = cluster.connect()

log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)

rows = session.execute('select * from clothes limit 5;')
for row in rows:
    print row

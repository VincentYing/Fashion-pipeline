#! /usr/bin/python
import sys
import config
# --------------------
# Cassandra related imports

import logging
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# --------------------
# Cassandra related initializations:

KEYSPACE = config.KEYSPACE

cluster = Cluster(['localhost'])
session = cluster.connect()
# HDA out:
# rows = session.execute("SELECT keyspace_name FROM system.schema_keyspaces")
# HDA in: Function name change  in Cassandra v3.
rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
print(rows[0])
# HDA done.
if KEYSPACE in [row[0] for row in rows]:
    log.info("dropping existing keyspace...")
    session.execute("DROP KEYSPACE " + KEYSPACE)

log.info("creating keyspace...")
session.execute("""
    CREATE KEYSPACE %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
    """ % KEYSPACE)

log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)

#log.info("creating table...")
#session.execute("""
#    CREATE TABLE logs (
#        reqID text,
#        p1 text,
#        c1 float,
#        path text,
#        PRIMARY KEY (reqID)
#    )
#    """)

log.info("creating table...")
session.execute("""
    CREATE TABLE stats (
        prediction text,
        count counter,
        acc_score counter,
        PRIMARY KEY (prediction)
    )
    """)

log.info("creating clothes table...")
session.execute("""
    CREATE TABLE clothes (
        imgId int,
        image text,
        pred1 text,
        conf1 float,
        pred2 text,
        conf2 float,
        pred3 text,
        conf3 float,
        PRIMARY KEY (imgId)
    )
    """)
sys.exit

#!/bin/bash
peg start kafka-cluster
peg service kafka-cluster zookeeper start
peg service kafka-cluster kafka start

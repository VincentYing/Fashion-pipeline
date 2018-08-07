#!/bin/bash
peg service kafka-cluster kafka stop
peg service kafka-cluster zookeeper stop
peg stop kafka-cluster

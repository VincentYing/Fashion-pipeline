#!/bin/bash
peg service spark-cluster spark stop
peg service spark-cluster kafka stop
peg service spark-cluster hadoop stop
peg service spark-cluster zookeeper stop
peg stop spark-cluster

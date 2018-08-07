#!/bin/bash
peg service gpu-cluster spark stop
peg service gpu-cluster kafka stop
peg service gpu-cluster hadoop stop
peg service gpu-cluster zookeeper stop
peg service gpu-cluster cassandra stop
peg stop gpu-cluster

#!/bin/bash
peg start gpu-cluster
peg service gpu-cluster hadoop start
peg service gpu-cluster zookeeper start
sleep 5s
peg service gpu-cluster spark start
peg service gpu-cluster kafka start

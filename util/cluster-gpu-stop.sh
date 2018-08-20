#!/bin/bash
peg service gpu-cluster spark stop
peg service gpu-cluster hadoop stop
peg stop gpu-cluster

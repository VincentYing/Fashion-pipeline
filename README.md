# Fast Fashion Recognition

This project optimizes an image pipeline for classification of clothing.

#### Motivation

The main motivation for the project is to help deliver image classifications at a faster rate for further use downstream. The particular use case I choose was clothing apparel, which would be useful in the first stage of a recommender system for popular image apps like Instagram. It can be extended to many other verticals, such as furniture and interior design for Pinterest and Houzz.

[Slides](http://bit.ly/fashion-ppt)

<hr/>

#### Data

* Imagenet subset containing people will be used as a data source (952k images).
* Dataset will be loaded locally onto the nodes used for ingestion.

<hr/>

#### Model

* Model is pre-trained GoogleNet (Inception v1) from DeepDetect.
* 304 Clothing possible classifications.

<hr/>

#### Pipeline

<img src="https://raw.githubusercontent.com/VincentYing/fashion-pipeline/master/images/data-pipeline.png" width="800" height="340">

<hr/>

#### Data Flow

1. Kafka ingests image paths of images stored locally.
2. Spark resizes image with OpenCV runs the TF model for each batch.
3. Pretrained TF model classifies likelihood of clothing for all 304 classes. ([Model](https://www.deepdetect.com/applications/model/))
4. Cassandra stores the iamge path, top 3 predictions and their likelihoods.
5. Flask displays the image top 3 predictions and their likelihoods.

<hr/>

#### Setup

* Initially, Kafka/Spark/Cassandra was run on one 4-node cluster.
* However, Kafka would run out of heap memory and Cassandra for that node would be unreachable.
* This resulted in separation of the setup into two clusters, one for Kafka/Spark and one for Cassandra.

<hr/>

#### Execution

1. Start Kafka/Spark cluster:

    fashion$ ./util/cluster-spark-start.sh

2. Start Cassandra cluster:

    fashion$ ./util/cluster-cassandra-start.sh

3. Initialize Cassandra db:

    fashion/cassandra$ python cass_init.py

4. Start Spark job:

    fashion/spark$ ./spark_cluster_run.sh

5. Start Kafka stream:

    fashion/kafka$ ./kafka_run.py

6. Start flask to view predictions:

    fashion/imageviewer$ gunicorn app:app  --bind 0.0.0.0:5000 -k gevent -w 8

<hr/>

#### Challenges

There were two main challenges to this project:
1. Conversion of pretrained Caffe model to optimized TF version and integration in Spark Streaming.
2. Working around the inference bottleneck.
  * It was found that the main delay in the pipeline was the classification performed by the TF model.
  * Preprocessing delay for image resizing was negligible compared to classification.

###### Performance Optimizations:

* Spark Parameter Tuning

  1. Experimented with different repartition() values. RDD partition size of 36 was found to be optimal.
    <img src="https://raw.githubusercontent.com/VincentYing/fashion-pipeline/master/images/repartition.png" width="480" height="270">

  2. Enabled dynamic allocation for Executor creation.

    The two adjustments above resulted in a 2x improvement in inference rate from 0.5 to 1 inference per second.

  3. Adjusted the number of Kafka partitions to match the number of SPARK_WORKER_CORES (6). This produced a 3x speedup.
    <img src="https://raw.githubusercontent.com/VincentYing/fashion-pipeline/master/images/kafka_partitions.png" width="480" height="270">

* Image Batching for TF ingestion

  Next, I manually batched 10 images for TF model ingestion. This produced a 4x speedup from 1 to 4 inferences per second.

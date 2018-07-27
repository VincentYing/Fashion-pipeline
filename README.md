# Image Data Pipeline

<!---
Github repo with a README containing:
Project Idea (1-sentence)
What is the purpose, and most common use cases?
Which technologies are well-suited to solve those challenges? (list all relevant)
Proposed architecture
Data: Talk in Numbers (size, volume, complexity)
--->

##### Project Idea

This project will perform image ingestion, processing, and analysis, with person detection as the specific use case.

<hr/>

##### Technologies

Kafka will be used for picture ingestion.

Spark will be used for image processing.

A pretrained Tensorflow model will be used for person detection. [Human Detection](https://medium.com/@madhawavidanapathirana/real-time-human-detection-in-computer-vision-part-2-c7eda27115c6)

Cassandra will be used for image store.

Flask will be used for display of picture and classification statistics.

<hr/>

##### Architecture

![Image Pipeline](https://github.com/VincentYing/image-pipeline/data-pipeline.png)

<hr/>

##### Data

ImageNet will be used as a data source.
* Size of dataset is 14,197,122 images with 952k containing people.
* Dataset will be loaded locally onto the nodes used for ingestion.

<!---
[Slides](https://docs.google.com/presentation/d/13n7iXGRkSrlzq3qGVe7PxvjCXLRpoNGjvC3pnGv_U3A/edit?usp=sharing)

<hr/>


## How to install and get it up and running


<hr/>

## Introduction

## Architecture

## Dataset

## Engineering challenges

## Trade-offs
--->

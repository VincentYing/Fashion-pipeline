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

Tensorflow will be used for person detection.

Cassandra will be used for image store.

Flask will be used for display of picture and classification statistics.

<hr/>

##### Architecture

A pretrained Tensorflow model for person detection will be used for classification.

[Human Detection](https://medium.com/@madhawavidanapathirana/real-time-human-detection-in-computer-vision-part-2-c7eda27115c6)

<hr/>

##### Data

ImageNet will be used as a data source.
* Size of dataset is 14,197,122 images with 952k containing people.

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

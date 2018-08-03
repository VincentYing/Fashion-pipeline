# Image Data Pipeline

<!---
Github repo with a README containing:
Project Idea (1-sentence)
What is the purpose, and most common use cases?
Which technologies are well-suited to solve those challenges? (list all relevant)
Proposed architecture
Data: Talk in Numbers (size, volume, complexity)
--->

#### Project Idea

Project purpose is to figure out what other people are wearing directly from images.

Useful for keeping in style and tracking fashion trends.

[Slides](http://bit.ly/style-strm)

<hr/>

#### Data

ImageNet will be used as a data source.
* Size of dataset is 14,197,122 images with 952k containing people.
* Dataset will be loaded locally onto the nodes used for ingestion.

<hr/>

#### Architecture

![Image Pipeline](https://raw.githubusercontent.com/VincentYing/image-pipeline/master/data-pipeline.png)

<hr/>

#### Technologies

Kafka ingests pictures of people

Spark processes image

Pretrained TF model recognizes clothing ([Model](https://www.deepdetect.com/applications/model/))

Cassandra stores top 3 predictions

Flask displays top 3 predictions

<hr/>

#### Challenges

The main challenge of this project is the construction of a pipeline to pass images through for classification.

<hr/>

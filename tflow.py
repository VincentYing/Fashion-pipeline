import numpy as np
import tensorflow as tf
import config
import os

num_top_predictions = 1
model_path = os.path.join(config.MODEL_DIR, 'classify_image_graph_def.pb')

def infer(msg, model_data_bc):
    paths = msg
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(model_data_bc.value)
    tf.import_graph_def(graph_def, name='')
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        for path in paths:
            with open(path, 'rb') as f:
                try:
                    image_data = f.read()
                except:
                    yield ('Can''t read the image.', (1, 0.0))
                try:
                    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
                    predictions = np.squeeze(predictions)
                    top_k = predictions.argsort()[-num_top_predictions:][::-1]
                    """
                    top_k_probs=[]
                    top_k_names=[]
                    for node_id in top_k:
                        score = 100*predictions[node_id]
                        top_k_names.append(node_id)
                        top_k_probs.append(score)
                    yield (top_k_names[0], (1, top_k_probs[0]))
                    """
                    yield (top_k[0], (1, 100*predictions[top_k[0]]))
                except:
                    err= ('tf_error', (1, 0.0))
                    yield err

def infer_single(msg):
    image_path    = msg[1]
    with open(image_path, 'rb') as f, \
         open(model_path, 'rb') as m:
        num_top_predictions = 1

        # Creates a new TensorFlow graph of computation and imports the model
        try:
            image_data = f.read()
        except:
            return ('Can''t read the image.', (1, 0.0))
        try:
            model_data = m.read()
        except:
            return ('Can''t read the pretrained model.', (1, 0.0))
        try:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(model_data)
            tf.import_graph_def(graph_def, name='')
            return(000, (1, 0.0))
            with tf.Session() as sess:
                softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
                predictions = np.squeeze(predictions)
                top_k = predictions.argsort()[-num_top_predictions:][::-1]
                top_k_probs=[]
                top_k_names=[]
                for node_id in top_k:
                    score = 100*predictions[node_id]
                    top_k_names.append(node_id)
                    top_k_probs.append(score)
                return(top_k_names[0], (1, top_k_probs[0]))
        except:
            err= ('tf_error', (1, 0.0))
            return err

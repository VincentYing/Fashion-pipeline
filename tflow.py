import numpy as np
import tensorflow as tf
import config
import os
import cv2

num_top_predictions = 3
model_path = os.path.join(config.MODEL_DIR, 'clothing-deploy.pb')

def infer(msg, model_data_bc):
    paths = msg
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(model_data_bc.value)
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='prefix')
    with tf.Session(graph=graph) as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('prefix/prob:0')
        for path in paths:
            try:
                image = cv2.imread(path)
                resized = cv2.resize(image,(224,224))
                np_img = np.asarray(resized)
                np_final = np.expand_dims(np_img, axis=0)
                image_data = []
                for i in range(10):
                    image_data.append(np_final[0])
            except:
                yield ('Can''t read the image.', ["err", "err", "err"], [0.0, 0.0, 0.0])
            try:
                predictions = sess.run(softmax_tensor, {'prefix/data:0': image_data})
                predictions = np.squeeze(predictions)
                top_k = predictions[0].argsort()[-num_top_predictions:][::-1]
                pred_k = [predictions[0][top_k[0]], predictions[0][top_k[1]], predictions[0][top_k[2]]]
                pred_k = [i * 100 for i in pred_k]
                yield (path, top_k[0:3], pred_k)
            except:
                yield ('tf_error', ["err", "err", "err"], [0.0, 0.0, 0.0])

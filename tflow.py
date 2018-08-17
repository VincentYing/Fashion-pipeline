import numpy as np
import tensorflow as tf
import config
import os
import cv2

num_top_predictions = 3
model_path = os.path.join(config.MODEL_DIR, 'clothing-deploy.pb')

def infer(msg, model_data_bc):
    # Image file paths
    paths = msg

    # Initialize model graph
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(model_data_bc.value)

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='prefix')

    with tf.Session(graph=graph) as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('prefix/prob:0')

        image_data = []
        locs, pred, conf = ([] for i in range(3))

        for path in paths:
            # Try to read in the image
            try:
                image = cv2.imread(path)
                resized = cv2.resize(image,(224,224))
                np_img = np.asarray(resized)

                image_data.append(np_img)
            except:
                # yield ('Can''t read the image.', ["err", "err", "err"], [0.0, 0.0, 0.0])
                image_data.append(np.zeros((224,224,3), dtype=int))

            if (len(image_data) == 10):
                try:
                    # Run array of 10 images through the pretrained model
                    predictions = sess.run(softmax_tensor, {'prefix/data:0': image_data})
                    predictions = np.squeeze(predictions)

                    for i in range(10):
                        pred_k = predictions[i].argsort()[-num_top_predictions:][::-1]
                        conf_k = [predictions[i][pred_k[0]], predictions[i][pred_k[1]], predictions[i][pred_k[2]]]
                        conf_k = [j * 100 for j in conf_k]

                        locs.append([path])
                        pred.append(pred_k[0:3])
                        conf.append(conf_k)
                except:
                    # yield ('tf_error', ["err", "err", "err"], [0.0, 0.0, 0.0])
                    locs = [['tf_error']] * 10
                    pred = [["err", "err", "err"]] * 10
                    conf = [[0.0, 0.0, 0.0]] * 10

                image_data = []
                yield (locs, pred, conf)

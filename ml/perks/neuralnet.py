import keras
from keras.layers import Dense
from keras.models import Sequential, load_model
import json
import os
import pickle
import matplotlib.pyplot as plt
from keras.utils import plot_model
import keras.backend as K
def maskedErrorFunc(y_true, y_pred):
    mask = K.cast(K.not_equal(y_true, -1), K.floatx())
    maskedError = (y_true - y_pred) * mask
    correct = K.mean(K.square(maskedError))
    return correct
"""
    {
        layers: Array<Layer> # see _getLayer
        optimizer: string # w/e keras allows
        loss: string # w/e keras allows
        metrics: Array<string> # w/e keras allows
        epochs: int # number of epochs
        batchSize: int # samples per batch ('weight_update'),
        modelName: string
    }
"""
from keras import metrics

def makeTopKAccuracy(k):
    def topKAccuracy(y_true, y_pred): 
        return metrics.top_k_categorical_accuracy(y_true, y_pred, k)
    return topKAccuracy

def build(netConfig):
    model = Sequential()
    first = True
    for layer in netConfig["layers"]:
        model.add(_getLayer(layer, first))
        first = False
    if netConfig["loss"] == "win_loss":
        loss = maskedErrorFunc
    else:
        loss = netConfig["loss"]
    metrics2 = netConfig["metrics"]
    if "top_k_categorical_accuracy" in netConfig["metrics"]:
        k = netConfig["top_k_parameter"]
        metrics2 += [makeTopKAccuracy(k)]
        metrics2.remove("top_k_categorical_accuracy")
    model.compile(optimizer=netConfig["optimizer"], loss=loss, metrics=metrics2)
    return model

def train(model, x_train, y_train, netConfig):
    history = model.fit(x_train.values, y_train.values, batch_size=netConfig["batchSize"], epochs=netConfig["epochs"], validation_split=0.1, shuffle=True)
    return history

import pickle

def save(model, history, netConfig, trainReport, testReport, smarties, cols):
    dir = "./perks/models" + netConfig["directory"] + "/"
    print("Saving model in " + dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    model.save(dir + "model")
    print("Saved model")
    model.save_weights(dir + "weights")
    print("Saved weights")
    architecture = model.to_json()
    # cols
    with open(dir + "columns", "w") as colFile:
        json.dump(cols, colFile, indent=4)
    print("Saved columns")
    # save architecture
    with open(dir +  "architecture", 'w') as outfile:
        json.dump(architecture, outfile, indent=4)
    print("Saved architecture")
    # save data transformation
    with open(dir + "smarties.pkl", 'wb') as smartiesFile:
        pickle.dump(smarties, smartiesFile, pickle.HIGHEST_PROTOCOL)
    print("Saved smarties")
    # save history
    with open(dir + "history", 'wb') as file_pi:
        pickle.dump(history.history, file_pi)
    print("Saved history")
    # save reports
    with open(dir + "reports", 'w') as reportFile:
        reportFile.write("Training Report:\n")
        reportFile.write(str(trainReport) + "\n")
        reportFile.write("\n\n\nTest Report: \n")
        reportFile.write(str(testReport))
        reportFile.write("\n")
        reportFile.flush()
    print("Saved reports")
    # save model image
    plot_model(model, to_file=dir + "model.png")
    # save history image
    training_loss = history.history['loss']
    test_loss = history.history['val_loss']
    epoch_count = range(1, len(training_loss) + 1)
    plt.plot(epoch_count, training_loss, 'r--')
    plt.ylim(ymin=0)
    plt.plot(epoch_count, test_loss, 'b-')
    plt.legend(['Training Loss', 'Test Loss'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig(dir + "history.png")
    print("Saved plot")

def load(netConfig):
    # todo implement
    return load_model("./perks/models/" + netConfig["modelName"] + "/model")

"""
    {
        name: # in [Dense, ]
        activation: # in [softmax, ... ] (w/e keras allows)
        neuronCount: # number of neurons
    }
"""
def _getLayer(layerConfig, first):
    if first:
        inputShape = layerConfig["inputDim"]
    else:
        inputShape = None
    if layerConfig["type"] == "Dense":
        layer = Dense(layerConfig["neuronCount"], activation=layerConfig["activation"], input_dim=inputShape)
        return layer
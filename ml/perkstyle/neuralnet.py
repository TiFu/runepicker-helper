import keras
from keras.layers import Dense
from keras.models import Sequential, load_model
import json
import os
import pickle
import matplotlib.pyplot as plt
from keras.utils import plot_model

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
def build(netConfig):
    model = Sequential()
    first = True
    for layer in netConfig["layers"]:
        model.add(_getLayer(layer, first))
        first = False
    model.compile(optimizer=netConfig["optimizer"], loss=netConfig["loss"], metrics=netConfig["metrics"])
    return model

def train(model, x_train, y_train, netConfig):
    history = model.fit(x_train.values, y_train.values, batch_size=netConfig["batchSize"], epochs=netConfig["epochs"], validation_split=0.1, shuffle=True)
    return history

def save(model, history, netConfig, trainReport, testReport):
    dir = "./perkstyle/models/" + netConfig["modelName"] + "/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    model.save(dir + "model")
    architecture = model.to_json()
    # save architecture
    with open(dir +  "architecture", 'w') as outfile:
        json.dump(architecture, outfile)
    # save history
    with open(dir + "history", 'wb') as file_pi:
        pickle.dump(history.history, file_pi)
    # save reports
    with open(dir + "reports", 'w') as reportFile:
        reportFile.write("Training Report:\n")
        reportFile.write(str(trainReport) + "\n")
        reportFile.write("\n\n\nTest Report: \n")
        reportFile.write(str(testReport))
        reportFile.write("\n")
        reportFile.flush()
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

def load(netConfig):
    # todo implement
    return load_model("./perkstyle/models/" + netConfig["modelName"] + "/model")

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
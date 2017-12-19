import keras
from keras.layers import Dense, Input
from keras.models import Sequential, load_model, Model
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
    # TODO fix with functional api and multiple outputs
    # https://keras.io/getting-started/functional-api-guide/
    input = Input(shape=(netConfig["sharedLayers"][0]["inputDim"],))
    sharedLayers = input
    for layer in netConfig["sharedLayers"]:
        sharedLayers = _getLayer(layer)(sharedLayers)
    # Add outputs
    outputs = []
    for output in netConfig["outputs"]:
        subModel = sharedLayers
        for layer in output:
            subModel = _getLayer(layer)(subModel)
        outputs.append(subModel)

    model = Model(inputs=[input], outputs=outputs)
    model.compile(optimizer=netConfig["optimizer"], loss=netConfig["loss"], metrics=netConfig["metrics"], loss_weights=netConfig["lossWeights"])
    return model

def train(model, x_train, y_train, netConfig):
    y_train = list(map(lambda x: x.values, y_train))
    history = model.fit([x_train.values], y_train, batch_size=netConfig["batchSize"], epochs=netConfig["epochs"], validation_split=0.1, shuffle=True)
    return history

def save(model, history, netConfig, trainReports, testReports):
    dir = "./perks/models/" + netConfig["modelName"] + "/"
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
        for i in range(len(trainReports)):
            reportFile.write(str(trainReports[i][0]) + "\n")
            reportFile.write("Training Report:\n")
            reportFile.write(str(trainReports[i][1]) + "\n")
            reportFile.write("\nTest Report: \n")
            reportFile.write(str(testReports[i][1]))
            reportFile.write("\n\n\n\n")
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
def _getLayer(layerConfig):
    if "name" not in layerConfig:
        layerConfig["name"] = None
    if layerConfig["type"] == "Dense":
        layer = Dense(layerConfig["neuronCount"], activation=layerConfig["activation"], name=layerConfig["name"])
        return layer
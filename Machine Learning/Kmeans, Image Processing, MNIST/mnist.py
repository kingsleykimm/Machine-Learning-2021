import tensorflow as tf
from tensorflow import keras
import numpy as np




(trainX, trainy), (testX, testy) = keras.datasets.mnist.load_data()
# summarize loaded dataset

X_valid, X_train = trainX[:5000] / 255.0, trainX[5000:] / 255.0
y_valid, y_train = trainy[:5000], trainy[5000:]

model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28, 28]))
model.add(keras.layers.Dense(300, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))
model.add(keras.layers.Dense(10, activation="softmax"))
model.compile(loss="sparse_categorical_crossentropy",
                optimizer = keras.optimizers.SGD(0.1),
                    metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid))
print(model.evaluate(testX, testy))
model.summary()


file1 = open("model_weights.txt", 'w')
for i in range(1, len(model.layers)):
    for item in model.layers[i].get_weights()[0]: #normal weights
        file1.write(str(item))
    for item1 in model.layers[i].get_weights()[1]: #bias weights
        file1.write(str(item1))

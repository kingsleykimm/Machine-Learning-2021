from keras.datasets import mnist
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import time

def main():
    (x_tr, y_tr), (x_te, y_te) = mnist.load_data()
    x_train, x_test, y_train, y_test = train_test_split(x_tr, y_tr, test_size = 0.2, random_state = 40, stratify=y_tr)
    x_train = x_train.astype("float64")
    x_test = x_test.astype("float64")
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    X_train = x_train.reshape(len(x_train), -1)
    X_test = x_test.reshape(len(x_test), -1)
    x_te = x_te.reshape(len(x_te), -1)
    k = 20
    classifier = KNeighborsClassifier(n_neighbors=k)
    start = time.process_time()
    classifier.fit(X_train, y_train)
    elapsed = time.process_time() - start
    start1 = time.process_time()
    predictions = classifier.predict(x_te)
    elapsed1 = time.process_time() - start1
    print("Accuracy:", accuracy_score(y_true = y_te, y_pred = predictions))    
    print("Training Time: ", elapsed)
    print("Prediction Time: ", elapsed1)




if __name__ == '__main__':
    main()

#Kingsley Kim 3, 22
from keras.datasets import mnist
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
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
    model = SVC(kernel ='poly')
    start = time.process_time()
    model.fit(X_train, y_train)
    elapsed_time = time.process_time() - start    
    predictions = model.predict(x_te)
    print("Accuracy:", accuracy_score(y_true = y_te, y_pred = predictions))
    # predictions = model.predict(X_test)
    # print("Accuracy on train_test_split test set: ", accuracy_score(y_true = y_test, y_pred=predictions))
    print("Time taken: ", elapsed_time)

    

if __name__ == '__main__':
    main()


#Kingsley Kim 3, 22
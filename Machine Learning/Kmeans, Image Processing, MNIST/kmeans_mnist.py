from keras.datasets import mnist
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import accuracy_score
import time 


def extract_labels(labels, y_train):
    #model.labels_ only labels all the 60000 images with the number of the cluster, but the identifier is not the actual number in the image
    output_labels = {}
    for i in range(len(np.unique(labels))): #goes through labels and creates an ndarray index that places a 1 if the label is there and a 0 if not
        index = list()
        for k in range(len(labels)):
            if labels[k] == i:
                index.append(1)
            else:
                index.append(0)
        
        li = list()
        for j in range(len(index)):
            if index[j] == 1:
                li.append(y_train[j])
        num = np.bincount(li).argmax() #np.bincount gives array with each count from input array
        output_labels[i] = num #assigns cluster to number on image
    return output_labels


def kmeans(X, y, clusters):
    model = MiniBatchKMeans(n_clusters = clusters)
    start = time.process_time()
    model.fit(X)
    elapsed_time = time.process_time() - start
    labels = extract_labels(model.labels_, y)
    number_labels = np.empty(len(model.labels_))
    for i in range(len(model.labels_)):
        number_labels[i] = labels[model.labels_[i]]
    return accuracy_score(number_labels, y), elapsed_time

def main():
    (x_train, y_train), (x_test, y_test) = mnist.load_data() #load data
    x_train = x_train.astype("float32") 
    x_test = x_test.astype("float32")# Normalization x_train = x_train/255.0
    x_train = x_train / 255.0
    x_test = x_test/ 255.0 #normalize
    X_train_reshaped = x_train.reshape(len(x_train), -1) #changes dimension from (28, 28) to (784)
    X_test_reshaped = x_test.reshape(len(x_test), -1)
    clusters = 270
    training_err, elapsed_time = kmeans(X_train_reshaped, y_train, clusters)
    test_err = kmeans(X_test_reshaped, y_test, clusters)[0]
    print("Accuracy on test set: {}, Time to converge: {} seconds".format(test_err, elapsed_time))
    # model = MiniBatchKMeans(n_clusters = 10)
    # model.fit(X_train_reshaped)
    # labels = extract_labels(model.labels_, y_train) #dictionary with 0 -> number of MNIST image, 1 -> another number of MNIST image, so on
    # number_labels = np.empty(len(model.labels_))
    # for i in range(len(number_labels)):
    #     number_labels[i] = labels[model.labels_[i]] #makes identical copy of model.labels_ but with correct MNIST number labels
    

if __name__=='__main__':
    main()
    

#Kingsley Kim 3, 22
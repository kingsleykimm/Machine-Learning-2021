import numpy as np
import cv2
import matplotlib

def main():

    image = cv2.imread("/Users/kingsleykim0319/Desktop/Machine Learning/yacht.jpg", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    guass = cv2.GaussianBlur(gray, (5,5), 0, cv2.BORDER_DEFAULT)
    thres, threshold = cv2.threshold(guass, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    cv2.imshow('Original image',image)
    cv2.imshow('Gray image', gray)
    cv2.imshow('Gaussian image', guass)
    cv2.imshow('Threshold image', threshold)



    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#Kingsley Kim 3, 22
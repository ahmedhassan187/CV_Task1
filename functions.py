import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

class Functions:
    def __init__(self):
        pass
    def padding(self,image):
        padded_image = np.zeros((image.shape[0]+2,image.shape[1]+2))
        padded_image[1:image.shape[0]+1,1:image.shape[1]+1]=image 
        return padded_image
    def average_filter(self,image_data,filter_size):
        filter = np.ones((filter_size,filter_size))/(filter_size)**2
        padded = self.padding(image_data)
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                new_img[i][j] = np.sum((padded[i:i+filter_size,j:j+filter_size]*filter))
        return new_img
    def median_filter(self,image_data,filter_size):
        padded = self.padding(image_data)
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                new_img[i][j] = np.median(padded[i:i+filter_size,j:j+filter_size])
        return new_img
    def gaussian_filter(self,image_data,filter_size=3):
        filter = np.array([[1,2,1],[2,4,2],[1,2,1]])/16
        padded = self.padding(image_data)
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                new_img[i][j] = np.sum((padded[i:i+filter_size,j:j+filter_size]*filter))
        return new_img
    def high_filter(self,image_data,filter_size=3):
        filter = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])/9
        padded = self.padding(image_data)
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                new_img[i][j] = np.sum((padded[i:i+filter_size,j:j+filter_size]*filter))
        return new_img
    def rgb2gray(self,image):
        new_image = 0.299*image[:,:,0]+0.587*image[:,:,1]+0.114*image[:,:,2]
        return new_image
    def hybrid(self,image1,image2):
        """image1: high filter image
        image2: low pass image"""
        image1 = self.rgb2gray(image1)
        image2 = self.rgb2gray(image2)
        image1 = self.high_filter(image1)
        image2 = self.average_filter(image2)
        new_image = image1+image2
        return new_image
    def rgb_histogram(image):
        r = image[:,:,0]
        g = image[:,:,1]
        b = image[:,:,2]
        plt.hist(r.ravel(),256,[0,256],color='r')
        plt.hist(g.ravel(),256,[0,256],color='g')
        plt.hist(b.ravel(),256,[0,256],color='b')
        plt.show()
    # Function to compute gray level histogram 
    def histogram_Compute(self,image):
        img_height = image.shape[0]
        img_width = image.shape[1]
        hist = np.zeros([256],np.int32)
        for x in range(0,img_height):
            for y in range(0,img_width):
                hist[image[x,y]] +=1
        np.savetxt("./saved_text/gray scale histogram.txt",hist)
        return hist
    # plotting the gray scale histogram 
    def histogram_Plot(self,histogram):
        plt.figure()
        plt.title("Histogram Distribution Curve")
        plt.xlabel("Brightness")
        plt.ylabel("number of Pixels")
        plt.xlim([0,256]) # As gray scale levels vary from 0 -> 256
        plt.plot(histogram)
        plt.savefig("./saved_imgs/hisogram.jpg")
        return "Success"
    # function to normalize the image
    def img_normalization(self,img):
        Min = np.min(img)
        Max = np.max(img)
        return (((img- Min)/((Max-Min)))) #stretching histogram equation from 0->255 to 0.0 -> 1.0
    
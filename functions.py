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
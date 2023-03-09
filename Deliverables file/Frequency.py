import matplotlib.pyplot as plt
import numpy as np
import cv2

import random
from scipy import ndimage
from scipy import signal

class Frequency():
    def hybrid(self,image1,image2,r1,r2):
        """image1: high filter image
        image2: low pass image"""
        # image1 = self.rgb2gray(self,image1)
        # image2 = self.rgb2gray(self,image2)
        image1 = self.low_high_pass(image1,'low',r1)
        image2 = self.low_high_pass(image2,'high',r2)
        new_image = image1+image2
        return new_image
    def padding(self,image):
        padded_image = np.zeros((image.shape[0]+2,image.shape[1]+2))
        padded_image[1:image.shape[0]+1,1:image.shape[1]+1]=image 
        return padded_image
    
    def non_max_suppression(self,image):
        # non max suppression
        image = self.padding(self,image)
        for i in range(1,image.shape[0]-1):
            for j in range(1,image.shape[1]-1):
                if image[i,j] == 0:
                    image[i,j] = 0
                elif image[i,j] == 45:
                    if image[i-1,j+1] > image[i,j] or image[i+1,j-1] > image[i,j]:
                        image[i,j] = 0
                elif image[i,j] == 90:
                    if image[i-1,j] > image[i,j] or image[i+1,j] > image[i,j]:
                        image[i,j] = 0
                elif image[i,j] == 135:
                    if image[i-1,j-1] > image[i,j] or image[i+1,j+1] > image[i,j]:
                        image[i,j] = 0
                else:
                    if image[i,j-1] > image[i,j] or image[i,j+1] > image[i,j]:
                        image[i,j] = 0
        return image
    def hysteresis(self,image,minVal=0.3,maxVal=.32):
            # hysteresis thresholding
        image = self.padding(self,image)
        image[image > maxVal] = 255
        image[image < minVal] = 0
        for i in range(1,image.shape[0]-1):
            for j in range(1,image.shape[1]-1):
                if image[i,j] < maxVal and image[i,j] > minVal:
                    if image[i-1,j-1] >= maxVal or image[i-1,j] >= maxVal or image[i-1,j+1] >= maxVal or image[i,j-1] >= maxVal or image[i,j+1] >= maxVal or image[i+1,j-1] >= maxVal or image[i+1,j] >= maxVal or image[i+1,j+1] >= maxVal:
                        image[i,j] = 255
                    else:
                        image[i,j] = 0
        return image
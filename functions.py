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
    def low_high_pass(image,selection,mask_size):
        x = 256-mask_size
        y = 256+mask_size
        img_fou = np.fft.fft2(image)
        img_fou = np.fft.fftshift(img_fou)
        if selection == "high":
            mask = np.ones((512,512))
            mask[x:y,x:y] = 0
        elif selection == "low":
            mask = np.zeros((512,512))
            mask[x:y,x:y] = 1
        new_fou = mask*img_fou
        new_fou = np.fft.ifftshift(new_fou)
        new_fou = np.fft.ifft2(new_fou)
        return np.abs(new_fou)
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
    def rgb_histogram(image): #cumulative
        r = image[:,:,0]
        g = image[:,:,1]
        b = image[:,:,2]
        plt.hist(r.ravel(),256,[0,256],color='r')
        plt.hist(g.ravel(),256,[0,256],color='g')
        plt.hist(b.ravel(),256,[0,256],color='b')
        plt.show()
    # Function to compute gray level histogram *distributive*
    def Gray_histogram_Compute(self,image):
        img_height = image.shape[0]
        img_width = image.shape[1]
        hist = np.zeros([256],np.int32)
        for x in range(0,img_height):
            for y in range(0,img_width):
                hist[image[x,y]] +=1
        np.savetxt("./saved_text/gray scale histogram.txt",hist)
        return hist
    # plotting the gray scale histogram *distributive* 
    def Gray_histogram_Plot(self,histogram):
        plt.figure()
        plt.title("Histogram Distribution Curve")
        plt.xlabel("Brightness")
        plt.ylabel("number of Pixels")
        plt.xlim([0,256]) # As gray scale levels vary from 0 -> 256
        plt.plot(histogram,'gray')
        plt.savefig("./saved_imgs/Gray_hisogram.jpg")
        return "Success"
    # histogram for RGB *distributive*
    def RGB_histogram(self,image):
        image_Height = image.shape[0]
        image_Width = image.shape[1]
        image_Channels = image.shape[2]
        histogram = np.zeros([256, image_Channels], np.int32)
        for x in range(0, image_Height):
            for y in range(0, image_Width):
                for c in range(0, image_Channels):
                        histogram[image[x,y,c], c] +=1
        return histogram
    #Plot the distributive RGB histogram each in separate plot
    def Plot_RGBHistogram(self,RGB_Histogram):
        # Separate Histograms for each color
        plt.subplot(3, 1, 1)
        plt.xlim([0, 256])
        plt.title("histogram of Blue")
        plt.plot(RGB_Histogram[:,0],'b')

        plt.subplot(3, 1, 2)
        plt.xlim([0, 256])
        plt.title("histogram of Green")
        plt.plot(RGB_Histogram[:,1],'g')
        
        plt.subplot(3, 1, 3)
        plt.xlim([0, 256])
        plt.title("histogram of Red")
        
        plt.plot(RGB_Histogram[:,2],'r')
        # for clear view
        plt.tight_layout()
        plt.savefig("./saved_imgs/RGB_histogram.jpg")
        return "success"
    # function to normalize the image
    def img_normalization(self,img):
        Min = np.min(img)
        Max = np.max(img)
        return (((img- Min)/((Max-Min)))) #stretching histogram equation from 0->255 to 0.0 -> 1.0
    

    #function to do sobel, roberts, prewitt and canny edge detection
    def edge_detection(self,image,method):
        image = self.rgb2gray(image)
        image = self.padding(image)

        if method == "sobel":
            Gx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
            Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])


        elif method == "canny":
            Gx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
            Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
            image = self.gaussian_filter(image)
       
        elif method == "roberts":
            Gx = np.array([[1,0],[0,-1]])
            Gy = np.array([[0,1],[-1,0]])

        elif method == "prewitt":
            Gx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
            Gy = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

        new_image = np.zeros((image.shape[0],image.shape[1]))
        for i in range(1,image.shape[0]-1):
            for j in range(1,image.shape[1]-1):
                Gx_value = np.sum((image[i-1:i+2,j-1:j+2]*Gx))
                Gy_value = np.sum((image[i-1:i+2,j-1:j+2]*Gy))
                new_image[i][j] = np.sqrt(Gx_value**2+Gy_value**2)


        
        return new_image
 
    # function to equalize the image
    def img_equalize(self,image):
        '''
        parameters:
        image: input image
        returns:
        img2: equalized image
        
        '''
        image = self.rgb2gray(image)
        hist = self.histogram_Compute(image)
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max()/ cdf.max()
        cdf_m = np.ma.masked_equal(cdf,0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
        cdf = np.ma.filled(cdf_m,0).astype('uint8')
        img2 = cdf[image]
        return img2
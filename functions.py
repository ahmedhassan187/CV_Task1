import matplotlib.pyplot as plt
import numpy as np
import cv2

import random
from scipy import ndimage
from scipy import signal


class Functions:
    def __init__(self):
        pass

    def noisy(noise_typ, image):
        if noise_typ == "gaussian":
            image = image/255
            row, col = image.shape
            mean = 0.0
            sigma = 0.2
            gauss = np.random.normal(mean, sigma, (row, col))
            gauss = gauss.reshape(row, col)
            image = image + gauss
            image = image * 255
            return image

        elif noise_typ == "s&p":
            row, col = image.shape
            number_of_pixels = random.randint(300, 10000)
            for i in range(number_of_pixels):
                y_coord = random.randint(0, row - 1)
                x_coord = random.randint(0, col - 1)
                image[y_coord][x_coord] = 255
            number_of_pixels = random.randint(300, 10000)
            for i in range(number_of_pixels):
                y_coord = random.randint(0, row - 1)
                x_coord = random.randint(0, col - 1)
                image[y_coord][x_coord] = 0
                return image

        elif noise_typ == 'uniform':
            row, col = image.shape
            image = image/255
            a = 0
            b = 0.2
            n = np.zeros((row, col), dtype=np.float64)
            for i in range(row):
                for j in range(col):
                    n[i][j] = np.random.uniform(a, b)
            image = image+n
            image = image * 255
            return image

    def display_image(self, image, name):
        image = np.array(image, dtype=np.uint8)
        cv2.imwrite(f'./static/imgs/{name}.jpg', image)

    def padding(self, image):
        padded_image = np.zeros((image.shape[0]+2, image.shape[1]+2))
        padded_image[1:image.shape[0]+1, 1:image.shape[1]+1] = image
        return padded_image

    def gkernel(self, kernel_size=3, sig=2):
        ax = np.linspace(-(kernel_size - 1) / 2.,
                         (kernel_size - 1) / 2., kernel_size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-0.5 * (np.square(xx) +
                        np.square(yy)) / np.square(sig))
        return kernel / np.sum(kernel)

    def average_filter(self, image_data, filter_size=3):
        filter = np.ones((filter_size, filter_size))/(filter_size)**2
        new_img = np.zeros((image_data.shape[0], image_data.shape[1]))
        new_img = signal.convolve2d(
            image_data, filter, mode='same', boundary='fill', fillvalue=0)
        return new_img

    def median_filter(self, image_data, filter_size=3):
        # padded = self.padding(self,image_data)
        new_img = np.zeros((image_data.shape[0], image_data.shape[1]))
        for i in range(image_data.shape[0]-1):
            for j in range(image_data.shape[1]-1):
                new_img[i][j] = np.median(
                    image_data[i:i+filter_size, j:j+filter_size])
        return new_img

    def gaussian_filter(self, image, kernel_size=3, sigma=2):
        kernel = self.gkernel(self, kernel_size, sigma)
        new_img = np.zeros((image.shape[0], image.shape[1]))
        new_img = signal.convolve2d(
            image, kernel, mode='same', boundary='fill', fillvalue=0)
        return new_img

    def low_high_pass(self, image, selection='low', mask_size=20):
        x = image.shape[0]//2-mask_size
        y = image.shape[1]//2+mask_size
        img_fou = np.fft.fft2(image)
        img_fou = np.fft.fftshift(img_fou)
        if selection == "high":
            mask = np.ones((image.shape[0], image.shape[1]))
            mask[x:y, x:y] = 0
        elif selection == "low":
            mask = np.zeros((image.shape[0], image.shape[1]))
            mask[x:y, x:y] = 1
        new_fou = mask*img_fou
        new_fou = np.fft.ifftshift(new_fou)
        new_fou = np.fft.ifft2(new_fou)
        return np.abs(new_fou)

    def rgb2gray(self, image):
        new_image = 0.299*image[:, :, 0]+0.587 * \
            image[:, :, 1]+0.114*image[:, :, 2]
        return new_image

    def hybrid(self, image1, image2, r1, r2):
        """image1: high filter image
        image2: low pass image"""
        # image1 = self.rgb2gray(self,image1)
        # image2 = self.rgb2gray(self,image2)
        image1 = self.low_high_pass(image1, 'low', r1)
        image2 = self.low_high_pass(image2, 'high', r2)
        new_image = image1+image2
        return new_image
    # Function to compute gray level histogram *distributive*

    def Gray_histogram_Compute(self, image):
        img_height = image.shape[0]
        img_width = image.shape[1]
        hist = np.zeros([256], np.int32)
        for x in range(0, img_height):
            for y in range(0, img_width):
                hist[image[x, y]] += 1
        return hist
    # plotting the gray scale histogram *distributive*

    def Gray_histogram_Plot(self, histogram, path):
        plt.figure()
        plt.title("Histogram Distribution Curve")
        plt.xlabel("Brightness")
        plt.ylabel("number of Pixels")
        plt.xlim([0, 256])  # As gray scale levels vary from 0 -> 256
        plt.plot(histogram, 'gray')
        plt.savefig(path)
        return "Success"
    # histogram for RGB *distributive*

    def RGB_histogram(self, image):
        image_Height = image.shape[0]
        image_Width = image.shape[1]
        image_Channels = image.shape[2]
        histogram = np.zeros([256, image_Channels], np.int32)
        for x in range(0, image_Height):
            for y in range(0, image_Width):
                for c in range(0, image_Channels):
                    histogram[image[x, y, c], c] += 1
        return histogram
    # Plot the distributive RGB histogram each in separate plot

    def Plot_RGBHistogram(self, RGB_Histogram, path):
        # Separate Histograms for each color
        plt.subplot(3, 1, 1)
        plt.xlim([0, 256])
        plt.title("histogram of Blue")
        plt.plot(RGB_Histogram[:, 0], 'b')

        plt.subplot(3, 1, 2)
        plt.xlim([0, 256])
        plt.title("histogram of Green")
        plt.plot(RGB_Histogram[:, 1], 'g')

        plt.subplot(3, 1, 3)
        plt.xlim([0, 256])
        plt.title("histogram of Red")

        plt.plot(RGB_Histogram[:, 2], 'r')
        # for clear view
        plt.tight_layout()
        plt.savefig(path)
        return "success"
    # function to normalize the image

    def img_normalization(self, img):
        Min = np.min(img)
        Max = np.max(img)
        # stretching histogram equation from 0->255 to 0.0 -> 1.0
        return (((img - Min)/((Max-Min))))

    # function to do sobel, roberts, prewitt and canny edge detection
    def edge_detection(self, image, method):
        # image = self.rgb2gray(image)
        image = self.padding(self, image)

        if method == "sobel":
            Gx, Gy = self.SobelFilter(self,image)
            Mag = np.hypot(Gx, Gy)
            return Mag

        elif method == "canny":
            return self.canny_edge(self, image)

        elif method == "roberts":
            Gx, Gy = self.RobertsFilter(self,image)
            Mag = np.hypot(Gx, Gy)
            return Mag

        elif method == "prewitt":
            Gx, Gy = self.PrewittFilter(self,image)
            Mag = np.hypot(Gx, Gy)
            return Mag
        
        pass

    def canny_edge(self, image, minVal=.1, maxVal=.15):
        # impelementing canny edge detection
        # image = self.rgb2gray(image)
        image = self.gaussian_filter(self, image, 3, 1)
        image = self.padding(self, image)
        gx, gy = self.SobelFilter(self, image)
        Mag = np.hypot(gx, gy)

        NMS = self.non_max_suppression(self, Mag)
        image = self.hysteresis(
            self, self.Normalize(self, NMS), minVal, maxVal)
        return image

    def SobelFilter(self, img):
        Gx = np.array([[-1, 0, +1], [-2, 0, +2],  [-1, 0, +1]])
        Res_x = ndimage.convolve(img, Gx)

        Gy = np.array([[-1, -2, -1], [0, 0, 0], [+1, +2, +1]])
        Res_y = ndimage.convolve(img, Gy)

        return self.Normalize(self, Res_x), self.Normalize(self, Res_y)
    
    
        def RobertsFilter(self,img):
        Gx = np.array([[1,0],[0,-1]])
        Gy = np.array([[0,1],[-1,0]])    
        Res_x = ndimage.convolve(img, Gx)

        Res_y = ndimage.convolve(img, Gy)

        return self.Normalize(Res_x), self.Normalize(Res_y)
    

    def PrewittFilter(self,img):
        Gx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        Gy = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])   
        Res_x = ndimage.convolve(img, Gx)

        Res_y = ndimage.convolve(img, Gy)

        return self.Normalize(Res_x), self.Normalize(Res_y)

    def Normalize(self, img):
        img = img/np.max(img)
        return img

    def non_max_suppression(self, image):
        # non max suppression
        image = self.padding(self, image)
        for i in range(1, image.shape[0]-1):
            for j in range(1, image.shape[1]-1):
                if image[i, j] == 0:
                    image[i, j] = 0
                elif image[i, j] == 45:
                    if image[i-1, j+1] > image[i, j] or image[i+1, j-1] > image[i, j]:
                        image[i, j] = 0
                elif image[i, j] == 90:
                    if image[i-1, j] > image[i, j] or image[i+1, j] > image[i, j]:
                        image[i, j] = 0
                elif image[i, j] == 135:
                    if image[i-1, j-1] > image[i, j] or image[i+1, j+1] > image[i, j]:
                        image[i, j] = 0
                else:
                    if image[i, j-1] > image[i, j] or image[i, j+1] > image[i, j]:
                        image[i, j] = 0
        return image

    def hysteresis(self, image, minVal=0.3, maxVal=.32):
        # hysteresis thresholding
        image = self.padding(self, image)
        image[image > maxVal] = 255
        image[image < minVal] = 0
        for i in range(1, image.shape[0]-1):
            for j in range(1, image.shape[1]-1):
                if image[i, j] < maxVal and image[i, j] > minVal:
                    if image[i-1, j-1] >= maxVal or image[i-1, j] >= maxVal or image[i-1, j+1] >= maxVal or image[i, j-1] >= maxVal or image[i, j+1] >= maxVal or image[i+1, j-1] >= maxVal or image[i+1, j] >= maxVal or image[i+1, j+1] >= maxVal:
                        image[i, j] = 255
                    else:
                        image[i, j] = 0
        return image

    # function to equalize the image

    def img_equalize(self, img):
        '''
        parameters:
        image: input image
        returns:
        img2: equalized image

        '''
        #image_1 = self.rgb2gray(self,img)
        hist = self.Gray_histogram_Compute(Functions, img)
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        img2 = cdf[img]
        return img2

    def thres_finder(self, img, thres=20, delta_T=1.0):
        # Step-2: Divide the images in two parts
        x_low, y_low = np.where(img <= thres)
        x_high, y_high = np.where(img > thres)

        # Step-3: Find the mean of two parts
        mean_low = np.mean(img[x_low, y_low])
        mean_high = np.mean(img[x_high, y_high])

        # Step-4: Calculate the new threshold
        new_thres = (mean_low + mean_high)/2

        # Step-5: Stopping criteria, otherwise iterate
        if abs(new_thres-thres) < delta_T:
            return new_thres
        else:
            return self.thres_finder(self, img, thres=new_thres, delta_T=1.0)

    def global_threshold(self, image, thres_value, val_high, val_low):
        img = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] > thres_value:
                    img[i, j] = val_high
                else:
                    img[i, j] = val_low
        return img

    def local_threshold(self, image, size):
        img = image.copy()
        i = 0
        j = 0
        while i < img.shape[0]:
            j = 0
            while j < img.shape[1]:
                x = i
                mean = 0
                cnt = 0
                while x < img.shape[0] and x < i+size:
                    y = j
                    while y < img.shape[1] and y < j+size:
                        cnt = cnt+1
                        mean = mean+img[x, y]
                        y = y+1
                    x = x+1
                mean = mean/(cnt)
                x = i
                while x < img.shape[0] and x < i+size:
                    y = j
                    while y < img.shape[1] and y < j+size:
                        if img[x, y] <= mean-5:
                            img[x, y] = 0
                        else:
                            img[x, y] = 255
                        y = y+1
                    x = x+1
                j = j+size
            i = i+size
        return img

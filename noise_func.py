import numpy as np
import os
import cv2
import random


def noisy(noise_typ, image):
    if noise_typ == "gaussian":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        image = image + gauss
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
        a = 0
        b = 0.2
        n = np.zeros((row, col), dtype=np.float64)
        for i in range(row):
            for j in range(col):
                n[i][j] = np.random.uniform(a, b)
        image = image+n
        return image

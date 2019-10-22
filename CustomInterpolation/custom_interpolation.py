from __future__ import division
import cv2
import numpy as np
import math



##最邻近插值
def nn_interpolate(image,scale_factor):
    (rows,cols,channels) = image.shape
    scaled_height = rows * scale_factor
    scaled_width = cols * scale_factor

    row_ratio = rows / scaled_height
    col_ratio = cols / scaled_width

    row_position = np.floor(np.arange(scaled_height) * row_ratio).astype(int)
    col_position = np.floor(np.arange(scaled_width) * col_ratio).astype(int)

    scaled_image = np.zeros((scaled_height, scaled_width,channels),np.uint8)

    for i in range(scaled_height):
        for j in range(scaled_width):
            scaled_image[i,j] = image[row_position[i],col_position[j]]
    return scaled_image

#双线性插值
def bilinear_interpolate(image,scaled_factor):
    '''

    '''
    return image

#三次插值
def Bicubic_interpolate(image,scaled_factor):
    return image

def main():
    image = cv2.imread('cameraman.jpg')
    bil = bilinear_interpolate(image, 2)
    nn = nn_interpolate(image, 2)
    bic = Bicubic_interpolate(image, 2)


    cv2.imshow('o', image)
    cv2.imshow('nn', nn)
    cv2.imshow('bil', bil)
    cv2.imshow('bic', bic)
    cv2.waitKey(0)

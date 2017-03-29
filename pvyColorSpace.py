# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:57:47 2017

@author: mimtiaz
"""

import numpy as np
import cv2



def adjust_gamma(image, gamma):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)



def pvyColorSpace(image):
    outputImg = image.copy()
    imageLAB = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    col = len(image[0])
    row = len(image)    

    #Process blue plane
    claheB = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2,2))
    imageLAB[:,:,1] = claheB.apply(imageLAB[:,:,1])
    gamma1 = 0.17
    processedBlue = adjust_gamma(imageLAB[:,:,1], gamma1)
    
    #Process green plane
    claheG = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(2,2))
    image[:,:,1] = claheG.apply(image[:,:,1])
    #gamma = 0.3
    gamma = 0.2
    processedGreen = adjust_gamma(image[:,:,1], gamma)    
    
    #Process red plane
    claheR = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
    image[:,:,2] = claheR.apply(image[:,:,2])
    gamma2 = 0.2
    processedRed = adjust_gamma(image[:,:,2], gamma2)   
    
    #Combine each processed planes
    for i in range(0, row):
        for j in range(0, col):
            outputImg[i,j,0] = processedBlue[i,j]
            outputImg[i,j,1] = processedGreen[i,j]
            outputImg[i,j,2] = processedRed[i,j]
            
    return outputImg
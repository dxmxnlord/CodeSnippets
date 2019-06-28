'''

  Code that removes bright tones from the image leaving darker tones thus useful for making amoled favoured wallpapers. 
   
  Thresholding: 
    * simple thresholding : For every pixel, the same threshold value is applied. If the pixel value is
                            smaller than the threshold, it is set to 0, otherwise it is set to a maximum
                            value. The function cv2.threshold is used to apply the thresholding. Here the 
                            inverse is used so pixel intensities below the threshold are kept.
                            
    * adaptive thresholding: When the image has different lighting conditions, the threshold constant
                             should differ per area. Hence we use adaptive thresholding. In this, the
                             algorithm calculates the threshold for a small regions of the image. If too
                             grainy increase size.
  
  Erosion: The kernel slides through the image (as in 2D convolution). A pixel in the
           original image (either 1 or 0) will be considered 1 only if all the pixels
           under the kernel is 1, otherwise it is eroded (made to zero).
           So what happends is that, all the pixels near boundary will be discarded
           depending upon the size of kernel. So the thickness or size of the foreground
           object decreases or simply white region decreases in the image. It is useful
           for removing small white noises, detach two connected objects etc. Use if 
           outline borders are too prevalent.
           
  Dilation: Opposite of erosion. Use to fill up patches in the image. 
  
  Smoothening : This is done by convolving the image with a normalized box filter. It simply
                takes the average of all the pixels under kernel area and replaces the central
                element with this average. Use if image is too sharp or rough or to spread out
                the colours.
                
 '''     
 
import os
import numpy as np 
import cv2
from matplotlib import pyplot as plt

#Inputs
directory=input('enter image directory : ')
output=input('output image name : ')
threshold_type=int(input('thresholding >> 1. regular 2. adaptive : '))

image=cv2.imread(directory,cv2.IMREAD_COLOR)
img=image
imggs=cv2.imread(directory,cv2.IMREAD_GRAYSCALE)
if(threshold_type == 1):
	threshold_value=int(input('threshold value : '))
	ret,mask=cv2.threshold(imggs,threshold_value,255,cv2.THRESH_BINARY_INV)
else:
	gaussian_size=int(input('filter size [ odd number ] : '))
	mask=cv2.adaptiveThreshold(imggs,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,gaussian_size,0)
erosion_factor=int(input('erosion factor; 0 for no erosion : '))
if(erosion_factor):
	kernel = np.ones((erosion_factor,erosion_factor),np.uint8)
	mask=cv2.erode(mask,kernel,iterations=1)
dilation_factor=int(input('dilation factor; 0 for no dilation : '))
if(dilation_factor):
	kernel = np.ones((dilation_factor,dilation_factor),np.uint8)
	mask=cv2.dilate(mask,kernel,iterations=1)
img=cv2.bitwise_and(img,img,mask = mask) 
blur_factor=int(input('smoothening factor; 0 for no smoothening : '))
if(blur_factor):
	img=cv2.blur(img,(blur_factor,blur_factor))
	img=cv2.bitwise_and(image,img) 
cv2.imwrite(output,img)
print('image saved. ')

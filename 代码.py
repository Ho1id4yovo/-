"""
in this code I use three methods to calculate the disparity of a pair of images
1.BM
2.SGBM
3.SAD
"""
#to import some package we need
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

#to load a pair of images 
imgL = cv2.imread("C:\\Users\\86183\\Pictures\\Saved Pictures\\view1.png",0)
imgR = cv2.imread("C:\\Users\\86183\\Pictures\\Saved Pictures\\view2.png",0)

####to show the images we load for testing
####cv2.imshow('imgL',imgL)
####cv2.imshow('imgR',imgR)
####cv2.waitKey(0)
####cv2.destroyAllWindows()

"""------------------------------BM----------------------------------------------------------------
with different matching window sizes.,use different similarity measures to achieve template matching
here are seven different matching blocksize for comparing
use the function of cv2.StereoBM_create to create block match objects
use the function of stereoBM.compute to calculate the disparity of the stereo image"""
stereo1 = cv2.StereoBM_create(numDisparities=16, blockSize=9)
disparity1 = stereo1.compute(imgL,imgR)

stereo2 = cv2.StereoBM_create(numDisparities=16, blockSize=11)
disparity2 = stereo2.compute(imgL,imgR)

stereo3 = cv2.StereoBM_create(numDisparities=16, blockSize=13)
disparity3 = stereo3.compute(imgL,imgR)

stereo4 = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity4 = stereo4.compute(imgL,imgR)

stereo5 = cv2.StereoBM_create(numDisparities=16, blockSize=17)
disparity5 = stereo5.compute(imgL,imgR)

stereo6 = cv2.StereoBM_create(numDisparities=16, blockSize=19)
disparity6 = stereo6.compute(imgL,imgR)

stereo7 = cv2.StereoBM_create(numDisparities=16, blockSize=21)
disparity7 = stereo7.compute(imgL,imgR)

#to show the disparity images
plt.imshow(disparity1,'gray')
plt.show()
plt.imshow(disparity2,'gray')
plt.show()
plt.imshow(disparity3,'gray')
plt.show()
plt.imshow(disparity4,'gray')
plt.show()
plt.imshow(disparity5,'gray')
plt.show()
plt.imshow(disparity6,'gray')
plt.show()
plt.imshow(disparity7,'gray')
plt.show()

"""----------------------------SGBM--------------------------------------------
define a function to manage the pair of image we set,in the function:
1.set the params
2.create the object
3.call functions in opencv to implementation algorithm
use the pair of images we load to calculate the disparity and show it  
"""
#define a function to calculate the disparity
def stereoMatchSGBM(left_image, right_image, down_scale=False):
    #set the SGBM matching params
    if left_image.ndim == 2:
        img_channels = 1
    else:
        img_channels = 3
    #blockSize = 3
    #blockSize=5
    blockSize=7
    param = {'minDisparity': 0,                                 #the minimum of disparity
             'numDisparities': 128,                             #the number of disparity
             'blockSize': blockSize,                            #the size of matching block
             'P1': 8 * img_channels * blockSize ** 2,
             'P2': 32 * img_channels * blockSize ** 2,
             'disp12MaxDiff': 1,
             'preFilterCap': 63,
             'uniquenessRatio': 15,                             #threshold for left and right consistency check
             'speckleWindowSize': 100,                          #window size when filtering connected domain size
             'speckleRange': 1,                                 #Range value during connected domain size filtering
             'mode': cv2.STEREO_SGBM_MODE_SGBM_3WAY
             }
 
    #create the SGBM objects using the function of cv2.StereSGBM_create
    stereo8 = cv2.StereoSGBM_create(**param)
    #using the function of compute to calculate the disparity
    disparity8 = stereo8.compute(imgL, imgR)
    #because the result of disparity is 16 times of the true disparity,so we need to calculate the true disparity
    trueDisp = disparity8.astype(np.float32) / 16.0
 
    return trueDisp
#using the pair of images we loaded before to calculate the disparity
trueDisp=stereoMatchSGBM(imgL,imgR)
plt.imshow(trueDisp/128,'gray')
plt.show()


"""----------------------------SAD--------------------------------------------
using SAD to calculate the disparity of a pair of image we read
1.read the images and show them
2.set the size of maximum of disparity and the window size,I set three different matching window sizes to test them one by one
3.calculate the disparity and show the disparity map 
"""                               
left_img = np.asanyarray(imgL) 
right_img = np.asanyarray(imgR)
left_img = np.asanyarray(left_img, dtype=np.double)     #transform the left image into double type
right_img = np.asanyarray(right_img, dtype=np.double)
img_size = np.shape(left_img)[0:2]                  #define an array whose size is the same as left image

plt.figure("the left image in grey")
plt.imshow(left_img)
plt.show()
plt.figure("the right image in grey")
plt.imshow(right_img)
plt.show()

t1 = time.time()      #record the start time
max_Disparty = 25       #the max disparity
#window_size = 3      #the first size of slide window  
#window_size = 5     #the second size of slide window
window_size = 7     #the third size of slide window
imgDiff = np.zeros((img_size[0], img_size[1], max_Disparty))   
e = np.zeros(img_size)
                       
for i in range(0, max_Disparty):
    e = np.abs(right_img[:, 0:(img_size[1]-i)]-left_img[:, i:img_size[1]])
    e2 = np.zeros(img_size)       #the sum of window_size
    for x in range(0, img_size[0]):
        for y in range(0, img_size[1]):
            e2[x, y] = np.sum(e[(x-window_size):(x+window_size), (y-window_size):(y+window_size)])
    imgDiff[:, :, i] = e2
    
dispMap = np.zeros(img_size)

for x in range(0,img_size[0]):
    for y in range(0,img_size[1]):
        val=imgDiff[x,y,:]
        min_index=np.argmin(val)
        dispMap[x,y]=min_index
plt.figure('the disparity image')
plt.imshow(dispMap,cmap='jet')
plt.colorbar()
plt.show()
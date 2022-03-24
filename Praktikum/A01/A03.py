'''
Assignment 03: Hybrid imaging
Group: Gruppe 6
Names: Felix Iltgen, Laura Moser, Alexander Reiprich
Date: 12.12.2021
Sources: GDV_tutorial_12
'''

# imports
import numpy as np
import cv2

# create point arrays
refPtSrc = []
refPtDst = [] 

# read images and resize them
image1 = cv2.imread("images\\image1.png", cv2.IMREAD_GRAYSCALE)
image1 = cv2.resize(image1, (474, 510))
image2 = cv2.imread("images\\image2.png", cv2.IMREAD_GRAYSCALE)
image2 = cv2.resize(image2, (474, 510))

# click function for first image
def clickSrc(event, x, y, flags, param):

    # grab references to the global variables
    global refPtSrc

    # if the left mouse button was clicked, add the point to the source array
    if event == cv2.EVENT_LBUTTONDOWN:        
        refPtSrc = [(x, y)]

        # draw a circle at the clicked position
        cv2.circle(image1, refPtSrc[0], 4, (0, 255, 0), 2)
        cv2.imshow('Image 1', image1)
        
        # show second image and set mouse callback
        cv2.namedWindow('Image 2')
        cv2.setMouseCallback('Image 2', clickDst)
        cv2.imshow("Image 2", image2)

# click function for second image
def clickDst(event, x, y, flags, param):
    # grab references to the global variables
    global refPtDst
    # if the left mouse button was clicked, add the point to the destination array
    if event == cv2.EVENT_LBUTTONDOWN:
        refPtDst = [(x, y)]

        # draw a circle at the clicked position
        cv2.circle(image2, refPtDst[0], 4, (0, 255, 0), 2)
        cv2.imshow('Image 2', image2)

        # show transformed image
        cv2.namedWindow('Image 2')
        cv2.imshow('Transformed image', createNewImage(image1, image2))

# apply highpass to image
def applyHighPass(img):
    return cv2.subtract(img, applyLowPass(img))

# apply lowpass to image
def applyLowPass(img):
    kernel = (25, 25)
    sigmaValue = 0
    return cv2.GaussianBlur(img, kernel, sigmaValue)

# translate images to overlap two selected points
def translateImages(image1, image2):
    # get selected points of the images
    offsetImg1 = refPtSrc[0]
    offsetImg2 = refPtDst[0]
    cols, rows = image1.shape

    # calculate point, where the selected points should overlap
    overlapPt = ((offsetImg1[0]+offsetImg2[0]) / 2, (offsetImg1[1]+offsetImg2[1]) / 2)

    # create translation matrices
    T_translationImg1 = np.float32([
    [1, 0, overlapPt[0] - offsetImg1[0]],
    [0, 1, overlapPt[1] - offsetImg1[1]],
    ])
    T_translationImg2 = np.float32([
    [1, 0, overlapPt[0] - offsetImg2[0]],
    [0, 1, overlapPt[1] - offsetImg2[1]],
    ])

    # apply transformations
    image1 = cv2.warpAffine(image1, T_translationImg1, (rows, cols))
    image2 = cv2.warpAffine(image2, T_translationImg2, (rows, cols))

    # return both images in an array
    return [image1, image2]

def createNewImage(image1, image2):
    # apply filters to both images and display them
    filteredImage1 = applyLowPass(image1)
    filteredImage2 = applyHighPass(image2)
    cv2.imshow("Image 1 - filtered", filteredImage1)
    cv2.imshow("Image 2 - filtered", filteredImage2)
    
    # translate images to overlap
    newImageArray = translateImages(filteredImage1, filteredImage2)

    # combine the filtered images to create the final hybrid image
    newImage = cv2.add(newImageArray[0], newImageArray[1])

    return newImage

# show first image and set mouse callback
cv2.namedWindow('Image 1')
cv2.setMouseCallback('Image 1', clickSrc)
cv2.imshow("Image 1", image1)

cv2.waitKey(0)
cv2.destroyAllWindows()
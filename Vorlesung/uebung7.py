import cv2
import numpy as np

### Goal: Count the number of green smarties in the images
# define green in HSV
hue = 60  # 60 is pure green / Farbraum geht bis 0-180
hue_range = 10
saturation = 155
saturation_range = 100
value = 155
value_range = 100
lower_green = np.array([hue - hue_range,saturation - saturation_range,value - value_range])
upper_green = np.array([hue + hue_range,saturation + saturation_range,value + value_range])

# load image
img = cv2.imread('smarties01.JPG',cv2.IMREAD_COLOR)
img = cv2.resize(img,(800,600))

# convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# create a mask
mask = cv2.inRange(hsv, lower_green, upper_green)

## morphological operations code
# optional mapping of values with morphological shapes
def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

# dilation with parameters
def dilatation(img,size,shape): 
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.dilate(img, element)

# dilation with parameters
def erosion(img,size,shape): 
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.erode(img, kernel)

# dilation with parameters
def opening(img,size,shape): 
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)

# dilation with parameters
def closing(img,size,shape): 
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.morphologyEx(img,cv2.MORPH_CLOSE, kernel)


# morphological operations (see https:)
kernel_size = 7
kernel_shape = morph_shape
mask = cv2.dilate(mask,kernel)


# find connected components
connectivity = 8
(numlabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(mask,connectivity, cv2.CV_32S)

# print out number of connected components
print('We have found ',str(numlabels),' green smarties.')


# find center of mass and draw a mark in the original image
red_BGR = (0,0,255)
circle_size = 10
circle_thickness = 5
min_size = 10

# go through all (reasonable) found connected components
for i in range(1,numlabels):
    # check size and roundness as plausibility
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    if w < min_size or h < min_size:
        print ('Found a too small component.')
        num_rejected += 1
        continue # found component is too small to be correct 
    if w > h:
        roundness = 1.0 / (w/h)
    elif h > w:
        roundness = 1.0 / (h/w)  
    if (roundness > 2):
        print ('Found a component that is not round enough.')
        break # ratio of width and height is not suitable

    # find and draw center
    center = centroids[i]
    center = np.round(center)
    center = center.astype(int)
    cv2.circle(img,center,circle_size,red_BGR,circle_thickness)

    # find and draw bounding box
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3) 



# show the original image with drawings in one window
cv2.imshow('Original image', img)
# show the masked image in another window

# show the mask image in another window
cv2.imshow('Mask image', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''
Assignement 02: Object counting
Group: Gruppe 6
Names: Felix Iltgen, Laura Moser, Alexander Reiprich
Date: 15.11.2021
Sources: -
'''

import cv2
import numpy as np
import glob  # for loading all images from a directory

# Goal: Count the number of all colored balls in the images

# ground truth
num_yellow = 30
num_blue = 5 
num_pink = 8
num_white = 10
num_green = 2
num_red = 6
gt_list = (num_red, num_green, num_blue, num_yellow, num_white, num_pink)

# define color ranges in HSV, note that OpenCV uses the following ranges H: 0-179, S: 0-255, V: 0-255

# create class Color, which includes all necessary values
class Color:
    def __init__(self, hue, hue_range, saturation, saturation_range, value, value_range, kernel_size, min_size):
        self.hue = hue
        self.hue_range = hue_range
        self.saturation = saturation
        self.saturation_range = saturation_range
        self.value = value
        self.value_range = value_range
        self.kernel_size = kernel_size
        self.min_size = min_size

# create dictionary for every color and initiate their values
colorDict = {
    "red": Color(0, 2, 170, 8, 154, 25, 10, 10),
    "green": Color(54, 10, 190, 20, 180, 70, 7, 10),
    "blue": Color(86, 17, 70, 38, 73, 65, 6, 5),
    "yellow": Color(35, 7, 130, 30, 255, 0, 7, 10),
    "white": Color(38 , 8, 5, 4, 255, 3, 3, 5),
    "pink": Color(4, 4, 142, 110, 230, 20, 4, 22),
}

# morphological operations
# optional mapping of values with morphological shapes


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

# dilation with parameters


def dilatation(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.dilate(img, element)

# erosion with parameters


def erosion(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.erode(img, element)

# opening


def opening(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

# closing


def closing(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)


# set color
num_colors = 6
color_names = ['red', 'green', 'blue', 'yellow', 'white', 'pink']

num_test_images_succeeded = 0

# iterate through images
for img_name in glob.glob('images/chewing_gum_balls*.jpg'):

    print('Searching for colored balls in image:', img_name)

    all_colors_correct = True

    # iterate through colors
    for c in range(0, num_colors):

        # load image
        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        height = img.shape[0]
        width = img.shape[1]

        # convert colors to HSV
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # create mask
        current_color = colorDict.get(color_names[c])
        lower_range_color = np.array([current_color.hue - current_color.hue_range, current_color.saturation -
                                     current_color.saturation_range, current_color.value - current_color.value_range])
        upper_range_color = np.array([current_color.hue + current_color.hue_range, current_color.saturation +
                                     current_color.saturation_range, current_color.value + current_color.value_range])
        mask = cv2.inRange(hsv_img, lower_range_color, upper_range_color)

        # create kernel
        kernel_size = current_color.kernel_size
        kernel_shape = morph_shape(2)
        mask = closing(mask, kernel_size, kernel_shape)
        mask = dilatation(mask, kernel_size, kernel_shape)

        # set connectivity, connect components
        connectivity = 8
        (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(
            mask, connectivity, cv2.CV_32S)

        # set the color for the shapes that mark the found elements
        green_BGR = (0, 255, 0)
        red_BGR = (0, 0, 255)

        # set values to check eligibility
        min_size = current_color.min_size
        roundness = 0

        # set counters
        num_labels = 0 
        num_rejected = 0
        
        # iterate through found elements
        for i in range(1, numLabels):
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            
            # check shape
            if w < min_size or h < min_size:
                num_rejected += 1
                continue
            if w > h:
                roundness = 1.0 / (w/h)
            elif h > w:
                roundness = 1.0 / (h/w)
            if (roundness > 2):
                num_rejected += 1
                continue  # ratio of width and height is not suitable

            # find and draw bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), green_BGR, 3)

            # find and draw center
            center = centroids[i]
            center = (np.round(center)).astype(int)
            cv2.circle(img, center, 7, red_BGR, 2)

            num_labels += 1

        # calculate final amount of found elements
        num_final_labels = num_labels-num_rejected

        success = (num_final_labels == int(gt_list[c]))

        # print message for each case
        # Case one: All elements are found
        if success:
            print('We have found all', str(num_final_labels), '/',
                  str(gt_list[c]), color_names[c], 'chewing gum balls. Yeah!')
            foo = 0
        
        # Case two: Too many elements were found
        elif (num_final_labels > int(gt_list[c])):
            print('We have found too many (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False

        # Case three: Not enough elements were found
        else:
            print('We have not found enough (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False

        # debug output of the test images
        if ((img_name == 'images\chewing_gum_balls02.jpg')
            or (img_name == 'images\chewing_gum_balls08.jpg')
                or (img_name == 'images\chewing_gum_balls12.jpg')):
            # show the original image with drawings in one window
            cv2.imshow("Original Image - " + str(color_names[c]), img)
            # show the mask in a separate window
            cv2.imshow('Masked  - ' + str(color_names[c]), mask)

            cv2.waitKey(0)
            cv2.destroyAllWindows() 

    # print message if all colors have been correctly identified
    if all_colors_correct:
        num_test_images_succeeded += 1
        print('Yeah, all colored objects have been found correctly in ', img_name)

# print message if all pictures have been corre
print('Test result:', str(num_test_images_succeeded), 'test images succeeded.')
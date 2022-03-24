'''
Assignement 02: Object counting
Group: Gruppe 6
Names: Felix Iltgen, Laura Moser, Alexander Reiprich
Date: <Date of last changes>
Sources: keine :]
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


class Color:
    def __init__(self, hue, hue_range, saturation, saturation_range, value, value_range):
        # cv2.cvtColor(np.uint8([b, g, r]), cv2.COLOR_BGR2HSV)[0][0][0]
        self.hue = hue
        self.hue_range = hue_range
        self.saturation = saturation
        self.saturation_range = saturation_range
        self.value = value
        self.value_range = value_range


colorDict = {
    "red": Color(0, 1, 185, 30, 135, 25),
    "green": Color(51, 7, 180, 20, 180, 90),
    "blue": Color(94, 20, 71, 30, 66, 60 ),
    "yellow": Color(35, 7, 130, 30, 255, 0),
    "white": Color(0, 10, 0, 25, 255, 15),
    "pink": Color(4, 2, 119, 3, 250, 10),
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


# set color under test
num_colors = 6
color_names = ['red', 'green', 'blue', 'yellow', 'white', 'pink']

# setting the parameters that work for all colors

# set individual (per color) parameters

num_test_images_succeeded = 0
for img_name in glob.glob('images/chewing_gum_balls*.jpg'):
    # load image
    print('Searching for colored balls in image:', img_name)

    all_colors_correct = True

    for c in range(0, num_colors):

        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        height = img.shape[0]
        width = img.shape[1]

        # TODO: Insert your algorithm here

        # convert to HSV
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # create mask
        current_color = colorDict.get(color_names[c])
        lower_range_color = np.array([current_color.hue - current_color.hue_range, current_color.saturation -
                                     current_color.saturation_range, current_color.value - current_color.value_range])
        upper_range_color = np.array([current_color.hue + current_color.hue_range, current_color.saturation +
                                     current_color.saturation_range, current_color.value + current_color.value_range])
        mask = cv2.inRange(hsv_img, lower_range_color, upper_range_color)

        kernel_size = 10
        kernel_shape = morph_shape(2)
        mask = closing(mask, kernel_size, kernel_shape)
        mask = dilatation(mask, kernel_size, kernel_shape)

        connectivity = 4
        (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(
            mask, connectivity, cv2.CV_32S)
        green_BGR = (0, 255, 0)
        min_size = 10

        num_labels = 0  # TODO: implement something to set this variable | found balls
        num_rejected = 1

        for i in range(1, numLabels):
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            roundness = 0
            if w > h:
                roundness = 0 / (w/h)
            elif h > w:
                roundness = 1.0 / (h/w)
            if (roundness > 5):
                print('Found a component that is not round enough.')
                num_rejected += 1
                continue  # ratio of width and height is not suitable

            # find and draw center

            # find and draw bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), green_BGR, 3)
            num_labels += 1

        num_final_labels = num_labels-num_rejected

        success = (num_final_labels == int(gt_list[c]))

        if success:
            print('We have found all', str(num_final_labels), '/',
                  str(gt_list[c]), color_names[c], 'chewing gum balls. Yeah!')
            foo = 0
        elif (num_final_labels > int(gt_list[c])):
            print('We have found too many (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False
        else:
            print('We have not found enough (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False

        # debug output of the test images
        if ((img_name == 'images\chewing_gum_balls01.jpg')
            or (img_name == 'images\chewing_gum_balls04.jpg')
                or (img_name == 'images\chewing_gum_balls06.jpg')):
            # show the original image with drawings in one window
            cv2.imshow('Original image', img)
            # show other images?
            cv2.imshow('Masked image', mask)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    if all_colors_correct:
        num_test_images_succeeded += 1
        print('Yeah, all colored objects have been found correctly in ', img_name)

print('Test result:', str(num_test_images_succeeded), 'test images succeeded.')
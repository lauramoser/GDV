# Edge detection on an example image

import numpy as np
import cv2

def showImagesSideBySide(img_A, img_B):
    '''Helper function to draw two images side by side'''
    cv2.imshow(window_name, np.concatenate((img_A, img_B), axis=1))


# TODO: Define callback function
def onSliderChange(self):
    '''callback function for the sliders'''
    # read slider positions
    value_blur = cv2.getTrackbarPos(trackbar_blur, window_name)
    value_lower = cv2.getTrackbarPos(trackbar_lower, window_name)
    value_upper = cv2.getTrackbarPos(trackbar_upper, window_name)
    # blur the image
    blurred_img = cv2.blur(img, (value_blur, value_blur))
    # blurred_img = img
    # run Canny edge detection with thresholds set by sliders
    canny = cv2.Canny(blurred_img, value_lower, value_upper)
    # show the resulting images in one window
    showImagesSideBySide(blurred_img, canny)


# TODO: load example image as grayscale
img = cv2.imread('images\\nl_clown.jpg', cv2.IMREAD_GRAYSCALE)
# resize if needed
img = cv2.resize(img, (400, 400), interpolation=cv2.INTER_CUBIC)
# clone if needed


# TODO: initial Canny edge detection result creation


# TODO: create window with sliders
# define a window name
window_name = 'Canny edge detection demo'

# show the resulting images in one window
showImagesSideBySide(img, img)
# create trackbars (sliders) for the window and define one callback function
trackbar_blur = "Blur"
trackbar_lower = "T_lower"
trackbar_upper = "T_upper"
cv2.createTrackbar(trackbar_blur, window_name, 0, 50, onSliderChange)
cv2.createTrackbar(trackbar_lower, window_name, 0, 300, onSliderChange)
cv2.createTrackbar(trackbar_upper, window_name, 0, 300, onSliderChange)

# wait until a key is pressed and end the application
cv2.waitKey(0)
cv2.destroyAllWindows()
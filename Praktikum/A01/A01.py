import cv2
import numpy as np

# set height and width for the image
height = 765
width = 765
size = (width, height)

# generate empty image
img = np.zeros(size, np.uint8)

# fill empty image with gradient
# further explanation of the for-loop can be found in the readme.md
lastJ = 0
for j in range (width):
    if j%3 == 0:
        img[:,j] = width-j/3
        lastJ = j
    else:
        img[:,j] = width-lastJ/3

# select square that is going to be copied
copiedSquare = img[332:432, 332:432]

# paste the square in different spots
img[50:150,50:150] = copiedSquare
img[600:700,600:700] = copiedSquare

# initialize video output
output = cv2.VideoWriter('illusion.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (765,765))

# animation
for i in range (width):
    # clean up gradiant
    img[332:432,:] = img[500:600,:]

    # paste moving square to new location
    img[332:432,0+i:100+i] = copiedSquare

    # save frame
    cv2.imwrite('frame.jpg', img)

    # show the image
    title = "Assignment #1 - Optical Illusion"
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, img)
    cv2.waitKey(2)

    # put the frame into the video
    output.write(cv2.imread("frame.jpg"))

# render video
output.release()
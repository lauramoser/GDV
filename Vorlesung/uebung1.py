import cv2

img = cv2.imread('HFU_logo.svg.png', cv2.IMREAD_COLOR)

cv2.imwrite('img_out.png', img)

title = "Hello OpenCV"
cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(title, img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
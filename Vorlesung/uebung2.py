import cv2
import numpy as np

#loading images in grey and color
img_color = cv2.imread('HFU_logo.svg.png', cv2.IMREAD_COLOR )
img_gray = cv2.imread('HFU_logo.svg.png', cv2.IMREAD_GRAYSCALE)

#line to switch the image between color and grayscale
cv2
img = img_gray
#do some point out about the loades data
print(type(img))
print(img.shape)

#Extract the sice or resolution of the image / jeder einzelne Wert ist aus Höhe und Breite definiert
width = img.shape[1]
height = img.shape[0]

#set area of the image to black 
for i in range (30,60):    
    for j in range (20,40):
        img[i][j] = 0 #BGR Farbmodell

#img[100][100] = 0 ein Punkt im Bild schwarz machen
#kleiner Teil in schwarz wenn es nur eine Zahl ist dann fängt es oben links an bei (30,60)/(20,40) fängt es mittendrin an 
#img = np.zeros((800,800))


#find all used colors in the image 
colors = []
for i in range (width):    
    for j in range (height):
        current_color= img[j][i]
        if colors.count(current_color) == 0:
            colors.append(current_color)
print(colors)
#'count' überprüft ob der Wert schon enthalten ist --> nicht sicher

#copy one part of an image into another one 
letters= img[30:105, 5:130]
img[115:188,150:275] = letters

#print frist row = print(img[0])

#print first column = print(img[:][0]) 

#show the image
title = "Hello OpenCV"
cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(title, img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
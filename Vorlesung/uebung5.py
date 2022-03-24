import cv2
import math
import operator

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
width = int(cap.get(cv2.cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT))
codec = int(cap.get(cv2.cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
print ('Video properties:')
print ('  Width = ' + str(width))
print ('  Height = ' + str(height))
print ('  Codec = ' + str(codec))

# drawing helper variables
## thickness
thick = (10)
thin = (2)

## color
blue = (255,0,0)


## fonts


# variables for moving rectangle
def circle_path(t,scale, offset)
    res = (int(scale*math.cos(t)+offset),int(scale*math.sin(t)+offset))
    return res
timer = 0.0

# start a loop
while True:
    # capture the image
    ret, frame = cap.read()
    # check if capture succeeded
    if (ret):
        
        # draw a blue diagonal cross over the image
        ptleft = (0,0)
        pt_bottomright = (width, height)
        pt_topright = (width, 0)
        pt_bottomleft = (0, height)
        cv2.line(frame, ptleft, pt_bottomright, blue, thick)
        cv2.line(frame, pt_topright,  pt_bottomleft, blue, thick)
        # draw a circle
       
        # write some text
        
        # draw arrows (potential assignment)
       

        # draw a rectangle that moves on a circular path
        timer += 0.01
        pt1= circle_path(timer,100,300)
        pt2= (width)
        cv2.rectangle(frame, pt1, pt2, thin) #noch nicht fertig!!

        # display the image
        cv2.imshow('Video image', frame)

        # press q to close the window
        if cv2.waitKey(10) == ord('q'): 
            break
    else:
        print('Could not start video camera')
        break

# release the video capture object and window
cap.release()
cv2.destroyAllWindows()
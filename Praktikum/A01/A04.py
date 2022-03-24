'''
Assignment 04: Object Detection
Group: Gruppe 6
Names: Felix Iltgen, Laura Moser, Alexander Reiprich
Date: 12.01.2022
Sources: GDV_tutorial_19
'''

import cv2
import time
import numpy as np

# load the COCO class names
with open('uebung4/models/object_detection_classes_coco.txt',
          'r',
          encoding="utf-8"
          ) as f:
    class_names = f.read().split('\n')
# DEBUG: print(class_names)

# generate a different color array for each of the classes
colors = np.random.uniform(0, 255, size=(len(class_names), 3))

# define objects that are supposed to be identified
objectArray = ["banana", "wine glass", "scissors", "potted plant"]

# set number of frames to zero, so that they can be incremeneted
allFrames = 0
correctFrames = 0

# load the DNN model
net = cv2.dnn.readNet(model='uebung4/models/frozen_inference_graph_ssd.pb',
                      config='uebung4/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt',
                      framework='TensorFlow')

# capture the video
cap = cv2.VideoCapture('uebung4/videos/source.mp4')

# get the video frames' width and height for proper saving of videos
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# create the `VideoWriter()` object
do_write_video = True
if do_write_video:
    out = cv2.VideoWriter('uebung4/video_result.mp4',
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          30,
                          (frame_width, frame_height))

# initialize window and helper variables
cv2.namedWindow('Object Detection', cv2.WINDOW_GUI_NORMAL)
conf_thresh = 0.41
max_object_size = 0.8

# detect objects in each frame of the video
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        image = frame
        image_height, image_width, _ = image.shape
        # create blob from image
        blob = cv2.dnn.blobFromImage(image=image,
                                     size=(320, 240),
                                     mean=(104, 117, 123),
                                     swapRB=True)
        # start time to calculate FPS
        start = time.time()
        # set the blob as input
        net.setInput(blob)
        # compute the output by forward inference
        output = net.forward()
        # loop over each of the detections
        for detection in output[0, 0, :, :]:
            # extract the confidence of the detection
            confidence = detection[2]
            # draw bounding boxes only if the detection confidence is above
            # a certain threshold, else skip
            if confidence > conf_thresh:
                # get the class id
                class_id = detection[1]
                # map the class id to the class
                class_name = class_names[int(class_id)-1]
                color = colors[int(class_id)-1]
                # get the bounding box coordinates
                box_x = detection[3] * image_width
                box_y = detection[4] * image_height
                # get the bounding box width and height
                box_width = detection[5] * image_width
                box_height = detection[6] * image_height
                # check if object is too large
                if ((detection[5] > max_object_size) or
                   (detection[6] > max_object_size)):
                    # DEBUG: print('Object is too big.')
                    continue
                # draw a rectangle around each detected object
                cv2.rectangle(image, (int(box_x), int(box_y)), (int(
                    box_width), int(box_height)), color, thickness=2)
                # put the class name text and the confidence on the detected
                # object
                output_text = class_name + ' %.2f' % confidence
                cv2.putText(image, output_text, (int(box_x), int(
                    box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
                # iterate through the objects that are supposed to be identified
                for i in range (len(objectArray)):
                    # if the name of the identified object is the same as the object in the array,
                    # increment the number of correctly identified frames by 1
                    if (class_name == objectArray[i]):
                        correctFrames += 1
                # print(class_name)
            else:
                # detection results are sorted, hence after first object
                # under threshold, we can exit the for loop
                break

        # end time after detection
        end = time.time()
        # calculate the FPS for current frame detection
        fps = 1 / (end-start)
        # put the FPS text on top of the frame
        cv2.putText(image, f"{fps:.2f} FPS", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # show the image with the results
        cv2.imshow('Object Detection', image)
        
        # increment frame counter by 1
        allFrames +=  1
        # write the video if intended
        if do_write_video:
            out.write(image)
        # abort with 'q'
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    else:
        break

# release the video capture
cap.release()
# write the correctly identified frames in a file
f = open("uebung4/frames.txt", "w")
content = "All Frames - " + str(allFrames) + "\n Correct Frames - " + str(correctFrames) + "\n Incorrect Frames - " + str(allFrames - correctFrames)
f.write(content)
# close all windows
cv2.destroyAllWindows()
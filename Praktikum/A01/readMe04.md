# gdv-Aufgabe04

This program can detect multiple objects within a video using the frozen interfence SSD module with the MobileNet SDD config, which includes the objects and their recognition. 
The detected objects are displayed on the output video.

We used the library of numpy version 1.21.2 and opencv version 4.5.3.56 to help with this task. 
The Python version that was used is 3.9.7.

To be able to use this program, the folder in which the .py file is stored must contain a video that is named
"source.mp4"

After the .py file is executed, a file called "video_result.mp4" is generated, which includes the rendered video.
A file called "frames.txt" is also generated, which lists the number of frames that were correctly identified.
This is only applicable to our video, as the objects in the video are listed in an array inside the code.

---

Group 6 - Felix Iltgen, Alexander Reiprich, Laura Moser
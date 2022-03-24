# gdv-Aufgabe01

The code shows an digital illusion where the brightness of a square seems to change depending on the position on the color gradient.

## Prerequisites
We used the library of [NumPy](https://numpy.org/) and [OpenCV](https://opencv.org/) to help with this task.

## Generating the image
At first we set the size of the image.

The size of the image is three times more than the range of the brightness on one pixel

(0-255, file is 255 * 3= 765 pixels) 

This results in a bigger picture to see the illusion in higher quality and it makes it easier to calculate the gradient as you can increase the brightness by one every three pixels.

Using this size we generate a blank image.

## Generating the gradient

To get the background gradient for the illusion we used a for-loop that iterates through the width of the image.

The variable "j" describes the position on the x-axis of the image.
Every third pixel, modulo of the current position divided by 3 equals zero, so we set theis pixel column to the next higher brightness level.
This brightness value is temporarily stored in the variable LastJ, so that the following two pixels keep this brightness level.

## Creating a static version of the illusion

In the following three lines a square in the center of the image is copied and pasted into the upper left and lower right corners of the picture to show a static version of the illusion.

## Creating the animation

The next big part is the animation where the middle square travels from the left to the right side of the gradient. 
In line 30 the output is generated which we use in the loop starting in line 33.

In this for loop we iterate through the whole width again.
The first thing that is done in the loop is the "cleaning" of the gradient.
All pixels between the heights 500 and 600 are copied onto the path where the square will be traveling. This gets rid of the square that has been pasted in in the previous iteration.
In the next line, the middle square is pasted onto the path. The x-position is determined by the variable i that is iterating through the width of the image, resulting in the square moving right during the animation.
After the square has been placed, a single image is exported as "frame.jpg" which is then shown in a window, that is created in the lines 44 to 46.

That frame is then added to the output in line 50, which will render the final video.
This procedure is then repeated until the variable i has reached the value of the width of the image.

The last line in the code releases the video.

---

Group 6 - Felix Iltgen, Laura Moser, Alexander Reiprich
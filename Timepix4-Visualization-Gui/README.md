# Timepix4-Visualization-Gui
I designed a GUI program that has functionality that both event and frame mode images
can be visualized. The event data includes the energy level of the incoming particle, the
timestamp of the particle when it hits the detector, and the coordinates of the pixel
which is hit. The algorithm behind the showing images in event mode is that after
processing raw data, it sorts events according to their timestamps behind and creates
images for every unique timestamp. The GUI has a slider on the left side which can
be used the visualize images according to the timestamps. On the right side, there is
a video label that makes a video of this list of events. Additionally, I
also added an option combobox which can be used to see only the count values of pixels
during the acquisition time and it will ignore the timestamps. On The second tab of the
GUI has frame mode visualization which can be used to illustrate frames from multiple
files. It is possible the change mode of files with using another combobox in the second
tab. As the images progress, it prints file names on the list and visualizes them. After
uploading process finishes, if one left click 2 times to the file names, it is possible to
see image at the right side which belongs to this file. There is a save button that can
be used to save all images in a sub folder. I also added a progress bar to illustrate the
situation of the program.

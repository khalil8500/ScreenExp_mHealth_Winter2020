import cv2
import numpy as np
import os

if __name__ == '__main__':
    from os.path import isfile, join

    pathIn = 'data/video1' \
             '/video1/'
    pathOut = 'video1' \
              '.avi'
    fps = 1.5

    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    # for sorting the file names properly
    print(files[0][0:9])
    files.sort(key=lambda x: float(x[0:9])+float(x[10:-4])/1000)
    files.sort()
    print(files[0])

    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    # for sorting the file names properly
    files.sort(key=lambda x: float(x[0:9])+float(x[10:-4])/1000)

    for i in range(len(files)):
        print(files[i])
        filename = pathIn + files[i]
        # reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)

        # inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
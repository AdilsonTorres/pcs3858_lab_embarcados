import sys,os,time,csv,getopt,cv2,argparse
from datetime import datetime
import numpy as np
from ObjectWrapper import *
from Visualize import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', dest='graph', type=str,
                        default='graph', help='MVNC graphs.')
    parser.add_argument('--image', dest='image', type=str,
                        help='An image path.')
    parser.add_argument('--video', dest='video',
                        default=0, help='A video path.')
    parser.add_argument("--display", help='Display video', action='store_true')
    args = parser.parse_args()

    network_blob=args.graph
    imagefile = args.image
    videofile = args.video

    detector = ObjectWrapper(network_blob)
    stickNum = ObjectWrapper.devNum

    if imagefile:
        # image preprocess
        img = cv2.imread(imagefile)
        start = datetime.now()

        results = detector.Detect(img)

        end = datetime.now()
        elapsedTime = end-start

        print ('total time is " milliseconds', elapsedTime.total_seconds()*1000)
        if args.display:
            imdraw = Visualize(img, results)
            cv2.imshow('Demo',imdraw)
            cv2.imwrite('test.jpg',imdraw)
            cv2.waitKey(10000)
    elif videofile is not None:
        # video preprocess
        cap = cv2.VideoCapture(0)
        fps = 0.0
        max_person_counter = 0
        while cap.isOpened():
            start = time.time()
            imArr = {}
            results = {}
            for i in range(stickNum):
                ret, img = cap.read()
                if i not in imArr:
                    imArr[i] = img
            if ret == True:
                tmp = detector.Parallel(imArr)
                for i in range(stickNum):
                    if i not in results:
                        results[i] = tmp[i]

                    person_counter = 0
                    for j in range(len(results[i])):
                        if results[i][j].name == 'person':
                            person_counter += 1
                    if person_counter > max_person_counter:
                        max_person_counter = person_counter
                        update_person_number(person_counter)

                    if args.display:
                        imdraw = Visualize(imArr[i], results[i])
                        fpsImg = cv2.putText(imdraw, "%.2ffps" % fps, (70, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                        cv2.imshow('Demo', fpsImg)
                end = time.time()
                seconds = end - start
                fps = stickNum / seconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

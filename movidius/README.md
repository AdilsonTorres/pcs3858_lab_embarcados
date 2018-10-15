## To run
```
python person_detector.py --graph graphs/mobilenetgraph_v2 --display 1
```

Without Movidius (inside pi_object_detection folder):
```
python real_time_object_detection.py \
	--prototxt MobileNetSSD_deploy.prototxt.txt \
	--model MobileNetSSD_deploy.caffemodel
```

## To compile a graph model
```
mvNCCompile models/MobileNetSSD_deploy.prototxt -w models/MobileNetSSD_deploy.caffemodel -s 12 -is 300 300 -o graphs/mobilenetgraph_v2
```

## References
https://www.pyimagesearch.com/2018/02/19/real-time-object-detection-on-the-raspberry-pi-with-the-movidius-ncs/ 
https://www.pyimagesearch.com/2017/10/16/raspberry-pi-deep-learning-object-detection-with-opencv/

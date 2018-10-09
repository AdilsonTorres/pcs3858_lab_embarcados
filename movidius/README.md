## To run
```
python person_detector.py --graph graphs/mobilenetgraph_v2 --display 1
```

## To compile a graph model
```
mvNCCompile models/MobileNetSSD_deploy.prototxt -w models/MobileNetSSD_deploy.caffemodel -s 12 -is 300 300 -o graphs/mobilenetgraph_v2
```
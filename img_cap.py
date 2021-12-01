import cv2

vcap = cv2.VideoCapture("rtsp://192.168.1.1:554/MJPG?W=1920&H=1080&Q=50&BR=5000000/track1")
vcap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1920
height = 1080
vcap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
ret, frame = vcap.read()
cv2.imshow('VIDEO', frame)
cv2.imwrite("./img/camcap.jpg",frame)
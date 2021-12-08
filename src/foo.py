import cv2
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QMainWindow

def updateImg():
    ret,orig_img = vcap.read()
    disp_img = cv2.resize(orig_img,(label.width(),label.height()),interpolation= cv2.INTER_AREA)
    disp_img = QtGui.QImage(disp_img.data, disp_img.shape[1], disp_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
    label.setPixmap(QtGui.QPixmap.fromImage(disp_img))

app = QApplication(sys.argv)

window = QWidget()
label = QLabel(parent=window)
label.resize(1280,720)
vcap = cv2.VideoCapture("rtsp://192.168.1.1:554/MJPG?W=720&H=400&Q=50&BR=5000000/track1")
timer = QtCore.QTimer()
timer.timeout.connect(updateImg)
timer.start(1)

window.show()

sys.exit(app.exec_())





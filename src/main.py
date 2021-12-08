import sys
import time
import datetime
import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QMainWindow
from mainwindow import Ui_MainWindow

# class FullScreenButton(QPushButton):
    
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.paddingLeft = 5
#         self.paddingTop = 5
#         self.resize(48,48)
#         self.pix = QtGui.QPixmap(QtGui.QPixmap("../img/fullscreen.png"))
#         self.pix.scaled(48,48,QtCore.Qt.KeepAspectRatio)
#         self.icon = QtGui.QIcon(self.pix)
#         self.setIcon(self.icon)
#         self.setIconSize(QtCore.QSize(48,48))
#         self.setStyleSheet("background-color: transparent;")

#     def update_position(self): 
#         if hasattr(self.parent(), 'viewport'):
#             parent_rect = self.parent().viewport().rect()
#         else:
#             parent_rect = self.parent().rect()

#         if not parent_rect:
#             return

#         x = parent_rect.width() - self.width() - self.paddingLeft
#         y = self.paddingTop 
#         self.setGeometry(x, y, self.width(), self.height())

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self.update_position()

#     def changeIcon(self,img_path):
#         self.pix = QtGui.QPixmap(QtGui.QPixmap(img_path))
#         self.pix.scaled(48,48,QtCore.Qt.KeepAspectRatio)
#         self.icon = QtGui.QIcon(self.pix)
#         self.setIcon(self.icon)
#         self.setIconSize(QtCore.QSize(48,48))

# class DurationLabel(QLabel):

#     def __init__(self,parent):
#         super().__init__(parent)
#         self.paddingLeft = 10
#         self.paddingTop = 10
#         self.resize(100,24)
#         self.setVisible(False)
#         self.setAlignment(QtCore.Qt.AlignRight or QtCore.Qt.AlignVCenter)
#         self.font = QtGui.QFont("Arial",18,QtGui.QFont.Bold)
#         self.setFont(self.font)
#         self.setStyleSheet("background-color: transparent; color: white;")


#     def update_position(self): 
#         if hasattr(self.parent(), 'viewport'):
#             parent_rect = self.parent().viewport().rect()
#         else:
#             parent_rect = self.parent().rect()

#         if not parent_rect:
#             return

#         x = parent_rect.width() - self.width() - self.paddingLeft
#         y = parent_rect.height() - self.height() - self.paddingTop 
#         self.setGeometry(x, y, self.width(), self.height())

class MyThread(QtCore.QThread):
    
    finished = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self,parent,vcap):
        super().__init__(parent)
        self.parent = parent
        self.vcap = vcap
    
    def run(self):
        while True:
            self.ret,self.disp_img = self.vcap.read()
            # if self.rec_flag:
            #     self.vwrite.write(self.orig_img)
            #     # cv2.putText(self.disp_img,str(int(time.time() - self.start_time)),(500,500),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,2)
            #     self.addRecPic()
            #     self.duration_label.setText(str(datetime.timedelta(seconds=int(time.time() - self.start_time))))
            #     self.duration_label.update_position()

            self.disp_img = QtGui.QImage(self.disp_img.data, self.disp_img.shape[1], self.disp_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.disp_img = QtGui.QImage.scaled(self.disp_img,self.parent.ui.label.width(),self.parent.ui.label.height())

            self.finished.emit(self.disp_img)


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rec_flag = False

        # self.logo_img = cv2.imread("../img/logo.png",-1)
        # self.logo_img = QtGui.QImage(self.logo_img.data, self.logo_img.shape[1], self.logo_img.shape[0], QtGui.QImage.Format_RGBA8888).rgbSwapped()
        # self.ui.logo_img.setPixmap(QtGui.QPixmap.fromImage(self.logo_img))

        # self.fullsrc_btn = FullScreenButton(parent=self.ui.label)
        # self.fullsrc_btn.clicked.connect(self.fullsrc_btn_clicked)
        # self.fullsrc_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # self.ui.recordButton.stateChanged.connect(self.record_btn_clicked)

        # self.duration_label = DurationLabel(parent=self.ui.label)

        self.vcap = cv2.VideoCapture("rtsp://192.168.1.1:554")
        th = MyThread(self,self.vcap)
        th.finished.connect(self.updateImg)
        th.start()

        # self.vwrite = cv2.VideoWriter('../vid/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1280,720)) 
        # self.setupRecPic()


    # def fullsrc_btn_clicked(self):
    #     if self.ui.label.isFullScreen():
    #         self.ui.label.setWindowFlag(QtCore.Qt.Window,False)
    #         self.ui.label.show()
    #         self.fullsrc_btn.changeIcon("../img/fullscreen.png")
    #         self.fullsrc_btn.update_position()

    #     else:
    #         self.ui.label.setWindowFlag(QtCore.Qt.Window,True)
    #         self.ui.label.showFullScreen()
    #         self.fullsrc_btn.changeIcon("../img/windowed.png")
    #         self.fullsrc_btn.update_position()

    # def record_btn_clicked(self,state): 
    #     if state == QtCore.Qt.Checked:
    #         self.start_time = time.time()
    #         self.rec_flag = True
    #         self.duration_label.setVisible(True)
    #     else:
    #         self.rec_flag = False
    #         self.duration_label.setVisible(False)
         
    def updateImg(self,img):
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(img))

    # def setupRecPic(self):
    #     self.s_img = cv2.imread("../img/rec.png", -1)
    #     self.s_img = cv2.resize(self.s_img,(70,70),interpolation= cv2.INTER_AREA)
    #     y_offset = 5
    #     x_offset = 15

    #     self.y1, self.y2 = y_offset, y_offset + self.s_img.shape[0]
    #     self.x1, self.x2 = x_offset, x_offset + self.s_img.shape[1]

    #     self.alpha_s = self.s_img[:, :, 3] / 255.0
    #     self.alpha_l = 1.0 - self.alpha_s

    # def addRecPic(self):
    #     for c in range(0, 3):
    #         self.disp_img[self.y1:self.y2, self.x1:self.x2, c] = ( self.alpha_s * self.s_img[:, :, c] +
    #                             self.alpha_l * self.disp_img[self.y1:self.y2, self.x1:self.x2, c])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.showFullScreen()
    sys.exit(app.exec_())
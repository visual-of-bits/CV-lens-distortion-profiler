import sys
import cv2
import numpy as np

args = sys.argv
frameRate = 1
square_size = 4
objpoints = []
imgpoints = []


def writefram(sec,clc):
 vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
 bol,image = vidcap.read()
 findcal(gx,gy,image,sec)
 return bol


def findcal(nx,ny,img,sc):
 try:
  pattern_size = (nx, ny)  
  pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
  pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
  pattern_points *= square_size
  img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  ret, corners = cv2.findChessboardCorners(img, (nx, ny), None)    
  if ret == True:
        print(str(sc)+"s, processed...")
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        cv2.cornerSubPix(img, corners, (5,5), (-1,-1), term)
        imgpoints.append(corners.reshape(-1, 2))
        objpoints.append(pattern_points)
 except Exception:
    pass

#main from here
if (len(args) != 2):  
 print("영상 파일의 이름을 써주세요...")
 quit() 

#sample image
vidcap = cv2.VideoCapture(args[1])
vidcap.set(cv2.CAP_PROP_FPS,1)
hav,image = vidcap.read()

#chessboard profile
print("체스보드의 길이(수평):",end='')
gx=int(input())
print("체스보드의 길이(수직):",end='')
gy=int(input())

#do until video end
sec = 0
clock=0
while writefram(sec,clock):
 sec = sec + frameRate
 clock = clock + 1
 sec = round(sec, 4)
 
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image.shape[1::-1], None, None)
#save profile
np.save("mtx", mtx)
np.save("dist", dist)

#display profiles
print("RMS: ", ret)
print("mtx: ", mtx)
print("dis: ", dist)
print("camera file exported")

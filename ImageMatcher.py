import cv2
import numpy as np
import os
import time


MATCH_THRESHOLD = 0.75
THRESHOLD = 10
# import Images
path = 'ImgTrain/Sample'
images = []
classNames = []
myList = os.listdir(path)
print('Total Images Detected', len(myList))
for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    filename = os.path.splitext(cl)[0]
    classNames.append(filename)
    # print(filename)
# print(len(classNames))
orb = cv2.ORB_create(nfeatures=1000)


def findDes(images):
    desList=[]
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList


def findID(img, desList):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, 2)
            good = []
            for m, n in matches:
                if m.distance < MATCH_THRESHOLD * n.distance:
                    good.append([m])
            matchList.append(len(good))
        # print(matchList)
    except:
        pass
    if len(matchList)!=0:
        if max(matchList) > THRESHOLD:
            finalVal = matchList.index(max(matchList))
    return finalVal


print("---starting feature extraction ---")
start_time = time.time()
desList = findDes(images)
# print(len(desList))
print("---pre-processing took %s seconds ---" % (time.time() - start_time))

# cap = cv2.VideoCapture(1)
cam_success = False
# while True:
#     success, img2 = cap.read()
#     cam_success = success
#     if success:
#         imgOriginal = img2.copy()
#         img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#         cv2.imshow('img2', imgOriginal)
#         cv2.waitKey(1)
#     else:
#         break

if not cam_success:
    img2 = cv2.imread('ImgTrain/Erics.jpg')
    imgOriginal = img2.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    start_time = time.time()
    id = findID(img2, desList)
    if id != -1:
        # cv2.putText(imgOriginal,classNames[id], (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        print(classNames[id])
    print("---match found in %s seconds ---" % (time.time() - start_time))
    # cv2.imshow('img2', imgOriginal)


#
# MATCH_THRESHOLD = 0.75
#
# img1 = cv2.imread('ImgQuery/fan_crop.jpg', 0)
# img2 = cv2.imread('ImgTrain/fan.jpg', 0)
#

#
# kp1, dsc1 = orb.detectAndCompute(img1, None)
# kp2, dsc2 = orb.detectAndCompute(img2, None)
#
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(dsc1, dsc2, 2)
#
# good = []
#
# for m, n in matches:
#     if m.distance < MATCH_THRESHOLD * n.distance:
#         good.append([m])

# print(len(good))
#
# img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
#
# imgKp1 = cv2.drawKeypoints(img1, kp1, None)
# imgKp2 = cv2.drawKeypoints(img2, kp2, None)
#
# cv2.namedWindow("img1", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
# cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
# cv2.namedWindow("img3", cv2.WINDOW_NORMAL)

# imS1 = cv2.resize(img1, (960, 540))                # Resize image
# cv2.imshow("output1", imS1)                       # Show image
# imS2 = cv2.resize(img2, (960, 540))                # Resize image
# cv2.imshow("output2", imS2)                       # Show image
# cv2.waitKey(0)

# cv2.imshow('img1', imgKp1)
# cv2.imshow('img2', imgKp2)


# cv2.imshow('img1', img1)
# cv2.imshow('img2', img2)
# cv2.imshow('img3', img3)
# cv2.waitKey(0)


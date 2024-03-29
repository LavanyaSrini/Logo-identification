from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt


image = cv2.imread('ex/passport_09.jpg')
image = imutils.resize(image, height=600)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (24,8))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15 ))
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
thresh = cv2.erode(thresh, None, iterations=4)
p = int(image.shape[1] * 0.05)
thresh[:, 0:p] = 0
thresh[:, image.shape[1] - p:] = 0
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    crWidth = w / float(gray.shape[1])
    if ar > 1 and crWidth > 0.0:
        pX = int((x + w) * 0.03)
        pY = int((y + h) * 0.03)
        (x, y) = (x - pX, y - pY)
        (w, h) = (w + (pX * 2), h + (pY * 2))
        roi = image[y:y + h, x:x + w].copy()
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break
cv2.imshow("Image", image)
cv2.imshow("ROI", roi)
cv2.waitKey(0)

   
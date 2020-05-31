import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image

img = cv2.imread('/home/pi/Pictures/img.jpg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620, 480)) #resizes the image to avoid dealing with bigger resolutions 

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converts to gray scale to avoid dealing with color details 
gray = cv2.bilateralFilter(gray, 11, 17, 17) # uses a bilateral filter to reduce noise within the image as the only import detail is the license plate 
edged = cv2.Canny(gray, 30, 200) # performs edge detection to have an intensity gradient 

# When contours have been detected, it will be sorted in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

# To filter license plate imaging, a for loop will be placed to filter all the results to find what has 4 sides, and a closed figure 
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4: # If the contour has exactly 4 points then we can assume we found our license plate 
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No contour detected")
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# When a license plate has been found, the entire picture will be cropped out besides the license plate to focus on.
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)

# The next step is to capture the sergment out of the plate by cropping it and making a new image.
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]


#Read the number plate, when picture is filtered

text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("Detected Number is:",text)


cv2.imshow('image', img)
cv2.imshow('Cropped',Cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()

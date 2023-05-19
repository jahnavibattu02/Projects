# Import required libraries
import cv2
import imutils
import numpy as np
import pytesseract
import matplotlib.pyplot as plt

# Import the readme file
pytesseract.pytesseract.tesseract_cmd=r"C:\Users\91995\Downloads\tesseract-ocr-w64-setup-v5.0.1.20220118.exe"

# Load and Read  the image
img = cv2.imread(r"C:\Users\91995\OneDrive\Desktop\1\2.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(cv2.imread(r"C:\Users\91995\OneDrive\Desktop\1\2.png",0), cv2.COLOR_BGR2RGB))

# Preprocess the image
bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 30, 200) #Edge detection
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

# Find the contours:
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:12]
location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour,5, True)
    if len(approx) == 4:
        location = approx
        print((location))
        break

# Create a mask and extract the region of interest:
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)
plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
plt.show()

# Perform OCR on the extracted text:
t=pytesseract.image_to_string(new_image)
print(t)
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=t, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
plt.show()
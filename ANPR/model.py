import cv2
import imutils
import easyocr
import numpy as np
import pytesseract
import matplotlib.pyplot as plt

image = cv2.imread(r'C:\Users\jahna\Desktop\SEM-6\ML\DL\Work\ANPR\test3.jpg')
#image = cv2.resize(image, (224, 224))
#image = imutils.resize(image, width=500, height=500)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply filters to remove noise
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Find the edges of the image
edged = cv2.Canny(gray, 170, 200)

# Find the contours of the edged image
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by area
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
screenCnt = None 

# loop over the contours
for c in cnts:
    # Approximate the contour
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

    # if the contour has four vertices, then we have found the paper
    if len(approx) == 4:
        screenCnt = approx
        break

# Apply Mask to the image
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], -1, (255,0,0), 2)
new_image = cv2.bitwise_and(image, image, mask=mask)

# Crop the image
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
plt.show()

# Extracting text from image
pytesseract.pytesseract.tesseract_cmd  = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(cropped)
print('Number plate of the Vehicle: {}'.format(text))
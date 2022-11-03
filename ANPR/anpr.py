# Import Libraries
import cv2
import imutils
import easyocr
import numpy as np
import pytesseract
from flask_mysqldb import MySQL
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.image import img_to_array

# Constructor
app = Flask(__name__)

# Connect to MySQL
mysql = MySQL()
mysql.init_app(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'images' # Database name

# route to home page
@app.route('/', methods=['GET','POST'])
def home():
	return render_template('home.html')

# route to about page
@app.route('/about')
def about():
    return render_template('about.html')

# route to predict page
@app.route('/submit', methods=['GET','POST'])
def predict():
    # Get the image from the request
    img = request.files['my_image']

    # save the file to the uploads folder
    img_path = 'static/' + img.filename
    img.save(img_path)

    image = cv2.imread(img_path)
    #image = cv2.resize(image, (224, 224))
    image = imutils.resize(image, width=500, height=500)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply filters to remove noise
    filtered_img = cv2.bilateralFilter(gray, 11, 17, 17)

    # Find the edges of the image
    edged = cv2.Canny(filtered_img, 170, 200)

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
    new_image = cv2.drawContours(mask, [screenCnt], -1, 255, 2)
    new_image = cv2.bitwise_and(image, image, mask=mask)

    # Crop the image
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    # Extracting text from image
    pytesseract.pytesseract.tesseract_cmd  = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(cropped)
    #print('Number plate of the Vehicle: {}'.format(text))

    # Save the results to the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO images(image, text) VALUES(%s, %s)", (img_path, text))
    mysql.connection.commit()
    cur.close()

    # return the text
    return render_template('home.html', text=text, img_path=img_path)

# run the app
if __name__ == '__main__':
    app.run(debug=True)
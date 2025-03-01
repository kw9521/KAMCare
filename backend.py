import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
import platform


def detectTesseract():
    system_os = platform.system()
    tesseract_path = None

    # macOS
    if system_os == "Darwin":  
        # M1/M2 Mac
        tesseract_path = "/opt/homebrew/bin/tesseract"  

        # Intel Mac
        if not os.path.exists(tesseract_path):
            tesseract_path = "/usr/local/bin/tesseract" 
    elif system_os == "Windows":
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        raise Exception("Unsupported OS")

    return tesseract_path


def openImage(imageName):
    file_path = "image/"+ imageName
    img = Image.open(file_path)
    return img

def processImage(img):
    # PIL image to OpenCV format
    img_cv = np.array(img)

    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # OTSU thresholding
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # specify structure shape and kernel size for dilation
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img_cv.copy()

    # store recognized text in a file
    with open("recognized.txt", "w") as file:
        file.write("")

    # loop through contours and extract text
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # draw a rectangle around the detected text
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # crop the text block
        cropped = im2[y:y + h, x:x + w]
        
        # apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        
        # add extracted text to file
        with open("recognized.txt", "a") as file:
            file.write(text + "\n")

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = detectTesseract()

    imageName = input("Enter Image Name with Exension: (image.png): ")
    img = openImage(imageName)
    processImage(img)




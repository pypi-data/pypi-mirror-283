import cv2
import numpy as np

class FileHelper:
    """description of class"""

    @staticmethod
    def convert_to_cv2_img(file):
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        return img

    @staticmethod
    def data_uri_to_cv2_img(uri):
        encoded_data = uri.split(',')[1]
        nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        return img



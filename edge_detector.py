import cv2
import numpy as np

def detect_edges(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("Image not found!")
        return
    
    edges = cv2.Canny(image, 50, 150)
    
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_edges("lakshtransaction.jpg")

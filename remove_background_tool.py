import cv2
import numpy as np
from PIL import Image

# Tăng giới hạn kích thước ảnh
Image.MAX_IMAGE_PIXELS = None


def remove_background(image_path, output_path):

    image = cv2.imread(image_path)
    original_image = Image.open(image_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edges = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mask = np.zeros_like(image)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)
    
    result = cv2.bitwise_and(image, mask)
    
    result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    
    result_image = result_image.convert("RGBA")
    datas = result_image.getdata()
    
    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    result_image.putdata(new_data)
    
    # Save the result
    result_image.save(output_path, format="PNG")
    print("Removed the background")

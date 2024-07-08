from PIL import Image, ImageFile
import os
import math

INFINITE = math.inf

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_PATH = r"E:\tools\input\caophong\CAOPHONG-2022.jpg"
OUTPUT_PATH = r"E:\tools\output"
TARGET_COLOR = [(234, 166, 255), (255, 171, 255), (255, 170, 255), (254, 172, 252), (255, 169, 255), 
                (242, 167, 255), (255, 167, 255), (254, 171, 254), (253, 172, 253), (254, 172, 254),
                (249, 175, 250), (254, 172, 253), (233, 190, 233), (234, 203, 233)]

# Hàm tìm tọa độ các pixel của màu viền
def find_color_pixels(image_path, target_color):
    img = Image.open(image_path)
    weight, height = img.size

    pixels = img.load()
    color_pixels = []

    for y in range(height):
        for x in range(weight):
            pixel_color = pixels[x, y]
            if pixel_color in target_color:
                color_pixels.append((x, y))
    
    return color_pixels

# Hàm tìm kích thước cropped box
def find_cropped_box(pixel_coordinates):
    left = INFINITE
    bottom = -INFINITE
    right = -INFINITE
    top = INFINITE

    for cor in pixel_coordinates:
        x, y = cor
        if x <= left:
            left = x
        if  x >= right:
            right = x
        if y <= top:
            top = y
        if y >= bottom:
            bottom = y

    return left, top, right, bottom

# Hàm crop ảnh theo viền
def advanced_crop_img(input_path, output):
    try:
        # Kiểm tra input 
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        _, ext = os.path.splitext(input_path)
        if ext.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Đọc ảnh từ input_path
        img = Image.open(input_path)
        img_name = os.path.basename(input_path)
        weight, height = img.size
        
        # Lấy tọa độ cropped box
        target_needed = find_color_pixels(INPUT_PATH, TARGET_COLOR)
        left, top, right, bottom = find_cropped_box(target_needed)

        # Lưu ảnh vào output_path
        img_cropped = img.crop((left - 20, top - 70, right + 60, bottom + 60))
        output = f"{OUTPUT_PATH}\{img_name}"
        img_cropped.save(output)

    except Exception as e:
        print(f"Lỗi: {e}")

advanced_crop_img(INPUT_PATH, OUTPUT_PATH)
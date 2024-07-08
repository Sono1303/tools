from PIL import Image, ImageFile
import os
import math
from resize_width_length import reduce_image_size
from rembg import remove

INFINITE = math.inf

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_PATH = r"E:\tools\input\lacthuy\LACTHUY-2020.jpg"
OUTPUT_PATH = r"E:\tools\output"

TARGET_COLOR = [(234, 166, 255), (255, 171, 255), (255, 170, 255), (254, 172, 252), (255, 169, 255), 
                (242, 167, 255), (255, 167, 255), (254, 171, 254), (253, 172, 253), (254, 172, 254),
                (249, 175, 250), (254, 172, 253), (233, 190, 233), (234, 203, 233), (249, 236, 251),
                (252, 166, 251), (246, 177, 247), (54, 44, 55), (46, 39, 46), (52, 43, 53), (98, 98, 97),
                (106, 107, 106), (95, 72, 101), (123, 92, 132), (230, 167, 252)]

# Hàm tìm tọa độ các pixel của màu viền
def find_color_pixels(image_path, target_color):
    img = Image.open(image_path).convert("RGBA")
    weight, height = img.size

    pixels = img.load()
    color_pixels = []

    for y in range(height):
        for x in range(weight):
            pixel_color = pixels[x, y]
            if pixel_color[:3] in target_color:
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
def advanced_crop_img(input_path, output_path):
    try:
        # Kiểm tra input 
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        _, ext = os.path.splitext(input_path)
        if ext.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Resize ảnh
        img_name = os.path.basename(input_path)
        output = f"{output_path}\{img_name}"
        reduce_image_size(input_path, output)
        print("Done resizing")

        # Remove background
        img = Image.open(output)
        removed_bg_img = remove(img)
        removed_bg_img.save(output, format="PNG")
        print("Done removing")

        # Lấy tọa độ cropped box
        target_needed = find_color_pixels(output, TARGET_COLOR)
        left, top, right, bottom = find_cropped_box(target_needed)
        print("Done getting cropped box")

        # Crop ảnh và lưu ảnh
        image = Image.open(output)
        img_cropped = image.crop((left - 40, top -30, right + 40, bottom + 30))
        img_cropped.save(output, format="PNG")
        print("Done cropping")

    except Exception as e:
        print(f"Lỗi: {e}")

advanced_crop_img(INPUT_PATH, OUTPUT_PATH)
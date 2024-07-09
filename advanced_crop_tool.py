from PIL import Image, ImageFile
import os
import math
from resize_width_length import reduce_image_size as reduce_width_height
from rembg import remove
from resize_50mb import reduce_image_size
# pip install rembg

INFINITE = math.inf

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_PATH = r"E:\tools\input\dabac\DABAC-2020.jpg"
OUTPUT_PATH = r"E:\tools\output"

          
TARGET_COLOR = []      
COLOR_PIXELS = []

# Hàm tìm tọa độ các pixel của màu viền
def find_color_pixels(image_path, target_color):
    img = Image.open(image_path).convert("RGBA")
    weight, height = img.size
    pixels = img.load()
    color_pixels = []

    for y in range(height):
        for x in range(weight):
            pixel_color = pixels[x, y]
            if (pixel_color[0] > 139) and (pixel_color[1] > 139) and (pixel_color[2] > 139) and (pixel_color not in TARGET_COLOR):
                COLOR_PIXELS.append(pixel_color)
                color_pixels.append((x, y))

    return color_pixels

# Hàm tìm kích thước cropped box
def find_cropped_box(pixel_coordinates):
    left = INFINITE
    bottom = -INFINITE
    right = -INFINITE
    top = INFINITE

    # max_left = None
    # max_right = None
    # max_top = None
    # max_bottom = None

    # i = -1
    for cor in pixel_coordinates:
        # i += 1 

        x, y = cor
        if x <= left:
            left = x
            # max_left = COLOR_PIXELS[i]
        if  x >= right:
            right = x 
            # max_right = COLOR_PIXELS[i]
        if y <= top:
            top = y
            # max_top = COLOR_PIXELS[i]
        if y >= bottom:
            bottom = y
            # max_bottom = COLOR_PIXELS[i]
    # print((max_left, max_top, max_right, max_bottom))
    return left, top, right, bottom

# Hàm crop ảnh theo viền
def advanced_crop_img(input_path, output_path):
    try:
        # Kiểm tra input 
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        _, ext = os.path.splitext(input_path)
        if ext.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Lấy tên ảnh và tạo đường dẫn output
        # img_name = os.path.basename(input_path)
        # output = f"{output_path}\{img_name}"
        output = output_path

        # Resize ảnh
        img = Image.open(input_path)
        width, height = img.size
        if (width < 20000 and height < 20000):
            img.save(output)
        else:
            reduce_width_height(input_path, output)
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
        img_cropped = image.crop((left, top, right, bottom))
        img_cropped.save(output, format="PNG")
        print("Done cropping")

        # Kiểm tra kích thước ảnh và resize
        reduce_image_size(output, output)
        print("Done resize again")

    except Exception as e:
        print(f"Lỗi: {e}")

# advanced_crop_img(INPUT_PATH, OUTPUT_PATH)
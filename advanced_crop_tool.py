from PIL import Image, ImageFile
import os
import math
from resize_width_length import reduce_image_size
from rembg import remove
# pip install rembg

INFINITE = math.inf

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_PATH = r"E:\tools\input\lacthuy\LACTHUY-2020.jpg"
OUTPUT_PATH = r"E:\tools\output"

          
TARGET_COLOR = [(0, 0, 0), (31, 31, 30), (29, 29, 28), (32, 32, 31), (33, 32, 29), (32, 32, 30), (32, 31, 29),
                (36, 36, 36), (1, 1, 1), (2, 2, 2), (1, 2, 2), (3, 3, 3), (4, 4, 4), (2, 3, 3), (5, 5, 5),
                (3, 4, 4), (6, 6, 6), (2, 4, 4), (5, 6, 5), (3, 5, 5), (4, 5, 5), (7, 7, 7), (0, 1, 1),
                (8, 8, 8), (6, 7, 7), (4, 4, 5), (9, 9, 9), (6, 7, 6), (10, 10, 10), (7, 8, 8), (11, 11, 11),
                (12, 12, 12), (13, 13, 13), (14, 14, 14), (15, 15, 15), (16, 16, 16), (17, 17, 17), (18, 18 , 18),
                (19, 19, 19), (20, 20, 20), (21, 21, 21), (22, 22, 22), (23, 23, 23), (24, 24, 24), (25, 25, 25),
                (5, 5, 4), (5, 6, 6)]      
COLOR_PIXELS = []

# Hàm tìm tọa độ các pixel của màu viền
def find_color_pixels(image_path, target_color):
    img = Image.open(image_path).convert("RGBA")
    weight, height = img.size
    pixels = img.load()
    # color_pixels = []

    for y in range(height):
        for x in range(weight):
            pixel_color = pixels[x, y]
            if (pixel_color[0] > 64) and (pixel_color[1] > 64) and (pixel_color[2] > 64):
                # COLOR_PIXELS.append(pixel_color)
                color_pixels.append((x, y))

    return color_pixels

# Hàm tìm kích thước cropped box
def find_cropped_box(pixel_coordinates):
    left = INFINITE
    bottom = -INFINITE
    right = -INFINITE
    top = INFINITE

    max_left = None
    max_right = None
    max_top = None
    max_bottom = None

    i = -1
    for cor in pixel_coordinates:
        i += 1 
        # if COLOR_PIXELS[i][:3] in TARGET_COLOR:
        #     continue

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
        img_name = os.path.basename(input_path)
        output = f"{output_path}\{img_name}"

        # Resize ảnh
        img = Image.open(input_path)
        width, height = img.size
        if (width < 20000 and height < 20000):
            img.save(output)
        else:
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
        img_cropped = image.crop((left, top, right, bottom))
        img_cropped.save(output, format="PNG")
        print("Done cropping")

    except Exception as e:
        print(f"Lỗi: {e}")

advanced_crop_img(INPUT_PATH, OUTPUT_PATH)
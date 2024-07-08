from PIL import Image, ImageFile
import os

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_PATH = r"E:\tools\input\caophong\CAOPHONG-2021.jpg"
OUTPUT_PATH = r'E:\tools\output'

def crop_image(input_path, output_path, new_width, new_height):
    try:
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        _, ext = os.path.splitext(input_path)
        if ext.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")

        img = Image.open(input_path)
        img_name = os.path.basename(input_path)
        width, height = img.size

        # Tạo lập kích thước crop box
        left = (width - new_width) / 2 
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        # Lưu ảnh tại output_path
        img_cropped = img.crop((left, top, right, bottom))
        output = f"{OUTPUT_PATH}\{img_name}"
        img_cropped.save(output)

    except Exception as e:
        print(f"Lỗi: {e}")

new_width = 300
new_height = 300
crop_image(INPUT_PATH, OUTPUT_PATH, new_width, new_height)


import os
from PIL import Image

# Tăng giới hạn kích thước ảnh
Image.MAX_IMAGE_PIXELS = None

def reduce_image_size(input_path, output_path, scale_factor=3, quality=90):
    try:
        # Mở ảnh
        image = Image.open(input_path)
        pic_name = os.path.basename(input_path)

        # Giảm kích thước ảnh bằng cách downscaling nhưng vẫn giữ nguyên tỷ lệ
        width, height = image.size
        new_width = int(width / scale_factor)
        new_height = int(height / scale_factor)
        
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Lưu ảnh với chất lượng giảm
        resized_image.save(output_path, quality=quality, optimize=True)
         
         # Lấy kích thước của ảnh mới và dung lượng
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        
        # In ra kích thước ban đầu và mới của ảnh
        print(f"Kích thước ban đầu: {width}x{height} pixels")
        print(f"Kích thước mới: {new_width}x{new_height} pixels")
        print(f"Ảnh đã được lưu với kích thước giảm tại: {output_path}, dung lượng: {new_size:.2f} MB")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

import os
from PIL import Image

# Tăng giới hạn kích thước ảnh
Image.MAX_IMAGE_PIXELS = None

def reduce_image_size(input_path, output_path, target_size_mb=50, quality=90):
    try:
        # Mở ảnh
        image = Image.open(input_path)
        pic_name = os.path.basename(input_path)
        image_format = image.format

        max_size_bytes = target_size_mb * 1024 * 1024
        image_size = os.path.getsize(input_path)
        if image_size <= max_size_bytes:
            if image_format == 'JPEG':
                image.save(os.path.join(output_path.replace(f'{pic_name}', ''), pic_name), quality=95)
            else:
                image.save(os.path.join(output_path.replace(f'{pic_name}', ''), pic_name))
            print(f"Ảnh đã được lưu với kích thước giảm tại: {output_path}, dung lượng: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")
            return

        # Giảm kích thước ảnh bằng cách downscaling nhưng vẫn giữ nguyên tỷ lệ
        width, height = image.size
        scale_factor = (max_size_bytes / image_size) ** 0.5
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # if new_width < 1 or new_height < 1:
        #     raise ValueError("Kích thước ảnh quá nhỏ sau khi giảm.")
        
        # resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Lưu ảnh với chất lượng giảm
        resized_image.save(output_path, quality=quality, optimize=True)
        
        # Kiểm tra kích thước tệp và giảm chất lượng thêm nếu cần
        while os.path.getsize(output_path) > target_size_mb * 1024 * 1024:
            quality -= 5
            if quality < 10:
                break
            resized_image.save(output_path, quality=quality, optimize=True)
        
        print(f"Ảnh đã được lưu với kích thước giảm tại: {output_path}, dung lượng: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

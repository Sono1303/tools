from pathlib import Path
from resize_50mb import reduce_image_size
from PIL import Image
from resize_width_length import reduce_image_size as reduce_width_length
INPUT_PATH = r'input'

def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SystemError) as e:
        return False

def read_image(image_path):
    try:
        with Image.open(image_path) as img:
            print(f"Image format: {img.format}, size: {img.size}, mode: {img.mode}")
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")

def create_directory(directory_path):
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        print(f"Directory '{directory_path}' created successfully.")
    except OSError as e:
        print(f"Error creating directory '{directory_path}': {e}")

def create_output_path(file_path):
    path = str(file_path).replace('input','')
    output_path = f'output{path}'
    return output_path

def check_path_type(path):
    path_obj = Path(path)
    if path_obj.is_file():
        return 0
    elif path_obj.is_dir():
        return 1
    else:
        return -1

def read_files_in_directory(directory_path):
    directory = Path(directory_path)

    if not directory.is_dir():
        print(f"{directory_path} is not a valid directory.")
        return
    
    for file_path in directory.iterdir():
        if file_path.is_file() and is_image(file_path):
            read_image(file_path)
            print(file_path)
            output_path = create_output_path(file_path)
            reduce_width_length(file_path, output_path)
            print("*******************")
        elif file_path.is_dir():
            output_path = create_output_path(file_path)
            create_directory(output_path)
            read_files_in_directory(file_path)           

path_type = check_path_type(INPUT_PATH)
if path_type == 1:
    read_files_in_directory(INPUT_PATH)
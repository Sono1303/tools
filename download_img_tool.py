import requests
import os
import re
from time import sleep

# url = f"https://han01.vstorage.vngcloud.vn/v1/AUTH_1dbb06310d21466fa9693a9d20fc3965/guland/hoa-binh-2030/{z}/{x}/{y}.png?fbclid=IwY2xjawEP_MNleHRuA2FlbQIxMAABHQkFFDar-VbOXz7-7gGOMAPYutxiCVCtiiQw_vSie3Ztkxxd75qirZEXww_aem_0JRlYO8WUIeOKMVzaxn3wg"
output = "E:/tools/output"

def get_coverage(z):
    response = requests.get(f"https://lyrs.meeymap.com/tileset/{z}/1/1.png?x-time=1721971407385&x-token=MTcyMBOyqrTk3MTQwNzM4NZtAhuS5TQ0tJZGVVbHRTbEcjGpqpyZUxScnROP2lBMUkFqUVNFVUJZSkVFb1hdjT1L0ejuXNqHZLUU1BenhCUWM5wGXdvSEZaYmdtSFZkUW51U3RRU0tYUHBLLjNlNGY5Nzk0YTI1MjY0OWEyYWU4Y2FkMGNiNmI1YTFi&fbclid=IwY2xjawEQKTJleHRuA2FlbQIxMAABHY1C4D8zmPwFYfNjoFYO0odEhQJGp1qSh5zE5KIW-sjfNle1TLAaD_fvLQ_aem_3jOioELIs0Zxij-tqlG3dg")
    text = response.text
    print(text)
    pattern = r"Coverage \[minx,miny,maxx,maxy\] is \[(\d+), (\d+), (\d+), (\d+)"
    match = re.search(pattern, text)

    if match:
        minx, miny, maxx, maxy = map(int, match.groups())
        print(f"minx: {minx}, miny: {miny}, maxx: {maxx}, maxy: {maxy}")
    else:
        print("Pattern not found")

    return minx, miny, maxx, maxy

def download_image(url, output_path, file_name):
    response = requests.get(url)
    print(output_path)
    file_path = os.path.join(output_path, file_name)

    with open(file_path, 'wb') as file:
        file.write(response.content)
        print(url)
        # print(response.content)
        # sleep(5)
    print(f"Image successfully downloaded: {output_path}")

def get_all_image():    
    if not os.path.exists(f"{output}/1"):
        output_path_z = os.makedirs(f"{output}/1")
    else:
        output_path_z = f"{output}/1"
    if not os.path.exists(f"{output}/1/1"):
        output_path_x = os.makedirs(f"{output}/1/1")
    else:
        output_path_x = f"{output}/1/1"
    download_image(f"https://lyrs.meeymap.com/tileset/1/1/1.png?x-time=1721971407385&x-token=MTcyMBOyqrTk3MTQwNzM4NZtAhuS5TQ0tJZGVVbHRTbEcjGpqpyZUxScnROP2lBMUkFqUVNFVUJZSkVFb1hdjT1L0ejuXNqHZLUU1BenhCUWM5wGXdvSEZaYmdtSFZkUW51U3RRU0tYUHBLLjNlNGY5Nzk0YTI1MjY0OWEyYWU4Y2FkMGNiNmI1YTFi&fbclid=IwY2xjawEQKTJleHRuA2FlbQIxMAABHY1C4D8zmPwFYfNjoFYO0odEhQJGp1qSh5zE5KIW-sjfNle1TLAaD_fvLQ_aem_3jOioELIs0Zxij-tqlG3dg", output_path_x, f'1.png')
    for z in range(2, 17):
        if not os.path.exists(f"{output}/{z}"):
            output_path_z = os.makedirs(f"{output}/{z}")
        output_path_z = f"{output}/{z}"
        print(f'z={z}')
        minx, miny, maxx, maxy = get_coverage(z)
        for x in range(minx, maxx + 1):
            print(f'x={x}')   
            if not os.path.exists(f"{output}/{z}/{x}"):
                output_path_x = os.makedirs(f"{output}/{z}/{x}")
            output_path_x = f"{output}/{z}/{x}"
            for y in range(miny, maxy + 1):
                print(f'y={y}')
                url = f"https://lyrs.meeymap.com/tileset/{z}/{x}/{y}.png?x-time=1721971407385&x-token=MTcyMBOyqrTk3MTQwNzM4NZtAhuS5TQ0tJZGVVbHRTbEcjGpqpyZUxScnROP2lBMUkFqUVNFVUJZSkVFb1hdjT1L0ejuXNqHZLUU1BenhCUWM5wGXdvSEZaYmdtSFZkUW51U3RRU0tYUHBLLjNlNGY5Nzk0YTI1MjY0OWEyYWU4Y2FkMGNiNmI1YTFi&fbclid=IwY2xjawEQKTJleHRuA2FlbQIxMAABHY1C4D8zmPwFYfNjoFYO0odEhQJGp1qSh5zE5KIW-sjfNle1TLAaD_fvLQ_aem_3jOioELIs0Zxij-tqlG3dg"
                download_image(url, output_path_x, f'{y}.png')
get_all_image()

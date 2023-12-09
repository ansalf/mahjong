import cv2
import os

src = './res/tile'
target = './res_test/tile'

# Membuat direktori target jika belum ada
os.makedirs(target, exist_ok=True)

files = os.listdir(src)
class OBJ:
    def __init__(self, filename, swapyz=False):
        # Your OBJ class implementation goes here
        pass

for file in files:
    full_path = os.path.join(src, file)
    # Memeriksa apakah file adalah file gambar
    if file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        img = cv2.imread(full_path)
        if img is not None:
            resized = cv2.resize(img, (50, 64))
            tar_path = os.path.join(target, file)
            cv2.imwrite(tar_path, resized)
        else:
            print(f"File {file} tidak dapat dibaca.")
    else:
        print(f"File {file} bukan file gambar.")
import cv2

import os

src = './res/tile'
target = './res_test/tile'
files = os.listdir(src)
for file in files:
    full_path = os.path.join(src, file)
    img = cv2.imread(full_path)
    resized = cv2.resize(img, (50, 64))
    tar_path = os.path.join(target, file)
    cv2.imwrite(tar_path, resized)

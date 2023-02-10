from data_generation.color_filter import color_filter
from data_generation.img_crop import crop_rescale
import os

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
raw_img_dir = folder_dir + 'raw_img\\'
images = os.listdir(raw_img_dir)
for img in images:
    if img.endswith(".jpg") or img.endswith(".png"):
        green_img = color_filter(img, raw_img_dir)
        crop_rescale(green_img, img, folder_dir)

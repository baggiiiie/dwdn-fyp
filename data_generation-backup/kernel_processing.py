import os
import random
from PIL import Image

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
img_dir = 'kernel_bmp\\'
# specify the directory path
directory = folder_dir + img_dir

# get all files in the directory
files = os.listdir(directory)

# create a new directory to save the cropped images
output_dir = folder_dir + '9_kernel\\'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# loop through the files and crop them
for file in files:
    filename = file.strip('.bmp')
    print(filename)
    output_dir = folder_dir + '9_kernel\\' + filename + '\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # Open the image
    im = Image.open(os.path.join(directory, file))
    im = im.convert("L")

    # Get the width and height of the image
    width, height = im.size
    size = 105
    stride = width // 3

    ker_num = 1
    # Crop the image
    for i in range(0, 3):
        top = stride // 2 - size // 2 + stride * i
        bottom = top + size
        for j in range(0, 3):
            left = stride // 2 - size // 2 + stride * j
            right = left + size

            cropped = im.crop((left, top, right, bottom))
            cropped.save(os.path.join(output_dir, f'{filename}_{ker_num}.png'))

            print(ker_num, (left, top, right, bottom))
            ker_num = ker_num + 1

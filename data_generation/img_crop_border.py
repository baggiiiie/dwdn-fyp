from PIL import Image
import random
import os

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
img_dir = 'GoogleEarthImage\\GoogleEarthImage5\\'
# specify the directory path
directory = folder_dir + img_dir

# get all files in the directory
files = os.listdir(directory)
# create a new directory to save the cropped images
output_dir = folder_dir + 'raw_img\\'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
img_num = len(os.listdir(output_dir))

# left, top, right, bottom = 150, 280, 250, 270
left, top, right, bottom = 130, 240, 240, 270
for file in files:
    if file.endswith(".jpg") or file.endswith(".png"):
        # Open the image
        im = Image.open(os.path.join(directory, file))
        # Get the width and height of the image
        width, height = im.size
        # Crop the image
        cropped = im.crop((left, top, width - right, height - bottom))
        # save the cropped image to the new directory
        print(f'saving img{img_num}')
        cropped.save(os.path.join(output_dir, f'img{img_num}.png'))
        img_num += 1




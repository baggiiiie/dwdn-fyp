from PIL import Image
import random
import os

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
img_dir = 'green_image\\'
# specify the directory path
directory = folder_dir + img_dir

# get all files in the directory
files = os.listdir(directory)

# create a new directory to save the cropped images
output_dir = folder_dir + 'cropped_img\\'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
size = 1250
# loop through the files and crop them
# img_count = 0
for file in files:
    if file.endswith(".jpg") or file.endswith(".png"):
        # size = random.choice([SIZE_1, SIZE_2])
        filename = file.strip('.png')
        im = Image.open(os.path.join(directory, file))
        width, height = im.size
        # print(width, height)
        # Crop the image
        cropped1 = im.crop((0, 0, size, size))
        cropped1.save(os.path.join(output_dir, f'{filename}_{1}.png'))
        cropped2 = im.crop((width - size, height - size, width, height))
        cropped2.save(os.path.join(output_dir, f'{filename}_{2}.png'))
        cropped3 = im.crop((600, height - size, 600 + size, height))
        flipped = cropped3.transpose(method=Image.FLIP_LEFT_RIGHT)
        flipped.save(os.path.join(output_dir, f'{filename}_{3}.png'))

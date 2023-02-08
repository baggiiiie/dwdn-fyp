import os
import random
from PIL import Image

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata2\\'
img_dir = 'kernel_bmp\\'
# specify the directory path
directory = folder_dir + img_dir

# get all files in the directory
files = os.listdir(directory)

# create a new directory to save the cropped images
output_dir = folder_dir + 'cropped_kernel\\'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# loop through the files and crop them
for file in files:
    filename = file.strip('.bmp')
    print(filename)
    output_dir = folder_dir + 'cropped_kernel\\' + filename + '\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # Open the image
    im = Image.open(os.path.join(directory, file))
    im = im.convert("L")

    # Get the width and height of the image
    width, height = im.size
    # size_list = [25, 45, 65, 95]
    # for i in range(0, 4):
        # Choose a random point on the image
        # size = random.choice(size_list)
        # size = size_list[i]
    size = 25
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2
    # Crop the image
    cropped = im.crop((left, top, right, bottom))
    cropped.save(os.path.join(output_dir, f'{filename}.png'))
    rotated = cropped.rotate(90)
    rotated.save(os.path.join(output_dir, f'{filename}_rotated.png'))
    flipped1 = cropped.transpose(method=Image.FLIP_LEFT_RIGHT)
    flipped1.save(os.path.join(output_dir, f'{filename}_flipped1.png'))
    flipped2 = rotated.transpose(method=Image.FLIP_LEFT_RIGHT)
    flipped2.save(os.path.join(output_dir, f'{filename}_flipped2.png'))
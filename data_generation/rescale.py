from PIL import Image
import os

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata2\\'
img_dir = 'cropped_img\\'
directory = folder_dir + img_dir
# get all files in the directory
files = os.listdir(directory)

# create a new directory to save the cropped images
output_dir = folder_dir + 'rescaled_img\\'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# loop through the files and rescale them
for file in files:
    if file.endswith(".jpg") or file.endswith(".png"):
        # size = random.choice([SIZE_1, SIZE_2])
        filename = file.strip('.png')
        # Open the image
        im = Image.open(os.path.join(directory, file))

        rescaled = im.resize((320, 320))

        # save the cropped image to the new directory
        rescaled.save(os.path.join(output_dir, file))


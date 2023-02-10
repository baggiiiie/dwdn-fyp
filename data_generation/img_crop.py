from PIL import Image
import random
import os


def crop_rescale(file, filename, dir):
    # img_dir = 'green_image\\'
    # # specify the directory path
    # directory = folder_dir + img_dir
    #
    # # get all files in the directory
    # files = os.listdir(directory)
    #
    # # create a new directory to save the cropped images
    output_dir = dir + 'GT_img\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    size = 1250
    # loop through the files and crop them
    # img_count = 0
    # for file in files:
    #     if file.endswith(".jpg") or file.endswith(".png"):
            # size = random.choice([SIZE_1, SIZE_2])

    filename = filename.strip('.png')
    # im = Image.open(os.path.join(dir, file))
    im = file
    width, height = im.size
    # print(width, height)
    # Crop the image
    print(f'cropping {filename}')
    cropped1 = im.crop((0, 0, size, size)).resize((320, 320))
    cropped1.save(os.path.join(output_dir, f'{filename}_{1}.png'))
    cropped2 = im.crop((width - size, height - size, width, height)).resize((320, 320))
    cropped2.save(os.path.join(output_dir, f'{filename}_{2}.png'))
    cropped3 = im.crop((600, height - size, 600 + size, height)).resize((320, 320))
    flipped = cropped3.transpose(method=Image.FLIP_LEFT_RIGHT)
    flipped.save(os.path.join(output_dir, f'{filename}_{3}.png'))

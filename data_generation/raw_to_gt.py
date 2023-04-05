import os
from PIL import Image

folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
raw_img_dir = folder_dir + 'raw_img\\'
SIZE = 320


def crop_rescale(file, filename, dir):
    output_dir = dir + 'GT_img\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    size = 1250

    filename = filename.strip('.png')

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


def rescale(folder_dir):
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
            filename = file.strip('.png')
            # Open the image
            im = Image.open(os.path.join(directory, file))

            rescaled = im.resize((SIZE, SIZE))

            # save the cropped image to the new directory
            rescaled.save(os.path.join(output_dir, file))


def color_filter(file, dir):
    img = Image.open(os.path.join(dir, file))
    # Extract the green channel
    r, g, b, _ = img.split()
    g = g.point(lambda x: x / 1.5)
    # Create a new image with all channels black except the green channel
    new_img = Image.merge("RGB", (Image.new("L", img.size, 0), g, Image.new("L", img.size, 0)))

    print(f'color filtering {file}')
    return new_img


images = os.listdir(raw_img_dir)
for img in images:
    if img.endswith(".jpg") or img.endswith(".png"):
        green_img = color_filter(img, raw_img_dir)
        crop_rescale(green_img, img, folder_dir)

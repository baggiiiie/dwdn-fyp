import os
from PIL import Image
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add long options
parser.add_argument('--working_dir', help='The working directory',
                    default='C:\\Users\\daiy0012\\Downloads\\mydata\\')
parser.add_argument('--raw_img_dir', help='The folder in working directory where raw images are located',
                    default='raw_img\\')
parser.add_argument('--gt_size', help='The size of final gt images',
                    default=320)

# Parse the command line arguments
args = parser.parse_args()

working_dir = args.working_dir
raw_img_dir = working_dir + args.raw_img_dir
gt_size = int(args.gt_size)
cropped_size = 1250


def crop_rescale(file, filename, dir):
    output_dir = dir + 'GT_img\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    filename = filename.strip('.png')

    im = file
    width, height = im.size
    # print(width, height)
    # Crop the image
    print(f'cropping {filename}')
    cropped1 = im.crop((0, 0, cropped_size, cropped_size)).resize((gt_size, gt_size))
    cropped1.save(os.path.join(output_dir, f'{filename}_{1}.png'))
    cropped2 = im.crop((width - cropped_size, height - cropped_size, width, height)).resize((gt_size, gt_size))
    cropped2.save(os.path.join(output_dir, f'{filename}_{2}.png'))
    cropped3 = im.crop((600, height - cropped_size, 600 + cropped_size, height)).resize((gt_size, gt_size))
    flipped = cropped3.transpose(method=Image.FLIP_LEFT_RIGHT)
    flipped.save(os.path.join(output_dir, f'{filename}_{3}.png'))


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
        crop_rescale(green_img, img, working_dir)

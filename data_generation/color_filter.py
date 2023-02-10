import os
import cv2
import numpy as np
from PIL import Image


def color_filter(file, dir):
    # img_dir = 'raw_img\\'
    # directory = folder_dir + img_dir
    # # get all files in the directory
    # files = os.listdir(directory)

    # create a new directory to save the cropped images
    # saved_dir = folder_dir + 'green_image\\'
    # if not os.path.exists(saved_dir):
    #     os.mkdir(saved_dir)

    # loop through the files and crop them
    # for file in files:
    #     if file.endswith(".jpg") or file.endswith(".png"):
    #
    # # Open the image
    # target_img = cv2.imread(os.path.join(dir, file))
    #
    # # target_img = cv2.convertScaleAbs(target_img, alpha=alpha, beta=beta)
    #
    # target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    # # Decrease the brightness by dividing each pixel's value by 1.8
    #
    # target_img = target_img / 1.5
    # black_img = np.full(target_img.shape, 0, np.uint8)
    #
    # target_img = np.stack([black_img, target_img, black_img], axis=2)
    # # cv2.imshow("Image", target_img)
    # # cv2.waitKey(0)
    # Load the original image
    img = Image.open(os.path.join(dir, file))
    # Extract the green channel
    r, g, b, _ = img.split()
    g = g.point(lambda x: x / 1.5)
    # Create a new image with all channels black except the green channel
    new_img = Image.merge("RGB", (Image.new("L", img.size, 0), g, Image.new("L", img.size, 0)))

    print(f'color filtering {file}')
    return new_img
    # cv2.imwrite(saved_dir + file, target_img)

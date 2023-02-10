from PIL import Image
import os

SIZE = 320


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


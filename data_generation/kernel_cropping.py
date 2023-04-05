import os
from PIL import Image

kernel_dir = 'C:\\Users\\daiy0012\\Downloads\\FYP_data\\pngKernel\\'
output_folder_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\kernels\\'
left_padding, right_padding = 12, 13
top_padding, bottom_padding = 12, 13
rows = [50, 159, 268]
cols = [51, 160, 268]

files = os.listdir(kernel_dir)

for kernel in files:
    kernel_name = kernel.split('.')[0]
    print(kernel_name, kernel)
    # create a new directory to save the cropped images
    output_dir = output_folder_dir + kernel_name + '_9ker\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Load the image
    image = Image.open(kernel_dir + kernel)
    img_idx = 1
    for row in rows:
        for col in cols:
            center_x, center_y = row, col

            # Calculate the coordinates of the top-left corner of the crop box
            left = center_x - left_padding
            top = center_y - top_padding

            # Calculate the coordinates of the bottom-right corner of the crop box
            right = center_x + right_padding
            bottom = center_y + bottom_padding

            # Crop the image using the calculated coordinates
            cropped_image = image.crop((left, top, right, bottom))

            # Save the cropped image
            cropped_image.save(output_dir + f'{kernel_name}_{img_idx}.png')

            img_idx = img_idx + 1





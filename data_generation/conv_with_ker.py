import cv2
import os
import numpy as np
import argparse

# what you need:
# a working dir, default is where this python code is stored
# a folder in working dir that stores gt img
# a folder in working dir that stores kernels (1 or multiple kernels in this folder)

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add long options
parser.add_argument('--working_dir', help='The working directory',
                    default='C:\\Users\\daiy0012\\Downloads\\mydata\\')
parser.add_argument('--gt_dir', help='The folder in working directory where gt images are located',
                    default='gt_imgs\\')
parser.add_argument('--kernel_dir', help='The folder in working directory where kernel images are located',
                    default='kernels\\')
parser.add_argument('--add_gblur', help='Whether Gaussian blur is added to the final convoluted images',
                    default=True)
parser.add_argument('--gblur_kernel', help='The kernel size for Gaussian blur',
                    default=5)
parser.add_argument('--num_augment', help='The number of data augmentations applied, from 0 to 2',
                    default=1)

# Parse the command line arguments
args = parser.parse_args()

data_root_dir = args.working_dir
gtImg_dir = data_root_dir + args.gt_dir
kernel_dir = os.path.join(data_root_dir + args.kernel_dir)


num_augment = args.num_augment
gblur_kernel = args.gblur_kernel
add_gblur = args.add_gblur

output_folder = 'dataset\\'
output_dir = data_root_dir + output_folder
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Output dataset generation
out_dirs1 = ['TrainingData\\', 'ValData\\', 'TestData\\']
out_dirs2 = ['blurred_img\\', 'blur_kernel\\', 'clear_img\\']
out_dirs = [[''] * 3 for i in range(3)]
for i, out_dir1 in enumerate(out_dirs1):
    dir1 = output_dir + out_dir1
    if not os.path.exists(dir1):
        os.mkdir(dir1)
    for j, out_dir2 in enumerate(out_dirs2):
        dir2 = dir1 + out_dir2
        if not os.path.exists(dir2):
            os.mkdir(dir2)
        out_dirs[i][j] = dir2


# overlapping boundaries
rows = [0, 107, 213, 320]
cols = [0, 107, 213, 320]


def conv_with_ker(img, kernels):
    height, width, channel = img.shape
    combined_image = np.zeros((height, width, channel), dtype=np.uint8)
    center_kernel = kernels[4]
    for kernel in kernels:
        kernel_used = cv2.imread(os.path.join(kernel_dir, kernel), 0)
        # Normalize the kernel
        kernel_norm = kernel_used / np.sum(kernel_used)
        result = cv2.filter2D(img, -1, kernel_norm)
        for row in range(0, 3):
            for col in range(0, 3):
                combined_image[rows[row]:rows[row + 1], cols[col]:cols[col + 1]] = result[rows[row]:rows[row + 1],
                                                                                   cols[col]:cols[col + 1]]
    return combined_image, center_kernel


gt_imgs = os.listdir(gtImg_dir)
total_img = len(gt_imgs) * (num_augment + 1)

files = os.listdir(kernel_dir)
kernels = []
for ker in files:
    if ker.endswith('.png'):
        kernels.append(ker)
num_kernels = len(kernels)

for file in gt_imgs:
    for i in range(0, num_augment + 1):
        if file.endswith(".png"):
            img = cv2.imread(os.path.join(gtImg_dir, file))
            if i == 1:
                img = cv2.flip(img, 0)
            elif i == 2:
                img = cv2.flip(img, 1)

            if num_kernels > 1:
                conv_img, kernel_used = conv_with_ker(img, kernels)
            else:
                kernel = kernels[0]
                kernel_used = cv2.imread(os.path.join(kernel_dir, kernel), 0)
                # Normalize the kernel
                kernel_norm = kernel_used / np.sum(kernel_used)
                conv_img = cv2.filter2D(img, -1, kernel_norm)

            if add_gblur:
                conv_img = cv2.GaussianBlur(conv_img, (gblur_kernel, gblur_kernel), 0)

            if im_idx < total_img // 10:
                out1 = out_dirs[2][0]
                out2 = out_dirs[2][1]
                out3 = out_dirs[2][2]
            elif im_idx < total_img // 5:
                out1 = out_dirs[1][0]
                out2 = out_dirs[1][1]
                out3 = out_dirs[1][2]
            else:
                out1 = out_dirs[0][0]
                out2 = out_dirs[0][1]
                out3 = out_dirs[0][2]

            cv2.imwrite(os.path.join(out1, f'img_{im_idx}.png'), conv_img)
            cv2.imwrite(os.path.join(out2, f'img_{im_idx}.png'), kernel_used)
            cv2.imwrite(os.path.join(out3, f'img_{im_idx}.png'), img)

            print(im_idx, img.shape, kernel_used.shape)
            im_idx = im_idx + 1

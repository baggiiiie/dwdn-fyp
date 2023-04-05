import cv2
import os
import numpy as np

kernel_type = '003deg_9ker'
center_kernel = '003deg_5.png'
root_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
gtImg_dir = root_dir + 'GT_img\\'
output_folder = '003deg_with_Gaussian\\'
kernel_dir = os.path.join(root_dir + 'kernels\\', kernel_type)
num_augment = 2
gblur_kernel = 5

# overlapping boundaries
rows = [0, 107, 213, 320]
cols = [0, 107, 213, 320]

# get all files in the directory
gt_imgs = os.listdir(gtImg_dir)
kernels = os.listdir(kernel_dir)

output_dir = root_dir + output_folder
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

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

im_idx = 1

center_ker = cv2.imread(os.path.join(kernel_dir, center_kernel), 0)
total_img = len(gt_imgs) * (num_augment + 1)

for file in gt_imgs:
    for i in range(0, num_augment + 1):
        if file.endswith(".png"):
            img = cv2.imread(os.path.join(gtImg_dir, file))
            if i == 1:
                img = cv2.flip(img, 0)
            elif i == 2:
                img = cv2.flip(img, 1)

            combined_image = np.zeros((320, 320, 3), dtype=np.uint8)

            for kernel_type in kernels:
                kernel_used = cv2.imread(os.path.join(kernel_dir, kernel_type), 0)
                # Normalize the kernel
                kernel_norm = kernel_used / np.sum(kernel_used)
                result = cv2.filter2D(img, -1, kernel_norm)
                for row in range(0, 3):
                    for col in range(0,3):
                        combined_image[rows[row]:rows[row+1], cols[col]:cols[col+1]] = result[rows[row]:rows[row+1],
                                                                                       cols[col]:cols[col+1]]

            combined_image = cv2.GaussianBlur(combined_image, (gblur_kernel, gblur_kernel), 0)

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

            cv2.imwrite(os.path.join(out1, f'img_{im_idx}.png'), combined_image)
            cv2.imwrite(os.path.join(out2, f'img_{im_idx}.png'), center_ker)
            cv2.imwrite(os.path.join(out3, f'img_{im_idx}.png'), img)

            print(im_idx, img.shape, kernel_used.shape)
            im_idx = im_idx + 1


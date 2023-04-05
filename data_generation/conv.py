import json
import cv2
import os
import random
import numpy as np

kernel_type = '003deg_with_GaussianBlur\\'
root_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
gtImg_dir = root_dir + 'GT_img\\'
# kernel_dir = root_dir + '9_kernel\\' + kernel_type
kernel_dir = root_dir + '0um_9_ker\\'

# get all files in the directory
files = os.listdir(gtImg_dir)

output_dir = root_dir + kernel_type

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
ker_count = dict()
im_idx = 0
non_shifted_ker = cv2.imread(kernel_dir + '600um_0.png', 0)
for file in files:
    for i in range(0, 1):
        kernel_used = random.choice(os.listdir(kernel_dir))
        # kernel_used = '600um_-3.png'
        # kernel_type = random.choice(['600u_1.png', '600u_4.png', '600u_7.png'])
        # kernel_type = '003deg_4.png'
        ker_count[kernel_used] = ker_count.get(kernel_used, 0) + 1
        if kernel_used.endswith(".png") and file.endswith(".png"):
            img = cv2.imread(os.path.join(gtImg_dir, file))
            if i == 1:
                img = cv2.flip(img, 0)
            elif i == 2:
                img = cv2.flip(img, 1)
            kernel_used = cv2.imread(os.path.join(kernel_dir, kernel_used), 0)
            print(im_idx, img.shape, kernel_used.shape)
            # Normalize the kernel
            kernel_norm = kernel_used / np.sum(kernel_used)
            result = cv2.filter2D(img, -1, kernel_norm)
            # # Add Gaussian blur to images
            # result = cv2.GaussianBlur(result, (5, 5), 0)
            if im_idx < 3:
                out1 = out_dirs[2][0]
                out2 = out_dirs[2][1]
                out3 = out_dirs[2][2]
            elif im_idx < len(files) // 5:
                out1 = out_dirs[1][0]
                out2 = out_dirs[1][1]
                out3 = out_dirs[1][2]
            else:
                out1 = out_dirs[0][0]
                out2 = out_dirs[0][1]
                out3 = out_dirs[0][2]
            cv2.imwrite(os.path.join(out1, f'img_{im_idx}.png'), result)
            cv2.imwrite(os.path.join(out2, f'img_{im_idx}.png'), kernel_used)
            # cv2.imwrite(os.path.join(out2, f'img_{im_idx}.png'), non_shifted_ker)
            cv2.imwrite(os.path.join(out3, f'img_{im_idx}.png'), img)

            im_idx = im_idx + 1

print(ker_count)
with open(output_dir + 'ker_count.json', 'w') as f:
    json.dump(ker_count, f)

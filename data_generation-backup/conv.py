import cv2
import os
import random
import numpy as np
kernel_type = '600u\\'
root_dir = 'C:\\Users\\daiy0012\\Downloads\\mydata\\'
input_dir = root_dir + 'rescaled_img\\'
# get all files in the directory
files = os.listdir(input_dir)

kernel_dir = root_dir + 'all_kernel\\' + kernel_type
ker_out_dir = root_dir + kernel_type

if not os.path.exists(ker_out_dir):
    os.mkdir(ker_out_dir)
out1_dirs = ['TrainingData\\', 'ValData\\', 'TestData\\']
out2_dirs =  ['blurred_img\\', 'blur_kernel\\', 'clear_img\\']
out_dirs = [['']*3 for i in range(3)]
for i, out_dir1 in enumerate(out1_dirs):
    dir1 = ker_out_dir + out_dir1
    if not os.path.exists(dir1):
        os.mkdir(dir1)
    for j, out_dir2 in enumerate(out2_dirs):
        dir2 = dir1 + out_dir2
        if not os.path.exists(dir2):
            os.mkdir(dir2)
        out_dirs[i][j] = dir2

im_idx = 0
for file in files:
    for i in range(0, 3):
        kernel_type = random.choice(os.listdir(kernel_dir))
        if kernel_type.endswith(".png") and file.endswith(".png"):
            img = cv2.imread(os.path.join(input_dir, file))
            if i == 1:
                img = cv2.flip(img, 0)
            elif i == 2:
                img = cv2.flip(img, 1)
            kernel_type = cv2.imread(os.path.join(kernel_dir, kernel_type), 0)
            print(im_idx, img.shape, kernel_type.shape)
            # Normalize the kernel
            kernel_norm = kernel_type / np.sum(kernel_type)
            # Convolve the image with the kernel
            result = cv2.filter2D(img, -1, kernel_norm)
            # Show the convolved image
            # cv2.imshow("convolved", result)
            # cv2.waitKey(0)
            # save the image
            if im_idx < 10:
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
            cv2.imwrite(os.path.join(out2, f'img_{im_idx}.png'), kernel_type)
            cv2.imwrite(os.path.join(out3, f'img_{im_idx}.png'), img)

            im_idx = im_idx + 1
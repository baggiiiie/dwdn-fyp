import cv2
import numpy as np
import os


def get_psnr(gt_dir, deblur_dir):
    gt_img = cv2.imread(gt_dir)
    deblur_img = cv2.imread(deblur_dir)
    # Calculate MSE (Mean Squared Error)
    mse = np.mean((gt_img - deblur_img) ** 2)
    # If mse is zero, return 100
    if mse == 0:
        psnr = 100
    else:
        # Calculate PSNR (Peak Signal-to-Noise Ratio)
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))

    return psnr


gt = '003deg_with_gaussian\\'
deblurred = 'results_003deg_with_gaussian\\'

gt_dir = 'C:\\Users\\daiy0012\\Downloads\\dwdn-data\\datasets\\'
gt_dir = gt_dir + gt + 'TestData\\clear_img\\'
deblur_dir = 'C:\\Users\\daiy0012\\Downloads\\dwdn-data\\results\\'
deblur_dir = deblur_dir + deblurred

avg_psnr = 0
for img in os.listdir(gt_dir):
    img_name = img.strip('.png')
    gt_img_dir = gt_dir + img
    deblur_img_dir = deblur_dir + img_name + 'DEBLUR.png'
    psnr = get_psnr(gt_img_dir, deblur_img_dir)
    avg_psnr = avg_psnr + psnr
    # Print the PSNR value
    print(f'PSNR value is {psnr} for {img}')
avg_psnr = avg_psnr / len(os.listdir(gt_dir))
print(f'Average PSNR value is {avg_psnr}.')

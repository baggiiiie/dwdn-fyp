import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim


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


def get_ssim(gt_dir, deblur_dir):
    img1 = cv2.imread(gt_dir)
    img2 = cv2.imread(deblur_dir)
    # Convert the images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    ssim_value = ssim(img1_gray, img2_gray)
    return ssim_value


dataset = '600u_center_ker\\'

root_dir = 'C:\\Users\\daiy0012\\Downloads\\dwdn-data\\datasets\\'
dataset_dir = root_dir + dataset
gt_dir = dataset_dir + 'TestData\\clear_img\\'
result_dir = dataset_dir + 'results\\'

avg_ssim = 0
avg_psnr = 0
for img in os.listdir(gt_dir):
    img_name = img.split('.')[0]
    gt_img_dir = gt_dir + img
    deblur_img_dir = result_dir + img_name + 'DEBLUR.png'
    # print(gt_img_dir, deblur_img_dir)
    psnr = get_psnr(gt_img_dir, deblur_img_dir)
    avg_psnr = avg_psnr + psnr
    ssim_value = get_ssim(gt_img_dir, deblur_img_dir)
    avg_ssim = avg_ssim + ssim_value

    print(f'PSNR: {psnr:.2f} | SSIM: {ssim_value:.3f} | {img}')

avg_psnr = avg_psnr / len(os.listdir(gt_dir))
avg_ssim = avg_ssim / len(os.listdir(gt_dir))
print(f'Average PSNR {avg_psnr:.2f} | Average SSIM {avg_ssim:.3f}.')
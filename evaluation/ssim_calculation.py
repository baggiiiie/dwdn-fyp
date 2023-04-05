from skimage.metrics import structural_similarity as ssim
import cv2
import os

def get_ssim(gt_dir, deblur_dir):
    img1 = cv2.imread(gt_dir)
    img2 = cv2.imread(deblur_dir)
    # Convert the images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    ssim_value = ssim(img1_gray, img2_gray)
    return ssim_value


gt = '003deg_with_gaussian\\'
deblurred = 'results_003deg_with_gaussian\\'

gt_dir = 'C:\\Users\\daiy0012\\Downloads\\dwdn-data\\datasets\\'
gt_dir = gt_dir + gt + 'TestData\\clear_img\\'
deblur_dir = 'C:\\Users\\daiy0012\\Downloads\\dwdn-data\\results\\'
deblur_dir = deblur_dir + deblurred

avg_ssim = 0

for img in os.listdir(gt_dir):
    img_name = img.strip('.png')
    gt_img_dir = gt_dir + img
    deblur_img_dir = deblur_dir + img_name + 'DEBLUR.png'
    ssim_value = get_ssim(gt_img_dir, deblur_img_dir)
    avg_ssim = avg_ssim + ssim_value
    # Print the PSNR value
    print(f'PSNR value is {ssim_value} for {img}')

avg_ssim = avg_ssim / len(os.listdir(gt_dir))
print(f'Average PSNR value is {avg_ssim}.')

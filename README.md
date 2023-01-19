# Deep Wiener Deconvolution:

This repository is a PyTorch implementation of the paper:

**Deep Wiener Deconvolution: Wiener Meets Deep Learning for Image Deblurring**

Jiangxin Dong, Stefan Roth, and Bernt Schiele

To appear at NeurIPS 2020 (**Oral Presentation**)

[[Paper]](https://proceedings.neurips.cc/paper/2020/file/0b8aff0438617c055eb55f0ba5d226fa-Paper.pdf)/[[Supplemental]](https://proceedings.neurips.cc/paper/2020/file/0b8aff0438617c055eb55f0ba5d226fa-Supplemental.pdf)

Please proceed to their official implementation code page for original codes.
![Official Page](https://gitlab.mpi-klsb.mpg.de/jdong/dwdn/-/tree/master)

![Pipeline](https://gitlab.mpi-klsb.mpg.de/jdong/dwdn/raw/master/images/pipeline5.png)

>Deep Wiener deconvolution network. While previous work mostly relies on a deconvolution in the image space, our network first extracts useful feature information from the blurry input image and then conducts an explicit Wiener deconvolution in the (deep) feature space through Eqs. (3) and (8). A multi-scale encoder-decoder network progressively restores clear images, with fewer artifacts and finer detail. The whole network is trained in an end-to-end manner.

## Requirements

Compatible with Python 3

Main requirements: PyTorch 1.1.0 or 1.5.0 or 0.4.1 are tested

To install requirements:

```setup
pip install torch==1.1.0 torchvision==0.3.0
pip install -r requirements.txt
```

## Evaluation

To evaluate the deep Wiener deconvolution network on test examples, run:

```eval
python main.py
```

## Pre-trained Model

./model/model_DWDN.pt

## Bibtex

Please cite our paper if it is helpful to your work:

```
@article{dong2020deep,
  title={Deep Wiener Deconvolution: Wiener Meets Deep Learning for Image Deblurring},
  author={Dong, Jiangxin and Roth, Stefan and Schiele, Bernt},
  journal={Advances in Neural Information Processing Systems},
  volume={33},
  year={2020}
}
```

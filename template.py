#!/usr/bin/env python
# -*- coding: utf-8 -*-

# below is the code for training
data_dir = '../train-val-test-data/003deg_with_Gaussian/'


def set_train_template(args):
    if args.template == 'DWDN':

        args.task = 'Deblurring'

        if args.task == "Deblurring":
            args.data_train = 'BLUR_IMAGE'
            args.dir_data = data_dir + 'TrainingData'
            args.data_test = 'BLUR_IMAGE'
            args.dir_data_test = data_dir + '/ValData'
            args.reset = False
            args.model = "deblur"
            args.pre_train = '.'
            args.load = '.'
            args.resume = False

            # change this following to resume a training
            # args.pre_train = "./experiment/20230119_2303/model/model_latest.pt"
            # args.resume = True
            # args.load = '20230119_2303'
            args.save = '.'

            args.loss = "1*L1"
            args.grad_clip = 0.5
            if args.test_only:
                args.save = "deblur_test"
            args.save_results = True
            args.save_models = True
            args.no_augment = False


# below is the code for testing
def set_test_template(args):
    if args.template == 'DWDN':

        args.task = 'Deblurring'

        if args.task == "Deblurring":
            args.data_train = 'BLUR_IMAGE'
            # args.dir_data = '../train-val-test-data/001deg/TrainingData'
            args.data_test = 'BLUR_IMAGE'
            args.dir_data_test = data_dir + '/TestData'
            args.reset = False
            args.model = "deblur"
            args.test_only = True
            args.pre_train = "./experiment/model_003deg_with_Gaussian/model/model_latest.pt"
            # args.pre_train = "./model/model_DWDN.pt"
            args.resume = True
            args.save = "deblur"
            args.loss = "1*L1"
            args.patch_size = 256
            args.grad_clip = 0.5
            if args.test_only:
                args.save = "deblur_test"
            args.save_results = True
            args.save_models = False
            args.no_augment = True

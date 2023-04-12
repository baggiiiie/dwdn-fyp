#!/usr/bin/env python
# -*- coding: utf-8 -*-

# below is the code for training
# data_dir = '../dwdn-data/datasets/600um_with_gaussian/'


def set_train_template(args):
    if args.template == 'DWDN':
        data_dir = args.dataset_dir

        if args.task == "Deblurring":

            args.data_train = 'BLUR_IMAGE'
            args.dir_data = data_dir + 'TrainingData'
            args.reset = False
            args.save_results = True
            args.save_models = True
            args.no_augment = True
            args.grad_clip = 0.5
            args.save = "deblur"

            if args.train_with_val:

                args.data_test = 'BLUR_IMAGE'
                args.dir_data_test = data_dir + '/ValData'
                args.pre_train = '.'
                args.load = '.'
                args.resume = False

                # change this following to resume a training
                # args.pre_train = "./experiment/20230119_2303/model/model_latest.pt"
                # args.resume = True
                # args.load = '20230119_2303'
                args.save = '.'

                if args.test_only:
                    args.save = "deblur_test"

            else:
                args.data_test = 'BLUR_IMAGE'
                args.dir_data_test = data_dir + '/TestData'
                args.test_only = True
                args.pre_train = "../dwdn-data/models/model_600um_with_Gaussian/model/model_latest.pt"
                args.resume = True
                args.save = "deblur_test"

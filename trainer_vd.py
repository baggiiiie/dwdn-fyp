import os
import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lrs
from tqdm import tqdm
import time
import utils_deblur
import torch.nn.functional as F


class Trainer_VD:
    def __init__(self, args, loader, my_model, my_loss, ckp):
        self.n_levels = None
        self.scale = None
        self.start_time = None
        self.args = args

        self.device = torch.device('cpu' if self.args.cpu else 'cuda')
        self.loader_train = loader.loader_train
        self.loader_test = loader.loader_test
        self.model = my_model
        self.loss = my_loss
        self.optimizer = self.make_optimizer()
        self.scheduler = self.make_scheduler()
        self.ckp = ckp
        self.best_val_loss = 0
        self.best_ep = 0
        self.error_last = 1e8

        if args.load != '.':
            self.optimizer.load_state_dict(torch.load(os.path.join(ckp.dir, 'optimizer.pt')))
            # for _ in range(len(ckp.psnr_log)):
            #     self.scheduler.step()

    def set_loader(self, new_loader):
        self.loader_train = new_loader.loader_train
        self.loader_test = new_loader.loader_test

    def make_optimizer(self):
        kwargs = {'lr': self.args.lr, 'weight_decay': self.args.weight_decay}
        return optim.Adam(self.model.parameters(), **kwargs)

    def clip_gradient(self, optimizer, grad_clip):
        """
        Clips gradients computed during backpropagation to avoid explosion of gradients.

        :param optimizer: optimizer with the gradients to be clipped
        :param grad_clip: clip value
        """
        for group in optimizer.param_groups:
            for param in group["params"]:
                if param.grad is not None:
                    param.grad.data.clamp_(-grad_clip, grad_clip)

    def make_scheduler(self):
        kwargs = {'step_size': self.args.lr_decay, 'gamma': self.args.gamma}
        return lrs.StepLR(self.optimizer, **kwargs)

    def train(self):
        # self.scheduler.step()
        self.loss.step()
        epoch = self.scheduler.last_epoch + 1
        lr = self.scheduler.get_last_lr()[0]
        total_epoch = self.args.epochs
        print()
        print(f'Image Deblur Training epoch {epoch}/{total_epoch}')
        self.start_time = time.time()
        loss = 0
        self.loss.start_log()
        self.model.train()
        self.ckp.start_log(train=True, val=False)

        tqdm_train = tqdm(self.loader_train, unit='batch', ncols=80)
        for batch, (blur, sharp, kernel, filename) in enumerate(tqdm_train):
            blur = torch.squeeze(blur, 1)
            sharp = torch.squeeze(sharp, 1)
            kernel = torch.squeeze(kernel, 1)

            blur = blur.to(self.device)
            sharp = sharp.to(self.device)

            self.optimizer.zero_grad()
            # print(f'train:{filename}')
            deblur = self.model(blur, kernel)
            self.n_levels = 2
            self.scale = 0.5
            loss = 0
            for level in range(self.n_levels):
                scale = self.scale ** (self.n_levels - level - 1)
                n, c, h, w = sharp.shape
                hi = int(round(h * scale))
                wi = int(round(w * scale))
                sharp_level = F.interpolate(sharp, (hi, wi), mode='bilinear')
                loss = loss + self.loss(deblur[level], sharp_level)

            self.ckp.report_log(loss.item(), train=True, val=False)
            loss.backward()
            self.clip_gradient(self.optimizer, self.args.grad_clip)
            self.optimizer.step()

            # if (batch + 1) % self.args.print_every == 0:
            #     self.ckp.write_log('[{}/{}]\tLoss : {}'.format(
            #         (batch + 1) * self.args.batch_size, len(self.loader_train.dataset),
            #         self.loss.display_loss(batch)))

        print("Training loss: %.4f" % (float(loss.item())))
        self.scheduler.step()
        self.loss.end_log(len(self.loader_train))
        self.error_last = self.loss.log[-1, -1]

    def test(self):
        if self.args.train_with_val:
            return self.validation()

        epoch = self.scheduler.last_epoch
        self.model.eval()
        self.ckp.start_log(train=False, val=False)

        with torch.no_grad():
            tqdm_test = tqdm(self.loader_test, ncols=80)
            for idx_img, (blur, sharp, kernel, filename) in enumerate(tqdm_test):

                blur = torch.squeeze(blur, 0)
                kernel = torch.squeeze(kernel, 0)

                blur = blur.to(self.device)

                deblur = self.model(blur, kernel)

                if self.args.save_images:
                    deblur = utils_deblur.postprocess(deblur[-1], rgb_range=self.args.rgb_range)
                    save_list = [deblur[0]]
                    self.ckp.save_images(filename, save_list)

            if self.args.save_models:
                self.ckp.save(self, epoch, False)

            # self.ckp.report_log(psnr.item(), train=False, val=False)
            self.ckp.end_log(len(self.loader_test), train=False, val=False)

    def validation(self):
        epoch = self.scheduler.last_epoch
        self.model.eval()
        self.ckp.start_log(train=False, val=True)
        # below is for validation set
        running_val_loss = 0
        loss = 0
        with torch.no_grad():
            for idx_img, (blur, sharp, kernel, filename) in enumerate(self.loader_test):
                blur = torch.squeeze(blur, 0)
                sharp = torch.squeeze(sharp, 0)
                kernel = torch.squeeze(kernel, 0)

                blur = blur.to(self.device)
                sharp = sharp.to(self.device)

                # print(f'val: {filename}')
                deblur = self.model(blur, kernel)

                self.n_levels = 2
                self.scale = 0.5

                for level in range(self.n_levels):
                    scale = self.scale ** (self.n_levels - level - 1)
                    # print(sharp.shape)
                    n, c, h, w = sharp.shape
                    hi = int(round(h * scale))
                    wi = int(round(w * scale))
                    sharp_level = F.interpolate(sharp, (hi, wi), mode='bilinear')
                    loss = loss + self.loss(deblur[level], sharp_level)
                    running_val_loss += loss

            avg_vloss = running_val_loss / (idx_img + 1)
            self.ckp.report_log(avg_vloss.item(), train=False, val=True)

        # if self.args.save_models and epoch % 10 == 0 or epoch == 1:
        if self.args.save_models:
            self.ckp.save(self, epoch, False)
        self.ckp.end_log(len(self.loader_test), train=True, val=True)
        self.ckp.plot_loss_log(epoch)

        if self.best_val_loss == 0 or self.best_val_loss > avg_vloss.item():
            self.best_val_loss = avg_vloss.item()
            self.best_ep = epoch

        print("Validation loss: %.4f" % (float(avg_vloss.item())))
        print("Time taken: %.2fs" % (time.time() - self.start_time))

    def terminate(self):
        if self.args.test_only:
            self.test()
            return True
        else:
            epoch = self.scheduler.last_epoch + 1
            print(f'lowest val loss at epoch {self.best_ep}: {self.best_val_loss}')
            return epoch >= self.args.epochs


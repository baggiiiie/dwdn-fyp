import os
from data import vsrdata


class Benchmark(vsrdata.VSRData):
    """
    Data generator for benchmark tasks
    """
    def __init__(self, args, name='', train=False):
        super(Benchmark, self).__init__(
            args, name=name, train=train
        )

    def _set_filesystem(self, dir_data):

        if self.args.template == "DWDN" :
            self.apath = os.path.join(dir_data)
            if not self.args.test_only:
                self.dir_image_blur = os.path.join(self.apath, "blurred_img")
                self.dir_image_gt = os.path.join(self.apath, "clear_img")
                self.dir_image_kernel = os.path.join(self.apath, "blur_kernel")
                print("validation image path :" , self.dir_image_blur)
            else:
                self.dir_image_blur = os.path.join(self.apath, "blurred_img")
                self.dir_image_gt = os.path.join(self.apath, "blurred_img")
                self.dir_image_kernel = os.path.join(self.apath, "blur_kernel")
                print("Test image path :" , self.dir_image_blur)




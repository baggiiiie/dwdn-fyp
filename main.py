import torch

import data
import model
import loss
from option import args
from trainer_vd import Trainer_VD
from logger import logger

torch.manual_seed(args.seed)
chkp = logger.Logger(args)

print("Deep Wiener Deconvolution Network")
loader = data.Data(args)
model = model.Model(args, chkp)
loss = loss.Loss(args, chkp) if not args.test_only else None
t = Trainer_VD(args, loader, model, loss, chkp)
while not t.terminate():
    t.train()
    t.test()
    # t.validation()

chkp.done()
# print(torch.cuda.is_available())
# current = torch.cuda.current_device()
# print(current)
# print(torch.cuda.get_device_name(current))
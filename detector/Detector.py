from detector.darknet import *


class Detector(object):
    model = None
    meta = None

    def __init__(self, net_cfg_path, net_weights_path, net_datafile_path):
        self.model = load_net(net_cfg_path, net_weights_path, 0)
        self.meta = load_meta(net_datafile_path)

    def detect(self, img_path):
        return detect(self.model, self.meta, img_path)

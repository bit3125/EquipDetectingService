from detector.darknet import *


class Detector(object):
    model = None
    meta = None

    def __init__(self, net_cfg_path, net_weights_path, net_datafile_path):
        self.model = load_net(net_cfg_path, net_weights_path, 0)
        self.meta = load_meta(net_datafile_path)

    def detect(self, img_path):
        if isinstance(img_path, str):
            img_path = str.encode(img_path)

        downstream_ret = detect(self.model, self.meta, img_path)
        if len(downstream_ret) == 0:
            return None

        downstream_ret = downstream_ret[0]
        map = dict()
        map["class"] = bytes.decode(downstream_ret[0]).strip()
        map["confidence"] = downstream_ret[1]
        map["box"] = downstream_ret[2]
        return map

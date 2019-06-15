import configparser
from detector.Detector import Detector


class Server(object):

    CFG_FILE_PATH = "conf/machine_room.cfg"  # 2brm

    NET_CFG_PATH = None
    NET_DATAFILE_PATH = None
    NET_WEIGHTS_PATH = None
    IMG_PATH = None

    detector = None

    def __init__(self):
        self.init_cfg()
        self.detector = Detector(self.NET_CFG_PATH, self.NET_WEIGHTS_PATH, self.NET_DATAFILE_PATH)

    def init_cfg(self):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(self.CFG_FILE_PATH)

        self.NET_CFG_PATH = str.encode(cfg_parser.get("cfg", "net_cfg_path"))
        self.NET_DATAFILE_PATH = str.encode(cfg_parser.get("cfg", "net_datafile_path"))
        self.NET_WEIGHTS_PATH = str.encode(cfg_parser.get("cfg", "net_weights_path"))
        self.IMG_PATH = str.encode(cfg_parser.get("img", "img_path"))
        # self.img_path = cfg_parser.get("img", "img_path")

    def run(self):
        img_path = self.IMG_PATH
        print(self.detect(img_path))
        # TODO
        '''
        接下来只要在这里开发就好了，把消息队列接进来，
        然后写一个死循环来阻塞式调用detect方法
        '''


        # while True:
        #     pass

    def detect(self, img_path):
        return self.detector.detect(img_path)







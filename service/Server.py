import configparser
from detector.Detector import Detector
from constant.constant import CFG_FILE_PATH, RBTMQ_CFG_FILE_PATH
from mq.rabbitmq import RabbitMQConnector
import json


class Server(object):

    detector = None
    detect_request_queue = None
    detect_main_response_queue = None

    def __init__(self):
        self.__init_detector()
        self.__init_mq()

    def __init_detector(self):
        cfgps = configparser.ConfigParser()
        cfgps.read(CFG_FILE_PATH)

        net_cfg_path = str.encode(cfgps.get("cfg", "net_cfg_path"))
        net_datafile_path = str.encode(cfgps.get("cfg", "net_datafile_path"))
        net_weights_path = str.encode(cfgps.get("cfg", "net_weights_path"))
        self.detector = Detector(net_cfg_path, net_weights_path, net_datafile_path)

    def __init_mq(self):
        cfgps = configparser.ConfigParser()
        cfgps.read(RBTMQ_CFG_FILE_PATH)

        self.detect_main_response_queue = RabbitMQConnector()
        self.detect_main_response_queue.set_producer(exchange_name=cfgps.get("exchange", "exchange_name")
                                                     , routing_key=cfgps.get("routing_key", "detect_main_response_queue"))

        self.detect_request_queue = RabbitMQConnector()
        self.detect_request_queue.set_consumer(queue_name=cfgps.get("queue", "detect_request_queue")
                                               , on_message_callback=self.request_handler)  # self.request_handler)

    def run(self):
        self.detect_request_queue.consume_run()

    def request_handler(self, ch, method, properties, body):
        # body type : bytes array
        print("receive msg:{}".format(body))

        req = json.loads(body)
        req_id = int(req["request_id"])
        req_path = req["path"]

        resp = dict()
        resp["request_id"] = req_id
        resp["path"] = req_path
        resp["item_list"] = self.detector.detect(req_path)  # list

        resp_json = json.dumps(resp)
        self.detect_main_response_queue.produce(resp_json)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息

import configparser
import pika
from constant.constant import RBTMQ_CFG_FILE_PATH


class RabbitMQConnector(object):

    connection = None
    channel = None
    queue_name = None
    exchange_name = None
    routing_key = None
    is_producer = None

    def __init__(self):
        self.__init_connection()
        self.channel = self.connection.channel()

    def __init_connection(self):
        cfgps = configparser.ConfigParser()
        cfgps.read(RBTMQ_CFG_FILE_PATH)

        ip_address = cfgps.get("connection", "ip_address_local")
        port = cfgps.get("connection", "port")
        credentials = pika.PlainCredentials(cfgps.get("connection", "username"), cfgps.get("connection", "password"))
        connection_params = pika.ConnectionParameters(host=ip_address, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(connection_params)
        return self.connection

    def set_consumer(self, queue_name, on_message_callback):
        self.queue_name = queue_name
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback)
        self.is_producer = False

    def set_producer(self, exchange_name, routing_key):
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.is_producer = True

    def produce(self, body):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, body=body)

    def consume_run(self):
        self.channel.start_consuming()


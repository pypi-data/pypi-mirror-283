import logging
from ..utility.kafka_handler import KafkaHandler

class Logger:
    def __init__(self, logLevel="INFO"):
        self.logger = logging.getLogger(__name__)
        log_level = getattr(logging, logLevel.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # Create & add handler to log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def addHandler(self, producer, domain, automation_uuid):
        # Create & add handler to log messages to kafka topic
        topic = 'zeno.automations.log'
        kafka_handler = KafkaHandler(producer, topic, domain, automation_uuid)
        self.logger.addHandler(kafka_handler)

    def info(self, message):
        """
        :param message: Message to log
        :return: None
        """
        self.logger.info(message)

    def error(self, message):
        """
        :param message: Message to log
        :return: None
        """
        self.logger.error(message, exc_info=True)

    def debug(self, message):
        """
        :param message: Message to log
        :return: None
        """
        self.logger.debug(message)

    def warning(self, message):
        """
        :param message: Message to log
        :return: None
        """
        self.logger.warning(message)
    
    def exception(self, message):
        """
        :param message: Message to log
        :return: None
        """
        self.logger.exception(message)
import uuid
from logging import Handler

class KafkaHandler(Handler):
    """
    A handler class which writes formatted logging records to kafka topic.
    """

    def __init__(self, producer, topic, domain, automation_uuid):
        Handler.__init__(self)
        self.topic = topic
        self.domain = domain
        self.automation_uuid = automation_uuid
        self.producer = producer
    
    def close(self):
        if self.producer is None:
            return
        self.producer.close()
        super().close()

    def emit(self, record):
        if self.producer is None:
            return
        
        try:
             # Format the log message
            level = record.levelname
            status = 'success'
            if level != 'INFO':
                status = 'failure'
            log_body = {
                "domain": self.domain,
                "execution_id": uuid.uuid4().hex,
                "automation_uuid": self.automation_uuid,
                "executed_at": record.created,
                "executed_by": 1234,
                "status": status,
                "message": record.getMessage(),
                "stack_trace": record.exc_text,
                "log_type": "inline"
            }
            self.producer.send(self.topic, value=log_body)
            self.producer.flush()
            return
        except Exception:
            self.handleError(record)
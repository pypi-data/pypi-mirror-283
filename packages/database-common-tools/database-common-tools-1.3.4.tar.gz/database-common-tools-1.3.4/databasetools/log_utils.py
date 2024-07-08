import logging
from logging import handlers

def setup_logging(log_file, time_unit='D', backupCount=3, encoding='utf-8'):
    """
    Setup logging configuration.
        
    :param log_file: Path to the log file
    :param time_unit: time unit
    :param backupCount: log backup count
    :param encoding:  text encode
    """
    log_format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    handler = handlers.TimedRotatingFileHandler(filename=log_file, when=time_unit, backupCount=backupCount, encoding=encoding)
    handler.setFormatter(log_format)
    logger = logging.getLogger(log_file)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

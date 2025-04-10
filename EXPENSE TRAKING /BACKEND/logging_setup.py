import logging

def setup_logger(name, log_file = 'server.log', level=logging.DEBUG):

    logger = logging.getLogger(name)

    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter) 
    logger.addHandler(file_handler)

    if not logger.handlers:
        logger.addHandler(file_handler)


    return logger
def setupLogging():
    from tornado.log import enable_pretty_logging
    enable_pretty_logging()

def getLogging():
    import logging
    logger = logging.getLogger("tornado.general")
    logger.setLevel(logging.DEBUG)
    return logger

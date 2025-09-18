import logging

# logging.basicConfig(level=logging.ERROR,
#                     format='[%(time)s.%(asctime)03d %(levelname)s] %(module)15s %(funcName)20s %(lineno)4d %(message)s')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('main_logger')
# handler = logging.Handler(logging.DEBUG)
# formatter = logging.Formatter(fmt='[%(time)s.%(asctime)03d %(levelname)s] %(module)15s %(funcName)20s %(lineno)4d %(message)s',
#                               datefmt=r'%Y-%m-%d %H:%M:%S')
# handler.setFormatter(formatter)
# logger.addHandler(handler)



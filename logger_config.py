import logging

logging.basicConfig(level=logging.ERROR,
                    format='[%(time)s.%(asctime)03d %(levelname)s] %(module)15s %(funcName)20s %(lineno)4d %(message)s',
                    datefmt=r'%Y-%m-%d %H:%M%:%S')

logger = logging.getLogger('main_logger')
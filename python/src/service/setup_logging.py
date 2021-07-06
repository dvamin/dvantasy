import logging
import sys

LOG_FORMAT = "%(asctime)s %(levelname)s: %(name)s - %(message)s"


def configure_logging(root_dir: str, verbosity=logging.INFO):
    root = logging.getLogger(root_dir)
    root.setLevel(verbosity)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    root.addHandler(handler)

import logging
from degel_python_utils import log_tools


def test_setup_logger():
    log_tools.setup_logger("my_app", logging.DEBUG)
    logger = logging.getLogger("my_app")
    assert logger.isEnabledFor(logging.DEBUG)
    log_tools.setup_logger("my_app", logging.INFO)
    assert logger.isEnabledFor(logging.INFO)
    assert not logger.isEnabledFor(logging.DEBUG)

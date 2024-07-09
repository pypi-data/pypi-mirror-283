import logging
from robot.libraries.BuiltIn import BuiltIn
from Xray import Xray

logger = logging.getLogger(__name__)

class Listener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3
    XRAY = Xray()

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(self, suite, result):
        logger.warning(f"Suite '{suite.name}' starting with status {result.status}.")
        self.XRAY.createTestExecution()

    def start_test(self, test, result):
        pass

    def end_test(self, test, result):
        pass

    def end_suite(self, suite, result):
        logger.warning(f"Suite '{suite.name}' ending with status {result.status}.")
        pass

    def log_message(self, message):
        pass

    def message(self, message):
        pass

    def debug_file(self, path):
        pass

    def output_file(self, path):
        pass

    def xunit_file(self, path):
        pass

    def log_file(self, path):
        pass

    def report_file(self, path):
        pass

    def close(self):
        pass
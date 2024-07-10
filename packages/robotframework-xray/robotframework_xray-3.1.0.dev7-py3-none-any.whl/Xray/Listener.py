import logging
from robot.libraries.BuiltIn import BuiltIn
from robot import result, running
from .xray import Xray

logger = logging.getLogger(__name__)


class Listener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3
    XRAY = Xray()

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(self, suite: running.TestSuite, result: result.TestSuite):
        logger.warning(f"Suite '{suite.name}' starting with status {result.status}.")
        print(result.test_class.tags)
        self.XRAY.createTestExecution(result.test_class.tags)

    def start_test(self, test, result):
        pass

    def end_test(self, test, result):
        pass

    def end_suite(self, suite, result):
        logger.warning(f"Suite '{suite.name}' ending with status {result.status}.")
        pass

    def start_keyword(self, data: running.Keyword, result: result.Keyword):
        pass
        # self.start_body_item(data, result)

    def end_keyword(self, data: running.Keyword, result: result.Keyword):
        pass
        # self.end_body_item(data, result)

    def log_message(self, message):
        pass

    def message(self, message):
        pass

    def debug_file(self, path):
        pass

    def output_file(self, path):
        pass

    def log_file(self, path):
        pass

    def report_file(self, path):
        pass

    def close(self):
        print("Fim.")
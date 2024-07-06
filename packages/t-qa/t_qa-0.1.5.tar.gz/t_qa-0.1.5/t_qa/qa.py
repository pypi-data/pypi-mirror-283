"""QA.py module contains the QA class for the Digital Worker's process."""
import atexit
import os
import re
import traceback
from datetime import datetime

import pytz
import yaml
from ta_bitwarden_cli.exceptions import NotLoggedInError
from ta_bitwarden_cli.handler import get_attachment
from thoughtful.supervisor import report_builder

from .config import DEFAULT_QA_RESULT_FILE_PATH, DEFAULT_TEST_CASES_FILE_PATH, LOCAL_RUN, SCOPES, Inputs
from .excel_processing.google_sheet import GoogleSheet
from .excel_processing.report import _Report
from .goole_api.account import Account
from .goole_api.google_drive_service import GoogleDriveService
from .logger import logger
from .models import RunData, TestCase
from .status import Status
from .utils import SingletonMeta, install_sys_hook
from .workitems import METADATA, VARIABLES


class QA(metaclass=SingletonMeta):
    """QA class for the Digital Worker's process."""

    def __init__(self):
        """Initialize the QA process."""
        self.test_cases: list[TestCase] = []
        self.run_status: str = Status.SUCCESS.value
        self.service_account_key_path: str = None
        self.start_datetime = None

    def configurate(
        self,
        test_cases_file_path: str = DEFAULT_TEST_CASES_FILE_PATH,
        service_account_key_path: str = None,
    ):
        """Configurate the QA process."""
        if Inputs.ENVIRONMENT == "production":
            return
        if not os.path.exists(test_cases_file_path):
            logger.warning(f"Test cases file not found: {test_cases_file_path}")
        if service_account_key_path:
            self.service_account_key_path = service_account_key_path
        else:
            try:
                self.service_account_key_path = get_attachment(
                    "T-QA Google",
                    "service_account_key.json",
                )
            except NotLoggedInError:
                return
            except ValueError:
                logger.warning("There are no access to 'T-QA Google' collection")
                return
            if LOCAL_RUN:
                return
            self.start_datetime = self.__get_start_datetime()
            try:
                with open(test_cases_file_path) as test_cases_file:
                    test_cases = yaml.safe_load(test_cases_file)["test_cases"]
                    self.test_cases = [TestCase(**test_case) for test_case in test_cases]
            except (TypeError, KeyError, ValueError) as e:
                logger.error(f"Error during reading test cases: {e}")
                return
            except FileNotFoundError:
                return

        atexit.register(self.dump)

    def __get_start_datetime(self):
        """Get the start datetime."""
        root_path = os.environ.get("ROBOT_ROOT")
        console_log_folder_path = os.path.abspath(os.path.join(root_path, os.pardir))
        console_log_file_path = os.path.join(console_log_folder_path, "console.txt")
        with open(console_log_file_path, "r") as file:
            data = file.read()
        date_str = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", data)[0]
        date_str += "UTC"
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%Z")

    def __set_test_case_status(self, id: str, status: str):
        """Check the test case."""
        if Inputs.ENVIRONMENT == "production":
            logger.info("QA process is in the PROD mode")
            return
        for test_case in self.test_cases:
            if test_case.id == id:
                test_case.status = status
            else:
                logger.warning(f"Test case with name {id} not found")

    def test_case_pass(self, id: str):
        """Check the test case passed."""
        self.__set_test_case_status(id=id, status=Status.PASS.value)

    def test_case_fail(self, id: str):
        """Check the test case failed."""
        self.__set_test_case_status(id=id, status=Status.FAIL.value)

    def dump(self):
        """Dump the test cases."""
        if Inputs.ENVIRONMENT == "production":
            logger.info("QA process is in the PROD mode")
            return
        try:
            run_data = RunData(
                run_date=self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                duration=self.__get_duration(),
                empower_env=VARIABLES.get("environment", ""),
                run_link=METADATA.get("processRunUrl", ""),
                status=self.__get_run_result(),
                test_cases=self.test_cases,
                bugs="Not implemented",
                code_coverage="Not implemented",
                total_records=0,
                success_records=0,
                failed_records=0,
            )
            BOT_ACCOUNT = Account(
                service_account_key_path=self.service_account_key_path,
                scopes=SCOPES,
            )
            google_sheet = GoogleSheet(BOT_ACCOUNT)
            google_drive = GoogleDriveService(BOT_ACCOUNT)
            report = _Report(DEFAULT_QA_RESULT_FILE_PATH, google_sheet=google_sheet, google_drive=google_drive)
            report.dump(run_data)

        except Exception as e:
            logger.error(f"Error during dumping: {e}")
            traceback.print_exc()

    def __get_run_result(self):
        if self.run_status == Status.SUCCESS.value:
            try:
                self.run_status = report_builder.status.value
            except AttributeError:
                logger.error("Could not get the run result from supervisor.")
        return self.run_status

    def __get_duration(self):
        duration = datetime.now(pytz.UTC) - self.start_datetime.astimezone(pytz.UTC)
        secondes = duration.seconds
        minutes = secondes // 60
        hours = minutes // 60
        duration_str = f"{hours}h {minutes}m {secondes % 60}s"
        return duration_str


t_qa = QA()
install_sys_hook(t_qa)

configure_qa = t_qa.configurate
test_case_failed = t_qa.test_case_fail
test_case_passed = t_qa.test_case_pass

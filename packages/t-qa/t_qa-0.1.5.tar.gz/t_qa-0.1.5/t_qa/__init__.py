"""Top-level package for T QA."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "__version__ = '0.1.5'"

from .qa import configure_qa, test_case_passed, test_case_failed

__all__ = [
    "configure_qa",
    "test_case_passed",
    "test_case_failed",
]

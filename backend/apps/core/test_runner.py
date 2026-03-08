import json
import time
import unittest
from pathlib import Path

from django.conf import settings
from django.test.runner import DiscoverRunner


class TimingTextTestResult(unittest.TextTestResult):
    def startTestRun(self):
        super().startTestRun()
        self._start_times = {}
        self.timings = []

    def startTest(self, test):
        self._start_times[test.id()] = time.perf_counter()
        super().startTest(test)

    def stopTest(self, test):
        started = self._start_times.pop(test.id(), None)
        if started is not None:
            self.timings.append(
                {
                    "test": test.id(),
                    "duration_seconds": round(time.perf_counter() - started, 6),
                }
            )
        super().stopTest(test)


class TimingTextTestRunner(unittest.TextTestRunner):
    resultclass = TimingTextTestResult


class GuardrailedDiscoverRunner(DiscoverRunner):
    test_runner = TimingTextTestRunner

    def run_suite(self, suite, **kwargs):
        result = super().run_suite(suite, **kwargs)
        self._last_result = result
        return result

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        started = time.perf_counter()
        failures = super().run_tests(test_labels, extra_tests=extra_tests, **kwargs)
        total = round(time.perf_counter() - started, 6)
        self._write_report(total)
        return failures

    def _write_report(self, total_duration):
        report_path = Path(settings.TEST_REPORT_PATH)
        report_path.parent.mkdir(parents=True, exist_ok=True)

        timings = getattr(self._last_result, "timings", []) if hasattr(self, "_last_result") else []
        slow_threshold = settings.TEST_SLOW_TEST_THRESHOLD_SECONDS
        slow_tests = [t for t in timings if t["duration_seconds"] >= slow_threshold]
        slow_tests.sort(key=lambda row: row["duration_seconds"], reverse=True)

        report = {
            "generated_at_unix": int(time.time()),
            "total_duration_seconds": total_duration,
            "runtime_target_seconds": settings.TEST_RUNTIME_TARGET_SECONDS,
            "runtime_target_met": total_duration <= settings.TEST_RUNTIME_TARGET_SECONDS,
            "slow_test_threshold_seconds": slow_threshold,
            "slow_tests": slow_tests,
            "top_10_slowest_tests": sorted(
                timings, key=lambda row: row["duration_seconds"], reverse=True
            )[:10],
            "known_flaky_tests": settings.KNOWN_FLAKY_TESTS,
        }

        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

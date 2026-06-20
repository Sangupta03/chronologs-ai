from django.test import TestCase

from .parser import normalize_level, parse_log_line, parse_timestamp


class ParseTimestampTests(TestCase):
    def test_parses_datetime_with_seconds(self):
        self.assertIsNotNone(parse_timestamp("2026-03-07 12:01:33"))

    def test_parses_iso_datetime(self):
        self.assertIsNotNone(parse_timestamp("2026-03-07T12:01:33"))

    def test_parses_date_only(self):
        self.assertIsNotNone(parse_timestamp("2026-03-07"))

    def test_returns_none_for_garbage(self):
        self.assertIsNone(parse_timestamp("not-a-timestamp"))

    def test_returns_none_for_empty_string(self):
        self.assertIsNone(parse_timestamp(""))


class NormalizeLevelTests(TestCase):
    def test_known_levels_map_to_canonical_form(self):
        self.assertEqual(normalize_level("warning"), "WARN")
        self.assertEqual(normalize_level("ERR"), "ERROR")
        self.assertEqual(normalize_level("Error"), "ERROR")
        self.assertEqual(normalize_level("debug"), "DEBUG")

    def test_unknown_level_defaults_to_info(self):
        self.assertEqual(normalize_level("TOTALLY_UNKNOWN"), "INFO")


class ParseLogLineTests(TestCase):
    def test_format_1_space_separated(self):
        line = "2026-03-07 12:01:33 ERROR payment-service Database connection timeout"
        parsed = parse_log_line(line)
        self.assertEqual(parsed["timestamp"], "2026-03-07 12:01:33")
        self.assertEqual(parsed["level"], "ERROR")
        self.assertEqual(parsed["service"], "payment-service")
        self.assertEqual(parsed["message"], "Database connection timeout")

    def test_format_2_bracketed_level(self):
        line = "[ERROR] 2026-03-07T12:01:33 payment-service: DB connection failed"
        parsed = parse_log_line(line)
        self.assertEqual(parsed["level"], "ERROR")
        self.assertEqual(parsed["service"], "payment-service")

    def test_format_3_date_only(self):
        line = "INFO 2026-03-07 user-service request completed"
        parsed = parse_log_line(line)
        self.assertEqual(parsed["level"], "INFO")
        self.assertEqual(parsed["service"], "user-service")

    def test_malformed_line_returns_none(self):
        self.assertIsNone(parse_log_line("this is not a log line at all"))

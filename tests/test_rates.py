import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service=service)

    def test_explicit_standard_matches_default(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 2, 3.14159):
                with self.subTest(zone=zone, weight=weight):
                    base = 5.0 if zone == "local" else 8.0
                    expected = round(base + 1.5 * weight, 2)
                    self.assertEqual(shipping_quote(weight, zone), expected)
                    self.assertEqual(shipping_quote(weight, zone, "standard"), expected)

    def test_express_rates(self):
        self.assertEqual(shipping_quote(2, "local", "express"), 15.0)
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_surcharge_and_rounding(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 2, 3.14159):
                with self.subTest(zone=zone, weight=weight):
                    standard = shipping_quote(weight, zone)
                    self.assertEqual(
                        shipping_quote(weight, zone, service="express"),
                        round(standard + 7.0, 2),
                    )

    def test_unknown_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service=service)

    def test_unknown_service(self):
        for service in ("overnight", "", "Express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service=service)

from datetime import date
from decimal import Decimal
import unittest

from receipt_ledger.parser import aggregate_by_category, parse_receipt_line, parse_receipts


class ReceiptParserTests(unittest.TestCase):
    def test_parse_valid_line(self):
        receipt = parse_receipt_line("2026-05-01 | Noodle Shop | Food | 18.50 | cny")

        self.assertEqual(receipt.purchased_at, date(2026, 5, 1))
        self.assertEqual(receipt.merchant, "Noodle Shop")
        self.assertEqual(receipt.category, "food")
        self.assertEqual(receipt.amount, Decimal("18.50"))
        self.assertEqual(receipt.currency, "CNY")

    def test_parse_receipts_skips_blank_lines_and_comments(self):
        receipts = parse_receipts(
            [
                "# exported from phone",
                "",
                "2026-05-01 | Metro | Transport | 4.00 | CNY",
            ]
        )

        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0].merchant, "Metro")

    def test_aggregate_by_category_keeps_currencies_separate(self):
        receipts = parse_receipts(
            [
                "2026-05-01 | Cafe | Food | 10.00 | CNY",
                "2026-05-02 | Bookstore | Books | 12.00 | USD",
                "2026-05-03 | Market | Food | 3.25 | CNY",
            ]
        )

        totals = aggregate_by_category(receipts)

        self.assertEqual(totals["food"]["CNY"], Decimal("13.25"))
        self.assertEqual(totals["books"]["USD"], Decimal("12.00"))

    def test_invalid_amount_mentions_line_number(self):
        with self.assertRaisesRegex(ValueError, "line 1: invalid amount"):
            parse_receipts(["2026-05-01 | Cafe | Food | no | CNY"])


if __name__ == "__main__":
    unittest.main()


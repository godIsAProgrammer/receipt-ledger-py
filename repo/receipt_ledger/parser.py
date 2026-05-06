from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable


@dataclass(frozen=True)
class Receipt:
    """单条收据记录，保留原始日期、商户、类别、金额和币种。"""

    purchased_at: date
    merchant: str
    category: str
    amount: Decimal
    currency: str


def parse_receipt_line(line: str) -> Receipt:
    """解析一行收据文本，并把类别和币种归一化。"""

    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 5:
        raise ValueError(f"expected 5 fields, got {len(parts)}: {line!r}")

    raw_date, merchant, category, raw_amount, currency = parts
    if not merchant:
        raise ValueError("merchant is required")
    if not category:
        raise ValueError("category is required")

    try:
        purchased_at = date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ValueError(f"invalid date {raw_date!r}") from exc

    try:
        amount = Decimal(raw_amount)
    except InvalidOperation as exc:
        raise ValueError(f"invalid amount {raw_amount!r}") from exc

    if amount < 0:
        raise ValueError("amount cannot be negative")

    normalized_currency = currency.upper()
    if len(normalized_currency) != 3:
        raise ValueError(f"currency must be a 3-letter code: {currency!r}")

    return Receipt(
        purchased_at=purchased_at,
        merchant=merchant,
        category=category.lower(),
        amount=amount,
        currency=normalized_currency,
    )


def parse_receipts(lines: Iterable[str]) -> list[Receipt]:
    """解析多行收据文本，跳过空行和以 # 开头的注释行。"""

    receipts: list[Receipt] = []
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            receipts.append(parse_receipt_line(stripped))
        except ValueError as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
    return receipts


def aggregate_by_category(receipts: Iterable[Receipt]) -> dict[str, dict[str, Decimal]]:
    """按消费类别聚合金额，并按币种分别保留，避免不同币种直接相加。"""

    totals: dict[str, dict[str, Decimal]] = {}
    for receipt in receipts:
        category_totals = totals.setdefault(receipt.category, {})
        category_totals[receipt.currency] = (
            category_totals.get(receipt.currency, Decimal("0")) + receipt.amount
        )
    return totals

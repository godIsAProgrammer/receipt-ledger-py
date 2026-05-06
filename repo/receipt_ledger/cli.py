from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path

from .parser import aggregate_by_category, parse_receipts


class DecimalEncoder(json.JSONEncoder):
    """把 Decimal 转成字符串，避免 JSON 序列化时丢失金额精度。"""

    def default(self, obj: object) -> object:
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="汇总收据导出文件")
    parser.add_argument("path", type=Path, help="收据文本文件路径")
    parser.add_argument("--category", help="只统计指定消费类别")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    return parser


def summarize_file(path: Path, category: str | None = None) -> dict[str, dict[str, Decimal]]:
    """读取收据文件，并按可选类别过滤后生成汇总。"""

    receipts = parse_receipts(path.read_text(encoding="utf-8").splitlines())
    if category:
        receipts = [receipt for receipt in receipts if receipt.category == category.lower()]
    return aggregate_by_category(receipts)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    totals = summarize_file(args.path, args.category)

    if args.json:
        print(json.dumps(totals, cls=DecimalEncoder, indent=2, sort_keys=True))
        return 0

    for category, currencies in sorted(totals.items()):
        joined = ", ".join(
            f"{currency} {amount:.2f}" for currency, amount in sorted(currencies.items())
        )
        print(f"{category}: {joined}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

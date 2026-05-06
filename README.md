# 收据流水汇总工具

这是一个小型命令行工具，用于把纯文本收据导出文件汇总成按类别统计的消费清单。
项目刻意保持轻量，但包含解析、聚合、命令行参数和测试，适合作为真实 Agent
开发任务的标注仓库。

## 输入格式

输入文件中每一条非空记录使用如下格式：

```text
YYYY-MM-DD | merchant | category | amount | currency
```

以 `#` 开头的行是注释，会被解析器忽略。

## 使用方式

```bash
python -m receipt_ledger.cli data/sample_receipts.txt
python -m receipt_ledger.cli data/sample_receipts.txt --category food
python -m receipt_ledger.cli data/sample_receipts.txt --json
```

## 测试

```bash
python -m unittest discover -s tests
```

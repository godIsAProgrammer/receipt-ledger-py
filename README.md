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

## Docker 环境

构建镜像：

```bash
docker build -t receipt-ledger-py .
```

运行默认测试：

```bash
docker run --rm receipt-ledger-py
```

验证容器工作目录：

```bash
docker run --rm receipt-ledger-py pwd
```

预期输出为：

```text
/app
```

验证容器内初始仓库是否为干净 Git 工作区：

```bash
docker run --rm receipt-ledger-py git status --short
```

预期没有任何输出。

在容器中执行 CLI：

```bash
docker run --rm receipt-ledger-py python -m receipt_ledger.cli data/sample_receipts.txt --json
```

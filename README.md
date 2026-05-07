# 收据流水汇总工具

这是一个小型命令行工具，用于把纯文本收据导出文件汇总成按类别统计的消费清单。
项目刻意保持轻量，但包含解析、聚合、命令行参数、HTTP 服务和测试，适合作为真实
命令行与 HTTP 双入口示例。

## 输入格式

输入文件中每一条非空记录使用如下格式：

```text
YYYY-MM-DD | merchant | category | amount | currency
```

以 `#` 开头的行是注释，会被解析器忽略。

## CLI 使用方式

```bash
python -m receipt_ledger.cli data/sample_receipts.txt
python -m receipt_ledger.cli data/sample_receipts.txt --category food
python -m receipt_ledger.cli data/sample_receipts.txt --json
```

## HTTP 服务

```bash
python -m receipt_ledger.server
# 默认监听 0.0.0.0:8788，可通过 PORT 环境变量覆盖
```

提供的端点：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查，返回 `{"ok": true}` |
| GET | `/summary?path=<file>&category=<cat>` | 读取指定收据文件并按类别聚合 |

示例：

```bash
curl http://127.0.0.1:8788/health
curl "http://127.0.0.1:8788/summary?path=data/sample_receipts.txt"
curl "http://127.0.0.1:8788/summary?path=data/sample_receipts.txt&category=food"
```

## 测试

```bash
python -m unittest discover -s tests
```

## Docker 环境

确保 Docker Desktop 已启动。

在项目根目录构建镜像：

```bash
docker build -t receipt-ledger-py .
```

启动 HTTP 服务：

```bash
docker run --rm -p 8788:8788 receipt-ledger-py
```

服务启动后，在另一个终端验证健康检查：

```bash
curl http://127.0.0.1:8788/health
```

预期响应：

```json
{"ok":true}
```

运行测试请使用显式命令：

```bash
docker run --rm receipt-ledger-py python -m unittest discover -s tests
```

容器内执行原 CLI（适合排查解析逻辑）：

```bash
docker run --rm receipt-ledger-py python -m receipt_ledger.cli data/sample_receipts.txt --json
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

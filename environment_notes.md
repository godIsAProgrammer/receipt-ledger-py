# 环境说明

- 项目语言：Python 3.11+
- Docker 基础镜像：`python:3.12`
- 容器工作目录：`/app`
- 构建时会把项目根目录的仓库文件复制到 `/app`
- 不需要第三方依赖
- 默认启动命令：`python -m receipt_ledger.server`（监听 `0.0.0.0:8788`，可用 `PORT` 环境变量覆盖）
- 默认验证命令：`python -m unittest discover -s tests`
- HTTP 端点：`GET /health`、`GET /summary?path=<file>&category=<cat>`
- Dockerfile 会把 `/app` 初始化为 `main` 分支 Git 仓库，并创建一个初始提交

## 手动验证命令

```bash
docker build -t receipt-ledger-py .
docker run --rm -d -p 8788:8788 --name receipt-ledger-qc receipt-ledger-py
curl http://127.0.0.1:8788/health
curl "http://127.0.0.1:8788/summary?path=data/sample_receipts.txt"
docker stop receipt-ledger-qc
docker run --rm receipt-ledger-py python -m unittest discover -s tests
docker run --rm receipt-ledger-py pwd
docker run --rm receipt-ledger-py git status --short
docker run --rm receipt-ledger-py python -m receipt_ledger.cli data/sample_receipts.txt --json
```

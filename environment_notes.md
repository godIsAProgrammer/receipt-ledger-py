# 环境说明

- 项目语言：Python 3.11+
- Docker 基础镜像：`python:3.12`
- 容器工作目录：`/app`
- 构建时会把 `repo/` 中的仓库文件复制到 `/app`
- 不需要第三方依赖
- 默认验证命令：`python -m unittest discover -s tests`
- Dockerfile 会把 `/app` 初始化为 Git 仓库，并创建一个初始提交

## 手动验证命令

```bash
docker build -t receipt-ledger-py .
docker run --rm receipt-ledger-py
docker run --rm receipt-ledger-py pwd
docker run --rm receipt-ledger-py git status --short
docker run --rm receipt-ledger-py python -m receipt_ledger.cli data/sample_receipts.txt --json
```

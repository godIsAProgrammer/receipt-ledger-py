# 验证记录

## 本机检查

- 2026-05-06 已通过：`python3 -m unittest discover -s tests`
  - 结果：4 个测试通过

## Docker 检查

- 2026-05-06 已通过：`docker build -t receipt-ledger-py .`
  - 结果：镜像构建成功
  - 构建阶段测试：4 个测试通过
  - 初始 Git 提交只包含源码、测试、README、pyproject 和样例数据
- 2026-05-06 已通过：`docker run --rm receipt-ledger-py`
  - 结果：4 个测试通过
- 2026-05-06 已通过：`docker run --rm receipt-ledger-py pwd`
  - 结果：`/app`
- 2026-05-06 已通过：`docker run --rm receipt-ledger-py git status --short`
  - 结果：无输出，工作区干净

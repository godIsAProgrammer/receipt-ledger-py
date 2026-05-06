FROM python:3.12

# 避免测试或运行时生成 __pycache__，保持容器内初始仓库干净。
ENV PYTHONDONTWRITEBYTECODE=1

# 标注文档要求容器内仓库统一位于 /app。
WORKDIR /app

# repo/ 是交付的初始仓库现场，复制后即可开始 Agent 任务。
COPY repo/ /app/

# 构建阶段先跑测试，再初始化 Git，确保进入容器后是干净可工作的现场。
RUN python -m unittest discover -s tests \
    && git init \
    && git config user.email "agent@example.invalid" \
    && git config user.name "Agent Fixture" \
    && git add . \
    && git commit -m "Initial receipt ledger fixture"

CMD ["python", "-m", "unittest", "discover", "-s", "tests"]

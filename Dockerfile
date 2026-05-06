FROM python:3.12

# 这个收据汇总工具会反复运行单元测试；关闭字节码写入，避免初始仓库出现缓存文件。
ENV PYTHONDONTWRITEBYTECODE=1

# CLI、样例数据和测试都围绕 /app 下的收据项目运行。
WORKDIR /app

# 复制收据解析器、CLI、样例收据和 unittest 测试作为任务起始现场。
COPY repo/ /app/

# 先确认解析与聚合测试通过，再把这个可工作的收据项目固化为 Git 初始提交。
RUN python -m unittest discover -s tests \
    && git init \
    && git config user.email "agent@example.invalid" \
    && git config user.name "Agent Fixture" \
    && git add . \
    && git commit -m "Initial receipt ledger fixture"

CMD ["python", "-m", "unittest", "discover", "-s", "tests"]

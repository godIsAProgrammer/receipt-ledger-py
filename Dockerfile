FROM python:3.12

# 收据汇总服务只使用 Python 标准库,上传包中源码位于 repo/ 下。
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 质检构建上下文为 Dockerfile + repo/,这里只初始化运行环境,不执行测试或 Git 初始化。
COPY repo/ .

# 暴露 HTTP 服务端口,质检和评审可以通过 -p 端口映射访问 /health 与 /summary。
EXPOSE 8788

# 容器默认启动只读 HTTP 服务,可访问 /health 做健康检查、/summary 触发样例汇总。
CMD ["python", "-m", "receipt_ledger.server"]

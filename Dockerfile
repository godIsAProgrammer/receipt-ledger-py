FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY repo/ .

EXPOSE 8788

CMD ["python", "-m", "receipt_ledger.server"]

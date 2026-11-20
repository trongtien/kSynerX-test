FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/cdms
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY cdms/core/ ./cdms/core/
COPY loadtest/ ./loadtest/
WORKDIR /app/loadtest
RUN useradd --create-home --uid 1000 app
USER app
EXPOSE 4000
CMD ["uvicorn", "server_test:app", "--host", "0.0.0.0", "--port", "4000"]

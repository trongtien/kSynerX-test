FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY cdms/ ./cdms/
WORKDIR /app/cdms
EXPOSE 3000
CMD ["uvicorn", "app.app:cdms_app_main", "--host", "0.0.0.0", "--port", "4000"]

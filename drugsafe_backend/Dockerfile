FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# static 파일 수집
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "drugsafe.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

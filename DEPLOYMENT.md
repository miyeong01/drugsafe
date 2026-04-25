# DrugSafe 배포 가이드

> Docker + GitHub Actions + AWS EC2 기반 CI/CD 파이프라인 구축

## 기술 스택

| 역할 | 기술 |
|------|------|
| Frontend | Vue 3 + Vite → Docker + Nginx |
| Backend | Django + DRF → Docker + Gunicorn |
| 리버스 프록시 | Nginx (외부 노출) |
| 컨테이너 오케스트레이션 | Docker Compose |
| CI/CD | GitHub Actions |
| 컨테이너 레지스트리 | Docker Hub |
| 서버 | AWS EC2 (t3.micro, ap-northeast-2) |
| DB | SQLite + Docker Named Volume (데이터 영속성) |

## 아키텍처

```
사용자
  │
  ▼
AWS EC2 (54.180.2.109)
  │
  └── Nginx (port 80) ← 리버스 프록시
        ├── /api/, /accounts/, /medicines/, /admin/, /static/
        │     → Backend 컨테이너 (Django + Gunicorn, port 8000)
        └── /*
              → Frontend 컨테이너 (Vue + Nginx, port 3000)
```

## CI/CD 흐름

```
git push (master)
  → GitHub Actions 트리거
  → Backend 이미지 빌드 & Docker Hub 푸시
  → Frontend 이미지 빌드 (VITE_API_URL 주입) & Docker Hub 푸시
  → EC2로 docker-compose.yml SCP 전송
  → EC2 SSH 접속 → docker-compose pull → down → up -d
```

---

## Step 1. 환경변수 분리

### 프론트엔드

하드코딩된 API URL을 환경변수로 교체:

- `drugsafe_frontend/src/stores/accounts.js`
- `drugsafe_frontend/src/stores/drug.js`
- `drugsafe_frontend/src/views/AIChatView.vue`

```js
// 변경 전
const API_URL = "http://127.0.0.1:8000"

// 변경 후
const API_URL = import.meta.env.VITE_API_URL
```

**`drugsafe_frontend/.env`** (로컬 개발용, git 제외)
```
VITE_API_URL=http://127.0.0.1:8000
```

### 백엔드

`drugsafe_backend/drugsafe/settings.py` 하단에 환경변수 오버라이드 추가:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DRUG_API_KEY = os.getenv('DRUG_API_KEY')

CORS_ALLOWED_ORIGINS_ENV = os.getenv('CORS_ALLOWED_ORIGINS', '')
if CORS_ALLOWED_ORIGINS_ENV:
    CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS_ENV.split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',  # 볼륨 마운트용 디렉토리
    }
}
```

> **포인트**: SQLite 경로를 `data/` 서브디렉토리로 지정해야 Docker 볼륨 마운트가 정상 동작한다. 파일 경로로 직접 마운트하면 `unable to open database file` 오류 발생.

---

## Step 2. Docker 컨테이너화

### Backend (`drugsafe_backend/Dockerfile`)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data          # SQLite 볼륨 마운트 디렉토리 사전 생성 필수
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "drugsafe.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

> **포인트**: `mkdir -p /app/data`를 Dockerfile에 추가해야 컨테이너 기동 시 SQLite가 해당 경로에 접근 가능하다.

`requirements.txt`에 `gunicorn==21.2.0` 추가 필요.

### Frontend (`drugsafe_frontend/Dockerfile`)

```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
ARG VITE_API_URL          # GitHub Actions에서 빌드 인자로 전달
ENV VITE_API_URL=$VITE_API_URL
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN echo 'server { \
    listen 3000; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

> **포인트**: Vite 빌드 시 환경변수를 주입하려면 `ARG` + `ENV` 선언이 `COPY . .` 이전에 있어야 한다. 없으면 `import.meta.env.VITE_API_URL`이 `undefined`로 빌드된다.

---

## Step 3. Docker Compose (`docker-compose.yml`)

```yaml
services:
  backend:
    image: ${DOCKER_HUB_USERNAME}/drugsafe-backend:latest
    env_file:
      - .env
    volumes:
      - sqlite_data:/app/data    # 디렉토리 단위 마운트 (파일 단위 X)
    restart: unless-stopped

  frontend:
    image: ${DOCKER_HUB_USERNAME}/drugsafe-frontend:latest
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  sqlite_data:
```

> **포인트**: EC2에는 소스코드가 없으므로 `build:` 섹션 없이 Docker Hub 이미지만 pull해서 사용한다.

---

## Step 4. Nginx 리버스 프록시 (`nginx/nginx.conf`)

```nginx
server {
    listen 80;

    location /api/ { proxy_pass http://backend:8000; }
    location /accounts/ { proxy_pass http://backend:8000; }
    location /medicines/ { proxy_pass http://backend:8000; }
    location /admin/ { proxy_pass http://backend:8000; }
    location /static/ { proxy_pass http://backend:8000; }

    location / { proxy_pass http://frontend:3000; }
}
```

---

## Step 5. GitHub Actions CI/CD (`.github/workflows/deploy.yml`)

```yaml
name: Deploy to EC2

on:
  push:
    branches:
      - master

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Docker Hub 로그인
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}

      - name: Backend 이미지 빌드 & 푸시
        uses: docker/build-push-action@v5
        with:
          context: ./drugsafe_backend
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/drugsafe-backend:latest

      - name: Frontend 이미지 빌드 & 푸시
        uses: docker/build-push-action@v5
        with:
          context: ./drugsafe_frontend
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/drugsafe-frontend:latest
          build-args: |
            VITE_API_URL=http://${{ secrets.EC2_HOST }}

      - name: docker-compose.yml EC2로 복사
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          source: "docker-compose.yml"
          target: "~/drugsafe/"

      - name: EC2 배포
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/drugsafe
            docker-compose pull
            docker-compose down
            docker-compose up -d
            docker image prune -f
```

> **포인트**: EC2에 설치된 docker-compose가 v1(1.29.2)이라 `docker compose`(v2) 명령어를 인식하지 못한다. `docker-compose`(하이픈)를 사용해야 한다.
>
> `up -d --remove-orphans` 대신 `down` 후 `up -d`를 사용하는 이유: docker-compose v1.29.2와 최신 Docker 이미지 포맷 간 `ContainerConfig` 키 호환성 문제로 `up --remove-orphans`가 실패한다.

### 필요한 GitHub Secrets

| Secret | 내용 |
|--------|------|
| `DOCKER_HUB_USERNAME` | Docker Hub 유저명 |
| `DOCKER_HUB_TOKEN` | Docker Hub Access Token (Read/Write/Delete 권한) |
| `EC2_HOST` | EC2 퍼블릭 IP |
| `EC2_SSH_KEY` | `.pem` 파일 내용 전체 |

---

## Step 6. AWS EC2 설정

### 6-1. EC2 인스턴스 생성

1. AWS 콘솔 → EC2 → 인스턴스 시작
2. AMI: `Ubuntu Server 22.04 LTS`
3. 인스턴스 유형: `t3.micro` (ap-northeast-2 프리티어 적용 가능)
4. 키 페어 생성 후 `.pem` 파일 저장
5. 보안 그룹 설정:

| 유형 | 포트 | 소스 |
|------|------|------|
| SSH | 22 | 0.0.0.0/0 (GitHub Actions 접속을 위해 전체 허용) |
| HTTP | 80 | 0.0.0.0/0 |
| HTTPS | 443 | 0.0.0.0/0 |

> **포인트**: SSH 소스를 "내 IP"로 제한하면 GitHub Actions에서 접속할 수 없다. `0.0.0.0/0`으로 설정해야 CI/CD가 동작한다.

### 6-2. EC2 초기 설정

```bash
# SSH 접속
ssh -i your-key.pem ubuntu@<EC2-IP>

# Docker 설치 (docker-compose v1 포함)
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker

# 프로젝트 디렉토리 및 nginx 설정 디렉토리 생성
mkdir -p ~/drugsafe/nginx
```

> **포인트**: `docker-compose-plugin`(v2)이 아닌 `docker-compose`(v1)를 설치한다. GitHub Actions 스크립트와 일치시켜야 한다.

### 6-3. 파일 업로드

```bash
# 로컬에서 실행
scp -i your-key.pem nginx/nginx.conf ubuntu@<EC2-IP>:~/drugsafe/nginx/
scp -i your-key.pem docker-compose.yml ubuntu@<EC2-IP>:~/drugsafe/
```

### 6-4. EC2에 .env 파일 생성

```bash
cd ~/drugsafe
nano .env
```

```
DJANGO_SECRET_KEY=<랜덤 시크릿 키>
DEBUG=False
ALLOWED_HOSTS=<EC2-퍼블릭-IP>
CORS_ALLOWED_ORIGINS=http://<EC2-퍼블릭-IP>
OPENAI_API_KEY=<OpenAI API 키>
DRUG_API_KEY=<공공데이터 API 키>
DOCKER_HUB_USERNAME=<Docker Hub 유저명>
```

### 6-5. 첫 배포 후 초기 데이터 작업 (최초 1회)

```bash
cd ~/drugsafe

# DB 마이그레이션
DOCKER_HUB_USERNAME=<유저명> docker-compose exec backend python manage.py migrate

# 의약품 데이터 로드 (CSV → DB)
DOCKER_HUB_USERNAME=<유저명> docker-compose exec backend python manage.py load_csv

# (선택) 의약품 이미지 URL 업데이트 - 약 1,500건 API 호출로 시간 소요
DOCKER_HUB_USERNAME=<유저명> docker-compose exec backend python manage.py load_drug_images
```

> **포인트**: EC2 `.env`에 `DOCKER_HUB_USERNAME`이 있어도 `docker-compose exec` 실행 시 인식 안 될 수 있다. 명령어 앞에 명시적으로 지정한다.

---

## 트러블슈팅 기록

| 문제 | 원인 | 해결 |
|------|------|------|
| `docker-compose: command not found` | v1이 기본 설치 안 됨 | `sudo apt-get install docker-compose` |
| GitHub Actions SSH 타임아웃 | 보안 그룹 SSH 소스가 내 IP로 제한됨 | SSH 소스를 `0.0.0.0/0`으로 변경 |
| Docker Hub push 실패 (insufficient scopes) | Access Token 권한 부족 | Token 재발급 시 Read/Write/Delete 선택 |
| `build path does not exist` | EC2 docker-compose.yml에 `build:` 섹션 있었음 | `build:` 섹션 제거, 이미지만 pull |
| `unable to open database file` | SQLite 볼륨을 파일 단위로 마운트 | 볼륨을 디렉토리(`/app/data`)로 변경, DB 경로도 `data/db.sqlite3`으로 수정 |
| `ContainerConfig` KeyError | docker-compose v1.29.2 + 최신 Docker 이미지 호환 버그 | `up --remove-orphans` 대신 `down` 후 `up -d` |
| `CSRF Failed: CSRF token missing` | DRF `SessionAuthentication`이 CSRF 강제 | `SessionAuthentication` 제거, `TokenAuthentication`만 유지 |
| API URL이 `/undefined/...`로 요청 | Frontend Dockerfile에 `ARG VITE_API_URL` 선언 누락 | `ARG` + `ENV` 추가 후 재빌드 |

---

## 진행 현황

- [x] Step 1. 환경변수 분리
- [x] Step 2. Docker 컨테이너화
- [x] Step 3. Docker Compose
- [x] Step 4. Nginx 리버스 프록시
- [x] Step 5. GitHub Actions CI/CD
- [x] Step 6. AWS EC2 설정 및 배포
- [ ] Step 7. HTTPS 설정 (도메인 필요, 선택)

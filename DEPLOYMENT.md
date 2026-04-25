# DrugSafe 배포 가이드

> Docker + GitHub Actions + AWS EC2 기반 CI/CD 파이프라인 구축

## 기술 스택

| 역할 | 기술 |
|------|------|
| Frontend | Vue 3 + Vite → Docker + Nginx |
| Backend | Django + DRF → Docker + Gunicorn |
| 리버스 프록시 | Nginx |
| 컨테이너 오케스트레이션 | Docker Compose |
| CI/CD | GitHub Actions |
| 서버 | AWS EC2 (t2.micro, 프리티어) |
| HTTPS | Let's Encrypt (Certbot) |

## 아키텍처

```
사용자
  │
  ▼
AWS EC2
  │
  ├── Nginx (80/443) ← 리버스 프록시 + SSL 종료
  │     ├── /api/*, /accounts/*, /medicines/*, /admin/*  → Backend (Django:8000)
  │     └── /*      → Frontend (Vue:3000)
  │
  ├── Docker: frontend (Vue + Nginx, port 3000)
  └── Docker: backend (Django + Gunicorn, port 8000)
```

## 배포 흐름

```
git push (main)
  → GitHub Actions 트리거
  → Docker 이미지 빌드 (backend, frontend)
  → Docker Hub push
  → EC2 SSH 접속
  → docker compose pull & up
```

---

## Step 1. 환경변수 분리 ✅

### 변경 내용

- `drugsafe_frontend/src/stores/accounts.js` — API_URL 하드코딩 → `import.meta.env.VITE_API_URL`
- `drugsafe_frontend/src/stores/drug.js` — 동일
- `drugsafe_frontend/src/views/AIChatView.vue` — 동일
- `drugsafe_backend/drugsafe/settings.py` — SECRET_KEY, DEBUG, ALLOWED_HOSTS, CORS를 환경변수로 분리

### 생성된 파일

**`drugsafe_frontend/.env`** (로컬 개발용, git 제외)
```
VITE_API_URL=http://127.0.0.1:8000
```

**`drugsafe_frontend/.env.production`** (프로덕션, git 제외)
```
VITE_API_URL=http://your-ec2-ip
```

**EC2 서버에 생성할 `.env`** (루트에 위치)
```
DJANGO_SECRET_KEY=<랜덤 시크릿 키>
DEBUG=False
ALLOWED_HOSTS=<EC2 퍼블릭 IP>
CORS_ALLOWED_ORIGINS=http://<EC2 퍼블릭 IP>
OPENAI_API_KEY=<OpenAI API 키>
DRUG_API_KEY=<공공데이터 API 키>
DOCKER_HUB_USERNAME=<Docker Hub 유저명>
```

---

## Step 2. Docker 컨테이너화 ✅

### Backend (`drugsafe_backend/Dockerfile`)

- `python:3.11-slim` 베이스
- `gunicorn`으로 WSGI 서버 실행 (workers: 2)
- `collectstatic` 빌드 시 실행
- 포트 8000

### Frontend (`drugsafe_frontend/Dockerfile`)

- **멀티스테이지 빌드**: Node 20으로 `npm run build` → Nginx alpine으로 정적 파일 서빙
- Vue Router history mode 지원 (`try_files $uri /index.html`)
- 포트 3000

---

## Step 3. Docker Compose ✅

위치: `docker-compose.yml`

- `backend`: Django + Gunicorn, SQLite DB 볼륨 마운트로 데이터 영속성 유지
- `frontend`: Vue 빌드 결과물 Nginx 서빙
- `nginx`: 80포트로 외부 노출, 리버스 프록시

---

## Step 4. Nginx 리버스 프록시 ✅

위치: `nginx/nginx.conf`

- `/api/`, `/accounts/`, `/medicines/`, `/admin/` → `backend:8000`
- `/static/` → `backend:8000`
- 나머지 → `frontend:3000`

---

## Step 5. GitHub Actions CI/CD ✅

위치: `.github/workflows/deploy.yml`

트리거: `main` 브랜치 push

### 필요한 GitHub Secrets

GitHub 레포 → Settings → Secrets and variables → Actions에서 등록

| Secret 이름 | 내용 |
|-------------|------|
| `DOCKER_HUB_USERNAME` | Docker Hub 유저명 |
| `DOCKER_HUB_TOKEN` | Docker Hub Access Token |
| `EC2_HOST` | EC2 퍼블릭 IP |
| `EC2_SSH_KEY` | EC2 접속용 private key (PEM 파일 내용 전체) |

---

## Step 6. AWS EC2 설정

### 6-1. EC2 인스턴스 생성

1. AWS 콘솔 → EC2 → 인스턴스 시작
2. AMI: `Ubuntu Server 22.04 LTS`
3. 인스턴스 유형: `t2.micro` (프리티어)
4. 키 페어 생성 후 `.pem` 파일 저장
5. 보안 그룹 설정:

| 유형 | 포트 | 소스 |
|------|------|------|
| SSH | 22 | 내 IP |
| HTTP | 80 | 0.0.0.0/0 |
| HTTPS | 443 | 0.0.0.0/0 |

### 6-2. EC2 초기 설정

EC2에 SSH 접속 후 실행:

```bash
# SSH 접속
ssh -i your-key.pem ubuntu@<EC2-퍼블릭-IP>

# Docker 설치
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker

# 프로젝트 디렉토리 생성
mkdir ~/drugsafe
cd ~/drugsafe

# nginx 설정 디렉토리 생성
mkdir nginx
```

### 6-3. 서버에 파일 업로드

로컬에서 EC2로 필요한 파일 복사:

```bash
# nginx 설정 업로드
scp -i your-key.pem nginx/nginx.conf ubuntu@<EC2-IP>:~/drugsafe/nginx/

# docker-compose.yml 업로드
scp -i your-key.pem docker-compose.yml ubuntu@<EC2-IP>:~/drugsafe/
```

### 6-4. EC2에 .env 파일 생성

EC2 접속 후 직접 생성 (git에 올리지 않음):

```bash
cd ~/drugsafe
nano .env
```

내용:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=<EC2-퍼블릭-IP>
CORS_ALLOWED_ORIGINS=http://<EC2-퍼블릭-IP>
OPENAI_API_KEY=your-openai-key
DRUG_API_KEY=your-drug-api-key
DOCKER_HUB_USERNAME=your-dockerhub-username
```

### 6-5. GitHub Secrets 등록

GitHub 레포 → Settings → Secrets and variables → Actions

- `DOCKER_HUB_USERNAME`: Docker Hub 유저명
- `DOCKER_HUB_TOKEN`: Docker Hub → Account Settings → Security → New Access Token
- `EC2_HOST`: EC2 퍼블릭 IP
- `EC2_SSH_KEY`: `.pem` 파일 내용 전체 붙여넣기

### 6-6. 첫 배포

```bash
git add .
git commit -m "feat: Docker + CI/CD 배포 설정"
git push origin main
```

→ GitHub Actions가 자동으로 빌드 & 배포

### 6-7. DB 마이그레이션 (최초 1회)

```bash
# EC2 접속 후
cd ~/drugsafe
docker compose exec backend python manage.py migrate
```

---

## Step 7. HTTPS 설정 (선택)

도메인이 있는 경우 Let's Encrypt로 무료 SSL 적용 가능

```bash
# EC2에서 Certbot 설치
sudo apt-get install -y certbot python3-certbot-nginx

# 인증서 발급 (도메인 필요)
sudo certbot --nginx -d your-domain.com
```

도메인 없이 IP만 사용할 경우 HTTP(80포트)로만 서비스

---

## 진행 현황

- [x] Step 1. 환경변수 분리
- [x] Step 2. Docker 컨테이너화
- [x] Step 3. Docker Compose
- [x] Step 4. Nginx 리버스 프록시
- [x] Step 5. GitHub Actions CI/CD
- [ ] Step 6. AWS EC2 설정
- [ ] Step 7. HTTPS 설정 (선택)

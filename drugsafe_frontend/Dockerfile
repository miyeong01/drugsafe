# Stage 1: 빌드
FROM node:20-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY . .
RUN npm run build

# Stage 2: Nginx로 서빙
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Vue Router history mode 지원을 위한 Nginx 설정
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

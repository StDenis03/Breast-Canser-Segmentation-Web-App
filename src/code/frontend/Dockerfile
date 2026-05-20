FROM node:20-alpine

WORKDIR /src/app

# Устанавливаем nginx
RUN apk add --no-cache nginx

# Копируем зависимости и исходники
COPY package*.json ./
RUN npm ci
COPY . .

# Копируем конфигурацию как ГЛАВНЫЙ файл nginx в корень конфигурации
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /run/nginx

EXPOSE 80

# Сборка при старте, копирование в dist и запуск nginx с явным указанием кастомного конфига
CMD npm run build && \
    cp -r /src/app/dist/* /usr/share/nginx/html/ && \
    nginx -g "daemon off;" -c /etc/nginx/nginx.conf

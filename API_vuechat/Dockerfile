# 1. Используем официальный образ Node.js
FROM node:20-alpine AS builder

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install

# 4. Копируем остальной код и собираем проект
COPY . .
RUN npm run build

# 5. Используем Nginx для запуска собранного проекта
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

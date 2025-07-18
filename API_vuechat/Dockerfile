FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Открываем порт
EXPOSE 5173

# Запускаем dev-сервер
CMD ["npm", "run", "dev"]

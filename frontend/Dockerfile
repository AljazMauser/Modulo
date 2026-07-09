FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Konfiguracija Nuxt za produkcijo
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000
# API base URL se prebere iz okolja v docker-compose
ENV NUXT_PUBLIC_API_BASE=http://backend:8000/api

RUN npm run build

# Ukaz za zagon produkcijske verzije Nuxt
CMD ["node", ".output/server/index.mjs"]

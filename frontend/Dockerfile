# --- Stage 1: Install dependencies ---
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# --- Stage 2: Build the application ---
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# --- Stage 3: Runner stage ---
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy build artifacts and dependencies
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
FROM node:20-alpine

WORKDIR /app

# 1. Copiar manifiestos y resolver dependencias como root para evitar bloqueos
COPY package.json package-lock.json* ./
RUN npm install

# 2. Crear directorios críticos y forzar la propiedad al usuario preexistente 'node'
RUN mkdir -p /app/.next /app/node_modules \
    && chown -R node:node /app

# 3. Restringir privilegios para la ejecución
USER node

# 4. Copiar el resto del código fuente (heredando la propiedad correcta)
COPY --chown=node:node . .

# 5. Configurar el entorno de desarrollo y exponer la red
ENV NODE_ENV=development
ENV HOSTNAME="0.0.0.0"
EXPOSE 3000

CMD ["npm", "run", "dev"]
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY next.config.ts tsconfig.json ./
COPY src ./src
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV HOSTNAME=0.0.0.0
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
RUN chown -R node:node /app
USER node
HEALTHCHECK --interval=10s --timeout=5s --retries=12 CMD node -e "fetch('http://localhost:3000/login').then(r=>process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"
EXPOSE 3000
CMD ["node", "server.js"]

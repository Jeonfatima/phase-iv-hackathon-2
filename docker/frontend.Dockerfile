# Use official Node.js runtime as base image
FROM node:18-alpine AS deps

# Install dependencies only when needed
WORKDIR /app

# Install only production dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# Rebuild the source code only when needed
FROM node:18-alpine AS builder

WORKDIR /app
COPY frontend/. .

# Copy dependency files
COPY --from=deps /app/node_modules ./node_modules

# Build the application
RUN npm run build

# Production image, copy all the files and run next
FROM node:18-alpine AS runner

WORKDIR /app

# Create a non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy the built application
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

USER nextjs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", ".next/standalone/server.js"]
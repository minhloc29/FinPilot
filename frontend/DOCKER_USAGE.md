# Docker Build & Run Commands

## Production Build
```bash
# Build production image
docker build --target production -t ai-finance-frontend:prod .

# Run with environment variables
docker run -p 3000:3000 \
  --build-arg VITE_API_URL=http://localhost:8000 \
  ai-finance-frontend:prod
```

## Development Build
```bash
# Build development image
docker build --target development -t ai-finance-frontend:dev .

# Run development server with volume mounting for hot reload
docker run -p 3000:3000 \
  -v $(pwd)/src:/app/src \
  ai-finance-frontend:dev
```

## Multi-stage Build Benefits
- **Production**: Optimized nginx-served static files (~50MB)
- **Development**: Full Bun environment with hot reload
- **Security**: Non-root user execution
- **Caching**: Optimized layer caching for faster rebuilds

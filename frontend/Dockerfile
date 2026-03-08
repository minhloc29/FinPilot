FROM node:22-alpine

WORKDIR /app

# Copy package files
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Default run command
CMD ["npm", "run", "dev", "--", "--host"]
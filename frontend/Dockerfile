# bus-tracker/frontend/Dockerfile
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm install

# Copy the frontend code
COPY . .

# Expose the port React app will run on
EXPOSE 3000

# Command to run the React app
CMD ["npm", "start"]

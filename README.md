# Bustracker Web App

## Installation

To get started with the Bustracker web app, you need to have Docker and Docker Compose installed on your machine. Follow the installation guides below if you haven’t installed them yet:

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

<br>

Clone the repository to your local machine using the following command:
```bash
git clone <repository-url>
```

## Configuration

Before running the application, you need to set up the following environment variables:

### Travel Time API

Obtain your Travel Time API credentials:

- **TRAVEL_TIME_API_ID**
- **TRAVEL_TIME_API_KEY**

You can get these credentials at [Travel Time API](https://traveltime.com/).

Export these variables in your terminal:

```bash
export TRAVEL_TIME_API_ID="your-api-id"
export TRAVEL_TIME_API_KEY="your-api-key"
```

### Email Sender

Specify an email alias and password that will be used as the sender email.

Export these variables in your terminal:

```bash
export EMAIL_SENDER_ALIAS="your-email-sender-alias"
export EMAIL_SENDER_PASSWORD="your-email-sender-password"
```

### Using .env  File

You can include all the above environment variables in a `.env` file located in the root directory of your project. 

Create a `.env` file with the following content:

```ini
TRAVEL_TIME_API_ID = "your-api-id"
TRAVEL_TIME_API_KEY = "your-api-key"
EMAIL_SENDER_ALIAS = "your-email-sender-alias"
EMAIL_SENDER_PASSWORD = "your-email-sender-password"
```

## Execution

Navigate to the project directory:

```bash
cd bustracker/
```

Use Docker Compose to build and start the application with the following command:

```bash
sudo docker-compose up --build
```

Then you can access the web app at:
[https://localhost:3000](https://localhost:3000)
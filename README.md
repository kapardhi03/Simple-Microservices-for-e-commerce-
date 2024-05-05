# Simple Microservices for e-commerce 
 a microservices-based system that manages a simple e-commerce application.

# Backend Engineering Challenge

This project is a microservices-based system that manages a simple e-commerce application. It handles user authentication, product management, and order processing.

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:
git clone <repository_url>


2. Navigate to the project directory:
cd backend-challenge


3. Build and run the microservices using Docker Compose:
docker-compose up --build

This command will build the Docker images for each microservice and start the containers.

4. The microservices will be accessible at the following endpoints:
- Auth Service: `http://localhost:8000`
- Product Service: `http://localhost:8001`
- Order Service: `http://localhost:8002`

## Usage

- To register a new user, send a POST request to `http://localhost:8000/register` with the user details in the request body.
- To obtain an access token, send a POST request to `http://localhost:8000/token` with the username and password in the request body.
- To create a new product, send a POST request to `http://localhost:8001/products` with the product details in the request body and the access token in the `Authorization` header.
- To retrieve all products, send a GET request to `http://localhost:8001/products` with the access token in the `Authorization` header.
- To create a new order, send a POST request to `http://localhost:8002/orders` with the order details in the request body and the access token in the `Authorization` header.
- To retrieve all orders for a user, send a GET request to `http://localhost:8002/orders` with the access token in the `Authorization` header.

## Assumptions

- The MongoDB connection URI is already set up and accessible.
- The MongoDB database and collections will be automatically created if they don't exist.
- The microservices communicate with each other using HTTP requests and share the same access token for authentication.
- The project focuses on the core functionality and may not include all the error handling and edge cases.

## Additional Notes

- The project uses FastAPI for building the microservices.
- The `mongo.py` file contains the MongoDB database operations.
- Pydantic is used for data validation and serialization.
- The microservices are containerized using Docker and orchestrated using Docker Compose.
- The authentication mechanism is based on OAuth2 using JWT tokens.
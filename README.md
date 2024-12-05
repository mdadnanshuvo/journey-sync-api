
# Journey Sync API

This project is a **Journey Sync API**, designed to manage multiple services related to **User Management**, **Authentication**, and **Destination Management** in a distributed manner. The API is built using **Flask** for each service and allows easy interaction between various components through separate services running on different ports.

## Table of Contents

- [Journey Sync API](#journey-sync-api)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Tech Stack](#tech-stack)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Setting Up the Project](#setting-up-the-project)

---

## Project Overview

The **Journey Sync API** is designed to simulate a multi-service architecture, where three main services are running:

- **User Service**: Manages user registration, login and profile.
- **Auth Service**: Handles and validate access token created in user_service/login with the functionalities of specifing role .
- **Destination Service**: Manages travel destinations and associated data.

Each service is self-contained and runs on a separate port, making it easy to scale, modify, and maintain.

---

## Tech Stack

- **Backend Framework**: Flask
- **Database**: (In-class memory)
- **Environment**: Python 3.x
- **Virtual Environment**: `venv`
- **Development Tools**: 
  - **Swagger UI** for API testing
  - **VS Code** 

---


## Project Directory Structure

```plaintext
journey-sync-api/
│
├── Users/
│   ├── user_service.py       # User management logic
│   └── schemas/
│       └── user_schema.py    # User schemas for validation
│
├── Auth/
│   ├── auth_service.py       # Authentication logic
│   └── schemas/
│       └── auth_schema.py    # Authentication schemas
│
├── Destination/
│   ├── destination_service.py # Destination management logic
│   └── schemas/
│       └── destination_schema.py # Destination schemas
│
├── run_services.py           # Main script to start all services
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```
## Getting Started

Follow the steps below to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed:

- **Python 3.x**
- **pip** (Python package installer)
- **Virtual Environment** (`venv`)
  
If you don’t have `pip` or `venv` installed, follow the installation guides on the official Python website:  
- [Install Python](https://www.python.org/downloads/)

### Setting Up the Project

1. **Clone the repository:**

 ```
 git clone https://github.com/mdadnanshuvo/journey-sync-api.git

```

2. **Change the working directory to the cloned repository:**

 ```
 cd journey-sync-api

```

3. **Create a virtual environment:**
Set up a virtual environment to manage project dependencies:
 ```
 python3 -m venv venv

```
   
4. **Activate the virtual environment**
   
   **On Windows**
   
   ```
   venv\Scripts\activate
   ```
  
   **On macOS/Linux**
  
   ```
   source venv/bin/activate
   ```

5. **Intall dependencies**
   
    ```
    pip install -r requirements.txt
   

### Running the server

1. **Run all services using run_services.py script**

   ```
   python run_services.py
   ```
   
Each service will start on its own port:

+ User Service:  http://127.0.0.1:5000
+ Auth Service:  http://127.0.0.1:5001
+ Destination Service:  http://127.0.0.1:5002


# API Testing with Swagger UI

This guide explains how to interact with and test the APIs of three services (User_Service, Auth_Service, and Destination_Service) using Swagger UI.

---

## 1. User_Service API

You can test the APIs of the **User_Service** by visiting the following Swagger UI:

- [User_Service Swagger UI](http://127.0.0.1:5000/swagger)

### Available Endpoints:
- **POST /register**:
  - Registers a new user or admin based on the data defined by the **User_Schema**.
  
- **POST /login**:
  - Logs in an existing user or admin.
  - Returns an **access token**, which is encrypted based on the user's/admin's ID and role. This token will be used to authorize requests for the user/admin's profile.

- **GET /profile**:
  - Retrieves the profile of the currently logged-in user/admin.
  - This endpoint requires a valid **access token** for authentication.

### Authentication:
- To interact with the protected endpoints (like **GET /profile**), you will first need to log in via **POST /login** and obtain an access token.
- **Swagger UI** provides an **Authorize** button in the top-right corner to enter your login credentials and receive the token.
- The access token must be included in the request to authorize the user/admin's profile interaction.

---

## 2. Auth_Service API

You can test the APIs of the **Auth_Service** by visiting the following Swagger UI:

- [Auth_Service Swagger UI](http://127.0.0.1:5001/swagger)

### Available Endpoints:
- **POST /validate-token**:
  - Validates the access token that was generated in the **POST /login** endpoint of **User_Service**.
  
- **POST /decrypt-role**:
  - Decodes and specifies the role of the user or admin by decrypting the access token.

### Authentication:
- Swagger UI provides an **Authorize** button in the top-right corner for entering your **Bearer token** (the access token from **User_Service**).
- Once the token is provided, you can test both endpoints. A valid access token is required for successful interactions with these methods.

---

## 3. Destination_Service API

You can test the APIs of the **Destination_Service** by visiting the following Swagger UI:

- [Destination_Service Swagger UI](http://127.0.0.1:5002/swagger)

### Available Endpoints:
- **POST /destinations** (Admin-only):
  - Adds a new destination. This is restricted to admin users only.

- **POST /delete/destination-id** (Admin-only):
  - Deletes a destination by ID. This is restricted to admin users only.

- **GET /destinations** (User and Admin):
  - Retrieves a list of all existing destinations. Both users and admins can access this endpoint.

### Authentication:
- Similar to the previous services, you will need to authorize using the **Bearer token** from **User_Service**.
- Swagger UI provides an **Authorize** button in the top-right corner for entering your **Bearer token**.
- After successful authorization, you can test the endpoints. Certain endpoints (like **POST /destinations** and **POST /delete/destination-id**) are restricted to **admin users** and require the role to be specified in the access token.

---


## **4. Automated Testing with `pytest`**

For automated testing, you can use `pytest` to test all the APIs across the three services and measure code coverage.

### **Running Tests**
Run the following command in your terminal:

```bash
pytest --cov=Users --cov=Auth --cov=Destination tests/

    



   



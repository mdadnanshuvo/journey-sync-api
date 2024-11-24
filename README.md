
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
   https://github.com/mdadnanshuvo/journey-sync-api.git
   
   cd journey-sync-api

2. **Create a Virtual Environment**
   ```
   python -m venv venv
   
3. **Activate the virtual environment**
   
   **On Windows**
   
   ```
   venv\Scripts\activate
  **On macOS/Linux**
  
```
 source venv/bin/activate
```
4. **Intall dependencies**
   ```
   pip install -r requirements.txt

### Running the server

1. **Run all services using run_services.py script**
   ```
   python run_services.py
   
Each service will start on its own port:

+ User Service: http://localhost:5000
+ Auth Service: http://localhost:5001
+ Destination Service: http://localhost:5002





   



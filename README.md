
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
 cd journey-sync-api
```
 

2. **Create a Virtual Environment**
   ```
   python -m venv venv
   
3. **Activate the virtual environment**
   
   **On Windows**
   
   ```
   venv\Scripts\activate
   ```
  
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
   ```
   
Each service will start on its own port:

+ User Service:  http://127.0.0.1:5000
+ Auth Service:  http://127.0.0.1:5001
+ Destination Service:  http://127.0.0.1:5002


2. **Test all the APIs using Swagger UI**
   
    1. **User_Service**
       + Please visit  [Swagger UI] http://127.0.0.1:5000/swagger to interact with Swagger UI to test the APIs of user_service.
       + There will be three http methods - POST/register, POST/login and GET/profil
       + POST/register will register new user/admin based on the data defined by the User_Schema
       + POST/login referes to logged in existing user/admin providing access token. The access token is encrypted based on user/admin's id and role in order to specify the role decrypting the access token. Swagger UI will provide a button called Authorize on the top-left corner to authorize the user/admin's credentials.
       + After successfully logged in using the secure and authentic token, current user/admin can explore thier profile and this will be done by GET/profile http method.

    2. **Auth_Service**
       + Please visit  [Swagger UI] http://127.0.0.1:5001/swagger to interact with Swagger UI to test the APIs of auth_service.
       + Two http methods can be found in this ui - one for validating the access token generated in the POST/login section in user_service or http://127.0.0.1:5000/swagger url, and the second one is desinged to specify the role decrypting the access token.
       + This ui will conclude an authorize button by Swagger ui, functioned by bearerAuth to provide the access token as http header.
       + Valid access token will lead successful interactions with both of the method.

    3. **Destination_Service**
        + Please visit  [Swagger UI] http://127.0.0.1:5002/swagger to interact with Swagger UI to test the APIs of destination_service.
        + This service provides three http methods - POST/destinations (Admin-only) to add new destination , POST/delete/destination-id (Admin-only) to delete destinations, and GET/destinations (both user and admin) to witness all the existing destinations.
        + The role will be specified based on the info by decrpyting the user/admin access token. Just like the previous to services, this service too will have a authorize button on the top-left corner or the Swagger UI provided by bearerAuth to authorize and specify the role as two of the crucial http methods can only be done by Admin.
        + After successfully authorize and if the role is specified as Admin, Deletion or Addition can be made.
        + POST/destinations can be made by both users and admins but they need to be authorized by the access token. 
        
    



   



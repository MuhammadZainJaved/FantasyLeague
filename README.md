# Fantasy Football Platform

## Overview

The Fantasy Football Platform is a web application that simulates a fantasy football league where users can manage their virtual teams and participate in player transfers. It includes features for user management, team management, player management, a transfer market, and transaction history.

## Project Structure

The project uses Django with Django REST Framework for the backend and is containerized using Docker. Below is the documentation for setting up, running, and testing the project.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Project

Clone the repository using Git:

```bash
git clone <repository-url>
cd <repository-directory>
```

### Setup using Docker

1. **Build and Start the Docker Containers**

   Ensure you are in the root directory of the project where `docker-compose.yml` is located, then run:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image and starts the `db` (PostgreSQL) and `web` (Django) services.

2. **Apply Migrations**

   Once the containers are running, you need to apply database migrations. Open a new terminal and run:

   ```bash
   docker-compose run web python manage.py migrate
   ```

3. **Create a Superuser**

   To access the Django admin interface, create a superuser by running:

   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

   Follow the prompts to create a superuser account.

### Running the Application

The application will be accessible at `http://localhost:8000/`. The Django development server will automatically start and listen on port 8000.

### API Endpoints

#### Authentication

- **Register a User**
  - **Endpoint:** `/api/register/`
  - **Method:** POST
  - **Data:**
    ```json
    {
      "username": "user123",
      "password": "password123",
      "email": "user@example.com"
    }
    ```

- **Protected View**
  - **Endpoint:** `/api/protected/`
  - **Method:** GET
  - **Authentication:** Bearer token required

#### User Management

- **List Users**
  - **Endpoint:** `/api/users/`
  - **Method:** GET

- **Retrieve, Update, Delete User**
  - **Endpoint:** `/api/users/{id}/`
  - **Method:** GET, PUT, PATCH, DELETE
  - **Authentication:** Bearer token required

#### Player Management

- **List Players**
  - **Endpoint:** `/api/players/`
  - **Method:** GET

- **Retrieve, Update, Delete Player**
  - **Endpoint:** `/api/players/{id}/`
  - **Method:** GET, PUT, PATCH, DELETE
  - **Authentication:** Bearer token required

#### Team Management

- **List Teams**
  - **Endpoint:** `/api/teams/`
  - **Method:** GET

- **Retrieve, Update, Delete Team**
  - **Endpoint:** `/api/teams/{id}/`
  - **Method:** GET, PUT, PATCH, DELETE
  - **Authentication:** Bearer token required

#### Transfer Market

- **List Active Transfers**
  - **Endpoint:** `/api/transfers/`
  - **Method:** GET

- **Buy a Player**
  - **Endpoint:** `/api/transfers/{id}/buy/`
  - **Method:** POST
  - **Data:**
    ```json
    {
      "price": 1500000
    }
    ```
  - **Authentication:** Bearer token required

### Testing the Application

1. **Run Unit Tests**

   To run unit tests, use the following command:

   ```bash
   docker-compose run web python manage.py test
   ```

2. **Test API Endpoints**

   You can test the API endpoints using tools like Postman or cURL by sending requests to `http://localhost:8000/api/`.

### Logging

Logging is configured by default in Django. The logs will be output to the console where the Docker container is running. For more detailed logging configurations, you may need to update the Django settings or use additional logging packages.

### Comments and Documentation

- **Code Comments:** Each method and class in the codebase is commented to explain its functionality.
- **Documentation:** API documentation can be generated and viewed through tools like Swagger or Django REST Framework's built-in documentation features.

## Contributing

If you want to contribute to the project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django
- Django REST Framework
- PostgreSQL
- Docker

```

Feel free to adjust any parts of the documentation to better fit your needs or to add any additional sections if required!

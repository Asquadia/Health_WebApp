# Health App Project

This project is a microservice application that provides BMI and BMR calculation services. It consists of three main components and a web interface:

*   **Backend:** A Flask application that serves as the main entry point and handles routing requests to the appropriate service.
*   **BMI Service:** A Flask application that calculates BMI.
*   **BMR Service:** A Flask application that calculates BMR.
*   **Frontend:** A simple HTML/JavaScript frontend that allows users to interact with the services.

The application is containerized using Docker for easy deployment and management.

## Prerequisites

*   **Docker:** Make sure you have Docker installed and running on your system. You can download it from the official Docker website: [https://www.docker.com/get-started](https://www.docker.com/get-started)

## Makefile Targets

The `Makefile` provides the following targets to manage the project:

### `init`

This target initializes the project by building the Docker image and creating a virtual environment inside the container with all necessary dependencies installed.

**How to use:**

```bash
make init
```

### `run_all`

This target starts all services (backend, BMI, and BMR) inside a Docker container. The services will be accessible on the following ports:

*   **Backend:** `http://localhost:5000`
*   **BMI Service:** `http://localhost:5001`
*   **BMR Service:** `http://localhost:5002`

**How to use:**

```bash
make run_all
```

### `stop`

This target stops the running Docker container.

**How to use:**

```bash
make stop
```

### `clean`

This target stops the Docker container, removes the Docker image, and deletes the virtual environments both inside the container and locally.

**How to use:**

```bash
make clean
```

### `test`

This target runs the tests locally using a virtual environment created on your host machine. It first sets up the virtual environment and installs the necessary dependencies, then executes the tests using the Python interpreter within the activated environment, it dont do test in container for simplicity reason.

**How to use:**

```bash
make test
```

## Getting Started

1. **Clone the repository:**

    ```bash
    git clone https://gitlab.com/Asquadia/Health_App.git
    cd Health_App
    ```

    ```bash
    apt install python3.11-venv
    ```

2. **Initialize the project:**

    ```bash
    make init
    ```

3. **Run the application:**

    ```bash
    make run_all
    ```

4. **Access the frontend:**

    Open your web browser and go to `http://localhost:5000` to interact with the application.

5. **Run tests (optional):**

    To avoid any issue make sure the container are not running

    ```bash
    make test
    ```

6. **Stop the application:**

    ```bash
    make stop
    ```

7. **Clean up (optional):**

    ```bash
    make clean
    ```

## Project Structure

```
├── backend         # Backend service (Flask app)
│   └── app.py
├── bmi_service     # BMI service (Flask app)
│   └── app.py
├── bmr_service     # BMR service (Flask app)
│   └── app.py
├── frontend        # Frontend application (HTML/JavaScript)
│   └── index.html
├── Dockerfile      # Dockerfile to build the application image
├── Makefile        # Makefile to manage the project
├── README.MD       # This README file
├── requirements.txt # Python dependencies
└── test            # Test scripts
    └── app.py
```
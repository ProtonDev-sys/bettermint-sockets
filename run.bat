@echo off
set IMAGE_NAME=my-python-engine
set CONTAINER_NAME=python-engine-container
set PORT=7860

:: Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not in PATH. Please install Docker first.
    pause
    exit /b
)

:: Build the Docker image if it doesn't exist
echo Checking if the Docker image "%IMAGE_NAME%" exists...
docker image inspect %IMAGE_NAME% >nul 2>&1
if errorlevel 1 (
    echo Image not found. Building the Docker image...
    docker build -t %IMAGE_NAME% .
    if errorlevel 1 (
        echo Failed to build the Docker image. Please check your Dockerfile.
        pause
        exit /b
    )
)

:: Check if the container exists
echo Checking if the container "%CONTAINER_NAME%" exists...
docker ps -a -q -f name=%CONTAINER_NAME% >nul
if errorlevel 1 (
    echo Container "%CONTAINER_NAME%" does not exist. Creating and starting the container...
    docker run -d -p %PORT%:7860 --name %CONTAINER_NAME% %IMAGE_NAME%
    if errorlevel 1 (
        echo Failed to create and start the Docker container.
        pause
        exit /b
    )
) else (
    :: If the container exists, remove and recreate it to prevent stale issues
    echo Stopping and removing stale container "%CONTAINER_NAME%"...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
    echo Recreating the container...
    docker run -d -p %PORT%:7860 --name %CONTAINER_NAME% %IMAGE_NAME%
    if errorlevel 1 (
        echo Failed to recreate the Docker container.
        pause
        exit /b
    )
)

:: Show logs from the container
echo Streaming logs from the container. Press Ctrl+C to stop.
docker logs -f %CONTAINER_NAME%
pause

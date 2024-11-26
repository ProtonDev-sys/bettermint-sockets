# Use the official Python 3.10.9 image
FROM python:3.10.9

# Copy the current directory contents into the container at .
COPY . .

# Set the working directory to /
WORKDIR /

RUN pip install python-multipart

# Install requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Install LeelaChessZero depencies
RUN apt update -y
RUN apt upgrade -y
RUN apt install ocl-icd-opencl-dev -y

# Make engines executable
RUN chmod +x engines/stockfish/*
RUN chmod +x engines/maia/*/lc0
RUN chmod +x engines/RodentIII/*
RUN chmod +x engines/Patricia/*

# Start the FastAPI app on port 7860, the default port expected by Spaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
# 1. Use an official, lightweight Python base image
FROM python:3.11-slim

# 2. Install essential Linux graphics libraries for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /code

# 4. Copy your requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your remaining application files and model weights
COPY . .

# 6. Expose the default port Hugging Face expects for Docker spaces
EXPOSE 7860

# 7. Command to run your Streamlit app on the correct port and host
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
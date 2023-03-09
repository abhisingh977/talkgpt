FROM python:3.8.0-slim

# Copy local code to the container image
COPY model /app/model
COPY templates /app/templates
COPY main.py /app/main.py
COPY static /app/static
COPY requirements.txt /app/requirements.txt
# Sets the working directory
WORKDIR /app

# Upgrade PIP
RUN pip install --upgrade pip
RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
#Install python libraries from requirements.txt
RUN pip install -r requirements.txt

# Set $PORT environment variable
ENV PORT 8080

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /

# Install necessary dependencies
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir runpod huggingface_hub transformers logging

# Copy necessary files
COPY rp_handler.py /
# COPY test_input.json /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]

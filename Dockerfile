# Gunakan Python sebagai base image
FROM python:3.10-slim

# Set lingkungan kerja di container
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Expose port 8000 untuk server
EXPOSE 8000

# Command untuk menjalankan server dengan Granian
CMD ["granian", "main:app", "--workers", "4", "--interface", "asgi"]

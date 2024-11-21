# Sử dụng phiên bản tối giản của Python làm base image
FROM python:3.10-slim AS build

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Cài đặt các dependencies cần thiết và làm sạch các file tạm trong cùng một layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    sox \
    git \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/

# Chỉ sao chép các file cần thiết để cài đặt dependencies
COPY requirements.txt .

# Cài đặt các dependencies của Python mà không lưu cache để giảm kích thước image
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Sao chép tất cả các file còn lại vào container
COPY . /usr/src/app
EXPOSE 50056
# Đặt lệnh chạy chính cho container
CMD ["python", "main.py"]